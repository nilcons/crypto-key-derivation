#!./venv/bin/python

from electrum import bip32, util
from stellar_sdk.keypair import Keypair

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

k = bip32.BIP32Node.from_xkey(lines[0]).eckey.get_secret_bytes()
kp = Keypair.from_raw_ed25519_seed(k)
print(kp.secret)
print(kp.public_key)
