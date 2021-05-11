import glob
from http.server import BaseHTTPRequestHandler
import json
from models.Key import Key
from urllib.parse import urlparse
from models import Const

class APIServer(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def loadKeys():
        keys = []
        for file in glob.glob(Const.directory + '*.txt'):
    
                filename = (file.split('.')[0]).split('/')[1]

                with open(file, 'r', encoding='utf-8') as f:
                    data = f.readline()

                keys.append(Key(filename, data))

        return keys

    def do_GET(self):

        self._set_response()

        if self.path == '/getPublicKeys':

            keys = APIServer.loadKeys()

            if keys:
                self.send_response(200, json.dumps(keys))
            else:
                self.send_response(404, json.dumps('[]'))

        if self.path == '/getPublicKey':

            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
            except:
                self.send_response(404, json.dumps('[]'))
                return

            keys = APIServer.loadKeys()
            searchId = query_components["id"]

            if keys:

                for key in keys:

                    if key.ID == searchId:
                        self.send_response(200, json.dumps(key))
                    else:
                        self.send_response(404, json.dumps('{}'))

            else:
                self.send_response(404, json.dumps([]))

        if self.path == '/setPublicKey':
            self._set_headers
            name = self

            with open(Const.directory + name + '.txt', 'w', encoding='utf-8') as f:
                f.write(key)

    def do_POST(self):
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself
        post_data = self.rfile.read(content_length)

        self._set_response()
        self.wfile.write("POST request for {}".format(
            self.path).encode('utf-8'))
