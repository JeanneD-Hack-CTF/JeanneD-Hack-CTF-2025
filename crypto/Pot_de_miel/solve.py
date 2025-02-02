#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes

h = 6966343192926317569595983766338492708381169847881721700879512706305212927745
modulus = 2 ** 256
multiplier = (13 * 13) ** 37

mod_inv = pow(multiplier, -1, modulus)
p = h * mod_inv % modulus

print(f"Password : {long_to_bytes(p).decode()}")