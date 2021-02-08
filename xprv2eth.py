#!./venv/bin/python

from electrum import bip32, util

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

k = bip32.BIP32Node.from_xkey(lines[0]).eckey.get_secret_bytes()
print(util.bh2u(k))
