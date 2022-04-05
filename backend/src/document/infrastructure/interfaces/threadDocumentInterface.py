import threading
import pythoncom
import win32com.client as win32

class ThreadDocument:
    def __init__(self):
        #self.thread = start(myPath, data, info, thread_function)
        pass
    
    def start(self, myPath, data, info, thread_function):
        print("base path ", myPath)
        pythoncom.CoInitialize()
        app = win32.gencache.EnsureDispatch("Word.Application")
        print("documento entrando ", app.Name)
        app_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, app)
        argumentos = {
            "myPath": myPath, 
            "data": data,
            "info": info,
            "app_id": app_id
        }
        print("argumentos: ", argumentos, thread_function)
        thread = threading.Thread(target=thread_function, kwargs=argumentos)
        thread.start()
        thread.join()
        print("documento saliendo ", app.Name, app.Documents.Count)
        #if app.Documents.Count < 1:
        #    app.Quit(SaveChanges=-1)
        #print("termina")
        #pythoncom.CoUninitialize()

    def closeThreading(self):
        app = win32.gencache.EnsureDispatch("Word.Application")
        if app.Documents.Count < 1:
            app.Quit(SaveChanges=-1)
        print("termina")