#!./venv/bin/python

from electrum import bitcoin, util
from sha3 import keccak_256

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

_xtype, _depth, _fp, _cn, _c, K = bitcoin.deserialize_xpub(lines[0])
# privkey = bitcoin.serialize_privkey(k, True, "p2pkh")
keccak = keccak_256()
keccak.update(bitcoin.point_to_ser(bitcoin.ser_to_point(K), False)[1:])
print("0x" + keccak.hexdigest()[24:])
