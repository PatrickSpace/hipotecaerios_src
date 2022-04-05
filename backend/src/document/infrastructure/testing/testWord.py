import win32com.client as win32

mydir = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\testing\\documents"

app = win32.Dispatch("Word.Application")
app.Visible = 1

document = app.Documents.Add()
myRange = document.Range(0,0)
myRange.InsertBefore('Escribiendo en documento')