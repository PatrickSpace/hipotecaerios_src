import platform
if platform.uname().node == 'EQUIPO':
    syspath = "D:\\Archivos-bot-hip"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"

import sys
sys.path.append(syspath)

from back.src.document.application.usecases.fixDocumentUseCase import FixDocumentUseCase
#from backend.src.document.application.usecases.fixFormatUseCase import FixFormatDocumentUseCase
from back.src.document.infrastructure.interfaces.threadingInterface import ThreadDocument
from back.src.document.infrastructure.interfaces.renamePathInterface import RenamePath
from back.src.document.infrastructure.interfaces.documentInterface import Document
from back.src.document.infrastructure.interfaces.wordsInterface import Words
from back.src.document.infrastructure.interfaces.formatInterface import Format
from back.src.document.infrastructure.interfaces.clausulaInterface import Clausula
from back.src.document.infrastructure.interfaces.sectionsInterface import Sections
from back.src.document.infrastructure.interfaces.extendDateInterface import ExtendDate
from back.src.document.infrastructure.interfaces.companyInterface import Company
from back.src.document.infrastructure.interfaces.comparecientesInterface import Comparecientes
from back.src.document.infrastructure.interfaces.exceptionsFunctionsInterface import ExceptionsFunctionsInterface

def fixDocument(myPath, entidades):
    print("en controlador; ")
    basePath = myPath
    threadDocument = ThreadDocument()
    renamePath = RenamePath()
    document = Document()
    words = Words()
    format_ = Format()
    clausula = Clausula()
    sections = Sections()
    extendDate = ExtendDate()
    company = Company()
    comparecientes = Comparecientes()
    ExceptionsFunctions = ExceptionsFunctionsInterface()
    #print(renamePath)

    fixDocument = FixDocumentUseCase(threadDocument, renamePath, document, words, format_, clausula, sections, extendDate, company, comparecientes, ExceptionsFunctions)
    response = fixDocument.execute(myPath, entidades)