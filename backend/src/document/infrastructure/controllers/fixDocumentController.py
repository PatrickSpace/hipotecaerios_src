import platform
if platform.uname().node == 'EQUIPO':
    syspath = "D:\\Archivos-bot-hip"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"

import sys
sys.path.append(syspath)

from backend.src.document.application.usecases.fixDocumentUseCase import FixDocumentUseCase
from backend.src.document.application.usecases.fixFormatUseCase import FixFormatDocumentUseCase
from backend.src.document.infrastructure.interfaces.threadDocumentInterface import ThreadDocument
from backend.src.document.infrastructure.interfaces.renamePathInterface import RenamePath
from backend.src.document.infrastructure.interfaces.wordsInterface import Words
from backend.src.document.infrastructure.interfaces.formatInterface import Format

def fixDocument(myPath, data, info):
    basePath = myPath
    threadDocument = ThreadDocument()
    renamePath = RenamePath()
    #words = Words()

    fixDocument = FixDocumentUseCase(threadDocument, renamePath, Words, Format)
    response = fixDocument.execute(myPath, data, info)
    """print("respuesta: ", response)

    if "banco" in response["fileFormatted"]:
        typeEntity = "banco"
    else:
        typeEntity = "inmobiliaria"

    format_ = Format(response["basePath"], response["basePath"] + "\\" + response["fileFormatted"], info, False, typeEntity)#info["banco"], False)
    fixFormatUseCase = FixFormatDocumentUseCase(format_, threadDocument)
    responseFixContract = fixFormatUseCase.execute(typeEntity)"""