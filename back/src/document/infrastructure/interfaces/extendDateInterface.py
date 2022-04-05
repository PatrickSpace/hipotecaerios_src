import re
from back.src.document.infrastructure.interfaces.text_utils import *


class ExtendDate:
    def __init__(self):
        pass

    def execute(self, document):
        paragraphs = document.Paragraphs
        countPar = paragraphs.Count
        for item in range(1, countPar + 1):
            txt = self.extension(paragraphs(item).Range.Text)
            #print(txt)
            if txt != paragraphs(item).Range.Text:
                paragraphs(item).Range.Text = txt

    def executeOld(self, document):
        #for paragraph in document.Paragraphs:
        paragraphs = document.Paragraphs
        countPar = paragraphs.Count
        for item in range(1, countPar + 1):
            paragraph = paragraphs(item)
            #self.extendDate2(paragraph, document)
            self.extendDateToString(paragraph, document)
            self.extendDateToStringWithPoint(paragraph, document)
            #self.extendNumbers(paragraph, document)

    def extendDate2(self, paragraph, document):
        rpStart = paragraph.Range.Start
        rangeInsert = document.Range(rpStart, rpStart)
        txt_ = extend_date(paragraph.Range.Text)
        if txt_ != paragraph.Range.Text:
            paragraph.Range.Delete(1)
            rangeInsert.InsertAfter(txt_)

    def extendDateToString(self, paragraph, document):
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
            paragraph.Range.Text = txt_
            #paragraph.Range.Delete(1)
            #rangeInsert.InsertAfter(txt_)

    def extendDateToStringWithPoint(self, paragraph, document):
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
            paragraph.Range.Text = txt_
            #paragraph.Range.Delete(1)
            #rangeInsert.InsertAfter(txt_)

    def extendNumbers(self, paragraph, document):
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
                paragraph.Range.Text = txt_# + "\r"
                #paragraph.Range.Delete(1)
                #rangeInsert.InsertAfter(txt_)

    def extensionOld(self, texto): #todavia hay que buscarle un nombre

        def extendArea (textoArea):
            auxiliar = re.sub('MT2','M2',textoArea)
            auxiliar = re.sub('METROS CUADRADOS', 'M2', textoArea)
            print("auxiliar ", auxiliar)
            
            textoArea = extended_numbers(auxiliar)[:-1]
            if auxiliar[-1] != "2":
                textoArea = textoArea+ auxiliar[-1]
            
            return textoArea

        def replaceCallback (objeto):
            textoBit = objeto.group(0)
            print("textoBit ", textoBit)
            if (textoBit[0] != '(' and textoBit[-1] != ')') and textoBit[-1] != '(': #No realiza la conversion si esta expandido o es la expansion de otra cosa
                if re.search('MT2|M2|METROS CUADRADOS',textoBit):
                    textoBit = extendArea(textoBit)
                else:
                    textoBit = extended_numbers(objeto.group(0))
            return textoBit

        if re.search('[0-9]+', texto):
            texto = re.sub(r'(?i)(\d{1,2} DE [A-Z ]+ (DEL|DE) \d{4})', replaceCallback, texto) #Reemplaza todas las fechas (formato largo) no extendidas
            texto = re.sub(r'(?i).?\d{1,2}[.\/]+\d{1,2}[.\/]+\d{4}(?! \().?', replaceCallback, texto) #Reemplaza todas las fechas (formato corto) no extendidas
            texto = re.sub(r'(?i).?\d*[.,]*\d*%(?! \().?', replaceCallback, texto) #Reemplaza todos los porcentajes no extendidos
            texto = re.sub(r'(?i).?(US\$|S\/) *[0-9,]+[.0-9]*.?\(*', replaceCallback, texto) #Reemplaza todos los montos no extendidos
            texto = re.sub(r'(?i)DIAS* \d*( \()*|\d+ DIAS', replaceCallback, texto) #Reemplaza todos los numeros de dias no extendidos
            texto = re.sub(r'(?i)MESES* \d*( \()*|\d+ MESES*', replaceCallback, texto) #Reemplaza todos los numeros de meses no extendidos
            texto = re.sub(r'(?i)(?i)AÑOS* \d*( \()*|\d+ AÑOS*', replaceCallback, texto) #Reemplaza todos los numeros de años no extendidos
            texto = re.sub(r'(?i).?[0-9,.]+ *(M2|MT2|METROS CUADRADOS)(?! \().?', replaceCallback, texto) #Reemplaza todas las areas no extendidas
        
        return texto

    def extension(self, texto): #todavia hay que buscarle un nombre

        def extendArea (textoArea):
            auxiliar = re.sub('MT2','M2',textoArea)
            auxiliar = re.sub('METROS CUADRADOS', 'M2', textoArea)
            print("auxiliar ", auxiliar)
            textoArea = extended_numbers(auxiliar)[:-1]
            if auxiliar[-1] != "2":
                textoArea = textoArea+ auxiliar[-1]  
                print("en if ", textoArea)
            return textoArea

        def replaceCallback (objeto):
            textoBit = objeto.group(0)
            if (textoBit[0] != '(' and textoBit[-1] != ')') and textoBit[-1] != '(': #No realiza la conversion si esta expandido o es la expansion de otra cosa
                if re.search('MT2|M2|METROS CUADRADOS',textoBit):
                    textoBit = extendArea(textoBit)
                else:
                    textoBit = extended_numbers(objeto.group(0))
            return textoBit

        def callBackAmounts(objeto):
            textoBit = objeto.group(0)
            monto1 = re.search(r'S\/.*?[0-9.,]+',textoBit)
            monto2 = re.search(r'US\$.*?[0-9.,]+',textoBit)
            monto1 = extended_numbers(monto1.group(0))
            monto2 = extended_numbers(monto2.group(0))
            textToReplace = re.sub(r'S\/.*?[0-9.,]+', monto1, textoBit)
            textToReplace = re.sub(r'US\$.*?[0-9.,]+', monto2, textToReplace)
            return textToReplace
            


        if re.search('[0-9]+', texto):
            texto = re.sub(r'(?i)(\d{1,2} DE [A-Z ]+ (DEL|DE) \d{4})', replaceCallback, texto) #Reemplaza todas las fechas (formato largo) no extendidas
            texto = re.sub(r'(?i)(\d{1,2} DE [A-Z ]+(\,)(\s|)+\d{4})', replaceCallback, texto) #Reemplaza todas las fechas (formato largo) no extendidas con coma
            texto = re.sub(r'(?i).?\d{1,2}[.\/]+\d{1,2}[.\/]+\d{4}(?! \().?|(?i).?\d{1,2}[.\-]+\d{1,2}[.\-]+\d{4}(?! \().?', replaceCallback, texto) #Reemplaza todas las fechas (formato corto) no extendidas
            texto = re.sub(r'(?i).?\d{4}[.\/]+\d{1,2}[.\/]+\d{1,2}(?! \().?|(?i).?\d{4}[.\-]+\d{1,2}[.\-]+\d{1,2}(?! \().?', replaceCallback, texto) #Reemplaza todas las fechas (formato corto) no extendidas formato extranjero
            texto = re.sub(r'(?i).?\d*[.,]*\d*%(?! \().?', replaceCallback, texto) #Reemplaza todos los porcentajes no extendidos
            texto = re.sub(r'(?i).?(US\$|S\/) *[0-9,]+[.0-9]*.?\(*', replaceCallback, texto) #Reemplaza todos los montos no extendidos
            texto = re.sub(r'(?i)DIAS* \d*( \()*|\d+ DIAS', replaceCallback, texto) #Reemplaza todos los numeros de dias no extendidos
            texto = re.sub(r'(?i)MESES* \d*( \()*|\d+ MESES*', replaceCallback, texto) #Reemplaza todos los numeros de meses no extendidos
            texto = re.sub(r'(?i)(?i)AÑOS* \d*( \()*|\d+ AÑOS*', replaceCallback, texto) #Reemplaza todos los numeros de años no extendidos
            texto = re.sub(r'(?i).?[0-9,.]+ *(M2|MT2|METROS CUADRADOS)(?! \().?', replaceCallback, texto) #Reemplaza todas las areas no extendidas
            texto = re.sub(r'(?i)S\/.+ \(US\$.+\)|US\$.+ \(S\/.+\)', callBackAmounts, texto) #Reemplaza montos representados en dolares entre parentesis no extendidos
            
        
        return texto