import glob
from http.server import BaseHTTPRequestHandler
import json
import os
from models.Key import Key
from urllib.parse import parse_qs, urlparse
from models import Const

class APIServer(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def _data_response(self, data):
        return bytearray(json.dumps(data), encoding= "utf-8")

    def loadKeys():
        keys = []
        for file in glob.glob(Const.directory + '*.txt'):
    
                filepath = os.path.basename(file)
                filename = filepath.split('.')[0]

                with open(file, 'r', encoding='utf-8') as f:
                    data = f.readline()

                keys.append(Key(filename, data).__dict__)

        return keys

    def do_GET(self):

        if str.startswith(self.path, "/getPublicKeys"):

            keys = APIServer.loadKeys()

            if keys:
                self._set_response()
                self.wfile.write(self._data_response(keys))
            else:
                self.send_response(404, json.dumps('[]'))

        if str.startswith(self.path, "/getPublicKeyById"):

            try:
                parsed = urlparse(self.path)
                searchId = parse_qs(parsed.query)['id'][0]
            except:
                self.send_response(404, json.dumps('[]'))
                return

            keys = APIServer.loadKeys()

            if keys:

                for key in keys:

                    if key["ID"] == searchId:
                        self._set_response()
                        self.wfile.write(self._data_response(key))
                        return;
                        
                    self.send_response(404, json.dumps('{}'))

            else:
                self.send_response(404, json.dumps([]))


    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)
 
        if self.path == '/setPublicKey':
            
            try:
                string = post_data.decode("utf-8")
                jsonData = json.loads(string)
                key = Key(jsonData['id'], jsonData['pubKey'])
                self._set_response()
            except:
                self.send_response(404)
                return;

            with open(Const.directory + key.ID + '.txt', 'w', encoding='utf-8') as f:
                f.write(key.pubKey)
