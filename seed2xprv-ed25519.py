#!./venv/bin/python

from electrum import util, bip32, ecc
from electrum.crypto import hmac_oneshot

import hashlib
import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

seed = util.bfh(lines[0])

# Electrum lib only supports creating a hmac seed the bitcoin way (used by ethereum too).
# But Stellar uses a different seed, so we create the rootnode manually here.
I = hmac_oneshot(b"ed25519 seed", seed, hashlib.sha512)
node = bip32.BIP32Node(xtype="standard",
                 eckey=ecc.ECPrivkey(I[0:32]),
                 chaincode=I[32:])

print(node.to_xprv())
