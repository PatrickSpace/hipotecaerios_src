from back.src.document.infrastructure.interfaces.text_utils import remove_spaces

class Contract:
    def __init__(self):
        pass

    def first_part(self, document, usuario, dataComp):
        cliente = 'DON '
        if "comparecientes" in dataComp.keys():
            for comp in dataComp["comparecientes"]:
                if comp["representante"] == "CLIENTE":
                    if comp["genero"] == "FEMENINO":
                        cliente = 'DOÑA '
                    cliente = cliente + comp["nombre"]
                else:
                    cliente = cliente
        else:
            cliente = cliente
        #"DON "+comparecientes_["comparecientes"][0]["nombre"],
        bancoName = dataComp['banco']['nombre'] if 'banco' in dataComp.keys() else ''
        inmobiliariaName = dataComp['inmobiliaria']['nombre'] if 'inmobiliaria' in dataComp.keys() else ''
        list_paragraphs = self.first_part_content(
            usuario, 
            str(dataComp['kardex']),#"459680", 
            "C O M P R A - V E N T A",
            inmobiliariaName,
            cliente,
            bancoName
            )
        end = 0
        for paragraph in list_paragraphs:
            range_ = document.Range(end, end)
            range_.InsertAfter(paragraph)
            document.Paragraphs.Add(range_)
            document.Paragraphs.Last.Range.Font.Size = 9
            document.Paragraphs.Last.Range.Font.Bold = True
            if "KR-" in paragraph:
                document.Paragraphs(document.Paragraphs.Count).Alignment = 1
                document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(0)
                document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(0)
            elif "C O M P R A - V E N T A" in paragraph:
                document.Paragraphs.Last.Range.Underline = True
                document.Paragraphs(document.Paragraphs.Count).Alignment = 1
                document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(0)
                document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(0)
            elif (bancoName in paragraph and bancoName != "") or cliente in paragraph or (inmobiliariaName in paragraph and inmobiliariaName != ""):
                document.Paragraphs.Last.Range.Underline = False
                document.Paragraphs(document.Paragraphs.Count).Alignment = 3
                document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(1)
                document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(1)
                self.__add_seps(document.Paragraphs.Last, '*')
            else:
                document.Paragraphs.Last.Range.ParagraphFormat.LeftIndent = self.InchesToPoints(0)
                document.Paragraphs.Last.Range.ParagraphFormat.RightIndent = self.InchesToPoints(0)
                document.Paragraphs(document.Paragraphs.Count).Alignment = 3

            end = document.Paragraphs.Last.Range.End - 1

    def first_part_content(self, usuario, kardex_id, tipo_contrato, inmobiliaraName, comprador, bancoName):
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
    
    def second_part(self, document):
        list_paragraphs = self.second_part_content()
        end = document.Paragraphs.Last.Range.End - 1
        for paragraph in list_paragraphs:
            range_ = document.Range(end, end)
            range_.InsertAfter(paragraph)
            document.Paragraphs.Add(range_)
            document.Paragraphs.Last.Range.Font.Size = 8
            self.__add_seps(document.Paragraphs.Last)
            end = document.Paragraphs.Last.Range.End - 1

    def second_part_content(self):
        content = [
            "I N T R O D U C C I O N: ",
            " ",
            " ",
            "C O M P A R E C E N: "
        ]
        return content

    def third_part(self, document, dataComp):
        list_paragraphs = self.third_part_content(dataComp)
        end = document.Paragraphs.Last.Range.End - 1
        for paragraph in list_paragraphs:
            range_ = document.Range(end, end)
            range_.InsertAfter(paragraph)
            document.Paragraphs.Add(range_)
            document.Paragraphs.Last.Range.Font.Bold = False
            self.__add_seps(document.Paragraphs.Last) ######
            end = document.Paragraphs.Last.Range.End - 1

    def third_part_content(self, dataComp):
        """ Comparecientes
        """
        list_paragraphs = []
        if 'comparecientes' in dataComp.keys():
            for signer in dataComp["comparecientes"]:#signers["comparecientes"]:
                if signer["representante"] == "INMOBILIARIA":
                    text = self.compareciente_text(signer)
                    list_paragraphs.append(text)
        if "inmobiliaria" in dataComp.keys():#signers["inmobiliaria"]:
            signer = dataComp["inmobiliaria"]
            text = "QUIENES EN ESTE ACTO DECLARAN PROCEDER EN NOMBRE Y REPRESENTACION DE "+signer["nombre"]+", CON REGISTRO UNICO DE CONTRIBUYENTE NUMERO: "+signer["ruc"]+", CON DOMICILIO EN "+signer["domicilio"]+", QUIENES DICEN ESTAR DEBIDAMENTE FACULTADOS SEGUN CONSTA DE LOS PODERES INSCRITOS EN LA PARTIDA NUMERO 14011552 DEL REGISTRO DE PERSONAS JURIDICAS DE LIMA."
            list_paragraphs.append(text)
        list_self_signers = self.compareciente_propio_text(dataComp)
        list_paragraphs = list_paragraphs+list_self_signers

        if 'comparecientes' in dataComp.keys():
            for signer in dataComp["comparecientes"]:
                if signer["representante"] == "BANCO":
                    text = self.compareciente_text(signer)
                    list_paragraphs.append(text)
        if "banco" in dataComp.keys():
            signer = dataComp["banco"]
            text = "QUIENES EN ESTE ACTO DECLARAN PROCEDER EN NOMBRE Y REPRESENTACION DE "+signer["nombre"]+", RESPECTO DE LA QUE, CONFORME A LO ESTABLECIDO EN EL PRIMER PARRAFO DEL ARTICULO 9 DEL DECRETO LEGISLATIVO N° 1372, SE HA CUMPLIDO CON VERIFICAR EN EL SISTEMA SUNAT, QUE ESTA HA PRESENTADO LA DECLARACION DEL BENEFICIARIO FINAL, CON REGISTRO UNICO DE CONTRIBUYENTE NUMERO: "+signer["ruc"]+", CON DOMICILIO EN "+signer["domicilio"]+", DEBIDAMENTE FACULTADAS SEGUN CONSTA DE LOS PODERES INSCRITOS EN LA PARTIDA ELECTRONICA NUMERO 11008578 DEL REGISTRO DE PERSONAS JURIDICAS DE LAS ZONA REGISTRAL N° IX - SEDE LIMA."
            list_paragraphs.append(text)

        text = "DOY FE DE HABER IDENTIFICADO A LOS COMPARECIENTES, QUE PROCEDEN CON CAPACIDAD, LIBERTAD Y CONOCIMIENTO BASTANTE DEL ACTO QUE REALIZAN Y QUE SON HABILES EN EL IDIOMA CASTELLANO; ASIMISMO, DE HABER UTILIZADO EL MECANISMO DE LA COMPARACION BIOMETRICA DE LAS HUELLAS DACTILARES Y LA CONSULTA EN LINEA DE RENIEC, CUMPLIENDO CON LO ESTABLECIDO EN EL LITERAL D) DEL ARTICULO 54, Y EL ARTICULO 55 DEL DECRETO LEGISLATIVO N° 1049 DE LA LEY DE NOTARIADO, MODIFICADO POR LOS DECRETOS LEGISLATIVOS N° 1350 Y N° 1232 RESPECTIVAMENTE, ELEVANDO A ESCRITURA PUBLICA LA MINUTA QUE SE ENCUENTRA FIRMADA Y AUTORIZADA, LA MISMA QUE ARCHIVO EN SU LEGAJO RESPECTIVO, Y CUYO TENOR ES EL SIGUIENTE:"
        list_paragraphs.append(text)
        return list_paragraphs

    def minuta(self, wordApp, document, path, fileName, isTitulo):
        if isTitulo:
            range_0 = document.Range(document.Content.End-1, document.Content.End-1)
            range_0.InsertAfter("M  I  N  U  T  A:")
            document.Paragraphs.Add(range_0)
            document.Range(range_0.Start, range_0.End-1).Font.Bold = True
            document.Range(range_0.Start, range_0.End-1).Underline = 1
        docMin = wordApp.Documents.Open(path+ "\\" + fileName) #"\\459680-format.rtf")
        docMin.Content.Copy()
        range_1 = document.Range(document.Content.End-1, document.Content.End-1)
        range_1.Paste()
        range_1.Start=range_1.Start+1
        document.Paragraphs.Add(range_1)
        paragraphs = range_1.Paragraphs
        docMin.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(document, paragraph)
        pass

    def clausula_adicional(self, wordApp, document, path, fileName):
        #range_0 = document.Range(document.Content.End-1, document.Content.End-1)
        docClausula = wordApp.Documents.Open(path+ "\\" + fileName)
        docClausula.Content.Copy()
        range_1 = document.Range(document.Content.End-1, document.Content.End-1)
        range_1.Paste()
        range_1.Start=range_1.Start+1
        document.Paragraphs.Add(range_1)
        paragraphs = range_1.Paragraphs
        docClausula.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(document, paragraph)
    
    def contrato(self, wordApp, document, path, fileName):
        range_0 = document.Range(document.Content.End-1, document.Content.End-1)
        range_0.InsertAfter("CLAUSULA ADICIONAL:")
        document.Paragraphs.Add(range_0)
        document.Range(range_0.Start, range_0.End-1).Font.Bold = True
        document.Range(range_0.Start, range_0.End-1).Underline = 1
        docCont = wordApp.Documents.Open(path+ "\\" + fileName) #"\\459680-format.rtf")
        docCont.Content.Copy()
        range_1 = document.Range(document.Content.End-1, document.Content.End-1)
        range_1.Paste()
        range_1.Start=range_1.Start+1
        document.Paragraphs.Add(range_1)
        paragraphs = range_1.Paragraphs
        range_1.Font.Name = "Anonymous"
        range_1.Font.Size = 8
        docCont.Close()
        for paragraph in paragraphs:
            self.__add_seps_2(document, paragraph)



    def last_inserto(self, document):
        last_par = document.Paragraphs.Count
        list_paragraphs = self.last_inserto_content()
        start = document.Paragraphs.Last.Range.End - 1
        end = document.Paragraphs.Last.Range.End - 1
        for paragraph in list_paragraphs:
            range_ = document.Range(end, end)
            range_.InsertAfter(paragraph)
            range_.Font.Bold = False
            range_.Underline = 0
            document.Paragraphs.Add(range_)
            document.Paragraphs.Last.Range.Font.Size = 8
            if "I N S E R T O" in document.Paragraphs.Last.Range.Text:
                range_i = document.Paragraphs.Last.Range
                range_i.Find.Execute(FindText="I N S E R T O:")
                range_i.Font.Bold = True
                range_i.Underline = 1
            elif "C O N C L U S I O N" in document.Paragraphs.Last.Range.Text:
                range_i = document.Paragraphs.Last.Range
                range_i.Find.Execute(FindText="C O N C L U S I O N")
                range_i.Font.Bold = True
                range_i.Underline = 1
            elif "ARTICULO 153° DEL CODIGO CIVIL" in document.Paragraphs.Last.Range.Text:
                range_i = document.Paragraphs.Last.Range
                range_i.Find.Execute(FindText="ARTICULO 153° DEL CODIGO CIVIL")
                range_i.Font.Bold = True
                range_i.Underline = 0
            #self.__add_seps_2(document.Paragraphs.Last)
            end = document.Paragraphs.Last.Range.End - 1
        for item in range(last_par, last_par+len(list_paragraphs)+1):#for paragraph in document.Range(start, end).Paragraphs:
            self.__add_seps_2(document, document.Paragraphs(item))
            pass

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
            paragraph.Range.Text = remove_spaces(paragraph_t[:-1] + paragraph_t[-1]) #+ '\n'
            new_l = paragraph.Range.ComputeStatistics(1)#win32com.client.constants.wdStatisticLines)

    def compareciente_text(self, signer):
        if signer["domicilio"] == "LIMA":
            domicilio = "ESTA CAPITAL"
        else:
            domicilio = signer["domicilio"]
        text = signer["genero"]+": "+signer["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer["nacionalidad"]+", DE ESTADO CIVIL: "+signer["estado civil"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+domicilio+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
        return text

    def compareciente_propio_text(self, dataComp):
        list_signers = []
        text_out = []
        print("comp propi", dataComp)
        if 'comparecientes' in dataComp.keys():
            signers = dataComp["comparecientes"]
            print("signers", signers)
            for signer in signers:
                if signer["representante"] == "CLIENTE":
                    list_signers.append(signer)
        
        if len(list_signers) == 0:
            pass
        elif len(list_signers) == 1:
            signer = list_signers[0]
            text = signer["genero"]+": "+signer["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer["nacionalidad"]+", DE ESTADO CIVIL: "+signer["estado civil"]+"."#+" CON"+signer["genero"]+" "+signer[1]["nombre"]+", DE PROFESION U OCUPACION: "+signer["profesion"]+", Y DOMICILIAR EN "+signer["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer["dni"]+"."
            text_out.append(text)
        else: #if len(list_signers) > 1:
            signer = list_signers
            text = signer[0]["genero"]+": "+signer[0]["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer[0]["nacionalidad"]+", DE ESTADO CIVIL: "+signer[0]["estado civil"]+" CON"+signer[1]["genero"]+" "+signer[1]["nombre"]+", DE PROFESION U OCUPACION: "+signer[1]["profesion"]+", Y DOMICILIAR EN "+signer[0]["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer[1]["dni"]+"."
            text_out.append(text)
            #for signer in list_signers:
            #    print(signer, "s---s")
            #    text = signer[0]["genero"]+": "+signer[0]["nombre"]+", QUIEN MANIFIESTA SER DE NACIONALIDAD: "+signer[0]["nacionalidad"]+", DE ESTADO CIVIL: "+signer[0]["estado civil"]+" CON"+signer[1]["genero"]+" "+signer[1]["nombre"]+", DE PROFESION U OCUPACION: "+signer[1]["profesion"]+", Y DOMICILIAR EN "+signer[0]["domicilio"]+", DEBIDAMENTE IDENTIFICADO CON DOCUMENTO NACIONAL DE IDENTIDAD NUMERO: "+signer[1]["dni"]+"."
            #    text_out.append(text)
            
        return text_out

    def __add_seps_2(self, document, paragraph, sep = '='):
        lines = paragraph.Range.ComputeStatistics(1)
        range_0 = document.Range(paragraph.Range.End - 1, paragraph.Range.End - 1)
        range_0.InsertAfter(" ")
        text = sep*30
        end = paragraph.Range.End - 1
        while(lines == paragraph.Range.ComputeStatistics(1)):
            range_ = document.Range(end, end)
            range_.InsertAfter(text)
            end = paragraph.Range.End - 1
        
        end = paragraph.Range.End - 1
        for i in range(100):
            range_2 = document.Range(end-1, end)
            range_2.Delete()
            end = paragraph.Range.End - 1
            if paragraph.Range.ComputeStatistics(1) == lines:
                break

    def remove_first_line(self, document):
        txt = document.Paragraphs(1).Range.Text
        if txt == '\r':
            document.Paragraphs(1).Range.Delete()