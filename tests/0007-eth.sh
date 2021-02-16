#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./x2eth.py <<< xprvA31ZwzYzpLm2uAmK3N8NdRNSVNbeaZcbCaXtrw73S7vpzD4nJDEKvCvaWzgrbCjJZDeub6vHUmCTPMeXWVgG4qJzy4CgRJAjRdhBui6u8ZZ) - <<EOF
bb36972e4db24cffd1dba3342c4c801c3344fe429500bdba192e2f49673f9139
EOF

diff -u <(./x2eth.py <<< xpub6FzvMW5teiKL7eqn9PfNzZKB3QS8z2LSZoTVfKWezTTos1PvqkYaU1F4NFiMjtDozG53B8mk2ZhBVJgv2fLyhqpBPYkMPCtT5G9rDtKQcCm) - <<EOF
0x154D15BB73A7c01a208D3b7fEB1d77cd65756f86
EOF
