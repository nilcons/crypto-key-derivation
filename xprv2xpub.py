#!./venv/bin/python

from lib import mbp32, utils

xprv = mbp32.XKey.from_xkey(utils.one_line_from_stdin())
print(xprv.neuter().to_xkey().decode('ascii'))
