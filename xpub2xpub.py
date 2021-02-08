#!./venv/bin/python

from electrum import bip32

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

index = int(sys.argv[1])
node = bip32.BIP32Node.from_xkey(lines[0])
print(node.subkey_at_public_derivation(str(index)).to_xpub())
