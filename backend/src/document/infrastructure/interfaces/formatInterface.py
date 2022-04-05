import win32com.client as win32
from backend.src.document.infrastructure.interfaces.text_utils import extend_date, extended_numbers, date_to_string, date_to_string_with_point
from backend.src.document.infrastructure.middlewares.formatMiddleware import *
from backend.src.document.infrastructure.middlewares.agregarMiddleware import *
from backend.src.document.infrastructure.middlewares.extendMiddleware import *
from backend.src.document.infrastructure.middlewares.extraerComparecientesMiddleware import *
from backend.src.document.infrastructure.middlewares.printExceptionInfo import *
#from backend.src.document.domain.document import Compareciente
import json
import re
import platform
if platform.uname().node == 'EQUIPO':
    bancosInfoPath = "D:\\bot-hip\\backend\\src\\libs\\bancosInfo.json"
    bancoDataPath = "D:\\bot-hip\\backend\\src\\libs\\bancos.json"
    bancoTablasPath = "D:\\bot-hip\\backend\\src\\libs\\tablasBancos.json"
    signersBancoPath = "D:\\bot-hip\\backend\\src\\libs\\signersBancos.json"
    clausulasBancoPath = "D:\\bot-hip\\backend\\src\\libs\\clausulasBancos.json"
    clausulasInmobiliariasPath = "D:\\bot-hip\\backend\\src\\libs\\clausulasInmobiliarias.json"
    inmobiliariasInfoPath = "D:\\bot-hip\\backend\\src\\libs\\inmobiliariaInfo.json"
    compRepresentantesInfoPath = "D:\\bot-hip\\backend\\src\\libs\\compRepresentantes.json"
else:
    bancosInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\bancosInfo.json" 
    bancoDataPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\bancos.json"
    bancoTablasPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\tablasBancos.json"
    signersBancoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\signersBancos.json"
    clausulasBancoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\clausulasBancos.json"
    clausulasInmobiliariasPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\clausulasInmobiliarias.json"
    inmobiliariasInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\inmobiliariaInfo.json"
    compRepresentantesInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\compRepresentantes.json"

class Format:
    def __init__(self, basePath, formattedPath, info, visible, typeInfo="inmobiliaria"):
        """ basePath: Donde se crean los proyectos
            formattedPath: Ruta del documento formateado
            info: Seleccion del usuario de la inmobiliaria y el banco
            visible: modo de procesamiento del documento
            typeInfo: puede ser banco o inmobiliaria
        """
        self.basePath = basePath
        self.formattedPath = formattedPath
        self.info = info[typeInfo]
        self.infoFull = info
        self.wordApp = win32.gencache.EnsureDispatch("Word.Application")
        self.wordApp.Visible = visible
        self.document = self.wordApp.Documents.Open(formattedPath)
        self.paragraphs = self.document.Paragraphs
        self.paragraphs.SpaceBefore = 0
        self.paragraphs.SpaceAfter = 0
        self.comparecientes = {}
        pass

    def fix(self):
        try:
            print("fixing format", self.info)
            with open(clausulasInmobiliariasPath) as f:
                clausulasInmobiliarias = json.load(f)
            ## EN CASO QUE EXISTAN TABLAS, SE DEBEN PROCESAR EN ESTE PUNTO
            self.document.Content.Cut()
            self.document.Content.PasteSpecial(DataType=2)
            self.basic_document_format()
            for blist in self.document.Lists:
                #self.removeBullets(blist)
                self.remove_list(blist)
            for paragraph in self.paragraphs:
                if self.info == None:#"Promotora Albamar S.A.C.":
                    formatClausulas2(self.document, paragraph, clausulasInmobiliarias[self.info])
                elif self.info == "Inversiones Inmobiliarias del Indico" or self.info == "Lider Ingenieria y Contruccion" or self.info == "Josmi Grupo Inversor S.A.C." or self.info == "Quatro Beta" or self.info == "Quatro Epsilon" or self.info == "Vienna Contructores S.A." or self.info == "Inversiones Rocazul S.A.C." or self.info == "Miranda Constructores S.A." or self.info == "Desarrollo y Proyectos Edifica" or self.info == "Buenas Inversiones S.A.C." or self.info == "Paz Centenario S.A." or self.info == "Promotora Albamar S.A.C." or self.info == "Espinoza Arquitectos S.A.C.":
                    formatClausulas4(self.document, paragraph, clausulasInmobiliarias["general"])
                else:
                    formatClausulas(self.document ,paragraph, clausulasInmobiliarias[self.info])
                if self.info == "Alcanfores" or self.info == "Buenas Inversiones S.A.C." or self.info == "Desarrollo y Proyectos Edifica":
                    formatAnexos2(self.document, paragraph)
                elif self.info == "Promotora Albamar S.A.C.":
                    formatAnexos3(self.document, paragraph)
            if self.info == "Espinoza Arquitectos S.A.C.":
                lastClausula = None
            self.general_paragraph_format()
            addNotario(self.document)
            for section in self.document.Sections:
                formatSectionComprador1(self.document, section)
            for section in self.document.Sections:
                print("secciones")
                format_sections(self.document, section)
            for section in self.document.Sections:
                print("extrayendo firmantes")
                extract_signers(self.document, self.basePath, self.info, self.infoFull, section, bancosInfoPath, inmobiliariasInfoPath, compRepresentantesInfoPath)
            for section in self.document.Sections:
                print("segundas secciones")
                addSigners(self.document, section)
            c1 = 0
            m1 = 0
            print(self.document.Paragraphs.Count)
            #for paragraph in self.document.Paragraphs:
            for item in range(1, self.document.Paragraphs.Count+1):
                print(self.document.Paragraphs.Count)
                if self.document.Paragraphs.Count == 188:
                    print(self.document.Paragraphs(item).Range.Text)
                #self.remove_at_beginning_of_paragraph(paragraph) #white spaces
                self.remove_at_beginning_of_paragraph(self.document.Paragraphs(item))
                extendNumbers(self.document, self.document.Paragraphs(item))
                if c1 == 20*m1:
                    m1 = m1 + 1
                    print("parte ", m1*20, self.document.Paragraphs(item).Range.Text)
                c1 = c1+1
            #self.remove_sections()
            #self.close_document()
        except Exception as exc:
            printExceptionInfo(exc)
            #print("exc---->", exc)
        finally:
            self.remove_sections()
            self.close_document()

    def fixAppendix(self):
        try:
            print("fixing appendix")
            self.basic_document_format()
            for blist in self.document.Lists:
                #self.removeBullets(blist)
                self.remove_list(blist)
            for paragraph in self.paragraphs:
                formatAnexos2(self.document, paragraph)
            self.general_paragraph_format()
            if self.document.Sections.Count < 2:
                print("no hay secciones adicionales")
                for paragraph in self.document.Paragraphs:
                    formatNumeralParagraph(self.document, paragraph)
            else:
                print("hay secciones adicionales")
                for section in self.document.Sections:
                    print("secciones")
                    format_sections(self.document, section)
                for section in self.document.Sections:
                    print("segundas secciones")
                    addSigners(self.document, section)
        except Exception as exc:
            printExceptionInfo(exc)
            #print(exc)
        finally:
            self.remove_sections()
            self.close_document()

    def fixClausulaAdicional(self):
        try:
            print("fixing clausula adicional")
            self.basic_document_format()
            tables = self.document.Tables
            for table in tables:
                table.ConvertToText(Separator="{")
            self.document.Content.Find.Execute(FindText="{", ReplaceWith=".== == ", Replace=2)
            for blist in self.document.Lists:
                #self.removeBullets(blist)
                self.remove_list(blist)
            for paragraph in self.paragraphs:
                formatClausulaAdicionalM(self.document, paragraph)
                formatAnexos2(self.document, paragraph)
                self.removeEmptyParagraph(paragraph)

            print("parrafos")
            self.paragraphs = self.document.Paragraphs
            self.paragraphs.Last.Range.Delete()

            self.general_paragraph_format()

            for section in self.document.Sections:
                print("segundas secciones")
                addSigners(self.document ,section)
            for paragraph in self.document.Paragraphs:
                self.remove_at_beginning_of_paragraph(paragraph) #white spaces
        except Exception as exc:
            printExceptionInfo(exc)
            #print(exc)
        finally:
            self.remove_sections()
            self.close_document()

    def fixContract(self):
        try:
            print("fixing contract", self.document.Shapes.Count)
            if self.document.Shapes.Count > 0:
                for index in range(self.document.Shapes.Count):
                    self.remove_shape(1)        
            print("entrado a tablas")
            tables = self.document.Tables
            if self.document.Tables.Count > 0:
                with open(bancoTablasPath) as f:
                    tablasBancos = json.load(f)
                for table in tables:
                    if self.info == "ScotiaBank Peru S.A.A.":
                        formatTabla(table, tablasBancos, banco=self.info)
                    table.ConvertToText(Separator="{")
                self.document.Content.Find.Execute(FindText="{", ReplaceWith=".== == ", Replace=2)
            self.document.Content.Cut()
            self.document.Content.PasteSpecial(DataType=2)
            self.document.Content.Font.Name = "Anonymous"
            self.document.Content.Font.Size = 8
            self.basic_document_format()
            if self.document.Lists.Count > 0:
                for blist in self.document.Lists:
                    #self.removeBullets(blist)
                    self.remove_list(blist)
            print("Paragraphs: ", self.document.Paragraphs.Count, self.info)
            for item in range(1, self.document.Paragraphs.Count+1):
                #self.formatClausulaAdicional(paragraph)
                if self.info == "ScotiaBank Peru S.A.A.":
                    formatBanco(self.document, self.document.Paragraphs(item), bancoDataPath, self.info)
                elif self.info == "Banco del Credito del Peru" or self.info == "Interbank":
                    with open(clausulasBancoPath) as f:
                        clausulasBancos = json.load(f)
                    formatClausulas4(self.document, self.document.Paragraphs(item), clausulasBancos["Banco del Credito del Peru"])#clausulasBancos[self.info])
                #print("saliendo de format")
                extendDate2(self.document, self.document.Paragraphs(item))
                extendDateToString(self.document, self.document.Paragraphs(item))
                extendDateToStringWithPoint(self.document, self.document.Paragraphs(item))
                extendNumbers(self.document, self.document.Paragraphs(item))

            print("parrafos")
            self.paragraphs = self.document.Paragraphs
            for paragraph in self.document.Paragraphs:
                formatIndentation(paragraph)
                self.justifyAlignment(paragraph)
                self.removeSectionBreak(paragraph)
                self.removeTabs(paragraph)
                self.removeSpecialCharacters(paragraph)
                self.setSpaceBetweenLetters(paragraph)
                #self.define_sections(paragraph)
                self.removeEmptyParagraph(paragraph)
            for paragraph in self.document.Paragraphs:
                self.remove_at_beginning_of_paragraph(paragraph)
            self.remove_sections()
            with open(signersBancoPath) as f:
                signersBancos = json.load(f)
            addSignerToBankDocument(self.document ,signersBancos, banco=self.info)
            print("before close")
            #self.close_document()
        except Exception as exc:
            printExceptionInfo(exc)
            #print(exc)
        finally:
            self.close_document()

#########################
    def basic_document_format(self):
        self.document.PageSetup.LeftMargin = self.cm_to_points(2.5)
        self.document.PageSetup.RightMargin = self.cm_to_points(2.5)
        self.document.PageSetup.TopMargin = self.cm_to_points(2.5)
        self.document.PageSetup.BottomMargin = self.cm_to_points(2.5)
        self.document.PageSetup.Gutter = self.cm_to_points(0)
        self.document.Content.ParagraphFormat.LineSpacing = 19.200000762939453
        self.document.Content.ParagraphFormat.SpaceAfter = 0
        self.document.Content.Font.Name = "Anonymous"
        self.document.Content.Font.Size = 8
   
    def cm_to_points(self, value):
        return value*10/0.353

    def deleteSigners(self, paragraph):
        range_ = paragraph.Range
        isDots = range_.Find.Execute(FindText="           ")
        if isDots:
            rdStart = range_.Start
            range_2 = paragraph.Range(rdStart, self.Document.Content.End)
            range_2.Delete()

    def define_sections(self, paragraph):
        """
            Separa las siguientes secciones: preambulo, clausulas y anexos.
            Agrupa todas las clausulas en una seccion
            Cada anexo lo separa por seccion.
        """
        rangeParagraph = paragraph.Range
        isClausula = rangeParagraph.Find.Execute(FindText="P R I M E R A")
        #rtStart, rtEnd = rangeParagraph.Start, rangeParagraph.End
        rangeParagraph = paragraph.Range
        isClausula2 = rangeParagraph.Find.Execute(FindText="CLAUSULA PRIMERA")
        rangeParagraph = paragraph.Range
        isAnexo = rangeParagraph.Find.Execute(FindText="ANEXO")
        isAnexo2 = re.search(r'^ANEXO', rangeParagraph.Text)
        isComprador = rangeParagraph.Find.Execute(FindText="COMPRADOR")
        #rtStart2, rtEnd2 = rangeParagraph.Start, rangeParagraph.End
        rtStart, rtEnd = paragraph.Range.Start, paragraph.Range.End
        if (isClausula==True and rtEnd - rtStart < 20) or (isClausula2==True and rtEnd - rtStart < 20):
            self.document.Sections.Add(Range=rangeParagraph, Start=0)#, Start=2)
            print("se definio una seccion")
        elif isAnexo2 and rtEnd - rtStart < 60:
            self.document.Sections.Add(Range=rangeParagraph, Start=0)
            print("se definio una seccion con anexo")
        """elif isAnexo == True and rtEnd - rtStart < 60:
            self.document.Sections.Add(Range=rangeParagraph, Start=0)#, Start=2)
            print("se definio una seccion con anexo")"""

    def justifyAlignment(self, paragraph):
        paragraph.Alignment = 3
        paragraph.Space1

    def removeEmptyParagraph(self, paragraph):
        range_ = paragraph.Range
        threshold = range_.End-range_.Start
        if threshold < 6:
            range_.Delete()

    def removeNotario(self, paragraph):
        range_ = paragraph.Range
        sn = range_.Find.Execute(FindText="SEÑOR NOTARIO")
        th_sn = range_.End-range_.Start
        threshold = paragraph.Range.End - paragraph.Range.Start
        if sn == True and threshold < th_sn*2:
            paragraph.Range.Delete()

    def removeSectionBreak(self, paragraph):
        paragraph.Range.Find.Execute(FindText="^b", ReplaceWith="", Replace=2)

    def removeTabs(self, paragraph):
        rt = paragraph.Range.Find.Execute(FindText="\t", ReplaceWith=" ", Replace=2)

    def removeSpecialCharacters(self, paragraph):
        paragraph.Range.Find.Execute(FindText="\x0b", ReplaceWith="", Replace=2)

    def removeBullets(self, blist):
        lista = []
        for la in blist.Range.ListParagraphs:
            lista.append(la.Range.Text)
        for la in blist.Range.ListParagraphs:
            for lb in lista:
                if la.Range.Text == lb:
                    la.Range.Find.Execute(FindText=la.Range.Text, ReplaceWith="• "+lb, Replace=2)

    def remove_list(self, blist):
        # Verificar el tipo de lista
        for par in blist.Range.ListParagraphs:
            listType_ = par.Range.ListFormat.ListType
            #print(listType_)
            if listType_ == 2:
                #print("son bullets")
                rangeStart = par.Range.Start
                range_ = self.document.Range(rangeStart, rangeStart)
                range_.InsertBefore("• ")
                par.Range.ListFormat.RemoveNumbers(3)
        # Eliminar las vinetas o numeracion
        # Si es bullet, insertar al principio de cada parrafo "• "
        # Si es numero, insertar el numero en cada parrafo "1. "
        # Si es letra, insertar la letra en cada parrafo "A. "

    def remove_sections(self):
        self.document.Content.Find.Execute(FindText="\x0c", ReplaceWith="", Replace=2)

    def remove_shape(self, item):
        self.document.Shapes(item).Delete

    def setSpaceBetweenLetters(self, paragraph):
        paragraph.Range.Font.Spacing = 0

    def close_document(self):
        #self.document.SaveAs2()
        print("closing")
        self.document.SaveAs()
        self.document.Close(SaveChanges=-1)

    def general_paragraph_format(self):
        print("parrafos")
        self.paragraphs = self.document.Paragraphs
        for paragraph in self.document.Paragraphs:
            formatIndentation(paragraph)
            self.justifyAlignment(paragraph)
            self.removeSectionBreak(paragraph)
            self.removeTabs(paragraph)
            extendDate(self.document, paragraph)
            self.removeSpecialCharacters(paragraph)
            self.setSpaceBetweenLetters(paragraph)
            self.define_sections(paragraph)
            self.removeEmptyParagraph(paragraph)

    def remove_at_beginning_of_paragraph(self, paragraph):
        isBold = paragraph.Range.Font.Bold
        isUnderline = paragraph.Range.Underline
        pStart, pEnd = paragraph.Range.Start, paragraph.Range.End
        txt_ = paragraph.Range.Text
        match = re.search(r'^\s+', txt_)
        if match:
            txt_out = txt_[match.end():]
            paragraph.Range.Text = txt_out
            if isBold:
                self.document.Range(pStart-match.end(), pEnd-match.end()).Font.Bold = True
            if isUnderline:
                self.document.Range(pStart-match.end(), pEnd-match.end()).Underline = 1