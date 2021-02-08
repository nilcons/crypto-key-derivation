#!./venv/bin/python

from electrum import ecc, bitcoin, bip32, util
from base58 import b58encode, b58decode, XRP_ALPHABET
import hashlib
from Crypto.Util import RFC1751

import sys

def sha256(b):
    return hashlib.sha256(b).digest()

def ripemd160(b):
    h = hashlib.new('ripemd160')
    h.update(b)
    return h.digest()

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

b32 = bip32.BIP32Node.from_xkey(lines[0])
prv = b32.eckey.get_secret_bytes()
print(util.bh2u(prv))
