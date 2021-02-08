#!/bin/bash

set -e

WORDS=$(gpg --gen-random 2 46 | od -An -tu2 -w2 | while read RET ; do
        cat ./venv/lib/python3.9/site-packages/electrum/wordlist/english.txt | sed -n "$(echo $((RET % 2048)))p"
done | tr '\n' ' ')
LAST=$(echo $WORDS | bip39-last-word/last_word.py | tail -n1)
echo $WORDS $LAST
