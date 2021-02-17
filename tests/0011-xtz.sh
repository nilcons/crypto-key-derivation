#!/bin/bash

set -e
set -o pipefail
set -u

diff -u <(./x2xtz.py <<< xprvA1TDzWUPxfe6jpSkMidYsEPPkG9B5FqUYBKt3xYmMNSvNmVtPVpbPCdQP5faUQddr1L7VfGav574YCPW4N3ksCrYjd38m24aWVJw8KR7VXs) - <<EOF
edsk3SASh4w2ZVAMGYuPvG617nxabj5Y97rBn18Jg2ZiLReMvrMfvD
EOF

diff -u <(./x2xtz.py <<< xpub6ESaQ21Ho3CPwSWxGS676y7EyQfvYtqLu7tFYvwSnUktcxrHEbT3un9EiPHyAJNEDU9gerqKWhVJCMJ5jr8LfZUns3hVyrYnXurXgMkfB9u) - <<EOF
tz1hDY7HSpaCFNeffwbF2mjmegdHAQUgyxg9
EOF
