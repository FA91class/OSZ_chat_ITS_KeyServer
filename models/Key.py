import json


class Key(object):
    
    def __init__(self, ID, pubKey):
        super(Key, self).__init__()

        self.ID = ID
        self.pubKey = pubKey