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
pub = b32.eckey.get_public_key_bytes()
aid = b'\x00' + ripemd160(sha256(pub))
cks = sha256(sha256(aid))[0:4]
print(b58encode(aid + cks, alphabet = XRP_ALPHABET).decode("ascii"))
