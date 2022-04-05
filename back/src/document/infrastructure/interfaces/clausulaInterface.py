import platform
import re
import json

from back.src.libs.config import archivos

if platform.uname().node == 'EQUIPO':
    clausulasPath = archivos()["clausulasPath"]#"D:\\bot-hip\\back\\src\\libs\\clausulas.json"
else:
    clausulasPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\back\\src\\libs\\clausulas.json"

class Clausula:
    def __init__(self):
        pass
    
    def matchClausula(self, txt_, clausula):
        re1 = r'CLAUSULA\s+{}:'.format(clausula["numero"])
        re2 = r'CLAUSULA\s+{}+\s+:'.format(clausula["numero"])
        re3 = r'\s+CLAUSULA\s+{}+\s+:'.format(clausula["numero"])
        matchClausula = re.search(re1, txt_) or re.search(re3, txt_) or re.search(re3, txt_)
        re4 = r'{}:'.format(clausula["numero"])
        re5 = r'{}\s:'.format(clausula["numero"])
        re6 = r'\s{}\s:'.format(clausula["numero"])
        matchClausula2 = re.search(re4, txt_) or re.search(re5, txt_) or re.search(re6, txt_)
        re7 = r'CLAUSULA\s+{}.(-|\s)'.format(clausula["numero"])
        re8 = r'CLAUSULA\s+{}+\s+.(-|\s)'.format(clausula["numero"])
        re9 = r'\s+CLAUSULA\s+{}+\s+.(-|\s)'.format(clausula["numero"])
        matchClausula3 = re.search(re7, txt_) or re.search(re8, txt_) or re.search(re9, txt_)
        re10 = r'{}.(-|\s)'.format(clausula["numero"])
        re11 = r'{}\s.(-|\s)'.format(clausula["numero"])
        re12 = r'\s{}\s.(-|\s)'.format(clausula["numero"])
        matchClausula4 = re.search(re10, txt_) or re.search(re11, txt_) or re.search(re12, txt_)

        clausulaReemplazo = None
        clausulaMatch = None

        if (matchClausula) or (matchClausula3 and matchClausula3.start() == 0):
            if matchClausula:
                clausulaMatch = matchClausula.group()
            if matchClausula3:
                clausulaMatch = matchClausula3.group()
            clausulaReemplazo = "CLAUSULA {}:".format(clausula["numero"])
        elif (matchClausula2 and matchClausula2.start() == 0) or (matchClausula4 and matchClausula4.start() == 0):
            if matchClausula2 and matchClausula2.start() == 0:
                clausulaMatch = matchClausula2.group()
            if matchClausula4:
                clausulaMatch = matchClausula4.group()
            #clausulaMatch = matchClausula2.group()
            clausulaReemplazo = clausula["reemplazo"]

        return clausulaMatch, clausulaReemplazo

    def format(self, document):
        with open(clausulasPath) as f:
            clausulas = json.load(f)
        for item in range(1, document.Paragraphs.Count + 1):
            txt_ = document.Paragraphs(item).Range.Text
            spanLineas = document.Paragraphs(item).Range.Words.Last.Information(10) - document.Paragraphs(item).Range.Words.First.Information(10)
            cond0 = spanLineas < 3
            wordsCount = document.Paragraphs(item).Range.Words.Count
            for clausula in clausulas["general"]:
                clausulaMatch, clausulaReemplazo = self.matchClausula(txt_, clausula)
                if clausulaMatch != None and clausulaReemplazo != None:
                    rpStart, rpEnd = document.Paragraphs(item).Range.Start, document.Paragraphs(item).Range.End
                    #document.Paragraphs(item).Range.Text = re.sub(clausulaMatch, clausulaReemplazo, document.Paragraphs(item).Range.Text)
                    document.Paragraphs(item).Range.Find.Execute(FindText=clausulaMatch, ReplaceWith=clausulaReemplazo, Replace=2)
                    rangeParagraph = document.Paragraphs(item).Range
                    rangeParagraph.Find.Execute(FindText=clausulaReemplazo)
                    rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
                    rpStart, rpEnd = document.Paragraphs(item).Range.Start, document.Paragraphs(item).Range.End
                    document.Range(rcStart, rcEnd).Font.Bold = True
                    document.Range(rcStart, rcEnd).Underline = 1
                    rtEnd = rpEnd
                    spanLineas = document.Paragraphs(item).Range.Words.Last.Information(10) - document.Paragraphs(item).Range.Words.First.Information(10)
                    cond0 = spanLineas < 3
                    wordsCount = document.Paragraphs(item).Range.Words.Count
                    if cond0 == True and rpEnd > rcEnd+2 and wordsCount<15:
                        rtStart, rtEnd = rcEnd+1, document.Paragraphs(item).Range.End #rpEnd
                        document.Range(rtStart-1, rtEnd).Font.Bold = True
                        document.Range(rtStart, rtEnd).Underline = 0
                    end = rcEnd #- 1
                    range_ = document.Range(end, rtEnd)#rpEnd)
                    document.Paragraphs.Add(range_)
                    if rcStart != rpStart:
                        document.Paragraphs.Add(document.Range(rcStart, rcEnd))

    def format2(self, document):
        with open(clausulasPath) as f:
            clausulas = json.load(f)
        for paragraph in document.Paragraphs:
            txt_ = paragraph.Range.Text
            spanLineas = paragraph.Range.Words.Last.Information(10) - paragraph.Range.Words.First.Information(10)
            cond0 = spanLineas < 3
            wordsCount = paragraph.Range.Words.Count
            for clausula in clausulas["general"]:
                clausulaMatch, clausulaReemplazo = self.matchClausula(txt_, clausula)
                if clausulaMatch != None and clausulaReemplazo != None:
                    rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
                    #paragraph.Range.Text = re.sub(clausulaMatch, clausulaReemplazo, paragraph.Range.Text)
                    paragraph.Range.Find.Execute(FindText=clausulaMatch, ReplaceWith=clausulaReemplazo, Replace=2)
                    rangeParagraph = paragraph.Range
                    rangeParagraph.Find.Execute(FindText=clausulaReemplazo)
                    rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
                    document.Range(rcStart, rcEnd).Font.Bold = True
                    document.Range(rcStart, rcEnd).Underline = 1
                    rtEnd = rpEnd
                    if cond0 == True and rpEnd > rcEnd+2 and wordsCount<15:
                        rtStart, rtEnd = rcEnd+1, paragraph.Range.End #rpEnd
                        document.Range(rtStart-1, rtEnd).Font.Bold = True
                        document.Range(rtStart, rtEnd).Underline = 0
                    end = rcEnd #- 1
                    range_ = document.Range(end, rtEnd)#rpEnd)
                    document.Paragraphs.Add(range_)
                    if rcStart != rpStart:
                        document.Paragraphs.Add(document.Range(rcStart, rcEnd))


    def formatClausaAdicional(self, document):
        sections = document.Sections
        for section in sections:
            paragraphs = section.Range.Paragraphs
            if "CLAUSULA ADICIONAL" in paragraphs(1).Range.Text:
                for paragraph in paragraphs:
                    rangeParagraph = paragraph.Range

                    titulo = re.findall("[ A-Z]*CLAUSULA ADICIONAL[ A-Z]*:(.*)",rangeParagraph.Text)

                    if titulo:
                        rangeParagraph.Font.Bold = True
                        rangeParagraph.Font.Underline = True

                        if titulo[0] != '\r':
                            paragEnd = rangeParagraph.End
                            rangeParagraph.Find.Execute(FindText=":")
                            newParagStart = rangeParagraph.End
                            document.Range(newParagStart, paragEnd).Font.Underline = False
                            rangeParagraph.InsertParagraphAfter()

    def formatTitulosScottia(self, document):
        section = document.Sections(1)
        paragraphs = section.Range.Paragraphs
        for paragraph in paragraphs:
            rangeParagraph = paragraph.Range
            titulo = re.search('^\d\.|^[IVXLCDM]+\)',rangeParagraph.Text)
            if titulo and rangeParagraph.Words.Count < 12:
                rangeParagraph.Font.Bold = True
                if re.search(r'^ANEXO', rangeParagraph.Text):
                    break

    def formatAnexos(self, document):

        params = [ 
            "ANEXO I", 
            "ANEXO", 
            "ANEXO 'A'",
            "ANEXO A",
            "ANEXO 1"
            ]

        for section in document.Sections:
            paragraphs = section.Range.Paragraphs
            for param in params:
                if param in paragraphs(1).Range.Text:
                    for paragraph in paragraphs:
                        spanLineas = paragraph.Range.Words.Last.Information(10) - paragraph.Range.Words.First.Information(10) 
                        cond0 = spanLineas < 3 
                        #if "NUMERAL" in paragraph.Range.Text:
                        match_numeral = re.match("^(\s*)(NUMERAL)(\s+)((M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})){1})(\s*)(:?)", paragraph.Range.Text)#paragraph.Range.Text)
                        match_anexo = re.match("^(\s*)(ANEXO)(\s*)(((M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))?)(([A-Z]{1})?))", paragraph.Range.Text)
                        rangeParagraph = paragraph.Range
                        if match_numeral and cond0:
                            rangeParagraph.Font.Bold = True

                        if match_anexo and cond0:
                            paragraph.Range.Font.Bold = True