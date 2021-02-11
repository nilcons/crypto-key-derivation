#!/bin/bash

set -e
set -o pipefail
set -u
set -x

for t in tests/*.sh; do
    $t
done
