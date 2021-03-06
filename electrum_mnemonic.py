#!./venv/bin/python

from electrum import util
from electrum.mnemonic import Mnemonic

import sys

lines = [x.strip() for x in sys.stdin.readlines()]

words = ""
passw = ""
if len(lines) == 2:
    passw = lines[1]
if not (len(lines) in [1, 2]):
    print("wrong input")
    sys.exit(1)

words = lines[0]
print(util.bh2u(Mnemonic.mnemonic_to_seed(words, passw)))
