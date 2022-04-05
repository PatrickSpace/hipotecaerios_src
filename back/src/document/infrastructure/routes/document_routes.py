import platform
from src.libs.config import archivos

files = archivos()
if platform.uname().node == 'EQUIPO':
    syspath = files["routesSys"]["syspath"] #"D:\\bot-hip"
    path = files["routesSys"]["path"]#"D:\\Archivos-bot-hip"
    basePath = files["routesSys"]["basePath"]#"D:\\bot-hip\\back\\src\\libs\\base.DOC"
else:
    syspath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip"
    path = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"
    basePath = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\back\\src\\libs\\base.DOC"

import sys
sys.path.append(syspath)

from flask import jsonify, request, Response
from flask_restful import Resource, Api, reqparse
import os
import shutil
import json
from werkzeug.utils import secure_filename

from back.src.document.infrastructure.controllers import document_controller
from back.src.document.infrastructure.controllers import fixDocumentController
from back.src.document.infrastructure.controllers import createDocumentController
from back.src.document.infrastructure.controllers import createComparecienteController
from back.src.document.infrastructure.middlewares.convertSpecialCharacter import convertSpecialCharacter
from src import app


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
    else:
        if not os.path.exists(firmantesPath):
            with open(firmantesPath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
    for file_key in file_keys:
        F = upload_files[file_key]
        filename = secure_filename(F.filename)
        kardex = filename.split("-")[0]
        #path = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores"
        path_file = os.path.join(dirName, filename)
        if not os.path.isfile(path_file):
            F.save(path_file)

    return dirName

class hola(Resource):
    def get(self):
        return {'hola': 'Aplicacion bot hipotecario'}

    def post(self):
        body = request.data

class FixMinutaRoute(Resource):
    def post(self):
        print("posting")
        upload_files = request.files
        params = request.args
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

class GenerarDocumento2(Resource):
    def post(self):
        data = request.get_json()
        dirName = path + "\\" + data["kardex"]
        document_controller.start_Document_threading(dirName, basePath)
        print("generando")
        return jsonify({"mensaje": "Documento generado"})

class GenerarDocumento(Resource):
    def post(self):
        data = request.get_json()
        if not data["kardex"]:
            return jsonify({"mensaje": "No se cargo un Kardex"})
        else:
            dirName = path + "\\" + data["kardex"]
            #document_controller.start_Document_threading(dirName, basePath)
            createDocumentController.createDocument(dirName, basePath)
            print("generando")
            return jsonify({"mensaje": "Documento generado"})

class testing(Resource):
    def post(self):
        upload_files = request.files
        params = request.args
        dirName = uploadFiles(upload_files)
        #rules = document_controller.inputCont()
        info = {
            "banco": params.get("banco"),#"bcp",#"scotiaBank",
            "inmobiliaria": params.get("inmobiliaria")#"alcanfores"
        }
        print(upload_files, params, dirName, info)
        fixDocumentController.fixDocument(dirName, info)
        shutil.copy2(dirName+'\\data.json', dirName+'\\comparecientes.json')
        with open(dirName+'\\data.json', encoding='utf-8') as f:
            dataOut = json.load(f)
        return jsonify(dataOut)

class CreateCompareciente(Resource):
    def get(self):
        return {'mensaje': 'get de prueba'}
    def post(self):
        body = request.get_json()
        #print(body, "--- path", path)
        output = body
        output = createComparecienteController.createCompareciente(body, path)
        return jsonify(output)
        

api.add_resource(hola, "/api/bothip/hola")
#api.add_resource(FixMinutaRoute, "/api/bothip/documentacion")
api.add_resource(EditComparecientes, "/api/bothip/comparecientes")
api.add_resource(GenerarDocumento, "/api/bothip/generar")
api.add_resource(testing, "/api/bothip/documentacion")
api.add_resource(CreateCompareciente, "/api/bothip/crear-compareciente")