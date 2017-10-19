#!./venv/bin/python

from electrum import bitcoin, util

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

_xtype, _depth, _fp, _cn, _c, K = bitcoin.deserialize_xpub(lines[0])
type = "p2pkh"
if len(sys.argv) == 2:
    type = sys.argv[1]
pubkey = bitcoin.pubkey_to_address(type, util.bh2u(K))

print(pubkey)
