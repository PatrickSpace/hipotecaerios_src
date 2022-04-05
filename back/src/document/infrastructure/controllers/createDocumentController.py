import platform
if platform.uname().node == 'EQUIPO':
    syspath = "D:\\Archivos-bot-hip"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"

import sys
sys.path.append(syspath)

from back.src.document.application.usecases.createContractUseCase import CreateContractUseCase
#from backend.src.document.application.usecases.fixFormatUseCase import FixFormatDocumentUseCase
from back.src.document.infrastructure.interfaces.threadingInterface import ThreadDocument
from back.src.document.infrastructure.interfaces.renamePathInterface import RenamePath
from back.src.document.infrastructure.interfaces.documentInterface import Document
from back.src.document.infrastructure.interfaces.contractInterface import Contract
from back.src.document.infrastructure.interfaces.comparecientesInterface import Comparecientes
from back.src.document.infrastructure.interfaces.exceptionsFunctionsInterface import ExceptionsFunctionsInterface


def createDocument(dirName, basePath):
    print("en controlador; ")
    threadDocument = ThreadDocument()
    renamePath = RenamePath()
    document = Document()
    contract = Contract()
    comparecientes = Comparecientes()
    exceptionsFunctions = ExceptionsFunctionsInterface()
    
    #print(renamePath)

    createDocument_ = CreateContractUseCase(threadDocument, renamePath, document, contract, comparecientes, exceptionsFunctions)
    response = createDocument_.execute(dirName, basePath)