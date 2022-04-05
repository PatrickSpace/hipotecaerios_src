import win32com.client as win32
import pythoncom


class Document:
    def __init__(self):
        pass

    def openApp(self, visible, app_id):
        pythoncom.CoInitialize()
        #wordApp = win32.Dispatch(
        #    pythoncom.CoGetInterfaceAndReleaseStream(app_id, pythoncom.IID_IDispatch)
        #)
        wordApp = win32.gencache.EnsureDispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(app_id, pythoncom.IID_IDispatch)
        )
        #####################################################
        wordApp.Visible = visible

        return wordApp

    def open(self, wordApp, verifiedInfo):
        filePath = verifiedInfo["filePath"]
        document = wordApp.Documents.Open(filePath)

        return document

    def close(self, document):
        #print("closing")
        document.SaveAs()
        document.Close(SaveChanges=-1)

    def closeContract(self, document, fileName):
        document.SaveAs(fileName)
        document.Close(SaveChanges=-1)