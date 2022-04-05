import os
import re
import shutil

class RenamePath:
    def __init__(self):
        pass

    def extract(self, basePath):
        """ Clasifica los tipos de documentos que se encuentran
            en el directorio de trabajo
        """
        filesName0 = os.listdir(basePath)
        minutaList = []
        clausulaList = []
        bancoList = []

        for fileName in filesName0:
            condA_minuta = "minuta" in fileName
            condA_banco = "banco" in fileName
            condA_clausula = "clausula" in fileName and "adicional" in fileName
            condB = not "$" in fileName
            condC = not "format" in fileName
            if condA_minuta and condB and condC:
                minutaList.append(fileName)
            elif condA_clausula and condB and condC:
                clausulaList.append(fileName)
            elif condA_banco and condB and condC:
                bancoList.append(fileName)
                
        documentos = {
            "minuta": minutaList,
            "clausula": clausulaList,
            "banco": bancoList
        }

        return documentos

    def extractFormatted(self, basePath):
        """ Clasifica los tipos de documentos que se encuentran
            en el directorio de trabajo
        """
        filesName0 = os.listdir(basePath)
        minutaList = []
        clausulaList = []
        bancoList = []

        for fileName in filesName0:
            condA_minuta = "minuta" in fileName
            condA_banco = "banco" in fileName
            condA_clausula = "clausula" in fileName and "adicional" in fileName
            condB = not "$" in fileName
            condC = "format" in fileName
            if condA_minuta and condB and condC:
                minutaList.append(fileName)
            elif condA_clausula and condB and condC:
                clausulaList.append(fileName)
            elif condA_banco and condB and condC:
                bancoList.append(fileName)
                
        documentos = {
            "minuta": minutaList,
            "clausula": clausulaList,
            "banco": bancoList
        }

        return documentos

    def verifyExistence(self, basePath, fileName):
        """ Verifica la existencia del documento formateado
        """
        extensions = [".rtf", ".doc", ".docx"]
        filePath = basePath + "\\" + fileName
        for extension in extensions:
            if re.search(r'{}$'.format(extension), fileName): #extension in fileName:
                fileFormatted = fileName.split(extension)[0]+"-format"+extension
                pathFormatted = basePath + "\\" + fileFormatted
        ##
        isPathFormatted = os.path.exists(pathFormatted)
        verifiedInfo = {
            "isPathFormatted": isPathFormatted,
            "filePath": filePath,
            "fileFormatted": fileFormatted,
            "basePath": basePath
        }
        return verifiedInfo

    def copyBase(self, basePath, path):
        print("copy", basePath, path)
        shutil.copy(basePath, path + "\\base.DOC")
        pass