#!./venv/bin/python

import sys

from lib import mbp32, utils

index = sys.argv[1]
xprv = mbp32.XKey.from_xkey(utils.one_line_from_stdin())
print(xprv.derivation(index).to_xkey().decode('ascii'))
