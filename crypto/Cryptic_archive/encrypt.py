#!/usr/bin/env python3

import os
import sys

from random import Random
from tqdm import tqdm


class Random:

    STATE_ELEM_MAX = 256

    def __init__(self, size: int=256):
        self.size = size
        self.state = [int.from_bytes(os.urandom(1)) for _ in range(size)]

    # Generate the next number of the generator
    def gen_next_number(self):
        number = 0

        # Some cryptographic operations
        for i in range(self.size):
            if i % 2 == 0:
                number += pow(self.state[i], i, self.STATE_ELEM_MAX) + self.state[i] * i
                number = ~number
            else:
                number ^= self.state[i] * i + 1

        number %= self.STATE_ELEM_MAX

        # Modify internal state
        self.state = self.state[1:]
        self.state.append(number)

        return number

    def gen_random_bytes(self, size: int=8):
        random = b''

        for _ in range(size):
            random += self.gen_next_number().to_bytes(1)

        return random


def xor(blob1: bytes, blob2: bytes):
    return bytes([a ^ b for a,b in zip(blob1, blob2)])

def pad(blob: bytes, block_size: int):
    return blob + b'\x00' * (block_size - len(blob) % block_size)

def gen_blocks(blob: bytes, block_size: int):
    return [blob[i:i+block_size] for i in range(0, len(blob), block_size)]

def encrypt(blob: bytes, block_size: int):
    encrypted = b''
    csprng = Random()

    # Initialize all blocks
    blocks = gen_blocks(pad(blob, block_size), block_size)
    total = len(blocks)
    progress = list(range(0, 100, 5))
    # Encrypt each block
    for i, block in enumerate(blocks):
        percent = round(i * 100 / total)
        if percent in progress:
            print("[+] {}% block encrypted".format(percent))
            progress.remove(percent)
        encrypted += xor(block, csprng.gen_random_bytes(block_size))

    return encrypted



if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("Usage: {} <filename>".format(sys.argv[0]))
        sys.exit(0)
    
    print("[+] Read file content...")
    with open(filename, "rb") as f:
        content = f.read()
    
    print("[+] Encrypt the file...")
    encrypted = encrypt(content, 256)

    print("[+] Write output...")
    with open(filename + ".enc", "wb") as out:
        out.write(encrypted)
    
    print("Done !")

