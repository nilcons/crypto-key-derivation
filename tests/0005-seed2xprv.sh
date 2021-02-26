#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./seed2xprv.py <<< 000102030405060708090a0b0c0d0e0f) - <<EOF
xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi
EOF

diff -u <(./seed2xprv.py <<< fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542) - <<EOF
xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U
EOF

# The ed25519 keys we represent a bit differently than how misc/slip-0010-tests.py officially does.
# Our representation has the advantage that the curve is encoded into the key.
# But because of this the xprv's are different, but the private key inside is the same.
# So instead of comparing the xprv, we compare only the secret keys.
diff -u <(./seed2xprv-ed25519.py <<< 000102030405060708090a0b0c0d0e0f | tools/xkeydump.py | grep Private | cut -d\  -f3) - <<EOF
2b4be7f19ee27bbf30c667b642d5f4aa69fd169872f8fc3059c08ebae2eb19e7
EOF

diff -u <(./seed2xprv-ed25519.py <<< fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542 | tools/xkeydump.py | grep Private | cut -d\  -f3) - <<EOF
171cb88b1b3c1db25add599712e36245d75bc65a1a5c9e18d76f9f2b1eab4012
EOF
