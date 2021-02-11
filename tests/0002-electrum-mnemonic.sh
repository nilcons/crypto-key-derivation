#!/bin/bash

set -e
set -o pipefail
set -u

# TODO: 12 words

# 18 words no passphrase
cmp <(echo scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump \
    | ./electrum_mnemonic.py) \
    <<EOF
d27376868abe32360d112c0afd31298b0d5a91d895a3edebbccabb96a58161b67a2e7f35902d958bb3fedac0b818c87ce7e97b5309af612ee0a539ed029a107b
EOF

# 18 words passphrase
cmp <(echo "scissors invite lock maple supreme raw rapid void congress muscle digital elegant little brisk hair mango congress clump
TREZOR" | ./electrum_mnemonic.py) \
    <<EOF
7d8b4005aa5e21e438057535a8a37944f5b110f3df91743bca22ffdcd2690fd1d83611d7740719199fa3e6093a756b2bf6a4e1975da733a114325733b056d86a
EOF

# TODO: 24 words
