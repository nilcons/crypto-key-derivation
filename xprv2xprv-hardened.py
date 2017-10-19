#!./venv/bin/python

from electrum import bitcoin

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

index = int(sys.argv[1])
xprv, _xpub = bitcoin.bip32_private_derivation(lines[0], "", str(index) + "'")

print(xprv)
