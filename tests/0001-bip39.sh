#!/bin/bash

set -e
set -o pipefail
set -u

# TODO: 12 words

# 18 words no passphrase
cmp <(echo scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump \
    | ./bip39.py) \
    <<EOF
a555426999448df9022c3afc2ed0e4aebff3a0ac37d8a395f81412e14994efc960ed168d39a80478e0467a3d5cfc134fef2767c1d3a27f18e3afeb11bfc8e6ad
EOF

# 18 words passphrase
cmp <(echo "scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
TREZOR" | ./bip39.py) \
    <<EOF
7b4a10be9d98e6cba265566db7f136718e1398c71cb581e1b2f464cac1ceedf4f3e274dc270003c670ad8d02c4558b2f8e39edea2775c9e232c7cb798b069e88
EOF

# TODO: 24 words
