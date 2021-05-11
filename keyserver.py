#!/usr/bin/env python3
""" einfacher Server zum Hinterlegen der RSA Schlüssel """
import socket
import threading
from classes import Helper
from threading import Thread
from models import Const
from socket import AF_INET, socket, SOCK_STREAM

def accept_incoming_connections():
        """ Eingehende Verbindungen"""
        while True:
            client, client_address = SERVER.accept()
            print("%s:%s ist verbunden." % client_address)
            client.send(
                bytes("Grüße vom keyserver! Gib Deine ID ein und drücke 'Enter'!", "utf8"))
            Const.addresses[client] = client_address
            threading(target=Helper.handle_client, args=(client,)).start()


def handle_client(client):  
    """ Für den ersten Dialog mit einem einzelnen Client """

    welcome = ""

    name = client.recv(Const.BUFSIZ).decode("utf8").replace("\n", "")

    welcome = "\nWillkommen %s!\nDu hast folgende Möglichkeiten:\n\n" \
            "speichere <publickey>\nspeichert Deinen öffentlichen Schlüssel unter Deiner ID ab.\n\n" \
            "zeige <ID>\nsendet den öffentlichen Schlüssel für die ID <ID>.\n\n" \
            "liste \nlistet alle vorhandenen IDs auf.\n\n" \
            "###q###\ntrennt die Verbindung zum Keyserver\n" % name


    client.send(bytes(welcome, "utf8"))
    msg = "%s hat sich am keyserver angemeldet!" % name
    print(msg)
    # broadcast(bytes(msg, "utf8"))
    Const.clients[client] = name

    while True:
        try:
            msg = client.recv(Const.BUFSIZ)
            msg = msg.decode()

            # alle Möglichkeiten durchgehen
            if "speichere" in msg:

                #print (msg)
                ID, key = msg[:9],msg[10:]
                key = key.strip()
                print("ID = %s, key = %s" % (ID, key))
                # speichere key unter ID.txt ab:
                with open(Const.directory + name + '.txt', 'w', encoding='utf-8') as f:
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
                    with open(Const.directory + ID + '.txt', 'r', encoding='utf-8') as f:
                        key = f.readline()
                        client.send(bytes(key, "utf8"))
                except:
                    client.send(bytes("Die ID '%s' ist nicht vorhanden" % ID, "utf8"))

                continue

            elif "liste" in msg:
                Helper.printListofIDs()
                IDs = Helper.printListofIDs()
                client.send(bytes("\n".join(IDs), "utf8"))
                continue
            elif "###q###" in msg:
                client.send(bytes("quit", "utf8"))
                client.close()
                del Const.clients[client]
                print("%s hat sich vom Keyserver abgemeldet." % name)
                break
            client.send(bytes("unbekanntes Kommando", "utf8"))
        except:
            print("Verbindung wurde unterbrochen")
            break


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(Const.ADDR)

if __name__ == "__main__":
    """ Datenverzeichnis checken und wenn nicht vorhanden anlegen. Keyfiles werden als txt-Datei abgelegt."""
    Helper.Helper.checkAndCreateDatadirectory()
    SERVER.listen(25)
    print("Keyserver - Höre auf Port %s " % Const.PORT)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
