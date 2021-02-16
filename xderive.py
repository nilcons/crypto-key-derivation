#!./venv/bin/python

import sys

from lib import mbp32, utils

xkey = mbp32.XKey.from_xkey(utils.one_line_from_stdin())
for i in sys.argv[1:]:
    if i == "n":
        xkey = xkey.neuter()
    else:
        xkey = xkey.derivation(i)
print(xkey.to_xkey().decode('ascii'))
