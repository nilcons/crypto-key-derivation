#!./venv/bin/python

from electrum import util, keystore, mnemonic, coinchooser

import argparse
import sys
import os

def input_with_message(message):
    print(message, file=sys.stderr)
    return input()


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("n", nargs="?", default=None)
    args = arg_parser.parse_args()

    if args.n:
        n = int(args.n)
    else:
        n = int(input_with_message("How many words do you want to type: "))
    assert(1 < n)

    order = list(range(n))
    prng = coinchooser.PRNG(os.urandom(100))
    prng.shuffle(order)

    wordlist = mnemonic.load_wordlist("english.txt")
    
    words = [""] * n
    for i in range(n):
        valid = False
        while not valid:
            word = input_with_message("Type word {0}: ".format(order[i] + 1))
            if word in wordlist:
                valid = True
            else:
                print("INVALID WORD, TYPE AGAIN", file=sys.stderr)
        words[order[i]] = word
    print(" ".join(words))


if __name__ == "__main__":
  main()
