import platform
from back.src.libs.config import archivos

if platform.uname().node == 'EQUIPO':
    syspath = archivos()["routesSys"]["path"]#D:\\Archivos-bot-hip"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"

import sys
sys.path.append(syspath)

from src.document.infrastructure.interfaces.comparecientesInterface import Comparecientes
from src.document.application.usecases.createComparecienteUseCase import CreateCompareciente


def createCompareciente(body, myPath):
    comparecientes = Comparecientes()
    createCompareciente_ = CreateCompareciente(comparecientes)
    print("controlador")
    response = createCompareciente_.execute(body, myPath)
    return response