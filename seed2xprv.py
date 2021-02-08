#!./venv/bin/python

from electrum import util, bip32

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

seed = util.bfh(lines[0])
node = bip32.BIP32Node.from_rootseed(seed, xtype = "standard")
print(node.to_xprv())
