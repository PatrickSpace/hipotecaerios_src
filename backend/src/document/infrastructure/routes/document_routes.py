import platform
if platform.uname().node == 'EQUIPO':
    syspath = "D:\\bot-hip"
    path = "D:\\Archivos-bot-hip"
    basePath = "D:\\bot-hip\\backend\\src\\libs\\base.DOC"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip"
    path = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"
    basePath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\base.DOC"

import sys
sys.path.append(syspath)

from flask import jsonify, request, Response
from flask_restful import Resource, Api, reqparse
import os
import shutil
import json
from werkzeug.utils import secure_filename

from backend.src.document.infrastructure.controllers import document_controller
from backend.src.document.infrastructure.controllers import fixDocumentController
from backend.src.document.infrastructure.middlewares.convertSpecialCharacter import convertSpecialCharacter
from src import app
print("dir", app.config['UPLOAD_FOLDER'])

# rutas GET y POST de la API.
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('document')

def uploadFiles(upload_files):
    """ Se cargan todos los documentos en un carpeta con el numero
        de kardex.
        Retorna el directorio donde se guardan los documentos.
    """
    file_keys = list(upload_files.keys())
    F = upload_files[file_keys[0]]
    filename = secure_filename(F.filename)
    kardex = filename.split("-")[0]
    #path = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"
    dirName = path + "\\" + kardex
    firmantesPath = dirName + "\\data.json"
    data = {"kardex": int(kardex)}
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        with open(firmantesPath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Directory " , dirName ,  " Created ")
    else:
        if not os.path.exists(firmantesPath):
            with open(firmantesPath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        print("Directory " , dirName ,  " already exists")
    #print("kardex", kardex)
    
    print("file keys: ", file_keys)
    for file_key in file_keys:
        F = upload_files[file_key]
        filename = secure_filename(F.filename)
        print(F.filename, filename)
        kardex = filename.split("-")[0]
        #path = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"
        path_file = os.path.join(dirName, filename)
        if not os.path.isfile(path_file):
            F.save(path_file)

    return dirName

"""def convertSpecialCharacter(data):
    for item in range(len(data["comparecientes"])):
        for key in data["comparecientes"][item].keys():
            data["comparecientes"][item][key] = data["comparecientes"][item][key].replace("Ã‘", "Ñ")
            data["comparecientes"][item][key] = data["comparecientes"][item][key].replace("Â°", "°")
    for key in data["banco"].keys():
        data["banco"][key] = data["banco"][key].replace("Ã‘", "Ñ")
        data["banco"][key] = data["banco"][key].replace("Â°", "°")
    for key in data["inmobiliaria"].keys():
        data["inmobiliaria"][key] = data["inmobiliaria"][key].replace("Ã‘", "Ñ")
        data["inmobiliaria"][key] = data["inmobiliaria"][key].replace("Â°", "°")

    return data
"""
class hola(Resource):
    def get(self):
        print("hola")
        return {'hola': 'Aplicacion bot hipotecario'}

    def post(self):
        print("hola post")
        body = request.data
        print(body)

class FixMinutaRoute(Resource):
    def post(self):
        print("posting")
        upload_files = request.files
        #print(request.headers)
        #print(upload_files)
        params = request.args
        #print("params ", request.args, params.get("banco"))
        dirName = uploadFiles(upload_files)
        rules = document_controller.inputCont()
        info = {
            "banco": params.get("banco"),#"bcp",#"scotiaBank",
            "inmobiliaria": params.get("inmobiliaria")#"alcanfores"
        }
        document_controller.start_fixD_threading(dirName, rules, info)
        shutil.copy2(dirName+'\\data.json', dirName+'\\comparecientes.json')
        with open(dirName+'\\data.json') as f:
            dataOut = json.load(f)
        return jsonify(dataOut)

class EditComparecientes(Resource):    
    def post(self): #put -->
        body = request.get_json()
        comp = document_controller.editSignersController(body)
        return jsonify(comp)

class GenerarDocumento(Resource):
    def post(self):
        data = request.get_json()
        print("body: ", data)
        dirName = path + "\\" + data["kardex"]
        document_controller.start_Document_threading(dirName, basePath)
        print("generando")
        return jsonify({"mensaje": "Documento generado"})

class testing(Resource):
    def post(self):
        print("testing")
        upload_files = request.files
        params = request.args
        dirName = uploadFiles(upload_files)
        rules = document_controller.inputCont()
        info = {
            "banco": params.get("banco"),#"bcp",#"scotiaBank",
            "inmobiliaria": params.get("inmobiliaria")#"alcanfores"
        }
        fixDocumentController.fixDocument(dirName, rules, info)
        shutil.copy2(dirName+'\\data.json', dirName+'\\comparecientes.json')
        with open(dirName+'\\data.json', encoding='utf-8') as f:
            dataOut = json.load(f)
        #print("data out: ", dataOut)
        dataOut_ = convertSpecialCharacter(dataOut)
        #print(dataOut_)
        return jsonify(dataOut_)
        

api.add_resource(hola, "/api/bothip/hola")
#api.add_resource(FixMinutaRoute, "/api/bothip/documentacion")
api.add_resource(EditComparecientes, "/api/bothip/comparecientes")
api.add_resource(GenerarDocumento, "/api/bothip/generar")
api.add_resource(testing, "/api/bothip/documentacion")