import threading
import pythoncom
import win32com.client as win32

class ThreadDocument:
    def __init__(self):
        pass
    
    def start(self, myPath, entidades, thread_function):
        """ Comienza el procesamiento de una funcion en un hilo.
            myPath: Directorio de trabajo
            entidades: nombre de banco y/o inmobiliaria
            thread_function: funcion que se ejecutara en el hilo
        """
        pythoncom.CoInitialize()
        app = win32.Dispatch("Word.Application")#app = win32.gencache.EnsureDispatch("Word.Application")
        print("documento entrando ", app.Name)
        app_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, app)
        argumentos = {
            "myPath": myPath, 
            "entidades": entidades,
            "app_id": app_id
        }
        print("argumentos: ", argumentos, thread_function)
        thread = threading.Thread(target=thread_function, kwargs=argumentos)
        thread.start()
        thread.join()
        print("documento saliendo ", app.Name, app.Documents.Count)

    def startCreate(self, argumentos, thread_function):
        """ Comienza el procesamiento de una funcion en un hilo.
            thread_function: funcion que se ejecutara en el hilo
        """
        pythoncom.CoInitialize()
        app = win32.Dispatch("Word.Application")#app = win32.gencache.EnsureDispatch("Word.Application")
        print("documento entrando ", app.Name)
        app_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, app)
        argumentos.update({"app_id": app_id})
        print("argumentos: ", argumentos, thread_function)
        thread = threading.Thread(target=thread_function, kwargs=argumentos)
        thread.start()
        thread.join()
        print("documento saliendo ", app.Name, app.Documents.Count)

    def closeThreading(self):
        app = win32.Dispatch("Word.Application")#app = win32.gencache.EnsureDispatch("Word.Application")
        if app.Documents.Count < 1:
            app.Quit(SaveChanges=-1)
        print("termina")