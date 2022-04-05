import platform
if platform.uname().node == 'EQUIPO':
    syspath = "D:\\Archivos-bot-hip"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"

import sys
sys.path.append(syspath)

from backend.src.document.infrastructure.interfaces.wordsInterface import Words
from backend.src.document.infrastructure.interfaces.formatInterface import Format
from backend.src.document.application.usecases.processDocumentUseCases import FixDocumentUseCase, FixFormatDocumentUseCase, FixAppendixUseCase, FixContractUseCase, EditSignersUseCase, CreateContractUseCase, FixClausulaUseCase
from backend.src.document.infrastructure.interfaces.editSignersInterface import Signers
from backend.src.document.infrastructure.interfaces.createContractInterface import Document

#from backend.src.document.infrastructure.interfaces.fixWords_interface import FixWords
import os
from backend.src.libs.database import rules
import threading
import pythoncom
import win32com.client as win32

def fixDController(myPath, data, info, app_id):
    basePath = myPath
    filesName0 = os.listdir(basePath)
    filesName = []
    #print("fix d controller", filesName0)
    msg = "no minuta"
    for fileName0 in filesName0:
        if "minuta" in fileName0 and not "format" in fileName0:
            kr = fileName0.split("-")[0]
            msg = "minuta"
            fileName = fileName0
            break
    print("msg", msg)
    words = Words(False, app_id)#words = Words(info["inmobiliaria"], False, app_id)
    fixDocument = FixDocumentUseCase(words)
    if msg == "minuta":
        filePath = basePath + "\\" + fileName
        fileFormatted = fileName.split(".rtf")[0]+"-format.rtf"
        pathFormatted = basePath + "\\" + fileFormatted
        print("path formatted: ", pathFormatted)
        if not os.path.exists(pathFormatted):
            responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
            format_ = Format(basePath, pathFormatted, info, False, "inmobiliaria")#info["inmobiliaria"], False)
            fixFormatDocument = FixFormatDocumentUseCase(format_)
            responseFixFormatDocument = fixFormatDocument.execute()
            for fileName in filesName0:
                condicionA = (kr in fileName and ".rtf" in fileName and not "minuta" in fileName and not "clausula" in fileName and not "banco" in fileName)# and not "$" in fileName and not "minuta")
                condicionB = (kr in fileName and ".doc" in fileName  and not "minuta" in fileName and not "KR" in fileName and not "$" in fileName and not "clausula" in fileName and not "banco" in fileName)
                if condicionA or condicionB:
                    print("anexos minutas ", basePath + "\\" + fileName)
                    filePath = basePath + "\\" + fileName
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    if ".rtf" in fileName:
                        fileFormatted = fileName.split(".rtf")[0]+"-format.rtf"
                    elif ".doc" in fileName:
                        fileFormatted = fileName.split(".doc")[0]+"-format.doc"
                    elif ".docx" in fileName:
                        fileFormatted = fileName.split(".doc")[0]+"-format.docx"
                    print(fileFormatted)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "inmobiliaria")#info["inmobiliaria"], False)
                    fixAppendix = FixAppendixUseCase(format_)
                    responseFixFormatDocument = fixAppendix.execute()
                    print(fileName, "se cumple")
        else:
            print("Ya existe minuta formateada")
    else:
        print("no minuta")
    
    clausulaAdicional = []
    for fileName0 in filesName0:
        condA = "clausula" in fileName0 and "adicional" in fileName0
        condB = not "$" in fileName0
        condC = not "format" in fileName0
        if condA and condB and condC:
            clausulaAdicional.append(fileName0)
    print("clausula adicional: ", clausulaAdicional)
    if clausulaAdicional != []:
        for fileName in clausulaAdicional:
            filePath = basePath + "\\" + fileName
            if ".rtf" in fileName:
                fileFormatted = fileName.split(".rtf")[0]+"-format.rtf"
                pathFormatted = basePath + "\\" + fileFormatted
                if not os.path.exists(pathFormatted):
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "inmobiliaria")
                    fixClausula = FixClausulaUseCase(format_)
                    responsefixClausula = fixClausula.execute()
            elif ".doc" in fileName:
                fileFormatted = fileName.split(".doc")[0]+"-format.doc"
                pathFormatted = basePath + "\\" + fileFormatted
                if not os.path.exists(pathFormatted):
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "inmobiliaria")
                    fixClausula = FixClausulaUseCase(format_)
                    responsefixClausula = fixClausula.execute()
            elif ".docx" in fileName:
                fileFormatted = fileName.split(".docx")[0]+"-format.docx"
                pathFormatted = basePath + "\\" + fileFormatted
                if not os.path.exists(pathFormatted):
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "inmobiliaria")
                    fixClausula = FixClausulaUseCase(format_)
                    responsefixClausula = fixClausula.execute()

    bancoFile = []
    for fileName0 in filesName0:
        if "banco" in fileName0 and not "$" in fileName0 and not "format" in fileName0:
            bancoFile.append(fileName0)
    print("banco: ", bancoFile)
    if bancoFile != []:
        for fileName in bancoFile:
            filePath = basePath + "\\" + fileName
            if ".rtf" in fileName:
                fileFormatted = fileName.split(".rtf")[0]+"-format.rtf"
                pathFormatted = basePath + "\\" + fileFormatted
                if not os.path.exists(pathFormatted):
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "banco")#info["banco"], False)
                    fixContractUseCase = FixContractUseCase(format_)
                    responseFixContract = fixContractUseCase.execute()
            elif ".doc" in fileName:
                fileFormatted = fileName.split(".doc")[0]+"-format.doc"
                pathFormatted = basePath + "\\" + fileFormatted
                if not os.path.exists(pathFormatted):
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "banco")#info["banco"], False)
                    fixContractUseCase = FixContractUseCase(format_)
                    responseFixContract = fixContractUseCase.execute()
            elif ".docx" in fileName:
                fileFormatted = fileName.split(".docx")[0]+"-format.docx"
                pathFormatted = basePath + "\\" + fileFormatted
                if not os.path.exists(pathFormatted):
                    responseFixDocument = fixDocument.execute(data, filePath, basePath, fileName)
                    format_ = Format(basePath, basePath + "\\" + fileFormatted, info, False, "banco")#info["banco"], False)
                    fixContractUseCase = FixContractUseCase(format_)
                    responseFixContract = fixContractUseCase.execute()

def start_fixD_threading(myPath, data, info):
    pythoncom.CoInitialize()
    app = win32.gencache.EnsureDispatch("Word.Application")
    print("documento entrando ", app.Name)
    app_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, app)
    thread = threading.Thread(target=fixDController, kwargs={
        "myPath": myPath, 
        "data": data,
        "info": info,
        "app_id": app_id
        })
    thread.start()
    thread.join()
    print("documento saliendo ", app.Name)
    if app.Documents.Count < 1:
        app.Quit(SaveChanges=-1)
    print("termina")

def start_Document_threading(dirName, basePath):
    pythoncom.CoInitialize()
    app = win32.gencache.EnsureDispatch("Word.Application")
    app_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, app)
    thread = threading.Thread(target=createContractController, kwargs={
        "myPath": dirName,
        "app_id": app_id,
        "visible": 1,
        "baseDocument": basePath
        })
    thread.start()
    thread.join()
    #print(msg)
    if app.Documents.Count < 1:
        app.Quit(SaveChanges=-1)
    print("termina")

def editSignersController(body):
    #print("comp", body["comparecientes"])
    #print(body, type(body["kardex"]))
    path = syspath + "\\" + str(body["kardex"]) + "\\data.json"
    signers = Signers()#(body)#["comparecientes"])
    updateSigners = EditSignersUseCase(signers)
    responseUpdateSigners = updateSigners.execute(path, body["compareciente"])
    #print("controller ", responseUpdateSigners)
    return responseUpdateSigners

def createContractController(myPath, app_id, visible, baseDocument):
    document = Document(myPath, app_id, visible, baseDocument)
    createDocument = CreateContractUseCase(document)
    responseCreateDocument = createDocument.execute()
    pass

def inputCont():
    data = rules()
    return data

if __name__ =="__main__":
    """data = rules()
    print("Ingrese el directorio del archivo: ")
    myPath = input()
    print(myPath)
    listPath = myPath.split("\\")
    basePath = "\\".join(listPath[0:len(listPath)-1])
    fileName = "\\"+listPath[len(listPath)-1]
    print("base: ", basePath, "file ", fileName)"""
    print("__name__")
