#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./x2xlm.py <<< xprv9zA1iiPxwyVSNZw1PorSVeLLfbVJ3Zr1tpamNfbAsTNpY3cy5wRZ1D8YXAKGG62ZAFPmYEwGaPRPVp8uPWNeBQG61uSUq2LGu1ezkQsKryd) - <<EOF
SCGVFOJNHSOR55IAQQT2R6PFHEHCD3HVTB7PGTC3DNVL74LZQBYUBHAT
EOF

diff -u <(./x2xlm.py <<< xpub6D9N8DvrnM3javAqd2tPR6tht7FftXuwYp5sEVEe1VXpJY7oS5o7YXdYZUgzfY9G9RdM46DXHqsFpyUvsG2TMSqJHYo1FNUP7BEGzMFBiXq) - <<EOF
GD23O4PMK22FKSQECOOBOE3WUEPHTB2QKMALHZIADYREY3WGZFUBHNFX
EOF
