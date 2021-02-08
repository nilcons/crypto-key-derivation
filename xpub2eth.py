#!./venv/bin/python

from electrum import bip32, ecc, util
from sha3 import keccak_256

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

K = bip32.BIP32Node.from_xkey(lines[0]).eckey.get_public_key_bytes()

keccak = keccak_256()
keccak.update(ecc.ECPubkey(K).get_public_key_bytes(compressed = False)[1:])
print("0x" + keccak.hexdigest()[24:])
