import win32com.client as win32
import re
from backend.src.document.infrastructure.interfaces.text_utils import *
import pythoncom
import threading

from back.src.libs.database import rules

class Words:
    def __init__(self):#, visible, app_id):
        """## Procesa la aplicacion en otro hilo ##############
        pythoncom.CoInitialize()
        self.wordApp = win32.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(app_id, pythoncom.IID_IDispatch)
        )
        #####################################################
        self.wordApp.Visible = visible"""
        pass

    def estandarizar(self, document, verifiedInfo, basePath, fileName):
        filePath = verifiedInfo["filePath"]
        ##document = self.wordApp.Documents.Open(filePath)
        paragraphs = document.Paragraphs
        data = rules()
        document.Content.Font.AllCaps = True
        for key in data.keys():
            #m=document.Content.Find.Execute(FindText=data[key][0], ReplaceWith=data[key][1], Replace=2)
            document.Content.Find.Execute(FindText=data[key][0], ReplaceWith=data[key][1], Replace=2)
        document.Content.Font.Bold = False
        document.Content.Font.Italic = False
        document.Content.Font.ColorIndex = 1
        document.Content.Underline = 0
        document.Content.Font.Name = "Anonymous"
        document.Content.Font.Size = 8
        spaces = [" "*2, " "*3, " "*4]
        for space in spaces:
            document.Content.Find.Execute(FindText=space, ReplaceWith=" ", Replace=2)
        #self.closeDocument(document, fileName, basePath)

        #return verifiedInfo
        return fileName, basePath, verifiedInfo

    def saveFormatDocument(self, document, fileName, basePath):
        if re.search(r'.rtf$', fileName): #".rtf" in self.fileName:
            #self.document.SaveAs2(self.basePath + "\\" + self.fileName.split(".rtf")[0]+"-format.rtf")
            document.SaveAs(basePath + "\\" + fileName.split(".rtf")[0]+"-format.rtf")
        elif re.search(r'.doc$', fileName): #".doc" in self.fileName:
            #self.document.SaveAs2(self.basePath + "\\" + self.fileName.split(".doc")[0]+"-format.doc")
            document.SaveAs(basePath + "\\" + fileName.split(".doc")[0]+"-format.doc")
        elif re.search(r'.docx$', fileName): #".docx" in self.fileName:
            #self.document.SaveAs2(self.basePath + "\\" + self.fileName.split(".docx")[0]+"-format.docx")
            document.SaveAs(basePath + "\\" + fileName.split(".docx")[0]+"-format.docx")