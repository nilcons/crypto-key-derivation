#!/bin/bash

set -e

for c in btc eth xrp xlm ltc xtz; do
    docker run -it --rm speculos-ledger-cli $c
done
