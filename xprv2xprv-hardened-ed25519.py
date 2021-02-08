#!./venv/bin/python

from electrum import bip32, ecc

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

if len(lines) !=1:
    print("wrong input")
    sys.exit(1)

# Stellar does the private key derivation a bit differently compared
# to ethereum/bitcoin, using the ed25519 curve instead of electrum.ecc.
#
# So we get out the bytes from electrum here and just reverse the
# computation.  This ugly code is the result of reverse-engineering
# electrum and stellar-sdk until we got it working... :(

index = int(sys.argv[1])
node = bip32.BIP32Node.from_xkey(lines[0])
sk = node.subkey_at_private_derivation(str(index) + "'")
skbytes = sk.eckey.get_secret_bytes()
sknum = ecc.string_to_number(skbytes)
scalar = ((sknum - ecc.string_to_number(node.eckey.get_secret_bytes())) + ecc.CURVE_ORDER) % ecc.CURVE_ORDER
fnode = node.subkey_at_private_derivation(str(index) + "'")
fnode = fnode._replace(eckey = ecc.ECPrivkey.from_secret_scalar(scalar))

print(fnode.to_xprv())
