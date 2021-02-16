#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./x2ltc.py <<< xprvA3zMRNqsK7orRd4pcbp4y4tvfgiiLQoUxonGhS4rdWgR3iEeU8vjjKWtLcnWqzonXtb1j6pSGLFs55DjS87WWiDPs1qHw8YrUcDQBWe4q7f) - <<EOF
p2pkh:TAsF1RAJXdXBVPZQjiuQDbcVUTHnnAwxsoMqtK7e6ywALtRsqf7v
EOF

diff -u <(./x2ltc.py p2wpkh-p2sh <<< xprvA3cBKv4hwr2vRBURaeuMiPXwqouvzT851SKFmWUDEDmJvzMA5kUmTm4LW6xfDSVjkeWYnBsQLxYMzAgvqir5sDs7xCBQqTirKdbEKzHMWv7) - <<EOF
p2wpkh-p2sh:T5p4aEcVZ3abdo6aBHctg4HkuZVMMaEiqy6KmDDc7jNHRfGUZXjf
EOF

diff -u <(./x2ltc.py p2wpkh <<< xprvA49DQyRupvRF8uhCFfPkRGNdCKdrNb9tmzVN7VxF23tPPDmcGQQkd51X23FayeXLw1wGYRwr1fi8nrB9AngK8CuAa8qWcHgZaQytshnxTAP) - <<EOF
p2wpkh:TAtmc58JUK2VsgQK9q2BF8B83URtxnTjWmhhPiy5qL2TCyBLYhiC
EOF

diff -u <(./x2ltc.py <<< xpub6GyhptNm9VN9e79HidM5LCqfDiZCjsXLL2hsVpUUBrDPvWZo1gEzH7qNBruKw3vzwVhph6ZwDHr33vTosrMuDDQ1AmixPkoMFXsLZjdrYdt) - <<EOF
LduZ8dL5REw7NnhNx9j5qBwdUfqPP9Sb4f
EOF

diff -u <(./x2ltc.py p2wpkh-p2sh <<< xpub6GbXjRbbnDbDdfYtggSN5XUgPqkRPuqvNfErZtspnZJHongJdHo21ZNpMNxAuKUv2fGUbcQJ3y4n2oQHVr3RxURxszRwGAgG9bNbBm8b6xc) - <<EOF
MG6vu3q25343H9JHkn3jAXffKsJbLua2Vx
EOF

diff -u <(./x2ltc.py p2wpkh <<< xpub6H8ZpUxofHyYMPmfMgvknQKMkMULn3sk9DQxutMraPRNG26kowj1AsKzsKm2cRhs3AKR6rAS4P3GNoXsfJr7JnLiN9mEuu3qehRmGXudJou) - <<EOF
ltc1qhqw64frfanzsktas5xtykpz0gxszzljrcwlmzz
EOF
