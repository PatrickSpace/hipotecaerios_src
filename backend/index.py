""" Autor: 
"""
from src import app
import platform
if platform.uname().node == 'EQUIPOo':
    from waitress import serve
    serve(app, port=5544)