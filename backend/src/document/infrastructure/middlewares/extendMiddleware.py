import re
""" Funciones que extienden numeros
"""
from backend.src.document.infrastructure.interfaces.text_utils import extend_date, extended_numbers, date_to_string, date_to_string_with_point

def extendDate(document, paragraph):
    rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
    months = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    for month in months:
        rangeParagraph = document.Range(rpStart, rpEnd)
        isWord = rangeParagraph.Find.Execute(FindText=month)
        if isWord == True:
            rdStart, rdEnd = rangeParagraph.Start, rangeParagraph.End
            if rdEnd+10 > rpEnd:
                txt = document.Range(rdStart-18, rpEnd).Text
            else:
                txt = document.Range(rdStart-18, rdEnd+10).Text
                #print(txt)
            txt_ = extended_numbers(txt)
            #print(txt_)
            paragraph.Range.Find.Execute(FindText=txt, ReplaceWith=txt_, Replace=2)

def extendDate2(document, paragraph):
    rpStart = paragraph.Range.Start
    rangeInsert = document.Range(rpStart, rpStart)
    txt_ = extend_date(paragraph.Range.Text)
    if txt_ != paragraph.Range.Text:
        paragraph.Range.Delete(1)
        rangeInsert.InsertAfter(txt_)
        print("extendDate")

def extendDateToString(document, paragraph):
    months = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    rpStart = paragraph.Range.Start
    rangeInsert = document.Range(rpStart, rpStart)
    txt_ = date_to_string(paragraph.Range.Text)
    matchs = re.findall(r'\(([\w\s.-]+)\)', txt_)
    matchs_ = []
    for month in months:
        for match in matchs:
            if month in match:
                matchs_.append(match)
    if txt_ != paragraph.Range.Text and len(matchs_) < 2:
        paragraph.Range.Delete(1)
        rangeInsert.InsertAfter(txt_)
        print("Date to string")

def extendDateToStringWithPoint(document, paragraph):
    months = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
    rpStart = paragraph.Range.Start
    rangeInsert = document.Range(rpStart, rpStart)
    txt_ = date_to_string_with_point(paragraph.Range.Text)
    matchs = re.findall(r'\(([\w\s.-]+)\)', txt_)
    matchs_ = []
    for month in months:
        for match in matchs:
            if month in match:
                matchs_.append(match)
    if txt_ != paragraph.Range.Text and len(matchs_) < 2:
        paragraph.Range.Delete(1)
        rangeInsert.InsertAfter(txt_)
        print("Date to string with point")

def extendNumbers(document, paragraph):
    cond1 = "US$" in paragraph.Range.Text or "S/" in paragraph.Range.Text or "%" in paragraph.Range.Text or "US$" in paragraph.Range.Text
    if cond1:
        params = ['POR CIENTO', 'SOLES', 'DOLARES AMERICANOS']
        rpStart = paragraph.Range.Start
        rangeInsert = document.Range(rpStart, rpStart)
        txt_ = extended_numbers(paragraph.Range.Text)
        matchs = re.findall(r'\(([\w\s\/.-]+)\)', txt_)
        matchs_ = []
        for match in matchs:
            if "CON" in match:
                m2 = match.split("CON")
                matchs_.append("Y".join(m2))
            else:
                matchs_.append(match)
        no_dupes = [x for n, x in enumerate(matchs_) if x not in matchs_[:n]] # igual a matchssi no hay duplicados
        
        if txt_ != paragraph.Range.Text and matchs_ == no_dupes:# and (cond1):
            print(txt_, "-------------", paragraph.Range.Text)
            paragraph.Range.Delete(1)
            rangeInsert.InsertAfter(txt_)
            #print("extend numbers")

def extendArea(document, paragraph):
    rpStart, rpEnd = paragraph.Range.Start, paragraph.Range.End
    #print(rpStart, rpEnd)
    area = ' M2'
    areaText = "METROS CUADRADOS"
    #for month in months:
    rangeParagraph = document.Range(rpStart, rpEnd)
    isWord = rangeParagraph.Find.Execute(FindText=area)
    rdStart, rdEnd = rangeParagraph.Start, rangeParagraph.End
    range2Paragraph = document.Range(rpStart, rpEnd)
    isWord2 = rangeParagraph.Find.Execute(FindText=areaText)
    if isWord == True and isWord2 == False:
        paragraph.Range.Find.Execute(FindText=" M2", ReplaceWith="%", Replace=2)
        txt = document.Range(rpStart, rdEnd).Text
        txt_ = extended_numbers(txt)
        paragraph.Range.Find.Execute(FindText=txt, ReplaceWith=txt_, Replace=2)