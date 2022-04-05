from backend.src.document.infrastructure.middlewares.printExceptionInfo import *

class FixDocumentUseCase:
    def __init__(self, threadInterface, renamePathInterface, wordsClass, FormatClass):
        self.threadInterface = threadInterface
        self.renamePathInterface = renamePathInterface
        self.wordsClass = wordsClass
        self.formatClass = FormatClass
        self.responseMain = None

    def execute(self, myPath, data, info):
        try:
            print("arreglar documento")
            self.threadInterface.start(myPath, data, info, self.main)
            return self.responseMain
        except Exception as exc:
            printExceptionInfo(exc)
            #print(exc)
        finally:
            self.threadInterface.closeThreading()
            print("finally")

    def main(self, myPath, data, info, app_id):
        basePath = myPath
        try:
            print("main")
            documentos = self.renamePathInterface.extract(basePath)
            words = self.wordsClass(True, app_id)
            for typeDoc in documentos.keys(): # ["minuta", "clausula", "banco"]
                if documentos[typeDoc] != []: #typeDoc != []:
                    for fileName in documentos[typeDoc]:
                        verifiedInfo = self.renamePathInterface.verifyExistence(basePath, fileName)
                        if not verifiedInfo["isPathFormatted"]:
                            #self.responseMain = words.fix(data, verifiedInfo, basePath, fileName)
                            response = words.fix(data, verifiedInfo, basePath, fileName)
            
                            if "banco" in response["fileFormatted"]:
                                typeEntity = "banco"
                            else:
                                typeEntity = "inmobiliaria"
                            
                            formatInterface = self.formatClass(response["basePath"], response["basePath"] + "\\" + response["fileFormatted"], info, False, typeEntity)
                            if typeEntity == "banco":
                                fixFormat = formatInterface.fixContract()
                            else:
                                fixFormat = formatInterface.fix()


            return "finalizado el caso de uso"

        except Exception as exc:
            printExceptionInfo(exc)
            print("main")
        finally:
            print("finally main")