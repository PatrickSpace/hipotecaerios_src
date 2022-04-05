import re

class Format:
    def __init__(self):
        pass

    def cutPasteSpecial(self, document):
        """ Pega el documento sin formato, eliminando
            las viñetas especiales.
        """
        document.Content.Cut()
        document.Content.PasteSpecial(DataType=2)
        #print("cortado")

    def basics(self, document):
        document.PageSetup.LeftMargin = self.cm_to_points(2.5)
        document.PageSetup.RightMargin = self.cm_to_points(2.5)
        document.PageSetup.TopMargin = self.cm_to_points(2.5)
        document.PageSetup.BottomMargin = self.cm_to_points(2.5)
        document.PageSetup.Gutter = self.cm_to_points(0)
        document.Content.ParagraphFormat.LineSpacing = 19.200000762939453
        document.Content.ParagraphFormat.SpaceAfter = 0
        document.Content.Font.Name = "Anonymous"
        document.Content.Font.Size = 8
        document.Content.Font.Bold = False
        document.Content.Font.Italic = False
        document.Content.Font.ColorIndex = 1
        document.Content.Underline = 0

    def cm_to_points(self, value):
        return value*10/0.353

    def remove_shapes(self, document):
        print("Numero de figuras: ", document.Shapes.Count)
        if document.Shapes.Count > 0:
            for index in range(document.Shapes.Count):
                #print("figura eliminada")
                document.Shapes(1).Delete

    def modify_tables(self, document):
        tables = document.Tables
        if document.Tables.Count > 0:
            #with open(bancoTablasPath) as f:
            #    tablasBancos = json.load(f)
            for table in tables:
                #if self.info == "ScotiaBank Peru S.A.A.":
                #    formatTabla(table, tablasBancos, banco=self.info)
                table.ConvertToText(Separator="{")
            document.Content.Find.Execute(FindText="{", ReplaceWith=".== == ", Replace=2)

    def remove_lists(self, document):
        for blist in document.Lists:
            for par in blist.Range.ListParagraphs:
                listType_ = par.Range.ListFormat.ListType
                if listType_ == 2:
                    rangeStart = par.Range.Start
                    range_ = document.Range(rangeStart, rangeStart)
                    range_.InsertBefore("• ")
                    par.Range.ListFormat.RemoveNumbers(3)

    def general_format(self, document):
        #print("parrafos")
        paragraphs = document.Paragraphs
        for paragraph in paragraphs:
            self.formatIndentation(paragraph)
            self.justifyAlignment(paragraph)
            self.removeSectionBreak(paragraph)
            self.removeTabs(paragraph)
            self.removeSpecialCharacters(paragraph)
            self.setSpaceBetweenLetters(paragraph)
            #self.define_sections(paragraph)

    def remove_at_beginning_of_paragraph(self, document):
        for paragraph in document.Paragraphs:
            isBold = paragraph.Range.Font.Bold
            isUnderline = paragraph.Range.Underline
            pStart, pEnd = paragraph.Range.Start, paragraph.Range.End
            txt_ = paragraph.Range.Text
            match = re.search(r'^\s+', txt_)
            if match:
                txt_out = txt_[match.end():]
                #match2 = re.search(r'\s+$', txt_out)
                #if match2:
                #    txt_out = txt_out[:match.start()] + '\r'
                paragraph.Range.Text = txt_out
                if isBold:
                    document.Range(pStart-match.end(), pEnd-match.end()).Font.Bold = True
                if isUnderline:
                    document.Range(pStart-match.end(), pEnd-match.end()).Underline = 1

    def removeEmptyParagraph(self, document):
        for paragraph in document.Paragraphs:
            range_ = paragraph.Range
            threshold = range_.End-range_.Start
            if threshold < 6:
                range_.Delete()

    ##########################

    def formatIndentation(self, paragraph):
        paragraph.LeftIndent = 0
        paragraph.RightIndent = 0
        paragraph.FirstLineIndent = 0

    def justifyAlignment(self, paragraph):
        paragraph.Alignment = 3
        paragraph.Space1

    def removeSectionBreak(self, paragraph):
        paragraph.Range.Find.Execute(FindText="^b", ReplaceWith="", Replace=2)

    def removeTabs(self, paragraph):
        rt = paragraph.Range.Find.Execute(FindText="\t", ReplaceWith=" ", Replace=2)

    def removeSpecialCharacters(self, paragraph):
        paragraph.Range.Find.Execute(FindText="\x0b", ReplaceWith="", Replace=2)

    def setSpaceBetweenLetters(self, paragraph):
        paragraph.Range.Font.Spacing = 0

    def standardColon(self, document):
        for paragraph in document.Paragraphs:
            rangeParagraph = paragraph.Range
            rangeParagEnd = rangeParagraph.End

            while rangeParagraph.Find.Execute(FindText=":"):
                rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
                document.Range(rcStart, rcEnd).Font.Bold = False
                document.Range(rcStart, rcEnd).Font.Italic = False
                document.Range(rcStart, rcEnd).Font.Underline = False
                rangeParagraph = document.Range(rcEnd, rangeParagEnd)

    def agregarFirmantes(self, document):
        cuenta = document.Paragraphs.Count
        for i in reversed(range(cuenta)):
            
            text = document.Paragraphs(i+1).Range.Text
            document.Paragraphs(i+1).Range.Delete() 
            if "CLIENTE" in text:
                break        
            
        cuenta = document.Paragraphs.Count
        document.Paragraphs(cuenta).Range.InsertParagraphAfter()
        cuenta = document.Paragraphs.Count
        document.Paragraphs(cuenta).Range.InsertAfter(Text:="A CONTINUACION ………. FIRMAS ILEGIBLES") 
        document.Paragraphs(cuenta).Range.InsertParagraphAfter()
        cuenta = document.Paragraphs.Count
        document.Paragraphs(cuenta).Range.InsertAfter(Text:="………….., ABOGADO, C.A.L. NRO. ………..., UNA FIRMA ILEGIBLE")