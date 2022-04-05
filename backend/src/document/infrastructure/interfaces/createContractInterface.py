import win32com.client as win32
import re
from backend.src.document.infrastructure.interfaces.text_utils import *
import pythoncom
#import threading
import json
import os
import platform

from backend.src.document.infrastructure.middlewares.convertSpecialCharacter import convertSpecialCharacter

class Document:
    def __init__(self, filesPath, app_id, visible, baseDocument):
        self.filesPath = filesPath
        pythoncom.CoInitialize()
        self.wordApp = win32.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(app_id, pythoncom.IID_IDispatch)
        )
        self.wordApp.Visible = visible
        print("base document --->", baseDocument)
        self.document = self.wordApp.Documents.Open(baseDocument)
        self.paragraphs = self.document.Paragraphs
        self.paragraphs.SpaceBefore = 0
        self.paragraphs.SpaceAfter = 0
        with open(self.filesPath+'\\data.json', encoding="utf-8") as f:
            self.comparecientes = json.load(f)
        self.comparecientes = convertSpecialCharacter(self.comparecientes)
        print("interface")
        pass

    def create(self):
        print("create")
        path = self.filesPath
        print(path)
        list_files = os.listdir(path)
        print(list_files)
        with open(path+'\\data.json', encoding='utf-8') as f:
            dataComp = json.load(f)
        dataComp = convertSpecialCharacter(dataComp)
        for fileName in list_files:
            if "minuta" in fileName:
                numeroKardex = fileName.split("-")[0]
            elif "banco" in fileName:
                numeroKardexB = fileName.split("-")[0]
                numeroKardex = numeroKardexB
        self.first_part("USUARIO", "DON "+dataComp["comparecientes"][0]["nombre"], dataComp)
        self.second_part()
        self.third_part(path)
        for fileName in list_files:
            if "minuta" in fileName and "format" in fileName:
                print("minuta")
                self.minuta(path, fileName)
        #if numeroKardex:
        #    self.insertos(path, numeroKardex)
        #    for num in range(self.document.InlineShapes.Count):
        #        self.document.InlineShapes(num+1).Width = self.InchesToPoints(6)
        #        self.document.InlineShapes(num+1).Height = self.InchesToPoints(8.5)
        #for fileName in list_files:
        #    if "clausula" in fileName and "adicional" in fileName and "format" in fileName:
        #        self.clausula_adicional(path, fileName)
        for fileName in list_files:
            if "banco" in fileName and "format" in fileName:
                self.contrato(path, fileName)
        print("before last inserto")
        documentName = path+'\\KR-'+str(dataComp['kardex'])+'.doc'
        print("nombre final:", documentName)
        #self.last_inserto()
        self.close_document(documentName)

    def first_part(self, usuario, compareciente, dataComp):
        bancoName = dataComp['banco']['nombre']
        list_paragraphs = self.first_part_content(
            usuario, 
            str(dataComp['kardex']),#"459680", 
            "C O M P R A - V E N T A",
            dataComp['inmobiliaria']['nombre'], #"INVERSIONES INMOBILIARIAS ALCANFORES S.A.C.",
            compareciente,
            bancoName
            )
        end = 0
        for paragraph in list_paragraphs:
            range_ = self.document.Range(end, end)
            range_.InsertAfter(paragraph)
            self.document.Paragraphs.Add(range_)
            self.document.Paragraphs.Last.Range.Font.Size = 9
            self.document.Paragraphs.Last.Range.Font.Bold = True
            print("num", self.document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent, self.document.Paragraphs.Last.Range.ParagraphFormat.RightIndent)
            if "KR-" in paragraph:
                self.document.Paragraphs(self.document.Paragraphs.Count).Alignment = 1
                self.document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(0)
                self.document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(0)
            elif "C O M P R A - V E N T A" in paragraph:
                self.document.Paragraphs.Last.Range.Underline = True
                self.document.Paragraphs(self.document.Paragraphs.Count).Alignment = 1
                self.document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(0)
                self.document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(0)
            elif bancoName in paragraph or compareciente in paragraph:
                self.document.Paragraphs.Last.Range.Underline = False
                self.document.Paragraphs(self.document.Paragraphs.Count).Alignment = 3
                self.document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(1)
                self.document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(1)
                self.__add_seps(self.document.Paragraphs.Last, '*')
            else:
                self.document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(0)
                self.document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(0)
                self.document.Paragraphs(self.document.Paragraphs.Count).Alignment = 3

            end = self.document.Paragraphs.Last.Range.End - 1
        
    def first_part_content(self, usuario, kardex_id, tipo_contrato, inmobiliaraName, comprador, bancoName):
        print("list", usuario, kardex_id, inmobiliaraName)
        content = [
            "NUMERO: * F. CONFRONTAR"+" "*40 + usuario,
            "MINUTA:  * F. M. PAGO GENERALES",
            " ",
            " ",
            "KR-"+ kardex_id,
            " ",
            tipo_contrato,
            " ",
            " ",
            "DE BIENES INMUEBLES FUTUROS, CON CREDITO Y GARANTIA HIPOTECARIA, QUE CELEBRAN DE UNA PARTE "+ inmobiliaraName + " Y DE LA OTRA PARTE " + comprador + ", CON LA INTERVENCION DEL " + bancoName,
            " ",
            " ",
            " ",
            " ",
            "*"*35+" E.S.O. "+"*"*32
        ]
        return content

    def second_part(self):
        list_paragraphs = self.second_part_content()
        end = self.document.Paragraphs.Last.Range.End - 1
        for paragraph in list_paragraphs:
            range_ = self.document.Range(end, end)
            range_.InsertAfter(paragraph)
            self.document.Paragraphs.Add(range_)
            self.document.Paragraphs.Last.Range.Font.Size = 8
            self.__add_seps(self.document.Paragraphs.Last)
            end = self.document.Paragraphs.Last.Range.End - 1

    def second_part_content(self):
        content = [
            "I N T R O D U C C I O N: ",
            " ",
            " ",
            "C O M P A R E C E N: "
        ]
        return content

    def third_part(self, path):
        list_paragraphs = self.third_part_content(path)
        end = self.document.Paragraphs.Last.Range.End - 1
        for paragraph in list_paragraphs:
            range_ = self.document.Range(end, end)
            range_.InsertAfter(paragraph)
            self.document.Paragraphs.Add(range_)
            self.document.Paragraphs.Last.Range.Font.Bold = False
            self.__add_seps(self.document.Paragraphs.Last)
            end = self.document.Paragraphs.Last.Range.End - 1

    def third_part_content(self, path):
        """ Comparecientes
        """
        with open(path+"\\comparecientes.json", encoding="utf-8") as f:
            signers = json.load(f)
        list_paragraphs = []
        for signer in signers["comparecientes"]:
            if signer["representante"] == "inmobiliaria":
                text = self.compareciente_text(signer)
                list_paragraphs.append(text)
        if signers["inmobiliaria"]:
            signer = signers["inmobiliaria"]
            text = "QUIENES EN ESTE ACTO DECLARAN PROCEDER EN NOMBRE Y REPRESENTACION DE "+signer["nombre"]+", CON REGISTRO UNICO DE CONTRIBUYENTE NUMERO: "+signer["ruc"]+", CON DOMICILIO EN "+signer["domicilio"]+", QUIENES DICEN ESTAR DEBIDAMENTE FACULTADOS SEGUN CONSTA DE LOS PODERES INSCRITOS EN LA PARTIDA NUMERO 14011552 DEL REGISTRO DE PERSONAS JURIDICAS DE LIMA."
            list_paragraphs.append(text)
        list_self_signers = self.compareciente_propio_text(signers["comparecientes"])
        list_paragraphs = list_paragraphs+list_self_signers
        for signer in signers["comparecientes"]:
            if signer["representante"] == "banco":
                text = self.compareciente_text(signer)
                list_paragraphs.append(text)
        if signers["banco"]:
            signer = signers["banco"]
            text = "QUIENES EN ESTE ACTO DECLARAN PROCEDER EN NOMBRE Y REPRESENTACION DE "+signer["nombre"]+", RESPECTO DE LA QUE, CONFORME A LO ESTABLECIDO EN EL PRIMER PARRAFO DEL ARTICULO 9 DEL DECRETO LEGISLATIVO N° 1372, SE HA CUMPLIDO CON VERIFICAR EN EL SISTEMA SUNAT, QUE ESTA HA PRESENTADO LA DECLARACION DEL BENEFICIARIO FINAL, CON REGISTRO UNICO DE CONTRIBUYENTE NUMERO: "+signer["ruc"]+", CON DOMICILIO EN "+signer["domicilio"]+", DEBIDAMENTE FACULTADAS SEGUN CONSTA DE LOS PODERES INSCRITOS EN LA PARTIDA ELECTRONICA NUMERO 11008578 DEL REGISTRO DE PERSONAS JURIDICAS DE LAS ZONA REGISTRAL N° IX - SEDE LIMA."
            list_paragraphs.append(text)
        text = "DOY FE DE HABER IDENTIFICADO A LOS COMPARECIENTES, QUE PROCEDEN CON CAPACIDAD, LIBERTAD Y CONOCIMIENTO BASTANTE DEL ACTO QUE REALIZAN Y QUE SON HABILES EN EL IDIOMA CASTELLANO; ASIMISMO, DE HABER UTILIZADO EL MECANISMO DE LA COMPARACION BIOMETRICA DE LAS HUELLAS DACTILARES Y LA CONSULTA EN LINEA DE RENIEC, CUMPLIENDO CON LO ESTABLECIDO EN EL LITERAL D) DEL ARTICULO 54, Y EL ARTICULO 55 DEL DECRETO LEGISLATIVO N° 1049 DE LA LEY DE NOTARIADO, MODIFICADO POR LOS DECRETOS LEGISLATIVOS N° 1350 Y N° 1232 RESPECTIVAMENTE, ELEVANDO A ESCRITURA PUBLICA LA MINUTA QUE SE ENCUENTRA FIRMADA Y AUTORIZADA, LA MISMA QUE ARCHIVO EN SU LEGAJO RESPECTIVO, Y CUYO TENOR ES EL SIGUIENTE:"
        list_paragraphs.append(text)
        return list_paragraphs

    def compareciente_text(self, signer):
        if signer["domicilio"] == "LIMA":
            domicilio = "ESTA CAPITAL"
        else:
            domicilio = signer["domicilio"]
        text = signer["genero"]+": "+signer["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer["nacionalidad"]+", DE ESTADO CIVIL: "+signer["estado civil"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+domicilio+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
        return text

    def compareciente_propio_text(self, signers):
        list_signers = []
        text_out = []
        for signer in signers:
            if signer["representante"] == "COMPRADOR":
                list_signers.append(signer)
        if len(list_signers) == 2:
            if list_signers[0]["estado civil"] == "CASADO" and list_signers[0]["estado civil"] == "CASADA":
                text = signer[0]["genero"]+": "+signer[0]["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer[0]["nacionalidad"]+", DE ESTADO CIVIL: "+signer[0]["estado civil"]+" CON"+singer[1]["genero"]+" "+signer[1]["nombre"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+signer[0]["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
                text_out.append(text)
            elif list_signers[0]["estado civil"] == "CASADA" and list_signers[0]["estado civil"] == "CASADO":
                text = signer[0]["genero"]+": "+signer[0]["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer[0]["nacionalidad"]+", DE ESTADO CIVIL: "+signer[0]["estado civil"]+" CON"+singer[1]["genero"]+" "+signer[1]["nombre"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+signer[0]["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
                text_out.append(text)
            else:
                for signer in list_signers:
                    text = signer["genero"]+": "+signer["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer["nacionalidad"]+", DE ESTADO CIVIL: "+signer["estado civil"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+signer["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
                    text_out.append(text)
        else:
            text = signer["genero"]+": "+signer["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer["nacionalidad"]+", DE ESTADO CIVIL: "+signer["estado civil"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+signer["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
            text_out.append(text)
        return text_out

    def minuta(self, path, fileName):
        range_0 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        range_0.InsertAfter("M  I  N  U  T  A:")
        self.document.Paragraphs.Add(range_0)
        self.document.Range(range_0.Start, range_0.End-1).Font.Bold = True
        self.document.Range(range_0.Start, range_0.End-1).Underline = 1
        docMin = self.wordApp.Documents.Open(path+ "\\" + fileName) #"\\459680-format.rtf")
        docMin.Content.Copy()
        range_1 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        range_1.Paste()
        self.document.Paragraphs.Add(range_1)
        print("rango 1", range_1.Start, range_1.End)
        paragraphs = range_1.Paragraphs
        print(paragraphs.Count)
        docMin.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(paragraph)
        #paragraphs(1)
        #for paragraph in paragraphs:
        #    self.__add_seps(paragraph)
        pass

    def insertos(self, path, numeroKardex):
        """ Inserta los documentos que son parte de la minuta,
            como imagenes o texto. Los documentos deben tener la siguiente
            estructura: "342434-1-inserto": donde -342434- es el numero de kardex,
            -1- es la secuencia de los documentos que se insertaran e -inserto-
            indicara si ese archivo debe estar precedido por la palabra inserto.
        """
        list_insertos = []
        for fileName in os.listdir(path):
            for i in range(len(os.listdir(path))):
                fileName2 = fileName.split(".")[0]
                cond1 = numeroKardex in fileName and "format" in fileName and fileName2.split("-")[1] == str(i)
                cond2 = numeroKardex in fileName and fileName2.split("-")[1] == str(i) and ".png" in fileName
                cond3 = numeroKardex in fileName and fileName2.split("-")[1] == str(i) and ".jpg" in fileName
                cond4 = numeroKardex in fileName and fileName2.split("-")[1] == str(i) and ".jpeg" in fileName
                if cond1 or cond2 or cond3 or cond4:
                    list_insertos.append(fileName)

        print(list_insertos)
        for fileName in list_insertos:
            if ".jpg" in fileName or ".jpeg" in fileName or ".png" in fileName:
                if "inserto" in fileName:
                    end = self.document.Content.End - 1
                    range_ = self.document.Range(end, end)
                    range_.InsertAfter("I N S E R T O.")
                    riStart, riEnd = range_.Start, range_.End
                    self.document.Paragraphs.Add(range_)
                    self.document.Range(riStart, riEnd).Font.Bold = True
                    self.document.Range(riStart, riEnd).Underline = 1
                    self.imagenInsertos(path, fileName)
                    print("agregar imagen con inserto")
                else:
                    print("agregar imagen sin inserto")
                    self.imagenInsertos(path, fileName)
            elif ".doc" in fileName or ".rtf" in fileName or ".docx" in fileName:
                if "inserto" in fileName:
                    range_0 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
                    range_0.InsertAfter("I N S E R T O:")
                    self.document.Paragraphs.Add(range_0)
                    self.document.Range(range_0.Start, range_0.End-1).Font.Bold = True
                    self.document.Range(range_0.Start, range_0.End-1).Underline = 1
                    self.documentInsertos(path, fileName)
                    print("agregar documento con inserto")
                else:
                    print("agregar documento sin inserto")
                    self.documentInsertos(path, fileName)

    def imagenInsertos(self, path, fileName):
        end = self.document.Content.End-1
        range_ = self.document.Range(end, end)
        range_.InsertAfter(" ")
        self.document.Paragraphs.Add(range_)
        range_ = self.document.Content
        range_.Collapse(0)
        self.document.InlineShapes.AddPicture(path+"\\"+fileName, Range=range_)
        #self.document.Shapes.AddPicture(path+"\\"+fileName, Top = 10, Width=100, Height=130)
        #self.document.Shapes(1).ConvertToInlineShape()

    def documentInsertos(self, path, fileName):
        docIns = self.wordApp.Documents.Open(path+"\\"+fileName)
        docIns.Content.Copy()
        range_1 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        range_1.Paste()
        self.document.Paragraphs.Add(range_1)
        print("rango 1", range_1.Start, range_1.End)
        paragraphs = range_1.Paragraphs
        print(paragraphs.Count)
        docIns.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(paragraph)

    def clausula_adicional(self, path, fileName):
        #range_0 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        docClausula = self.wordApp.Documents.Open(path+ "\\" + fileName)
        docClausula.Content.Copy()
        range_1 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        range_1.Paste()
        self.document.Paragraphs.Add(range_1)
        print("rango 1", range_1.Start, range_1.End)
        paragraphs = range_1.Paragraphs
        print(paragraphs.Count)
        docClausula.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(paragraph)

    def contrato(self, path, fileName):
        range_0 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        range_0.InsertAfter("CLAUSULA ADICIONAL:")
        self.document.Paragraphs.Add(range_0)
        self.document.Range(range_0.Start, range_0.End-1).Font.Bold = True
        self.document.Range(range_0.Start, range_0.End-1).Underline = 1
        docCont = self.wordApp.Documents.Open(path+ "\\" + fileName) #"\\459680-format.rtf")
        docCont.Content.Copy()
        range_1 = self.document.Range(self.document.Content.End-1, self.document.Content.End-1)
        range_1.Paste()
        self.document.Paragraphs.Add(range_1)
        print("rango 1", range_1.Start, range_1.End)
        paragraphs = range_1.Paragraphs
        print(paragraphs.Count)
        range_1.Font.Name = "Anonymous"
        range_1.Font.Size = 8
        docCont.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(paragraph)

    def last_inserto(self):
        last_par = self.document.Paragraphs.Count
        list_paragraphs = self.last_inserto_content()
        print("tipos: ", type(last_par), last_par, type(len(list_paragraphs)), len(list_paragraphs))
        start = self.document.Paragraphs.Last.Range.End - 1
        end = self.document.Paragraphs.Last.Range.End - 1
        for paragraph in list_paragraphs:
            range_ = self.document.Range(end, end)
            range_.InsertAfter(paragraph)
            range_.Font.Bold = False
            range_.Underline = 0
            self.document.Paragraphs.Add(range_)
            self.document.Paragraphs.Last.Range.Font.Size = 8
            if "I N S E R T O" in self.document.Paragraphs.Last.Range.Text:
                range_i = self.document.Paragraphs.Last.Range
                range_i.Find.Execute(FindText="I N S E R T O:")
                range_i.Font.Bold = True
                range_i.Underline = 1
            elif "C O N C L U S I O N" in self.document.Paragraphs.Last.Range.Text:
                range_i = self.document.Paragraphs.Last.Range
                range_i.Find.Execute(FindText="C O N C L U S I O N")
                range_i.Font.Bold = True
                range_i.Underline = 1
            elif "ARTICULO 153° DEL CODIGO CIVIL" in self.document.Paragraphs.Last.Range.Text:
                range_i = self.document.Paragraphs.Last.Range
                range_i.Find.Execute(FindText="ARTICULO 153° DEL CODIGO CIVIL")
                range_i.Font.Bold = True
                range_i.Underline = 0
            #self.__add_seps_2(self.document.Paragraphs.Last)
            end = self.document.Paragraphs.Last.Range.End - 1
        for item in range(last_par, last_par+len(list_paragraphs)+1):#for paragraph in self.document.Range(start, end).Paragraphs:
            #self.__add_seps_2(paragraph)
            self.__add_seps_2(self.document.Paragraphs(item))

    def last_inserto_content(self):
        content = [
            "I N S E R T O: ",
            "ARTICULO 153° DEL CODIGO CIVIL ",
            "ART. 153°.- EL PODER ES IRREVOCABLE SIEMPRE QUE SE ESTIPULE PARA UN ACTO ESPECIAL O POR TIEMPO LIMITADO O CUANDO ES OTORGADA EN INTERES COMUN DEL REPRESENTADO Y DEL REPRESENTANTE O UN TERCERO.",
            "EL PLAZO DEL PODER IRREVOCABLE NO PUEDE SER MAYOR DE UN AÑO.",
            "C O N C L U S I O N. ",
            " ",
            " ",
            "FORMALIZADO EL INSTRUMENTO, Y DE CONFORMIDAD CON EL ARTICULO 27 DEL DECRETO LEGISLATIVO NUMERO 1049, LEY DEL NOTARIADO, DEJO CONSTANCIA QUE LOS INTERESADOS FUERON ADVERTIDOS DE LOS EFECTOS LEGALES DEL MISMO, ASIMISMO DE CONFORMIDAD CON EL ARTICULO 59 DE ESTE MISMO DECRETO, LOS OTORGANTES MANIFIESTAN QUE CONVIENEN EN ENCARGAR A ESTE OFICIO NOTARIAL EL PAGO DE LOS DERECHOS REGISTRALES, MONTO QUE SERA MANTENIDO EN CUSTODIA SIN OPCION DE DEVOLUCION, HASTA CONCLUIR CON LA INSCRIPCION DEL CONTRATO; LOS COMPARECIENTES LE DIERON LECTURA, DESPUES DE LO CUAL SE AFIRMARON Y RATIFICARON EN SU CONTENIDO, SUSCRIBIENDOLO, DECLARANDO QUE SE TRATA DE UN ACTO VALIDO Y NO SIMULADO, MANIFESTANDO IGUALMENTE CONOCER LOS ANTECEDENTES Y/O TITULOS QUE ORIGINAN EL PRESENTE INSTRUMENTO, Y RECONOCER COMO SUYAS LAS FIRMAS DE LA MINUTA QUE LA ORIGINA.",
            "LOS OTORGANTES DAN SU CONSENTIMIENTO EXPRESO PARA EL TRATAMIENTO DE SUS DATOS PERSONALES Y LA FINALIDAD QUE SE LE DARAN DE CONFORMIDAD CON LO ESTABLECIDO POR LA LEY 29733 Y SU REGLAMENTO",
            "DEJO CONSTANCIA QUE AL OTORGARSE LA PRESENTE ESCRITURA PUBLICA, SE HAN TOMADO LAS MEDIDAS DE CONTROL Y DILIGENCIA EN MATERIA DE PREVENCION DE LAVADO DE ACTIVOS, ENTRE ESTAS LA IDENTIFICACION DEL BENEFICIARIO FINAL DE CONFORMIDAD CON EL INCISO K) DEL ARTICULO 59 DEL DECRETO LEGISLATIVO N° 1049 DE LA LAY DEL NOTARIADO, MODIFICADO POR EL DECRETO LEGISLATIVO N° 1232. DE TODO LO QUE DOY FE."
        ]
        return content

    def InchesToPoints(self,inches):
        return inches * 72.0

    def __add_seps(self,paragraph, sep = '='):
        ori_l = paragraph.Range.ComputeStatistics(1)#win32com.client.constants.wdStatisticLines)
        
        paragraph_t = paragraph.Range.Text
        paragraph_t = paragraph_t.splitlines()[-1]

        max_l = 86
        
        if len(paragraph_t) <= max_l:
            paragraph_t = paragraph_t + (max_l-len(paragraph_t))*sep 
        else:
            for i in range(1,100):
                if len(paragraph_t) <= i*max_l:
                    paragraph_t = paragraph_t + (i*max_l - len(paragraph_t))*sep
                    break
        
        paragraph.Range.Text = remove_spaces(paragraph_t)
        new_l = paragraph.Range.ComputeStatistics(1)#win32com.client.constants.wdStatisticLines)

        while(new_l == ori_l):
            paragraph_t_old = paragraph_t[:-1] + paragraph_t[-1] 
            paragraph_t = paragraph_t.splitlines()[-1]
            paragraph_t += sep
            paragraph.Range.Text = remove_spaces(paragraph_t[:-1] + paragraph_t[-1])

            new_l = paragraph.Range.ComputeStatistics(1)#win32com.client.constants.wdStatisticLines)
            
            if new_l > ori_l:
                paragraph.Range.Text = remove_spaces(paragraph_t_old[:-1] + paragraph_t_old[-1]) #+ '\n'
        
        while(new_l > ori_l):  
            paragraph_t = paragraph_t.splitlines()[-1][:-1]
            #print(paragraph_t)
            #print(len(paragraph_t))
            paragraph.Range.Text = remove_spaces(paragraph_t[:-1] + paragraph_t[-1]) #+ '\n'

            new_l = paragraph.Range.ComputeStatistics(1)#win32com.client.constants.wdStatisticLines)

    def __add_seps_2(self, paragraph, sep = '='):
        lines = paragraph.Range.ComputeStatistics(1)
        range_0 = self.document.Range(paragraph.Range.End - 1, paragraph.Range.End - 1)
        range_0.InsertAfter(" ")
        text = sep*30
        end = paragraph.Range.End - 1
        while(lines == paragraph.Range.ComputeStatistics(1)):
            range_ = self.document.Range(end, end)
            range_.InsertAfter(text)
            end = paragraph.Range.End - 1
        
        end = paragraph.Range.End - 1
        for i in range(100):
            range_2 = self.document.Range(end-1, end)
            range_2.Delete()
            end = paragraph.Range.End - 1
            if paragraph.Range.ComputeStatistics(1) == lines:
                break

    def close_document(self, fileName):
        #self.document.SaveAs2()
        print("closing")
        self.document.SaveAs(fileName)
        self.document.Close(SaveChanges=-1)