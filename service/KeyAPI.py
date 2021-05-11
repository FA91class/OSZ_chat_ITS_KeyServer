from http.server import BaseHTTPRequestHandler
import socketserver
from models import Const
from models import Key
import glob
import json

class KeyAPI(BaseHTTPRequestHandler):

    def run():
        print("Keyserver API - Höre auf Port %s " % Const.API_PORT)
        httpd = socketserver.TCPServer(("", Const.API_PORT), KeyAPI.getPublicKeys)
        httpd.serve_forever()
    
    def getPublicKeys(self):
        if self.path == '/getPublicKeys':
            keys = KeyAPI.loadKeys()
            if keys != False:
                self.send_response(200, json.dumps(keys))
            else:
                self.send_response(404, json.dumps([]))
        

    def loadKeys():
        keys = []
        try:
            for file in glob.glob(Const.directory+ '*.txt'):
    
                filename = (file.split('.')[0]).split('/')[1]

                with open(file, 'r', encoding='utf-8') as f:
                    data = f.readline()
                
                keys.append(Key(filename, data))
            
            return keys

        except:
            return False
        
            
        # try:
        #     with open(Const.directory + ID + '.txt', 'r', encoding='utf-8') as f:
        #         key = f.readline()
        # except:
        #     return False
