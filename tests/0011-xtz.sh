#!/bin/bash

set -e
set -o pipefail
set -u

# ED25519 curve for tz1 addresses
diff -u <(./x2xtz.py <<< xprvA1TDzWUPxfe6jpSkMidYsEPPkG9B5FqUYBKt3xYmMNSvNmVtPVpbPCdQP5faUQddr1L7VfGav574YCPW4N3ksCrYjd38m24aWVJw8KR7VXs) - <<EOF
edsk3SASh4w2ZVAMGYuPvG617nxabj5Y97rBn18Jg2ZiLReMvrMfvD
EOF

diff -u <(./x2xtz.py <<< xpub6ESaQ21Ho3CPwSWxGS676y7EyQfvYtqLu7tFYvwSnUktcxrHEbT3un9EiPHyAJNEDU9gerqKWhVJCMJ5jr8LfZUns3hVyrYnXurXgMkfB9u) - <<EOF
tz1hDY7HSpaCFNeffwbF2mjmegdHAQUgyxg9
EOF

# Secp256k1 curve for tz2 addresses
diff -u <(./x2xtz.py <<< xprv9zyre4rnL24WXvVS1nuBAZLzrzTb4Mz7pjUegPoD6Hm9zjRQrh31PY6Qo6xSaEjsjEDyfAy4RCjGwmt7mYMz2pKjbJhuGsHEdEaGrQLwLGZ) - <<EOF
spsk24mup6mo8132KGD2goYpV17FEvvDnk1RQYD5EcTCpARaVcTC7p
EOF

diff -u <(./x2xtz.py <<< xpub6DyD3aPgAPcokQZu7pSBXhHjR2J5TphyBxQFUnCpedJ8sXkZQEMFwLQteNPjS44pSih4RWCooKi7zc2Pa81Y2oYdFYEKsRAqHbibv8CxnFH) - <<EOF
tz2RvYDs1YgBfUXGPo9UijX4Ck2HcbQ7C63p
EOF
