#!/usr/bin/python3

import re
import signal
import socket
import subprocess
import sys

from _thread import *
from datetime import datetime

from flag import FLAG


WELCOME = """Bienvenue, ce service permet de vérifier si votre clé privée respecte nos conventions.
                Relatively Secret Agency, le style avant la sécurité !
"""

DESCRIPTION = """
Votre clé doit être une clé privée RSA au format PEM.
Elle doit contenir les header et footer d'une clé OpenSSL, c'est-à-dire :
-----BEGIN PRIVATE KEY-----     ou      -----BEGIN RSA PRIVATE KEY-----
-----END PRIVATE KEY-----       ou      -----END RSA PRIVATE KEY-----

Entrer la clé à vérifier :
"""

# Server and socket logic
SOCKET_HOST = "0.0.0.0"
SOCKET_PORT = 50002


# Helper to write server logs
class Logger():

    def __init__(self, outfile: str=None):
        self.outfile = open(outfile, 'a') if outfile else None

    def info(self, msg):
        if self.outfile:
            self.outfile.write(f"\n[{datetime.now()}] {msg}")
        else:
            print(f"[{datetime.now()}] {msg}")

    def close(self):
        self.outfile.close()


# Handle clients connections and check the sumbmitted key
def client_handler(connection, client):
    connection.send(WELCOME.encode())

    try: 
        connection.send(DESCRIPTION.encode())

        msg = ""
        while not re.search("-----END( RSA)? PRIVATE KEY-----", msg):
            msg += connection.recv(1024).decode()

        filename = f"key-{datetime.now().timestamp()}.pem"
        with open(filename, 'w') as key:
            key.write(msg)

        check = subprocess.run(["./check.sh", filename])

        if check.returncode == 0:
            connection.send(f"\nFélicitations ! Voici le flag : {FLAG}\n".encode())
        else:
            connection.send(f"\nDommage, votre clé manque de style !\n".encode())

        subprocess.run(["rm", filename])

    except (ConnectionResetError, BrokenPipeError):
        log.info(f"Client {client} closed connection")

    connection.close()


# Accept a connection to the server and start a new thread
def accept_connections(socket_server):
    conn, address = socket_server.accept()
    client = f"{address[0]}:{address[1]}"
    log.info(f"Connection from: {client}")
    start_new_thread(client_handler, (conn, client))


# Handle Ctrl+C
def handler(signum, frame):
    log.info("Ctrl+C received: stopping the server")
    log.close()
    sys.exit(0)


# Start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SOCKET_HOST, SOCKET_PORT))
    server.listen(5)

    log.info("Jeanned'Hack CTF - PEMp My Key ! - Check key server")
    log.info(f"Server start listening at: {SOCKET_HOST}:{SOCKET_PORT}")
    signal.signal(signal.SIGINT, handler)

    while True:
        accept_connections(server)

    log.info("Server stop")


if __name__ == "__main__":
    # Define a global logger
    logfile = f"pemp_my_key-{datetime.now().strftime('%Y-%m-%d')}.log"
    log = Logger(logfile)

    start_server()

    log.close()
