#!./venv/bin/python

from electrum import util, bitcoin

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

seed = util.bfh(lines[0])
xprv, _xpub = bitcoin.bip32_root(seed, "standard")
print(xprv)
