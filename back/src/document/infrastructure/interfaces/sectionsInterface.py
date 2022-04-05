import re

class Sections:
    def __init__(self):
        pass

    def define(self, document):
        print("secciones entrada ", document.Sections.Count)
        paragraphs = document.Paragraphs
        params = [ 
            "P R I M E R A:", 
            "P R I M E R O:", 
            "CLAUSULA PRIMERA:", 
            "CLAUSULA PRIMERO:", 
            "ANEXO I", 
            "ANEXO", 
            "CLAUSULA ADICIONAL",
            "ANEXO 'A'",
            "ANEXO A",
            "ANEXO 1",
            "CLAUSULA DE PROTECCION DE DATOS PERSONALES" ##NUEVA DEFINICION DE CLAUSULA 
            ]
        for paragraph in paragraphs:
            """txt_ = paragraph.Range.Text
            if self.findParameterAtBeginning(txt_, "ANEXO"):
                document.Sections.Add(Range=paragraph.Range, Start=0)
                print("seccion def", txt_)"""
            for param in params:
                txt_ = paragraph.Range.Text
                isClausula = self.findParameterAtBeginning(txt_, param)
                if isClausula == True:
                    document.Sections.Add(Range=paragraph.Range, Start=0)

        print("secciones salida ", document.Sections.Count)


    def findParameterAtBeginning(self, txt, param):
        param_ = None
        if param == "ANEXO" and param == "ANEXO 1":
            param_ = r'^(|\s+){}(|\s+)$'.format(param)
        else:
            param_ = r'^(|\s){}'.format(param)
        isClausula = re.search(param_, txt)
        if isClausula:
            return True
        else:
            return False

    def remove(self, document):
        document.Content.Find.Execute(FindText="\x0c", ReplaceWith="", Replace=2)

    def sectionClausulaFormat(self, document):
        params = [ 
            "P R I M E R A:", 
            "P R I M E R O:", 
            "CLAUSULA PRIMERA:", 
            "CLAUSULA PRIMERO:"
            ]
        for section in document.Sections:
            paragraphs = section.Range.Paragraphs
            for param in params:
                if param in paragraphs(1).Range.Text:
                    seccion = section.Range
                    cuenta = seccion.Paragraphs.Count
                    for i in reversed(range(cuenta)):
                        
                        text = seccion.Paragraphs(i+1).Range.Text
                        seccion.Paragraphs(i+1).Range.Delete() 
                        if "CLIENTE" in text:
                            break        
                        
                    cuenta = seccion.Paragraphs.Count
                    seccion.Paragraphs(cuenta).Range.InsertParagraphAfter()
                    cuenta = seccion.Paragraphs.Count
                    seccion.Paragraphs(cuenta).Range.InsertAfter(Text:="A CONTINUACION ………. FIRMAS ILEGIBLES") 
                    seccion.Paragraphs(cuenta).Range.InsertParagraphAfter()
                    cuenta = seccion.Paragraphs.Count
                    seccion.Paragraphs(cuenta).Range.InsertAfter(Text:="………….., ABOGADO, C.A.L. NRO. ………..., UNA FIRMA ILEGIBLE")

    def eliminarFirmantes(self, document):

        document.Content.Find.Execute(FindText="\x0c", ReplaceWith="", Replace=2)

        ##CONSTRUCTOR DE REGEX 
        def regexFirmas():

            tiposFirmas = [
                '(?i)^CLIENTE +CONYUGE DEL CLIENTE',
                '^CLIENTE$',
                '^\.==.+EL CLIENTE.+\.==',
                '^(EL|LA) \w+ +(EL|LA) +\w+$',
                '^EL BANCO +EL CLIENTE'
            ]
            regFirma = ''
            for tipoFirma in tiposFirmas:
                if regFirma == '':
                    regFirma = tipoFirma
                else:
                    regFirma = regFirma + '|' + tipoFirma #"OR" PARA MAS POSIBILIDADES DE FIRMAS
            return regFirma
        regFirmas = regexFirmas()
    

        secciones= document.Sections

        for seccion in secciones:
            erase = False
            parrafos= seccion.Range.Paragraphs
            numParrafos = parrafos.Count
            for parrafo in parrafos:
                if re.search(regFirmas,parrafo.Range.Text):
                    erase = True
                if erase:
                    parrafo.Range.Delete()
            if erase:
                numParrafos = parrafos.Count
                seccion.Range.Paragraphs(numParrafos).Range.InsertParagraphAfter()
                seccion.Range.Paragraphs(numParrafos).Range.InsertAfter(Text:="………….., ABOGADO, C.A.L. NRO. ………..., UNA FIRMA ILEGIBLE")
                seccion.Range.Paragraphs(numParrafos).Range.InsertParagraphAfter()
                seccion.Range.Paragraphs(numParrafos).Range.InsertAfter(Text:="A CONTINUACION ………. FIRMAS ILEGIBLES")                                    