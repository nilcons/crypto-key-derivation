#!./venv/bin/python

from electrum import keystore

import argparse
import sys

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--no-check', action='store_true', default=False)
args = arg_parser.parse_args()

lines = [x.strip() for x in sys.stdin.readlines()]

words = ""
passw = ""
if len(lines) == 2:
    passw = lines[1]
if not (len(lines) in [1, 2]):
    print("wrong input", file=sys.stderr)
    sys.exit(1)

words = lines[0]

if not args.no_check:
    (checksum_ok, wordlist_ok) = keystore.bip39_is_checksum_valid(words)
    if not wordlist_ok:
        print("Unknown words!", file=sys.stderr)
        sys.exit(1)
    if not checksum_ok:
        print("Checksum NOT OK!", file=sys.stderr)
        sys.exit(1)

print(keystore.bip39_to_seed(words, passw).hex())
