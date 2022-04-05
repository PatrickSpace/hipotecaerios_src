import json
import re
from backend.src.document.infrastructure.middlewares.printExceptionInfo import *
""" Extrae los comparecientes
"""
def extract_signers(document, basePath, info, infoFull, section, bancosInfoPath, inmobiliariasInfoPath, entidadPath): #titulo,
    try:
        print("------------ EXTRAE FIRMANTES -------------")
        print(info)
        paragraphs = section.Range.Paragraphs
        rangeTitle = paragraphs(1).Range
        print(rangeTitle)
        signers = []
        comprador = {
            "nombre": "",
            "nacionalidad": "",
            "estado civil": "",
            "profesion": "",
            "domicilio": "",
            "dni": "",
            "representante": "COMPRADOR",
            "genero": ""
        }
        flag_comprador, flag_comprador_dni = "no", "no" #
        with open(basePath + '\\data.json') as f:
            comparecientes = json.load(f)
        signers.extend(getRepresentantesInfo(entidadPath, infoFull))
        comparecientes["comparecientes"] = signers
        comparecientes["banco"] = getBancoInfo(bancosInfoPath, infoFull)
        comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath, infoFull)
        #print("comparecientes agregados ---", comparecientes)
        with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
            json.dump(comparecientes, f, ensure_ascii=False, indent=4)
    except Exception as exc:
        printExceptionInfo(exc)
        #print("---excepcion----", exc)


def extract_signers2(document, basePath, info, infoFull, section, bancosInfoPath, inmobiliariasInfoPath, entidadPath): #titulo,
    try:
        print("------------ EXTRAE FIRMANTES -------------")
        print(info)
        paragraphs = section.Range.Paragraphs
        rangeTitle = paragraphs(1).Range
        print(rangeTitle)
        signers = []
        comprador = {
            "nombre": "",
            "nacionalidad": "",
            "estado civil": "",
            "profesion": "",
            "domicilio": "",
            "dni": "",
            "representante": "COMPRADOR",
            "genero": ""
        }
        flag_comprador, flag_comprador_dni = "no", "no" #
        if paragraphs(1).Range.Find.Execute(FindText="ANEXO A") == True and (info == "Alcanfores" or info == "Quatro Beta" or info == "Quatro Epsilon"):
            print("primer caso ", info)
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                #print(estado)
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                    range_ = paragraphs(i).Range
                    fnombre = range_.Find.Execute(FindText=":")
                    if fnombre == True:
                        nombre_ = document.Range(range_.End, paragraphs(i).Range.End-1).Text
                        comprador["nombre"] = nombre_
                elif paragraphs(i).Range.Find.Execute(FindText="NOMBRE") == True and paragraphs(i).Range.Find.Execute(FindText=estado) == True:
                    range_ = paragraphs(i).Range
                    fnombre = range_.Find.Execute(FindText=":")
                    if fnombre == True:
                        nombre_ = document.Range(range_.End, paragraphs(i).Range.End-1).Text
                        comprador["nombre"] = nombre_
                elif paragraphs(i).Range.Find.Execute(FindText="DNI") == True:
                    range_ = paragraphs(i).Range
                    fdni = range_.Find.Execute(FindText=":")
                    if fdni == True:
                        numero_ = document.Range(range_.End, paragraphs(i).Range.End-1).Text
                        comprador["dni"] = numero_
                elif paragraphs(i).Range.Find.Execute(FindText="DIRECCION") == True:
                    range_ = paragraphs(i).Range
                    fdir = range_.Find.Execute(FindText=":")
                    if fdir == True:
                        direccion_ = document.Range(range_.End, paragraphs(i).Range.End-1).Text
                        comprador["domicilio"] = direccion_
                elif paragraphs(i).Range.Find.Execute(FindText="ESTADO CIVIL") == True:
                    range_ = paragraphs(i).Range
                    fec = range_.Find.Execute(FindText=":")
                    if fec == True:
                        ec_ = document.Range(range_.End, paragraphs(i).Range.End-1).Text
                        comprador["estado civil"] = ec_
            #print("formato area", comprador)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
        elif paragraphs(1).Range.Find.Execute(FindText="ANEXO A") == True and info == None:#"Buenas Inversiones S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            rangoEstado = "EN ESPERA"
            for i in range(1, paragraphs.Count+1):
                if estado == "CONYUGE":
                    signers.append(comprador)
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                if "NUMERAL" in paragraphs(i).Range.Text and "COMPRADOR" in paragraphs(i).Range.Text:
                    rangoEstado = "EN NUMERAL"
                    print(rangoEstado, i)
                    #text_ = document.Paragraphs(i).Range.Text
                if rangoEstado == "EN NUMERAL" and "NACIONALIDAD" in paragraphs(i).Range.Text:
                    text_ = paragraphs(i).Range.Text
                    print("----",text_ , "-----")
                    parametros = {
                        "NACIONALIDAD": "nacionalidad", 
                        "N°": "dni",
                        "PROFESION": "profesion",
                        "ESTADO CIVIL": "estado civil"
                        }
                    list_text_ = text_.split(",")
                    if list_text_ != []:
                        for index_list in range(len(list_text_)):
                            if "NACIONALIDAD" in list_text_[index_list] and index_list !=0:
                                comprador["nombre"] = list_text_[index_list-1]
                    for parametro in parametros.keys():
                        match = re.findall('([\s\w\.-]+)'+parametro+'([\s\w\.-]+)', text_)
                        print(match)
                        if match != []:
                            comprador[parametros[parametro]] = match[0][1]
                            print(comprador)
                    print("comp ", comprador)
                    #signers.append(comprador)
                    estado == "CONYUGE"
                    print("signers in", signers)
                elif rangoEstado == "EN NUMERAL" and "NUMERAL" in paragraphs(i).Range.Text and "DATOS DEL COMPRADOR" not in paragraphs(i).Range.Text:
                    rangoEstado = "CONYUGE"
                    print("breaking", i)
                    #break
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            print("signers", signers)
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath, infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
        elif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "Promotora Albamar S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                elif re.search(r'EL\s+COMPRADOR', paragraphs(i).Range.Text) and estado == "COMPRADOR":
                    if re.search(r'[\w\s]+', paragraphs(i).Range.Text):
                        comprador["nombre"] = re.search(r'[\w\s]+', paragraphs(i).Range.Text).group()
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = paragraphs(i).Range.Text[re.search(r'DNI', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'AV+[\S\s]+A QUIEN', txt_dom).group()
                        comprador["domicilio"] = match_dom[:len(match_dom)-7]
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
            #passelif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "Promotora Albamar S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                elif re.search(r'EL\s+COMPRADOR', paragraphs(i).Range.Text) and estado == "COMPRADOR":
                    if re.search(r'[\w\s]+', paragraphs(i).Range.Text):
                        comprador["nombre"] = re.search(r'[\w\s]+', paragraphs(i).Range.Text).group()
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = paragraphs(i).Range.Text[re.search(r'DNI', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'AV+[\S\s]+A QUIEN', txt_dom).group()
                        comprador["domicilio"] = match_dom[:len(match_dom)-7]
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
            #pass
        elif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "CP Building SAC":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                elif re.search(r'EL\s+COMPRADOR', paragraphs(i).Range.Text) and estado == "COMPRADOR":
                    if re.search(r'[\w\s]+', paragraphs(i).Range.Text):
                        comprador["nombre"] = re.search(r'[\w\s]+', paragraphs(i).Range.Text).group()
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = paragraphs(i).Range.Text[re.search(r'DNI', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'(AV+[\S\s]+A QUIEN)|(CALLE+[\S\s]+A QUIEN)', txt_dom).group()
                        comprador["domicilio"] = match_dom[:len(match_dom)-7]
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
            #pass
        elif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "Promotora Albamar S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                elif re.search(r'(EL\s+COMPRADOR)|(LA\s+COMPRADORA)', paragraphs(i).Range.Text) and estado == "COMPRADOR":
                    if re.search(r'[\w\s]+', paragraphs(i).Range.Text):
                        txt_f = re.search(r'VENDODOR+[\S\s]+COMPRADOR', paragraphs(i).Range.Text).group()
                        comprador["nombre"] = re.search(r'((?<=señora\s)|(?<=señor\s))+[\w\s]+', txt_f).group()
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = paragraphs(i).Range.Text[re.search(r'DNI', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'(AV+[\S\s]+A QUIEN)|(CALLE+[\S\s]+A QUIEN)', txt_dom).group()
                        comprador["domicilio"] = match_dom[:len(match_dom)-7]
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
            #pass
        elif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "Josmi Grupo Inversor S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                elif re.search(r'EL\s+COMPRADOR', paragraphs(i).Range.Text) and re.search(r'DNI', paragraphs(i).Range.Text) and estado == "COMPRADOR":
                    if re.search(r'[\w\s]+(?=\sidentificad.)', paragraphs(i).Range.Text):
                        comprador["nombre"] = re.search(r'[\w\s]+(?=\sidentificad.)', paragraphs(i).Range.Text).group()
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = re.search(r'(DNI)+[\s\S]+', paragraphs(i).Range.Text).group()
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'(AV+[\S\s]+CUYOS)|(CALLE+[\S\s]+CUYOS)', txt_dom).group()
                        comprador["domicilio"] = match_dom[:len(match_dom)-7]
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
            #passelif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "Promotora Albamar S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            for i in range(1, paragraphs.Count+1):
                if paragraphs(i).Range.Find.Execute(FindText="CONYUGE") == True:
                    signers.append(comprador)
                    estado = "CONYUGE"
                    comprador = {
                        "nombre": "",
                        "nacionalidad": "",
                        "estado civil": "CASADO",
                        "profesion": "",
                        "domicilio": "",
                        "dni": "",
                        "representante": "COMPRADOR",
                        "genero": ""
                    }
                elif re.search(r'(EL\s+COMPRADOR)|(LA\s+COMPRADORA)', paragraphs(i).Range.Text) and estado == "COMPRADOR":
                    if re.search(r'[\w\s]+', paragraphs(i).Range.Text):
                        txt_f = re.search(r'VENDODOR+[\S\s]+COMPRADOR', paragraphs(i).Range.Text).group()
                        comprador["nombre"] = re.search(r'((?<=señora\s)|(?<=señor\s))+[\w\s]+', txt_f).group()
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = paragraphs(i).Range.Text[re.search(r'DNI', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'(AV+[\S\s]+A QUIEN)|(CALLE+[\S\s]+A QUIEN)', txt_dom).group()
                        comprador["domicilio"] = match_dom[:len(match_dom)-7]
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
            #pass
        elif paragraphs(1).Range.Find.Execute(FindText="ANEXO A") == True and info == "Buenas Inversiones S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            rangoEstado = "EN ESPERA"
            for i in range(1, paragraphs.Count+1):
                #txt_ = paragraphs(i).Range.Text
                #print(txt_)
                """if re.search(r'DATOS+[\w\s]+COMPRADOR', paragraphs(i).Range.Text) and rangoEstado == "EN ESPERA":
                    rangoEstado = "LISTO"
                    print("datos del comprador")"""
                if "NACIONALIDAD" in paragraphs(i).Range.Text and "EN ESPERA" in rangoEstado:
                    txt_ = paragraphs(i).Range.Text
                    print("despues de comprador:   ",txt_, "     .")
                    if re.search(r'[\w\s]+', txt_):
                        comprador["nombre"] = re.search(r'^[\w\s]+', txt_).group()
                    if re.search(r'NACIONALIDAD', paragraphs(i).Range.Text):
                        txt_nac = re.search(r'NACIONALIDAD\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["nacionalidad"] = txt_nac.group(1)
                    if re.search(r'DNI', paragraphs(i).Range.Text):
                        txt_dni = paragraphs(i).Range.Text[re.search(r'DNI', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_dni).group()
                    if re.search(r'EXTRANJERIA', paragraphs(i).Range.Text):
                        txt_ext = paragraphs(i).Range.Text[re.search(r'EXTRANJERIA', paragraphs(i).Range.Text).start():]
                        comprador["dni"] = re.search(r'\d+', txt_ext).group()
                    if re.search(r'DOMICILIO', paragraphs(i).Range.Text):
                        txt_dom = paragraphs(i).Range.Text[re.search(r'DOMICILIO', paragraphs(i).Range.Text).start():]
                        match_dom = re.search(r'AV+[\S\s]+', txt_dom).group()
                        comprador["domicilio"] = match_dom
                    if re.search(r'ESTADO\s+CIVIL', paragraphs(i).Range.Text):
                        txt_ec = re.search(r'ESTADO\s+CIVIL\s+([\w]+)', paragraphs(i).Range.Text)
                        comprador["estado civil"] = txt_ec.group(1)
                    rangoEstado = "LISTO"
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
        elif paragraphs(1).Range.Find.Execute(FindText="PAINO") == True and info == "Espinoza Arquitectos S.A.C.":
            print("--- en if -----")
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            estado = "COMPRADOR"
            rangoEstado = "EN ESPERA"
            for i in range(1, paragraphs.Count+1):
                pass
            signers.append(comprador)
            signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath,infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
        elif paragraphs(1).Range.Find.Execute(FindText="ANEXO A") == True and info == "Paz Centenario S.A.":
            print("--- en if Paz Centenario S.A.---")
            with open(basePath, '\\data.json') as f:
                comparecientes = json.load(f)
        else:
            with open(basePath + '\\data.json') as f:
                comparecientes = json.load(f)
            signers.append(comprador)
            if not entidadPath:
                pass
            else:    
                signers.extend(getRepresentantesInfo(entidadPath, infoFull))
            print("signers else", signers)
            comparecientes["comparecientes"] = signers
            comparecientes["banco"] = getBancoInfo(bancosInfoPath, infoFull)
            comparecientes["inmobiliaria"] = getInmobiliariaInfo(inmobiliariasInfoPath,infoFull)
            #print("comparecientes agregados ---", comparecientes)
            with open(basePath + '\\' + 'data.json', 'w', encoding='utf-8') as f:
                json.dump(comparecientes, f, ensure_ascii=False, indent=4)
    except Exception as exc:
        printExceptionInfo(exc)
        #print("---excepcion----", exc)

def getBancoInfo(bancosInfoPath, infoFull):
    with open(bancosInfoPath) as f:
        infoBanco = json.load(f)
    print("----", infoBanco)
    print("---", infoFull)
    if infoFull["banco"] != '':
        print("not---")
        outB = infoBanco[infoFull["banco"]]
        return outB
    else:
        print("---else")
        outB = {
        "nombre": "",
        "ruc": "",
        "domicilio": ""
        }
        return outB

def getInmobiliariaInfo(inmobiliariasInfoPath ,infoFull):
    with open(inmobiliariasInfoPath) as f:
        infoInmobiliaria = json.load(f)
    if not infoFull["inmobiliaria"]:
        outI = infoInmobiliaria[infoFull["inmobiliaria"]]
        return outI
    else:
        outI = {
        "nombre": "",
        "ruc": "",
        "domicilio": ""
        }
        return outI

def getRepresentantesInfo(entidadPath, infoFull):
    listE = []
    with open(entidadPath) as f:
        infoEntidad = json.load(f)
    for keyR in infoFull.keys():
        if keyR == "banco" and infoFull[keyR] != "":
            listE.extend(infoEntidad[infoFull["banco"]])
        elif keyR == "inmobiliaria" and infoFull[keyR] != "":
            listE.extend(infoEntidad[infoFull["inmobiliaria"]])
    #outE = infoEntidad[infoFull[tipoEntidad]]
    return listE