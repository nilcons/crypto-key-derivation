#!./venv/bin/python

from electrum import bip32

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

print(bip32.xpub_from_xprv(lines[0]))
