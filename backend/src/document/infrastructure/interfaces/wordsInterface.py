import win32com.client as win32
import re
from backend.src.document.infrastructure.interfaces.text_utils import *
import pythoncom
import threading

class Words:
    def __init__(self, visible, app_id): #def __init__(self, filePath, inmobiliaria, visible, basePath, fileName, app_id):
        #self.inmobiliaria = inmobiliaria
        ## Procesa la aplicacion en otro hilo ##############
        pythoncom.CoInitialize()
        self.wordApp = win32.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(app_id, pythoncom.IID_IDispatch)
        )
        #####################################################
        self.wordApp.Visible = visible

    def fix(self, data, verifiedInfo, basePath, fileName):
        self.filePath = verifiedInfo["filePath"]
        self.basePath = basePath
        self.fileName = fileName
        self.document = self.wordApp.Documents.Open(self.filePath)
        self.paragraphs = self.document.Paragraphs
        print("parrafos: ", self.paragraphs.Count)
        self.document.Content.Font.AllCaps = True
        for key in data.keys():
            self.document.Content.Find.Execute(FindText=data[key][0], ReplaceWith=data[key][1], Replace=2)
        self.document.Content.Font.Bold = False
        self.document.Content.Font.Italic = False
        self.document.Content.Font.ColorIndex = 1
        self.document.Content.Underline = 0
        self.document.Content.Font.Name = "Anonymous"
        self.document.Content.Font.Size = 8
        spaces = [" "*2, " "*3, " "*4]
        for space in spaces:
            self.document.Content.Find.Execute(FindText=space, ReplaceWith=" ", Replace=2)
        self.closeDocument()
        print("documento cerrado")

        return verifiedInfo

    def closeDocument(self):
        if re.search(r'.rtf$', self.fileName): #".rtf" in self.fileName:
            #self.document.SaveAs2(self.basePath + "\\" + self.fileName.split(".rtf")[0]+"-format.rtf")
            self.document.SaveAs(self.basePath + "\\" + self.fileName.split(".rtf")[0]+"-format.rtf")
            print("documento salvado")
        elif re.search(r'.doc$', self.fileName): #".doc" in self.fileName:
            #self.document.SaveAs2(self.basePath + "\\" + self.fileName.split(".doc")[0]+"-format.doc")
            self.document.SaveAs(self.basePath + "\\" + self.fileName.split(".doc")[0]+"-format.doc")
        elif re.search(r'.docx$', self.fileName): #".docx" in self.fileName:
            #self.document.SaveAs2(self.basePath + "\\" + self.fileName.split(".docx")[0]+"-format.docx")
            self.document.SaveAs(self.basePath + "\\" + self.fileName.split(".docx")[0]+"-format.docx")