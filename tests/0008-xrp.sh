#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./xprv2xrp.py <<< xprvA2aNtHmSxo934J5ziFmGBonLSgXuz12S7NXLG4Nbv2b1Wu8pjhDddtDfKNfpqfpXR3wjT8Cje7XkzRHynpL1WsPPgxv36ZDH26PuEtVAXrx) - <<EOF
xrp-hex:58fe510ffea22709defc4a2c55d1054d2d37ef46bb4a728f38d6b3fbe112850b
EOF

diff -u <(./xpub2xrp.py <<< xpub6FZjHoJLoAhLGnATpHJGYwj4ziNQPTkHUbSw4SnDUN7zPhTyHEXtBgY9Af5E3EVUXWLmrw69d5U28GU6WkugRtubg5j9JAAKhMmbyFiSCfy) - <<EOF
rH4b7nXtPgfjmtdfVLcY7qvMUFcMwLE5HX
EOF
