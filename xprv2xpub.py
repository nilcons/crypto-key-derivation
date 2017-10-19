#!./venv/bin/python

from electrum import bitcoin

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

print(bitcoin.xpub_from_xprv(lines[0]))
