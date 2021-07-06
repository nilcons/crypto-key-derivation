#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./x2doge.py <<< xprvA2iFkvvYGPxHZpKhHKwZia9TbiNofmi7H5FukcugMMEB6DJeUaDMh3B8iuSU2VGeYvswFAVa3pn7TZXDAZrDhHSaH8subdnhuimuxSaFauV) - <<EOF
p2pkh:QWuNRagebPYP5oaEdPwV3QJspWZbe2yWD9pmX4LyUN2kYCVgVUsQ
EOF

diff -u <(./x2doge.py <<< xpub6FhcASTS6mWanJQAPMUa5i6C9kDJ5ERxeJBWZ1KHugm9y1do27XcEqVcaBYeFcRgvMPN8dNMsDMt97eSCBgg34yqGQbFvdyNUphhSH7rffU) - <<EOF
D59PrFM5WCx1RupDRTN3a8cSLX8E8pSQHt
EOF
