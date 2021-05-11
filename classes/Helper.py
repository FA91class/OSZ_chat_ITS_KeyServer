import os
from models import Const


class Helper():

    def checkAndCreateDatadirectory():
        # checkt, ob es das Datenverzeichnis gibt
        try:
            if not os.path.exists(Const.directory):
                os.makedirs(Const.directory)
        except OSError:
            print('Fehler: Kann das Verzeichnis %s nicht erstellen. ' %
                  Const.directory)

    def checkIfFileExists(name):
        # gibt es die Datei "name" schon?
        try:
            if os.path.exists(Const.directory + name + '.txt'):
                return True
            else:
                return False
        except OSError:
            print('Fehler: Die ID gibt es schon: ' + Const.directory)

    def printListofIDs():
        # gibt eine Liste der vorhandenen Dateien aus
        try:
            filelist = os.listdir(Const.directory)
            return [sub.replace('.txt', '') for sub in filelist]
        except:
            print('Fehler: Das Verzeichnis lässt sich nicht lesen')

    def broadcast(msg, prefix=""):
        """ Nachricht an alle Clients """

        for sock in Const.clients:
            sock.send(bytes(prefix, "utf8") + msg)
