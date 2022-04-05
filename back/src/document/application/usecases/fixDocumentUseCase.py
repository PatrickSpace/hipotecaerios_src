from backend.src.document.infrastructure.middlewares.printExceptionInfo import *

class FixDocumentUseCase:
    def __init__(self, threadInterface, renamePathInterface, document, words, format_, clausula, sections, extendDate, company, comparecientes, exceptionsFunctions):
        self.threadInterface = threadInterface
        self.renamePathInterface = renamePathInterface
        self.document = document
        self.words = words
        self.format = format_
        self.clausula = clausula
        self.sections = sections
        self.extendDate = extendDate
        self.company = company
        self.comparecientes = comparecientes
        self.exceptionsFunctions = exceptionsFunctions
        self.responseMain = None

    def execute(self, myPath, entidades):
        try:
            print("arreglar documento")
            self.threadInterface.start(myPath, entidades, self.main)
            return self.responseMain
        except Exception as exc:
            printExceptionInfo(exc)
            #print(exc)
        finally:
            self.threadInterface.closeThreading()
            print("finally")

    def main(self, myPath, entidades, app_id):
        basePath = myPath
        try:
            documentos = self.renamePathInterface.extract(basePath)
            wordApp = self.document.openApp(False, app_id)
            self.app = wordApp
            for typeDoc in documentos.keys(): # ==> ["minuta", "clausula", "banco"]
                if documentos[typeDoc] != []: #typeDoc != []:
                    for fileName in documentos[typeDoc]:
                        verifiedInfo = self.renamePathInterface.verifyExistence(basePath, fileName)
                        if not verifiedInfo["isPathFormatted"]:
                            document_ = self.document.open(wordApp, verifiedInfo)
                            self.doc = document_ ## Para colocar en finally
                            fileName, basePath, responseVerified = self.words.estandarizar(document_, verifiedInfo, basePath, fileName)
                            self.words.saveFormatDocument(document_, fileName, basePath)
                            print("no esta formateado", verifiedInfo, responseVerified, "22255")

                            self.format.modify_tables(document_)###
                            if "banco" in responseVerified["fileFormatted"]:
                                typeEntity = "banco"
                            else:
                                typeEntity = "inmobiliaria"
                            
                            if typeEntity == "banco":
                                self.format.remove_shapes(document_)
                                ###self.format.modify_tables(document_)
                            self.format.cutPasteSpecial(document_)
                            self.format.basics(document_)
                            self.format.remove_lists(document_)
                            self.clausula.format(document_)
                            # Formatear caso especial (scotiabank)
                            ###self.format.removeEmptyParagraph(document_) ##
                            self.format.general_format(document_)
                            self.format.standardColon(document_)
                            self.extendDate.execute(document_) ##
                            # Definir secciones del documento
                            ## Sec 1 -> preambulo, sec 2 -> clausulas, sec 3 -> anexos, clausula ad
                            self.sections.define(document_) # paino, clausula, anex
                            print("Cuenta secciones: ", document_.Sections.Count)
                            self.clausula.formatClausaAdicional(document_)
                            self.clausula.formatAnexos(document_)
                            #self.sections.sectionClausulaFormat(document_)
                            # agregar notario a minuta de inmobiliaria (primera linea)
                            # borrar notario a banco (primera linea)
                            # extraer comparecientes de bancos: interbank, scotia y bcp
                            # borrar firmantes
                            # agregar firmantes

                            if typeEntity == "banco":
                                print("es banco")
                                bancoNombre = self.company.detect(document_, typeEntity)
                                clientes = self.comparecientes.extraerClientes(document_, bancoNombre)
                                representantesBanco = self.comparecientes.extraerRepresentantesBanco(document_, bancoNombre)
                                self.comparecientes.saveInFileBanco(bancoNombre, clientes, representantesBanco, basePath)
                                print(bancoNombre)
                                if bancoNombre == "SCOTIABANK PERU S.A.A." or bancoNombre == "BANCO BBVA PERU":
                                    self.clausula.formatTitulosScottia(document_)
                                #fixFormat = formatInterface.fixContract()
                            elif typeEntity == "inmobiliaria":
                                print("es inmobiliaria")
                                #fixFormat = formatInterface.fix()
                                inmobiliariaNombre = self.company.detect(document_, typeEntity)
                                representantesInmo = []
                                self.comparecientes.saveInFileInmo(inmobiliariaNombre, representantesInmo, basePath)
                                print("sale de inmobiliaria")

                            self.format.remove_at_beginning_of_paragraph(document_) ##

                            self.format.standardColon(document_)### PARA REMOVER DOS PUNTOS SUBRAYADOS.

                            self.sections.eliminarFirmantes(document_)

                            self.sections.remove(document_)

                            self.document.close(document_)

        except Exception as exc:
            printExceptionInfo(exc)
            if self.doc:
                self.doc.SaveAs()
                self.doc.Close(SaveChanges=-1)
                if type(exc).__name__ == "AttributeError":
                    self.exceptionsFunctions.run_clean()
            #print("main exc")
        finally:
            #self.document.close(document_)
            print("finally main")
            #if self.doc:
            #    self.doc.SaveAs()
            #    self.doc.Close(SaveChanges=-1)