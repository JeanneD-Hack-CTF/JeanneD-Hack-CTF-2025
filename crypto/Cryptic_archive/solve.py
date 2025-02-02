#!/usr/bin/env python3

from encrypt import Random, xor, gen_blocks


def decrypt(encrypted: bytes, block_size: int, generator: Random) -> bytes:
    # Check message is padded
    assert(len(encrypted) % block_size == 0)

    clear = b''

    # Initialize all blocks
    blocks = gen_blocks(encrypted, block_size)
    total = len(blocks)
    progress = list(range(0, 100, 5))

    # Decrypt each block
    for i, block in enumerate(blocks):

        percent = round(i * 100 / total)
        if percent in progress:
            print("[+] {}% block decrypted".format(percent))
            progress.remove(percent)

        # The first block is decrypted using generator state because we recover the first 128 bytes generated
        # not the state directly
        if (i == 0):
            clear += xor(block, generator.state)
        else:
            clear += xor(block, generator.gen_random_bytes(block_size))

    return clear


def main():
    archive = "archive.zip"
    secret = "secret.zip.enc"

    # Read first 128 bytes
    with open(archive, 'rb') as a, open(secret, 'rb') as s:
        arch_clear = a.read(256)
        encrypted = s.read()

    # Compute initial state
    state = xor(arch_clear, encrypted[:256])

    # Init a new random generator and set state
    generator = Random()
    generator.state = [i for i in state]
    print("Computed state:", generator.state)

    # Ensure message is padded
    clear = decrypt(encrypted, 256, generator)

    with open("out.zip", 'wb') as out:
        out.write(clear)

    print("Done !")


if __name__ == "__main__":
    main()
