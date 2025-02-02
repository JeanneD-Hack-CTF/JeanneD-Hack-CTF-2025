#!/usr/bin/env python3

import math
import base64
import pyasn1.codec.der.encoder
import pyasn1.type.univ

from Crypto.Util import number


target = "/jeannedhackctf/"

def compute_PQ():
    p, q = number.getPrime(512), number.getPrime(512)
    phi = (p - 1) * (q - 1)
    return p, q, phi


def pempriv(n, e, d, p, q, dP, dQ, qInv):
    template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    seq = pyasn1.type.univ.Sequence()
    for i,x in enumerate((0, n, e, d, p, q, dP, dQ, qInv)):
        seq.setComponentByPosition(i, pyasn1.type.univ.Integer(x))
    der = pyasn1.codec.der.encoder.encode(seq)
    return template.format(base64.encodebytes(der).decode('ascii'))


def solve():
    e = int.from_bytes(base64.b64decode(target))
    p, q, phi = compute_PQ()

    while math.gcd(e, phi) != 1:
        p, q, phi = compute_PQ()

    N = p * q
    d = pow(e, -1, phi)

    dP = d % (p - 1)
    dQ = d % (q - 1)
    qInv = pow(q, p - 2, p)

    print("Public exponent e:", e)
    key = pempriv(N, e, d, p, q, dP, dQ, qInv)

    return key


if __name__ == "__main__":
    key = solve()
    while target not in key:
        key = solve()

    with open("key.pem", 'w') as keyfile:
        keyfile.write(key)

