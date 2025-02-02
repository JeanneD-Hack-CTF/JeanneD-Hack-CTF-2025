#!/usr/bin/env python3

import socketserver
import sys
from hashlib import sha1
from ctypes import c_int32
from secret import SEED, FLAG
 
HOST = "0.0.0.0"
PORT = 50003

def int32_t(x: int) -> int:
    """ Return the given value casted as a int32 types """
    return c_int32(x).value

class Random(object):
    
    def __init__(self):
        self.state = [0] * 32
        self.fptr = 0
        self.rptr = 0

    def srand(self, seed: int) -> None:
        """ Seed this random number generator """
        
        # We must make sure the seed is not 0.  Take arbitrarily 1 in this case. 
        if seed == 0:
            seed = 1

        self.state[0] = int32_t(seed)
        dst = 0
        word = int32_t(seed)
        kc = 31
        for i in range(kc):
            # This does:
            #   state[i] = (16807 * state[i - 1]) % 2147483647;
            # but avoids overflowing 31 bits. 
            hi = int32_t(word // 127773)
            lo = int32_t(word % 127773)
            word = int32_t(16807 * lo - 2836 * hi)
            if word < 0:
                word = int32_t(word + 2147483647)

            dst += 1
            self.state[dst] = word 

        self.fptr = 3
        self.rptr = 0
        kc *= 10
        while kc > 0:
            kc -= 1
            self.rand()


    def rand(self) -> int:
        """ Return a new random number """
        result = 0
        fptr = self.fptr
        rptr = self.rptr
        end_ptr = 31

        self.state[fptr] = int32_t(self.state[fptr] + self.state[rptr])
        val = self.state[fptr]
        # Chucking least random bit. 
        result = int32_t((val >> 1) & 0x7fffffff)
        fptr += 1
        if fptr >= end_ptr:
            fptr = 0
            rptr += 1
        else:
            rptr += 1
            if rptr >= end_ptr:
                rptr = 0

        self.fptr = fptr
        self.rptr = rptr

        return result

class SecureCache(object):
    
    def __init__(self):
        # Use our random as it's more secure than the python one!
        self.random = Random()
        self.rand = self.random.rand 
        self.srand = self.random.srand

        # Seed our random using the super secret seed
        self.srand(SEED)
        # Initialize our database 
        self.database = { self.generate_key(): FLAG }

    def generate_key(self) -> str:
        """ Generate a new secure key for the database """
        # Generate a new key 
        key = self.rand()
        # Convert integer to string and then to bytes 
        key_bytes = str(key).encode('utf-8') 
        # Create a SHA256 hash object 
        sha256_hash = sha1(key_bytes) 
        # Return the hexadecimal representation of the hash 
        return sha256_hash.hexdigest() 

    def store(self, value: bytes) -> str:
        """ Store a new value inside the secure database """
        if not isinstance(value, bytes) or len(value) == 0 or b'JDHACK' in value:
            raise Exception("Invalid value!")

        key = self.generate_key()
        while key in self.database:
            key = self.generate_key()
            
        self.database[key] = value
        return key

    def load(self, key: str) -> bytes:
        """ Load a value from the secure database """
        if not isinstance(key, str) or not len(key) == 40:
            raise Exception("Invalid key!")

        return self.database.get(key)
    
    def list_values(self) -> list[bytes]:
        """ List the values present inside the secure database """
        result = [] 
        for value in self.database.values():
            if len(value) > 6:
                # Shorten keys that are too large
                value = value[0:6] + b'[REDACTED]'
            result.append(value)

        return result

class SecureCacheServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


class SecureCacheHandler(socketserver.BaseRequestHandler):

    def options(self):
        self.request.send(
            "\nChoose an option:\n"
            "\t1. Read something using your key\n"
            "\t2. Store something\n"
            "\t3. List all the values from the store\n"
            "\t4. Quit\n"
            "> ".encode()
        )
    
    def list_values(self):
        self.request.send(
            b"Here is the list of values:\n"
        )
        for value in self.store.list_values():
            self.request.send(b' - ' + value + b'\n')
  

    def load_value(self):
        self.request.send(
            b"Please enter the key corresponding to the value you want to read\n > "
        )
        try:
            key = self.request.recv(128).decode().strip()
            value = self.store.load(key)
            if not value:
                self.request.send(b"Could not found value") 
            else:
                self.request.send(b"Here is your data:\n"+value+b"\n")

        except Exception as e:
            self.request.send(str(e).encode())

    def store_value(self):
        self.request.send(
            b"Please enter the value you want to store (limited to 32 bytes for now)\n > "
        )
        try:
            value = self.request.recv(32)
            if value and len(value) > 0 and len(value) <= 32:
                key = self.store.store(value)
                self.request.send("Here is your key: {}\n".format(key).encode())
            else:
                self.request.send(b"Could not store requested value!")
                
        except Exception as e:
            self.request.send(str(e).encode())


    def handle(self):
        self.store = SecureCache()
        self.request.send(
            b"Welcome to the SecureCacheServer! Here you can save/retrieve your data.\n"
            b"WARNING: All data will be lost upon disconnection!\n"
        )

        try:
            while True:
                # Receive user choice
                self.options()
                option = self.request.recv(1024)[:1].decode()

                match option:
                    case "1":
                        self.load_value()
                    case "2":
                        self.store_value()
                    case "3":
                        self.list_values()
                    case "4":
                        self.request.send("Disconneting\n".encode())
                        self.request.close()
                        break
                    case _:
                        self.request.send("Invalid option\n".encode())
        except (ConnectionResetError, BrokenPipeError):
            print("Connection reset by client")


if __name__ == "__main__":
    server = SecureCacheServer((HOST, PORT), SecureCacheHandler)
    print("Start listening on [{}:{}]".format(HOST,PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
