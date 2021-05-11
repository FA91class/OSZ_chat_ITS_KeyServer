from http.server import BaseHTTPRequestHandler, HTTPServer
from classes.ApiServer import APIServer
from models import Const
from models import Key
import glob

class KeyAPI(BaseHTTPRequestHandler):

    def run(server_class=HTTPServer, handler_class=APIServer, port=8080):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        try:
            print("Keyserver API - Höre auf Port %s " % Const.API_PORT)
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

