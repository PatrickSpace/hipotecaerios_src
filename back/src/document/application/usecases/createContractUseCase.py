from backend.src.document.infrastructure.middlewares.printExceptionInfo import *

class CreateContractUseCase:
    def __init__(self, threadInterface, renamePathInterface, document, contract, comparecientes, exceptionsFunctions):
        self.threadInterface = threadInterface
        self.renamePathInterface = renamePathInterface
        self.document = document
        self.contract = contract
        self.comparecientes = comparecientes
        self.exceptionsFunctions = exceptionsFunctions
        self.responseMain = None
        pass

    def execute(self, dirName, basePath):
        try:
            print("arreglar documento", dirName, basePath)
            argumentos = {
                "myPath": dirName,
                "basePath": basePath
            }
            self.threadInterface.startCreate(argumentos, self.main)
            return self.responseMain
        except Exception as exc:
            printExceptionInfo(exc)
            #print(exc)
        finally:
            self.threadInterface.closeThreading()
            print("finally")

    def main(self, myPath, basePath, app_id):
        try:
            print("try", myPath)
            documentos = self.renamePathInterface.extractFormatted(myPath)
            wordApp = self.document.openApp(False, app_id)
            self.app = wordApp
            self.renamePathInterface.copyBase(basePath, myPath)
            if documentos["minuta"] != [] or documentos["clausula"] != [] or documentos["banco"] != []:
                baseDoc = myPath + "\\base.DOC"
                verifiedInfo = {"filePath": baseDoc}
                document_ = self.document.open(wordApp, verifiedInfo)
                self.doc = document_
                comparecientes_ = self.comparecientes.getComparecientes(myPath)
                contractName = myPath +'\\KR-'+str(comparecientes_['kardex'])+'.doc'
                self.contName = contractName
                self.contract.first_part(document_, "USUARIO", comparecientes_)
                self.contract.second_part(document_)
                self.contract.third_part(document_, comparecientes_)
                for i in range(len(documentos["minuta"])):
                    isTitulo = True if i == 0 else False
                    self.contract.minuta(wordApp, document_, myPath, documentos["minuta"][i], isTitulo)
                for i in range(len(documentos["clausula"])):
                    self.contract.clausula_adicional(wordApp, document_, myPath, documentos["clausula"][i])
                    pass
                for i in range(len(documentos["banco"])):
                    self.contract.contrato(wordApp, document_, myPath, documentos["banco"][i])
                    pass

                self.contract.last_inserto(document_)

                self.contract.remove_first_line(document_)

                self.document.closeContract(document_, contractName)

            print(documentos)
            self.responseMain = {
                "mensaje": "Documento creado!"
            }
        except Exception as exc:
            printExceptionInfo(exc)
            if self.doc and self.contName:
                self.document.closeContract(self.doc, self.contName)
                if exc["type"] == "AttributeError":
                    self.exceptionsFunctions.run_clean()
            print("main")
        finally:
            print("finally")
