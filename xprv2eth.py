#!./venv/bin/python

from electrum import bitcoin, util

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

_xtype, _depth, _fp, _cn, _c, k = bitcoin.deserialize_xprv(lines[0])
# privkey = bitcoin.serialize_privkey(k, True, "p2pkh")

print(util.bh2u(k))
