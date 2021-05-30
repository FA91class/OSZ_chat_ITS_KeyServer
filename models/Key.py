import json


class Key(object):
    
    def __init__(self, id, pubKey):
        super(Key, self).__init__()

        self.id = id
        self.pubKey = pubKey