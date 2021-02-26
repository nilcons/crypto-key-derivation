#!/bin/bash

set -e
set -o pipefail
set -u

# 12 words no passphrase
cmp <(echo legal winner thank year wave sausage worth useful legal winner thank yellow \
    | ./bip39.py) \
    <<EOF
878386efb78845b3355bd15ea4d39ef97d179cb712b77d5c12b6be415fffeffe5f377ba02bf3f8544ab800b955e51fbff09828f682052a20faa6addbbddfb096
EOF

# 12 words passphrase
cmp <(echo "legal winner thank year wave sausage worth useful legal winner thank yellow
TREZOR" | ./bip39.py) \
    <<EOF
2e8905819b8723fe2c1d161860e5ee1830318dbf49a83bd451cfb8440c28bd6fa457fe1296106559a3c80937a1c1069be3a3a5bd381ee6260e8d9739fce1f607
EOF

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

# 24 words no passphrase
cmp <(echo nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst \
    | ./bip39.py) \
    <<EOF
3a11c61fde54b15018434eca77495b16ef093531b563c0e56052c0b623df9ba1b72ea76e94fec997d8304e6dcd95845cd39ecc1979dace68d7456914fad50713
EOF

# 24 words passphrase
cmp <(echo "void come effort suffer camp survey warrior heavy shoot primary clutch crush open amazing screen patrol group space point ten exist slush involve unfold
TREZOR" | ./bip39.py) \
    <<EOF
01f5bced59dec48e362f2c45b5de68b9fd6c92c6634f44d6d40aab69056506f0e35524a518034ddc1192e1dacd32c1ed3eaa3c3b131c88ed8e7e54c49a5d0998
EOF
