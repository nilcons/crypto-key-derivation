#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./x2btc.py <<< xprv9xAtkRR4Ru4DcgwbM22eoVpBEnJysuy7mxxur8Lrqad6qTnnQHhtR64MvvhXUZYhzUc7FDNwT9xC3ym47vvWB3XEst63pjkPWDRf79a6DTP) - <<EOF
p2pkh:L15hj1TsQC1eCnMwd4CkZTGh8iusyHjDtz2oNL968oPz9dXGEeP4
EOF

diff -u <(./x2btc.py <<< xpub6BAF9vwxGGcWqB24T3ZfAdkunp9UHNgy9BtWeWkUPvA5iG7vwq28xtNqnCSkxDLfkZpKbk4rNQ3w95HCr5FN8o9FexSfqZboebW6Pr3JLBS) - <<EOF
19C8rUkmD1QG13qrpqypo3pEGuVMfEd8q5
EOF

diff -u <(./x2btc.py p2wpkh-p2sh <<< xpub6BAF9vwxGGcWqB24T3ZfAdkunp9UHNgy9BtWeWkUPvA5iG7vwq28xtNqnCSkxDLfkZpKbk4rNQ3w95HCr5FN8o9FexSfqZboebW6Pr3JLBS) - <<EOF
37GxRVzwaiQ7vdZbVJpmfG64gy8tWWomFz
EOF

diff -u <(./x2btc.py p2wpkh <<< xpub6BAF9vwxGGcWqB24T3ZfAdkunp9UHNgy9BtWeWkUPvA5iG7vwq28xtNqnCSkxDLfkZpKbk4rNQ3w95HCr5FN8o9FexSfqZboebW6Pr3JLBS) - <<EOF
bc1qt8wzxfq4p2ufpumd6w02p7kdr5c7uaqeekmeje
EOF
