#!./venv/bin/python

from electrum import keystore, mnemonic, coinchooser

import argparse
import sys
import os

# We support only standard lengths
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
ACCEPTED_LENGTHS = [12, 15, 18, 21, 24]

def read_and_validate():
    lines = [x.strip() for x in sys.stdin.readlines()]

    if len(lines) != 1:
        print("Give words in one line", file=sys.stderr)
        sys.exit(1)

    first_line = lines[0]
    words = first_line.split()
    if (len(words) + 1) not in ACCEPTED_LENGTHS:
        print(
            "{0} words given, but number should be one of {1}".format(
                len(words),
                str([x - 1 for x in ACCEPTED_LENGTHS])),
            file=sys.stderr)
        sys.exit(1)

    (first_checksum_ok, first_wordlist_ok) = keystore.bip39_is_checksum_valid(" ".join(words))
    if not first_wordlist_ok:
        print("Unkown words!", file=sys.stderr)
        sys.exit(1)

    return words


def main():
    words = read_and_validate()

    wordlist = mnemonic.Mnemonic().wordlist
    print("Good last words:")
    ok_words = []
    for last in wordlist:
        (checksum_ok, wordlist_ok) = keystore.bip39_is_checksum_valid(
            " ".join(words + [last]))
        assert wordlist_ok
        if checksum_ok:
            print(last)
            ok_words.append(last)

    prng = coinchooser.PRNG(os.urandom(100))
    print("\nA random choice would be:")
    print(prng.choice(ok_words))

if __name__ == "__main__":
  main()
