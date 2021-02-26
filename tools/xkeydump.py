#!./venv/bin/python

from lib.mbp32 import XKey
from lib.utils import one_line_from_stdin

xkey = XKey.from_xkey(one_line_from_stdin())
print(xkey)
print("Version:", xkey.version)
print("Depth:", xkey.depth)
print("Parent FP:", xkey.parent_fp.hex())
print("Child number:", xkey.child_number_with_tick())
print("Chain code:", xkey.chain_code.hex())
print("Key:", xkey.key)
if xkey.key.get_private_bytes():
    print("Private bytes:", xkey.key.get_private_bytes().hex())
print("Public bytes:", xkey.key.get_public_bytes().hex())
print("Key ID:", xkey.keyid().hex())
print("XKey:", xkey.to_xkey().decode('ascii'))
