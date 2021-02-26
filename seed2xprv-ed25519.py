#!./venv/bin/python

from lib import mbp32, utils
xprv = mbp32.XKey.from_seed_ed25519(bytes.fromhex(utils.one_line_from_stdin()))
print(xprv.to_xkey().decode("ascii"))
