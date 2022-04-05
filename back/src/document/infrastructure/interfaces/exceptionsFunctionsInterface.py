import subprocess

class ExceptionsFunctionsInterface:
    def __init__(self):
        pass

    def run_clean(self): 
        return subprocess.run( ["powershell", "-Command", "Remove-Item -path $env:LOCALAPPDATA\Temp\gen_py -recurse"]) 
