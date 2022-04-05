import re
import json
import platform
import os
if platform.uname().node == 'EQUIPO':
    bancosInfoPath = "D:\\bot-hip\\backend\\src\\libs\\bancosInfo.json"
    inmobiliariasInfoPath = "D:\\bot-hip\\backend\\src\\libs\\inmobiliariaInfo.json"
else:
    bancosInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\bancosInfo.json" 
    inmobiliariasInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\inmobiliariaInfo.json"

from back.src.document.infrastructure.middlewares.convertSpecialCharacter import convertSpecialCharacter

class Comparecientes:
    def __init__(self):
        pass

    def extraerClientes(self, document, bancoNombre):
        listParagraph = []
        clientes = None
        if bancoNombre == "BANCO DE CREDITO DEL PERU":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "DEL CLIENTE"
                    flagEnd = "DE LOS REPRESENTANTES DEL BANCO"
                    for paragraph in paragraphs:
                        if flagEnd in paragraph.Range.Text:
                            break
                        else:
                            nombreCliente = paragraph.Range.Text
                            listParagraph.append(nombreCliente.upper())
            clientes = self.datosCliente(listParagraph, bancoNombre)

        elif bancoNombre == "SCOTIABANK PERU S.A.A.":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "DATOS DEL CLIENTE"
                    flagEnd = "DATOS DEL BANCO"
                    for paragraph in paragraphs:
                        if flagEnd in paragraph.Range.Text:
                            break
                        else:
                            nombreCliente = paragraph.Range.Text
                            listParagraph.append(nombreCliente.upper())
            clientes = self.datosCliente(listParagraph, bancoNombre)
        elif bancoNombre == "INTERBANK":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "EL CLIENTE"
                    flagEnd = "INTERBANK"
                    for paragraph in paragraphs:
                        if flagEnd in paragraph.Range.Text:
                            break
                        else:
                            nombreCliente = paragraph.Range.Text
                            listParagraph.append(nombreCliente.upper())
            clientes = self.datosCliente(listParagraph, bancoNombre)

        return clientes

    def datosCliente(self, listaEntrada, bancoNombre, extraerConyugue=True):
        formatoClientes = { #Formato de salida de los datos (mismo para todos los datos)
            "nombre": '',
            "nacionalidad": "PERUANA",
            "estado civil": '',
            "profesion": "",
            "domicilio": '',
            "dni": '',
            "representante": "CLIENTE",
            "genero": "DON"
        }

        regexInterbank = {
            "nombre": 'NOMBRE\(S\) Y APELLIDO\(S\):[^A-Z]*(.*[A-Z])',
            "estado civil": 'ESTADO CIVIL:[^A-Z]*(.*[A-Z])',
            "domicilio": 'DOMICILIO: (.+)',
            "dni": 'DOCUMENTO DE IDENTIDAD: (.+)',
        }
        regexBCP = {
            "nombre": 'NOMBRES Y APELLIDOS[A-Z ]*:[^A-Z]*(.*[A-Z])',
            "estado civil": 'ESTADO CIVIL:[^A-Z]*(.*[A-Z])',
            "domicilio": 'DOMICILIO:[^A-Z0-9]*(.*[A-Z0-9])',
            "dni": 'D.N.I.[^0-9]*(.*[0-9])',
        }
        regexScottia = {
            "nombre": 'NOMBRES Y APELLIDOS[A-Z ]*[^A-Z]*(.*[A-Z])',
            "estado civil": 'ESTADO CIVIL[^A-Z]*(.*[A-Z])',
            "domicilio": 'DOMICILIO[^A-Z0-9]*(.*[A-Z0-9])',
            "dni": 'DNI[^0-9]*(.*[0-9])',
        }

        regexDict = {}

        if bancoNombre == "BANCO DE CREDITO DEL PERU":
            regexDict.update(regexBCP)
        elif bancoNombre == "SCOTIABANK PERU S.A.A.":
            regexDict.update(regexScottia)
        elif bancoNombre == "INTERBANK":
            regexDict.update(regexInterbank)

        cliente = [formatoClientes.copy()]
        index = 0 #Permite acceder al diccionario con datos del conyuge mas adelante (Si los hay)

        for linea in listaEntrada:
            if (re.search("CONYUGE",linea) is not None) and (not extraerConyugue):
                return cliente #Si no se quieren extraer datos del conyuge, la funcion se detiene despues de que tiene todos los datos del clinte
            if extraerConyugue and (not len(cliente)==2) and re.search("CONYUGE",linea) is not None:
                cliente.append(cliente[0].copy()) #Si se quieren extraer datos del conyuge, añade su diccionario al array de salida
                index = 1

            for tipoDato in regexDict: #Ciclo que recorre cada tipo de dato que se puede extraer y lo busca con la linea actual
                                            #Si encuentra el dato, sale del ciclo y pasa a la siguiente linea
                x = re.findall(regexDict[tipoDato], linea)
                if len(x) > 0:
                    cliente[index][tipoDato] = x[0]
                    break

        return cliente

    def extraerRepresentantesBanco(self, document, bancoNombre):
        listParagraph = []
        representantesBanco = None
        if bancoNombre == "BANCO DE CREDITO DEL PERU":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
    
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "DE LOS REPRESENTANTES DEL BANCO"
                    itemEnd = 10
                    startCount = False
                    item = 0
                    for paragraph in paragraphs:
                        if flagStart in paragraph.Range.Text:
                            startCount = True
                        elif startCount == True:
                            nombreRepresentante = paragraph.Range.Text.upper() 
                            listParagraph.append(nombreRepresentante)
                            item = item + 1
                            if item == 10:
                                break
            representantesBanco = self.datosBanco(listParagraph, bancoNombre)
        elif bancoNombre == "SCOTIABANK PERU S.A.A.":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "DATOS DEL BANCO"
                    flagEnd = "DATOS DEL VENDEDOR"
                    itemEnd = 10
                    startCount = False
                    item = 0
                    for paragraph in paragraphs:
                        if flagStart in paragraph.Range.Text:
                            startCount = True
                        elif startCount == True and not flagEnd in paragraph.Range.Text:
                            nombreRepresentante = paragraph.Range.Text.upper() 
                            listParagraph.append(nombreRepresentante)
                            item = item + 1
                            if item == 10:
                                break
                        elif flagEnd in paragraph.Range.Text:
                            break
            representantesBanco = self.datosBancoScottia(listParagraph)
        elif bancoNombre == "INTERBANK":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "INTERBANK"
                    itemEnd = 10
                    startCount = False
                    item = 0
                    for paragraph in paragraphs:
                        if flagStart in paragraph.Range.Text:
                            startCount = True
                        elif startCount == True:
                            nombreRepresentante = paragraph.Range.Text.upper() 
                            listParagraph.append(nombreRepresentante)
                            item = item + 1
                            if item == 10:
                                break
            representantesBanco = self.datosBanco(listParagraph, bancoNombre)
        return representantesBanco

    def datosBanco(self, listaEntrada, bancoNombre):
        formatoBancos = { #Formato de salida de los datos
            "nombre": '',
            "nacionalidad": "PERUANA",
            "estado civil": '',
            "profesion": "",
            "domicilio": '',
            "dni": '',
            "representante": "BANCO",
            "genero": ""
        }

        regexRepBankInterbank = {
            "nombre": 'NOMBRE\(S\) Y APELLIDO\(S\) :[^A-Z]*(.*[A-Z])',
            "dni": 'DOCUMENTO DE IDENTIDAD[^0-9]*(.*[0-9])',
            "domicilio": '^DOMICILIO:.*PROVINCIA DE ([A-Z ]*),'
        }
        regexRepInmoInterbank = {
            "nombre": 'NOMBRE\(S\) Y APELLIDO\(S\): [^A-Z]*(.*[A-Z])',
            "dni": 'DOCUMENTO DE IDENTIDAD: [^0-9]*(.*[0-9])',
            "domicilio": '^DOMICILIO:.*PROVINCIA DE ([A-Z ]*),'
        }
        regexRepBancoBCP = {
            "nombre": '\(.*\)[^A-Z]([A-Z ]*[A-Z])',
            "dni": 'CON D\.N\.I\. N°(|\s+)([0-9]*).*',
            "domicilio": 'REGISTRO DE PERSONAS JURIDICAS DE ([A-Z ]*)'
        }

        regexDict = {}

        if bancoNombre == "BANCO DE CREDITO DEL PERU":
            regexDict.update(regexRepBancoBCP)
        elif bancoNombre == "INTERBANK":
            regexDict.update(regexRepBankInterbank)

        cliente = [formatoBancos.copy()]
        index = 0

        for linea in listaEntrada:
            if (cliente[index]['dni'] != '') and (cliente[index]['nombre'] != ''):
                cliente.append(formatoBancos.copy())
                index += 1
                cliente[index]['domicilio'] = cliente[0]['domicilio']

            for tipoDato in regexDict:   
                x = re.findall(regexDict[tipoDato], linea)
                if len(x) > 0:
                    cliente[index][tipoDato] = x[0]

        if cliente[index]['nombre'] == '':
            cliente.pop()
        return cliente

    def datosBancoScottia(self, listaEntrada):
        formatoBancos = {
            "nombre": '',
            "nacionalidad": "PERUANA",
            "estado civil": '',
            "profesion": "",
            "domicilio": 'LIMA',
            "dni": '',
            "representante": "BANCO",
            "genero": ""
        }

        regexScottia = {
            "nombre": '[^A-Z]*(.*[A-Z])',
            "dni": '[^0-9]*(.*[0-9])',
        }


        representantes = []
        for linea in listaEntrada:

            listLinea = linea.split('== ==')

            if listLinea[0] == "RAZON SOCIAL." or listLinea[0] == "DOMICILIO." or listLinea[0] == "REPRESENTANTES." or listLinea[0] == "DATOS DE INSCRIPCION REGISTRAL.":
                continue
            formatoBancos = formatoBancos.copy()
            name1 = re.findall(regexScottia["nombre"], listLinea[0])
            dni1 = re.findall(regexScottia["dni"], listLinea[1])
    
            if len(name1) > 0:
                formatoBancos["nombre"] = name1[0]
            if len(dni1) > 0:
                formatoBancos["dni"] = dni1[0]
            representantes.append(formatoBancos)

            if len(listLinea) > 3:
                formatoBancos = formatoBancos.copy()
                name2 = re.findall(regexScottia["nombre"], listLinea[3])
                dni2 = re.findall(regexScottia["dni"], listLinea[4])
                if name2 and dni2:
                    formatoBancos["nombre"] = name2[0]
                    formatoBancos["dni"] = dni2[0]
                    formatoBancos["representante"] = "BANCO"
                    representantes.append(formatoBancos)
                elif not name2 and not dni2 and len(listLinea) > 6:
                    name2 = re.findall(regexScottia["nombre"], listLinea[5])
                    dni2 = re.findall(regexScottia["dni"], listLinea[6])
        return representantes

    
    def saveInFileBanco(self, bancoNombre, clientes, representantesBanco, basePath):
        with open(basePath + '\\data.json') as f:
            comparecientes = json.load(f)
        #signers.extend(getRepresentantesInfo(entidadPath, infoFull))
        comparecientes["comparecientes"] = clientes
        comparecientes["comparecientes"].extend(representantesBanco)
        comparecientes["banco"] = self.getBancoInfo(bancoNombre)
        with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
            json.dump(comparecientes, f, ensure_ascii=False, indent=4)

    def saveInFileInmo(self, inmobiliariaNombre, representantesInmo, basePath):
        with open(basePath + '\\data.json') as f:
            comparecientes = json.load(f)
        #signers.extend(getRepresentantesInfo(entidadPath, infoFull))
        if "comparecientes" in comparecientes.keys():
            if comparecientes["comparecientes"]:
                rep = comparecientes["comparecientes"]
                comparecientes["comparecientes"] = rep.extend(representantesInmo)
        else:
            comparecientes["comparecientes"] = representantesInmo
        comparecientes["inmobiliaria"] = self.getInmobiliariaInfo(inmobiliariaNombre)
        with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
            json.dump(comparecientes, f, ensure_ascii=False, indent=4)

    def getBancoInfo(self, infoFull):
        with open(bancosInfoPath) as f:
            infoBanco = json.load(f)
        if infoFull != '':

            outB = infoBanco[infoFull]
            return outB
        else:

            outB = {
            "nombre": "",
            "ruc": "",
            "domicilio": ""
            }
            return outB

    def getInmobiliariaInfo(self, infoFull):
        with open(inmobiliariasInfoPath) as f:
            infoInmobiliaria = json.load(f)
        if infoFull == '' or infoFull == None:#not infoFull:
            outI = {
            "nombre": "",
            "ruc": "",
            "domicilio": ""
            }
            return outI
        else:
            outI = infoInmobiliaria[infoFull]
            return outI

    def getComparecientes(self, myPath):
        with open(myPath+'\\data.json', encoding="utf-8") as f:
            comparecientes = json.load(f)
        comparecientes = convertSpecialCharacter(comparecientes)
        return comparecientes

    def crearCompareciente(self, body, myPath):
        kardex = body["data"]["kardex"]
        data = body["data"]
        docPath = myPath + '\\' + str(kardex) + '\\data.json'
        os.remove(docPath)
        with open(docPath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        outPut = {
            "message": "Agregado"
        }
        return outPut