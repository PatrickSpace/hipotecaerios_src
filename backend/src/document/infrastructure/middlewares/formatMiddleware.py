import json
import re
from backend.src.document.infrastructure.middlewares.printExceptionInfo import *
""" Prueba de middleware
"""
def formatClausulaAdicionalM(document, paragraph):
    clausulas = [
        {"numero": "PRIMERA: ", "reemplazo": "P R I M E R A:"},
        {"numero": "SEGUNDA: ", "reemplazo": "S E G U N D A:"},
        {"numero": "TERCERA: ", "reemplazo": "T E R C E R A:"},
        {"numero": "TERCERA:", "reemplazo": "T E R C E R A:"},
        {"numero": "CUARTA: ", "reemplazo": "C U A R T A:"},
        {"numero": "QUINTA: ", "reemplazo": "Q U I N T A:"},
        {"numero": "SEXTA: ", "reemplazo": "S E X T A:"},
        {"numero": "SEPTIMA: ", "reemplazo": "S E P T I M A:"},
        {"numero": "OCTAVA: ", "reemplazo": "O C T A V A:"},
        {"numero": "NOVENA: ", "reemplazo": "N O V E N A:"},
        {"numero": "DECIMA: ", "reemplazo": "D E C I M A:"},
        {"numero": "DECIMO PRIMERA: ", "reemplazo": "DECIMO PRIMERA:"},
        {"numero": "DECIMO SEGUNDA: ", "reemplazo": "DECIMO SEGUNDA:"},
        {"numero": "DECIMO TERCERA: ", "reemplazo": "DECIMO TERCERA:"},
        {"numero": "DECIMO CUARTA: ", "reemplazo": "DECIMO CUARTA:"},
        {"numero": "DECIMO QUINTA: ", "reemplazo": "DECIMO QUINTA:"},
        {"numero": "DECIMO SEXTA: ", "reemplazo": "DECIMO SEXTA:"},
        {"numero": "DECIMO SEPTIMA: ", "reemplazo": "DECIMO SEPTIMA:"},
        {"numero": "DECIMO OCTAVA: ", "reemplazo": "DECIMO OCTAVA:"},
        {"numero": "DECIMO NOVENA: ", "reemplazo": "DECIMO NOVENA:"},
        {"numero": "VIGESIMA: ", "reemplazo": "V I G E S I M A:"},
        {"numero": "CLAUSULA ADICIONAL:", "reemplazo": "CLAUSULA ADICIONAL:"}
    ]
    for clausula in clausulas:
        rangeParagraph = paragraph.Range
        rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
        isWord = rangeParagraph.Find.Execute(FindText=clausula["numero"])
        if isWord == True:
            rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
            if rpStart == rcStart:
                rangeParagraph.Find.Execute(FindText=clausula["numero"], ReplaceWith=clausula["reemplazo"], Replace=2)
                rangeParagraph.Find.Execute(FindText=clausula["reemplazo"])
                rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
                rangeParagraph = paragraph.Range
                #rangeParagraph.Find.Execute(FindText=clausula["titulo"])
                #rtStart, rtEnd = rangeParagraph.Start, rangeParagraph.End
                rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
                document.Range(rcStart, rcEnd-1).Font.Bold = True
                document.Range(rcStart, rcEnd-1).Underline = 1
                #document.Range(rtStart, rtEnd).Font.Bold = True
                #document.Range(rtStart, rtEnd).Underline = 0
                end = rcEnd #- 1
                range_ = document.Range(end, rpEnd)
                document.Paragraphs.Add(range_)
                #if rcStart != rpStart:
                #    document.Paragraphs.Add(document.Range(rcStart, rcEnd))
    pass

def formatAnexos(document, paragraph):
    anexos = [
        {"anexo": "ANEXO A", "titulo": "INFORMACION DEL COMPRADOR"},
        {"anexo": "ANEXO B", "titulo": "INFORMACION DEL EDIFICIO"},
        {"anexo": "ANEXO C", "titulo": "INFORMACION DE LOS INMUEBLES"},
        {"anexo": "ANEXO E", "titulo": "HOJA RESUMEN"}
    ]
    for anexo in anexos:
        rangeParagraph = paragraph.Range
        rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
        isAnexo = rangeParagraph.Find.Execute(FindText=anexo["anexo"])
        if isAnexo==True and rangeParagraph.Start==rpStart:# and rpStart==raStart:#rpEnd-rpStart < raEnd-raStart+rtEnd-rtStart+10:
            document.Range(rpStart, rpEnd).Font.Bold = True
            #print(document.Range(rpStart, rpEnd).Text)
            print("formating anexos")
            raStart, raEnd = rangeParagraph.Start, rangeParagraph.End
            rangeParagraph = paragraph.Range
            isTitulo = rangeParagraph.Find.Execute(FindText=anexo["titulo"])
            if isTitulo == True:
                rtStart, rtEnd = rangeParagraph.Start, rangeParagraph.End
                print("titulo coincide")
            isNumeral = paragraph.Range.Find.Execute(FindText="NUMERAL")
            if isNumeral == True:
                print("encontro numeral")
                range_ = document.Range(rtEnd+1, rpEnd)
                document.Paragraphs.Add(range_)

def formatAnexos2(document, paragraph):
    #print("format anexos 2")
    match_ = re.search(r'^ANEXO', paragraph.Range.Text)
    spanLineas = paragraph.Range.Words.Last.Information(10) - paragraph.Range.Words.First.Information(10)
    cond0 = spanLineas < 3
    if match_ and cond0 == True:
        paragraph.Range.Font.Bold = True
        if "NUMERAL" in paragraph.Range.Text:
            range_ = paragraph.Range
            rpEnd = range_.End
            range_.Find.Execute(FindText="NUMERAL")
            rnStart = range_.Start
            range_numeral = document.Range(rnStart, rpEnd)
            document.Paragraphs.Add(range_numeral)

def formatAnexos3(document, paragraph):
    match_ = re.search(r'^ANEXO\s+\w+:', paragraph.Range.Text)
    spanLineas = paragraph.Range.Words.Last.Information(10) - paragraph.Range.Words.First.Information(10)
    cond0 = spanLineas < 3
    if match_ and cond0:
        txt_ = match_.group()
        rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
        rangeParagraph = paragraph.Range
        rangeParagraph.Find.Execute(FindText=txt_)
        raStart, raEnd = rangeParagraph.Start, rangeParagraph.End
        if rpEnd != raEnd:
            rtStart, rtEnd = raEnd, rpEnd
            document.Range(raStart, raEnd).Font.Bold = True
            document.Range(raStart, raEnd).Underline = 1
            document.Range(rtStart, rtEnd).Font.Bold = True
            document.Range(rtStart, rtEnd).Underline = 0
            end = raEnd
            range_ = document.Range(end, raEnd)
            document.Paragraphs.Add(range_)
        else:
            document.Range(raStart, raEnd).Font.Bold = True
            document.Range(raStart, raEnd).Underline = 1

def formatBanco(document, paragraph, bancoDataPath, banco="ScotiaBank Peru S.A.A."):
    #print("dentro de format banco")
    with open(bancoDataPath) as f:
        datosBancos = json.load(f)
    datosBanco = datosBancos[banco]
    for datoBanco in datosBanco:
        rangeParagraph = paragraph.Range
        rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
        isBanco = rangeParagraph.Find.Execute(FindText=datoBanco["nombre"]) ##
        rbStart, rbEnd = rangeParagraph.Start, rangeParagraph.End
        lenParagraph = rpEnd - rpStart
        lenBanco = rbEnd - rbStart
        if isBanco==True and lenParagraph < 3.5*lenBanco:
            document.Range(rpStart, rpEnd).Font.Bold = True

def formatClausulas(document, paragraph, clausulas):
    for clausula in clausulas:
        rangeParagraph = paragraph.Range
        isWord = rangeParagraph.Find.Execute(FindText=clausula["numero"] + clausula["titulo"])
        if isWord == True:
            rangeParagraph.Find.Execute(FindText=clausula["numero"], ReplaceWith=clausula["reemplazo"], Replace=2)
            rangeParagraph.Find.Execute(FindText=clausula["reemplazo"])
            rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
            rangeParagraph = paragraph.Range
            rangeParagraph.Find.Execute(FindText=clausula["titulo"])
            rtStart, rtEnd = rangeParagraph.Start, rangeParagraph.End
            rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
            document.Range(rcStart, rcEnd-1).Font.Bold = True
            document.Range(rcStart, rcEnd-1).Underline = 1
            document.Range(rtStart, rpEnd).Font.Bold = True
            document.Range(rtStart, rpEnd).Underline = 0
            end = rcEnd - 1
            range_ = document.Range(rtStart, rtEnd)
            document.Paragraphs.Add(range_)
            if rcStart != rpStart:
                document.Paragraphs.Add(document.Range(rcStart, rcEnd))

def formatClausulas2(document, paragraph, clausulas):#def formatClausulaAdicional( paragraph):
    for clausula in clausulas:
        rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
        rangeParagraph = paragraph.Range
        isWord = rangeParagraph.Find.Execute(FindText=clausula["numero"])
        if isWord == True:
            rangeParagraph = paragraph.Range
            rangeParagraph.Find.Execute(FindText=clausula["numero"])
            rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
            print("rangos", rpStart, rpEnd, rcStart, rcEnd)
            if rpStart == rcStart:
                rangeParagraph.Find.Execute(FindText=clausula["numero"], ReplaceWith=clausula["reemplazo"], Replace=2)
                rangeParagraph.Find.Execute(FindText=clausula["reemplazo"])
                rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
                rangeParagraph = paragraph.Range
                #rangeParagraph.Find.Execute(FindText=clausula["titulo"])
                #rtStart, rtEnd = rangeParagraph.Start, rangeParagraph.End
                rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
                document.Range(rcStart, rcEnd-1).Font.Bold = True
                document.Range(rcStart, rcEnd-1).Underline = 1
                #document.Range(rtStart, rtEnd).Font.Bold = True
                #document.Range(rtStart, rtEnd).Underline = 0
                end = rcEnd #- 1
                range_ = document.Range(end, rpEnd)
                document.Paragraphs.Add(range_)
                #if rcStart != rpStart:
                #    document.Paragraphs.Add(document.Range(rcStart, rcEnd))
    pass

def formatNumeralParagraph(document, paragraph):
    range_ = paragraph.Range
    match_ = re.search(r'^NUMERAL', paragraph.Range.Text)
    isNumeral = range_.Find.Execute(FindText="NUMERAL")
    #if isNumeral == True and range_.Start == paragraph.Range.Start:
    if match_:
        paragraph.Range.Font.Bold = True
                
def format_sections(document, section):
    #for section in sections:
    paragraphs = section.Range.Paragraphs
    rangeTitle = paragraphs(1).Range
    if rangeTitle.Find.Execute(FindText="ANEXO A") == True:
        print("formato area")
        pass
    elif rangeTitle.Find.Execute(FindText="PAINO") == True:
        pass
    elif rangeTitle.Find.Execute(FindText="P R I M E R A") == True:
        pass
    elif rangeTitle.Find.Execute(FindText="CLAUSULA PRIMERA") == True:
        pass
    elif paragraphs(1).Range.End - paragraphs(1).Range.Start < 5:
        pass
    else:
        range_ = document.Range(rangeTitle.Start, rangeTitle.Start)
        range_.InsertBefore("I N S E R T O.")
        document.Range(range_.Start, range_.End-1).Font.Bold = True
        #range_.Font.Bold = True
        #range_.Underline = 1
        document.Range(range_.Start, range_.End-1).Underline = 1
        insertoEnd = range_.End
        paragraphs = section.Range.Paragraphs
        pEnd = paragraphs(1).Range.End
        document.Paragraphs.Add(document.Range(insertoEnd, pEnd))
            
def formatIndentation(paragraph):
    paragraph.LeftIndent = 0
    paragraph.RightIndent = 0
    paragraph.FirstLineIndent = 0

def formatTabla(tabla, datos, banco= "ScotiaBank Peru S.A.A."):
    datos[banco]
    for key in datos[banco].keys():
        tabla.Range.Find.Execute(FindText=datos[banco][key][0], ReplaceWith=datos[banco][key][1], Replace=2)

def formatSectionComprador1(document, section):
    if "ANEXO" in section.Range.Paragraphs(1).Range.Text:
        paragraphs = section.Range.Paragraphs
        lista = ["NOMBRE", "DNI", "DIRECCION", "N° PARTIDA", "ESTADO CIVIL", "CORREO ELECTRONICO"]
        for paragraph in paragraphs:
            rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
            for element in lista:
                range_ = paragraph.Range
                isElement = range_.Find.Execute(FindText=element)
                if isElement == True:
                    reStart = range_.Start
                    if reStart != rpStart:
                        document.Paragraphs.Add(document.Range(reStart, rpEnd))

def formatClausulas3(document, paragraph, clausulas):
    try:
        txt_ = paragraph.Range.Text
        print(txt_)
        for clausula in clausulas:
            # contruir un patron con la clausula
            print("numero cla....", clausula["numero"])
            re1 = r'([\s\w\.-]+{}+[\s]+):'.format(clausula["numero"])
            re2 = r'([\s\w\.-]+{}+):'.format(clausula["numero"])
            print(re2)
            reClausula = re.search(re1, txt_) or re.search(re2, txt_)
            ## si el patron existe en el parrafo y
            ## si el parrafo es menor a tres lineas
            #spanLineas = paragraph.Range.Words.Last.Information(10) - paragraph.Range.Words.First.Information(10)
            if reClausula:# and spanLineas < 3:
                print("entro a la clausula")
                # tomar el rango de la clausula
                rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
                rangeParagraph = paragraph.Range
                isWord = rangeParagraph.Find.Execute(FindText=clausula["numero"])
                rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.Start + reClausula.end() - reClausula.start()
                realWord = document.Range(rcStart, rcEnd)
                rangeParagraph = paragraph.Range
                rangeParagraph.Find.Execute(FindText=realWord, ReplaceWith=clausula["reemplazo"], Replace=2)
                isWord = rangeParagraph.Find.Execute(FindText=clausula["reemplazo"])
                rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
                rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
                rtStart, rtEnd = rcEnd+1, rpEnd
                document.Range(rcStart, rcEnd).Font.Bold = True
                document.Range(rcStart, rcEnd).Underline = 1
                document.Range(rtStart, rtEnd).Font.Bold = True
                document.Range(rtStart, rtEnd).Underline = 0
                end = rcEnd #- 1
                range_ = document.Range(end, rpEnd)
                document.Paragraphs.Add(range_)
                if rcStart != rpStart:
                    document.Paragraphs.Add(document.Range(rcStart, rcEnd))
                #- si la clausula es de una sola palabra, primera, entonces P R I M E R A:
                # dividir en dos parrafos despues de :
                # el parrafo de la clausula va en negrita y subrayado
                # el parrafo del subtitulo va en negrita
    except Exception as exc:
        printExceptionInfo(exc)
        #print("excepcion------", exc)

def formatClausulas4(document, paragraph, clausulas):
    txt_ = paragraph.Range.Text
    spanLineas = paragraph.Range.Words.Last.Information(10) - paragraph.Range.Words.First.Information(10)
    cond0 = spanLineas < 3
    wordsCount = paragraph.Range.Words.Count
    for clausula in clausulas:
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
        if (matchClausula) or (matchClausula3 and matchClausula3.start() == 0):
            if matchClausula:
                clausulaMatch = matchClausula.group()
            if matchClausula3:
                clausulaMatch = matchClausula3.group()
            clausulaReemplazo = "CLAUSULA {}:".format(clausula["numero"])
            # ahora trabajo con win32
            rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
            paragraph.Range.Find.Execute(FindText=clausulaMatch, ReplaceWith=clausulaReemplazo, Replace=2)
            rangeParagraph = paragraph.Range
            rangeParagraph.Find.Execute(FindText=clausulaReemplazo)
            rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
            #rtStart, rtEnd = rcEnd+1, rpEnd
            document.Range(rcStart, rcEnd).Font.Bold = True
            document.Range(rcStart, rcEnd).Underline = 1
            if cond0 == True and rpEnd > rcEnd+2 and wordsCount<15:
                rtStart, rtEnd = rcEnd+1, rpEnd
                #print("condicion cero", cond0)
                document.Range(rtStart, rtEnd).Font.Bold = True
                document.Range(rtStart, rtEnd).Underline = 0
            end = rcEnd #- 1
            range_ = document.Range(end, rpEnd)
            document.Paragraphs.Add(range_)
            if rcStart != rpStart:
                document.Paragraphs.Add(document.Range(rcStart, rcEnd))
        elif (matchClausula2 and matchClausula2.start() == 0) or (matchClausula4 and matchClausula4.start() == 0):
            if matchClausula2 and matchClausula2.start() == 0:
                clausulaMatch = matchClausula2.group()
            if matchClausula4:
                clausulaMatch = matchClausula4.group()
            #clausulaMatch = matchClausula2.group()
            clausulaReemplazo = clausula["reemplazo"]
            #rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
            paragraph.Range.Find.Execute(FindText=clausulaMatch, ReplaceWith=clausulaReemplazo, Replace=2)
            rangeParagraph = paragraph.Range
            rangeParagraph.Find.Execute(FindText=clausulaReemplazo)
            rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
            rcStart, rcEnd = rangeParagraph.Start, rangeParagraph.End
            #rtStart, rtEnd = rcEnd+1, rpEnd
            document.Range(rcStart, rcEnd).Font.Bold = True
            document.Range(rcStart, rcEnd).Underline = 1
            if cond0 == True and rpEnd > rcEnd+2 and wordsCount<15:
                print("condicion cero 2", cond0)
                rtStart, rtEnd = rcEnd+1, rpEnd
                document.Range(rtStart, rtEnd).Font.Bold = True
                document.Range(rtStart, rtEnd).Underline = 0
            end = rcEnd #- 1
            range_ = document.Range(end, rpEnd)
            document.Paragraphs.Add(range_)
            if rcStart != rpStart:
                document.Paragraphs.Add(document.Range(rcStart, rcEnd))

def remove_at_beginning_of_paragraph(paragraph):
    txt_ = paragraph.Range.Text
    match = re.search(r'^\s+', txt_)
    if match:
        txt_out = txt_[match.end():]
        paragraph.Range.Text = txt_out