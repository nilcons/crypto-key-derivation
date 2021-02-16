#!./venv/bin/python

import sys

from lib import mbp32, utils

type = "p2pkh"
if len(sys.argv) == 2:
    type = sys.argv[1]
xkey = mbp32.XKey.from_xkey(utils.one_line_from_stdin())
print(xkey.to_btc(type))
