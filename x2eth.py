#!./venv/bin/python

from lib import mbp32, utils

xkey = mbp32.XKey.from_xkey(utils.one_line_from_stdin())
print(xkey.to_eth())
