from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
#cors = CORS(app, origins = '*', headers = ['Content-Type', 'Authorization'], expose_headers='Authorization', methods=['GET','POST','DELETE'])
cors = CORS(app, origins = '*')#, origins = '*', methods=[GET, POST, DELETE])
app.config['CORS_HEADERS'] = ['Content-Type']
#app.config['UPLOAD_FOLDER'] = "C:\\Users\\Alejandro Herrera\\Documents"
app.config['UPLOAD_FOLDER'] = "D:\\bot-hip\\back"
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024

print("en init back")
from src.document.infrastructure.routes import document_routes
