import platform
if platform.uname().node == 'EQUIPO':
    syspath = "D:\\Archivos-bot-hip"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"

import sys
sys.path.append(syspath)

from back.src.document.application.usecases.processDocumentUseCases import EditSignersUseCase, CreateContractUseCase
from back.src.document.infrastructure.interfaces.createContractInterface import Contract

#from backend.src.document.infrastructure.interfaces.fixWords_interface import FixWords
import os
from backend.src.libs.database import rules
import threading
import pythoncom
import win32com.client as win32


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

def createContractController(myPath, app_id, visible, baseDocument):
    document = Contract(myPath, app_id, visible, baseDocument)
    createDocument = CreateContractUseCase(document)
    responseCreateDocument = createDocument.execute()
    pass

def inputCont():
    data = rules()
    return data
