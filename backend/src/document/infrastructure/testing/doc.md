# Classes
Las clases se registran con un único Id (class Id) y un program Id (ProgID). Los ProgID pueden ser "Excel.Application" o "Word.Application", y permiten crear una instancia del objeto.

Python utiliza el método win32com.client.Dispatch() para crear un objeto COM a través de un ProgID. 

> import win32com.client
> wd = win32com.client.Dispatch("Word.Application")
> wd.Visible = 0