#!/usr/bin/env python3
""" einfacher Server zum Hinterlegen der RSA Schlüssel """
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os

"""globals"""
directory = './data/'

def checkAndCreateDatadirectory():
    # checkt, ob es das Datenverzeichnis gibt
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Fehler: Kann das Verzeichnis %s nicht erstellen. ' % directory)

def checkIfFileExists(name):
    # gibt es die Datei "name" schon?
    try:
        if os.path.exists(directory + name + '.txt'):
            return True
        else:
            return False
    except OSError:
        print('Fehler: Die ID gibt es schon: ' + directory)

def printListofIDs():
    # gibt eine Liste der vorhandenen Dateien aus
    try:
        filelist = os.listdir(directory)
        return [sub.replace('.txt', '') for sub in filelist]
    except:
        print('Fehler: Das Verzeichnis lässt sich nicht lesen')


def accept_incoming_connections():
    """ Eingehende Verbindungen"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s ist verbunden." % client_address)
        client.send(bytes("Grüße vom keyserver! Gib Deine ID ein und drücke 'Enter'!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  
    """ Für den ersten Dialog mit einem einzelnen Client """

    welcome = ""

    name = client.recv(BUFSIZ).decode("utf8").replace("\n", "")

    welcome = "\nWillkommen %s!\nDu hast folgende Möglichkeiten:\n\n" \
              "speichere <publickey>\nspeichert Deinen öffentlichen Schlüssel unter Deiner ID ab.\n\n" \
              "zeige <ID>\nsendet den öffentlichen Schlüssel für die ID <ID>.\n\n" \
              "liste \nlistet alle vorhandenen IDs auf.\n\n" \
              "###q###\ntrennt die Verbindung zum Keyserver\n" % name


    client.send(bytes(welcome, "utf8"))
    msg = "%s hat sich am keyserver angemeldet!" % name
    print(msg)
    # broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        try:
            msg = client.recv(BUFSIZ)
            msg = msg.decode()

            # alle Möglichkeiten durchgehen
            if "speichere" in msg:

                #print (msg)
                ID, key = msg[:9],msg[10:]
                key = key.strip()
                print("ID = %s, key = %s" % (ID, key))
                # speichere key unter ID.txt ab:
                with open( directory + name + '.txt','w', encoding='utf-8') as f:
                    f.write(key)

                client.send(bytes("gespeichert", "utf8"))
                continue

            elif "zeige" in msg:
                dummy, ID = msg[:5],msg[6:]

                # die ID muss gestripped werden
                ID = ID.strip()
                print("ID = %s, dummy = %s" % (ID, dummy))
                # hole key aus ID.txt:
                key = ''
                try:
                    with open(directory + ID + '.txt', 'r', encoding='utf-8') as f:
                        key = f.readline()
                        client.send(bytes(key, "utf8"))
                except:
                    client.send(bytes("Die ID '%s' ist nicht vorhanden" % ID, "utf8"))

                continue

            elif "liste" in msg:
                printListofIDs()
                IDs = printListofIDs()
                client.send(bytes("\n".join(IDs), "utf8"))
                continue
            elif "###q###" in msg:
                client.send(bytes("quit", "utf8"))
                client.close()
                del clients[client]
                print("%s hat sich vom Keyserver abgemeldet." % name)
                break
            client.send(bytes("unbekanntes Kommando", "utf8"))
        except:
            print("Verbindung wurde unterbrochen")
            break


def broadcast(msg, prefix=""):
    """ Nachricht an alle Clients """

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 65267
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    """ Datenverzeichnis checken und wenn nicht vorhanden anlegen. Keyfiles werden als txt-Datei abgelegt."""
    checkAndCreateDatadirectory()
    SERVER.listen(25)
    print("Keyserver - Höre auf Port %s " % PORT)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()






