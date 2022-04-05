import re
import json
import platform
if platform.uname().node == 'EQUIPO':
    bancosInfoPath = "D:\\bot-hip\\backend\\src\\libs\\bancosInfo.json"
    inmobiliariasInfoPath = "D:\\bot-hip\\backend\\src\\libs\\inmobiliariaInfo.json"
else:
    bancosInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\bancosInfo.json" 
    inmobiliariasInfoPath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\inmobiliariaInfo.json"

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
                            listParagraph.append(paragraph.Range.Text)
                            clientes = self.clienteBCP(listParagraph)
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
                            listParagraph.append(paragraph.Range.Text)
                            clientes = self.clienteScottia(listParagraph)
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
                            listParagraph.append(paragraph.Range.Text)
                            clientes = self.clienteInterbank(listParagraph)

        return clientes

    def clienteBCP(self, listParagraph):
        regexName = 'NOMBRES Y APELLIDOS:[^A-Z]*(.*[A-Z])'
        regexestadoCiv = 'ESTADO CIVIL:[^A-Z]*(.*[A-Z])'
        regexAddress = 'DOMICILIO:[^A-Z0-9]*(.*[A-Z0-9])'
        regexDNI = 'D.N.I.[^0-9]*(.*[0-9])'
        regexPartnerName = 'NOMBRES Y APELLIDOS DEL CONYUGE:[^A-Z]*(.*[A-Z])'

        regexComparecientes = {
            "nombre": 'NOMBRES Y APELLIDOS:[^A-Z]*(.*[A-Z])',
            "estado civil": 'ESTADO CIVIL:[^A-Z]*(.*[A-Z])',
            "domicilio": 'DOMICILIO:[^A-Z0-9]*(.*[A-Z0-9])',
            "dni": 'D.N.I.[^0-9]*(.*[0-9])'
            }


        client = {
        "nombre": "",
        "nacionalidad": "",
        "estado civil": "",
        "profesion": "",
        "domicilio": "",
        "dni": "",
        "representante": "cliente",
        "genero": "DONA"
        }
        clients = []
        for string in listParagraph:
            ######### PRIMER CLIENTE #########
            # Nombre
            name = re.findall(regexComparecientes["nombre"], string)
            if (len(name) > 0):
                client["nombre"] = name[0]
                print(name[0])
                continue
            # Estado Civil
            estadoCiv = re.findall(regexestadoCiv, string)
            if (len(estadoCiv) > 0):
                client["estado civil"] = estadoCiv[0]
                if (estadoCiv[0] == "CASADO"):
                    estadoCivPartner = "CASADA"
                if (estadoCiv[0] == "CASADA"):
                    estadoCivPartner = "CASADO"
                print(estadoCiv[0])
                continue
            # Domicilio
            address = re.findall(regexAddress, string)
            if (len(address) > 0):
                client["domicilio"] = address[0]
                #coupleAddress = address[0]
                print(address[0])
                continue
            # DNI
            dni = re.findall(regexDNI, string)
            if (len(dni) > 0):
                client["dni"] = dni[0]
                print(dni[0])
                continue

            ######### EN CASO DE ESTAR CASADO #########
            nextPoint = re.findall('CONYUGE DEL CLIENTE:', string)
            if (len(nextPoint) > 0):
                clients.append(client)
                client = client.copy()
                client["estado civil"] = estadoCivPartner

                
                continue
            partnerName = re.findall(regexPartnerName, string)
            if (len(partnerName) > 0):
                client["nombre"] = partnerName[0]
                print(partnerName[0])

        clients.append(client)
        return clients

    def clienteScottia(self, listParagraph):
        return []

    def clienteInterbank(self, listParagraph):
        return []

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
                            listParagraph.append(paragraph.Range.Text)
                            representantesBanco = self.representantesBCP(listParagraph)
                            item = item + 1
                            if item == 10:
                                break
        elif bancoNombre == "SCOTIABANK PERU S.A.A.":
            for section in document.Sections:
                paragraphs = section.Range.Paragraphs
                if "ANEXO" in paragraphs(1).Range.Text:
                    flagStart = "DATOS DEL BANCO"
                    itemEnd = 10
                    startCount = False
                    item = 0
                    for paragraph in paragraphs:
                        if flagStart in paragraph.Range.Text:
                            startCount = True
                        elif startCount == True:
                            listParagraph.append(paragraph.Range.Text)
                            representantesBanco = self.representantesScottia(listParagraph)
                            item = item + 1
                            if item == 10:
                                break
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
                            listParagraph.append(paragraph.Range.Text)
                            representantesBanco = self.representantesInterbank(listParagraph)
                            item = item + 1
                            if item == 10:
                                break

        return representantesBanco


    def representantesBCP(self, listParagraph):
        return []

    def representantesScottia(self, listParagraph):
        return []

    def representantesInterbank(self, listParagraph):
        return []
    
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
        #print("----", infoBanco)
        #print("---", infoFull)
        if infoFull != '':
            print("not---")
            outB = infoBanco[infoFull]
            return outB
        else:
            print("---else")
            outB = {
            "nombre": "",
            "ruc": "",
            "domicilio": ""
            }
            return outB

    def getInmobiliariaInfo(self, infoFull):
        with open(inmobiliariasInfoPath) as f:
            infoInmobiliaria = json.load(f)
        if not infoFull:
            outI = infoInmobiliaria[infoFull]
            return outI
        else:
            outI = {
            "nombre": "",
            "ruc": "",
            "domicilio": ""
            }
            return outI