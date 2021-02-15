#!./venv/bin/python

import sys

from lib import mbp32, utils

index = sys.argv[1]
xpub = mbp32.XKey.from_xkey(utils.one_line_from_stdin())
print(xpub.derivation(index).to_xkey().decode('ascii'))
