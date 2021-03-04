#!/bin/bash

set -e
set -o pipefail
set -u
set -x

for t in tests/*.sh; do
    $t
done

byexample --timeout=30 -j8 -l shell README.md
