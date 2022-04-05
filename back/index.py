""" Autor: 
"""
from src import app
import platform
if platform.uname().node == 'EQUIPO':
    from waitress import serve
    serve(app,host="0.0.0.0",port=5544)
