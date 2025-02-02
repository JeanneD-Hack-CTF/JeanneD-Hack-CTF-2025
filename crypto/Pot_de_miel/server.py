#!/usr/bin/env python3

import socketserver
import base64
import sys

from Crypto.Util.number import bytes_to_long
from flag import FLAG


HOST = "127.0.0.1"
PORT = 50001


class Factory(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


class FactoryHandler(socketserver.BaseRequestHandler):

    # Variables
    is_connected = False
    # Constants
    flag = FLAG
    hashed_admin_pass = 6966343192926317569595983766338492708381169847881721700879512706305212927745
    coef = (13 * 13) ** 37     # coef > modulus
    modulus = 2 ** 256         # fits NIST recommendations

    # Quick and simple hash function found on Internet, others
    # were to hard to implement (think about you SHA256)
    def hash_password(self, password: bytes) -> int:
        # Convert a password into an integer
        p = bytes_to_long(password)
        # Hash computation
        hashed_pwd = (p * self.coef) % self.modulus
        return hashed_pwd
    
    # Welcome !
    def welcome(self):
        banner = base64.b64decode(
            "X19fX19fX19fICAgICAgICBfX18uICAgICAgICAgICAgICAgX19fX19fX19fX18gICAgICAgICAgICAgIF9fICAgICAgICAgICAgICAg"
            "ICAgICAgICAKXF8gICBfX18gXF9fXy5fXy5cXyB8X18gICBfX19fX19fX19fXF8gICBfX19fXy9fX19fICAgIF9fX19fLyAgfF8gIF9f"
            "X19fX19fX19fIF9fXy5fXy4KLyAgICBcICBcPCAgIHwgIHwgfCBfXyBcXy8gX18gXF8gIF9fIFwgICAgX18pIFxfXyAgXCBfLyBfX19c"
            "ICAgX19cLyAgXyBcXyAgX18gPCAgIHwgIHwKXCAgICAgXF9fX1xfX18gIHwgfCBcX1wgXCAgX19fL3wgIHwgXC8gICAgIFwgICAvIF9f"
            "IFxcICBcX19ffCAgfCAoICA8Xz4gKSAgfCBcL1xfX18gIHwKXF9fX19fXyAgLyBfX19ffCB8X19fICAvXF9fXyAgPl9ffCAgXF9fXyAg"
            "LyAgKF9fX18gIC9cX19fICA+X198ICBcX19fXy98X198ICAgLyBfX19ffAogICAgICAgIFwvXC8gICAgICAgICAgXC8gICAgIFwvICAg"
            "ICAgICAgIFwvICAgICAgICBcLyAgICAgXC8gICAgICAgICAgICAgICAgICAgXC8gICAK"
        )
        self.request.send(
            "Bienvenue sur le service d'administration de la CyberFactory. Les secrets de l'usine sont bien gardés "
            "grâce à un algorithme de notre conception.\n"
            "PS: il s'agit bien évidemment du véritable et authentique service d'administration ;)\n".encode()
            + banner + b'\n'
        )

    # Menu
    def options(self):
        self.request.send(
            "\nChoisissez une option :\n"
            "\t1. Se connecter\n"
            "\t2. Afficher les secrets\n"
            "\t3. Quitter\n"
            "> ".encode()
        )

    # Login menu
    def login(self):
        self.request.send("Entrer le mot de passe administrateur : ".encode())
        password = self.request.recv(1024)[:-1]     # Trim '\n'

        # If password is valid, change user status as connected
        if (self.hash_password(password) == self.hashed_admin_pass):
            self.request.send("Vous êtes connectés !\n".encode())
            self.is_connected = True
        else:
            self.request.send("Mot de passe invalide !\n".encode())
            self.is_connected = False

    # Show flag menu
    def show_flag(self):
        # Return flag only if user is connected
        if (self.is_connected):
            self.request.send(f"Bien tenté ! Mais vous êtes tombé dans le piège de mon honeypot !\n".encode())
            self.request.send(f"En tant que lot de consolation, voici le flag : {self.flag}\n".encode())
        else:
            self.request.send("Vous n'êtes pas connectés !\n".encode())
    
    # Quit
    def quit(self):
        self.request.send("À bientôt !\n".encode())

    def handle(self):
        self.welcome()

        try:
            while True:
                # Receive user choice
                self.options()
                option = self.request.recv(1024)[:1].decode()

                if option == "1":
                    self.login()
                elif option == "2":
                    self.show_flag()
                elif option == "3":
                    self.quit()
                    break
                else:
                    self.request.send("Option invalide !\n".encode())
        except (ConnectionResetError, BrokenPipeError):
            print("Connection reset by client")



if __name__ == "__main__":
    server = Factory((HOST, PORT), FactoryHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
