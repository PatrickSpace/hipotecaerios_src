""" Funciones que agregan informacion adicional
    a los documentos
"""
import re

def addNotario(document):
    range_ = document.Range(0,0)
    document.Paragraphs.Add(range_)
    range_.InsertBefore("SEÑOR NOTARIO: DR. ALFREDO PAINO SCARPATI")

def addSigner(document, section):
    paragraphs = section.Range.Paragraphs
    if paragraphs(paragraphs.Count).Range.Text == '\x0C':
        range_ = paragraphs(paragraphs.Count-1).Range
    else:
        range_ = paragraphs(paragraphs.Count).Range
    range_Insert = document.Range(range_.End-1, range_.End-1)
    range_Insert.InsertAfter("A CONTINUACION ... FIRMAS ILEGIBLES \rUN SELLO QUE DICE: ........, ABOGADO, C.A.C. ........ (...).- UNA FIRMA ILEGIBLE.")
    document.Paragraphs.Add(range_Insert)

def addSigners(document, section):
    #for section in sections:
    paragraphs = section.Range.Paragraphs
    print("parrafos: ", paragraphs.Count)
    print(paragraphs(1).Range.End - paragraphs(1).Range.Start)
    rangeTitle = paragraphs(1).Range
    if rangeTitle.Find.Execute(FindText="ANEXO A") == True:
        addSigner(document, section)
        formatNumeral(section)
        pass
    elif rangeTitle.Find.Execute(FindText="PAINO") == True:
        pass
    elif rangeTitle.Find.Execute(FindText="P R I M E R A") == True:
        addSigner(document, section)
        pass
    elif rangeTitle.Find.Execute(FindText="CLAUSULA PRIMERA") == True:
        addSigner(document, section)
        pass
    elif paragraphs(1).Range.End - paragraphs(1).Range.Start < 5:
        pass
    else:
        addSigner(document, section)
        formatNumeral(section)

def formatNumeral(section):
    """for paragraph in section.Range.Paragraphs:
        range_ = paragraph.Range
        isNumeral = range_.Find.Execute(FindText="NUMERAL")
        if isNumeral == True:
            paragraph.Range.Font.Bold = True"""
    for paragraph in section.Range.Paragraphs:
        range_ = paragraph.Range
        match_ = re.search(r'^NUMERAL', paragraph.Range.Text)
        isNumeral = range_.Find.Execute(FindText="NUMERAL")
        #if isNumeral == True and range_.Start == paragraph.Range.Start:
        if match_:
            paragraph.Range.Font.Bold = True

def addSignerToBankDocument(document, signers, banco="ScotiaBank Peru S.A.A."):
    paragraph = document.Paragraphs.Last
    range_ = paragraph.Range
    banco_ = range_.Find.Execute(FindText="EL BANCO")
    th_bn = range_.End-range_.Start
    range_ = paragraph.Range
    cliente = range_.Find.Execute(FindText="EL CLIENTE")
    th_cl = range_.End-range_.Start
    threshold = paragraph.Range.End - paragraph.Range.Start
    if banco_ == True and cliente == True and threshold < (th_bn+th_cl)*2:
        paragraph.Range.Delete()
    end = document.Content.End - 1
    range_ = document.Range(end, end)
    print("signers ", signers, signers[banco])
    range_.InsertAfter(signers[banco]["abogado"])
    document.Paragraphs.Add(range_)