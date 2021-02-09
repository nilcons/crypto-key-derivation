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
print("Key ID:", xkey.keyid().hex())
print("XKey:", xkey.to_xkey().decode('ascii'))
