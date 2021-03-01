#!/bin/bash

set -e

for c in btc eth xrp xlm ltc xtz; do
    docker run -it --rm speculos-ledger-cli $c \
        | grep -v "Failed to initialize libusb" \
        | grep -v "UTXOs" \
        | cut -d: -f2- \
        | cut -d')' -f1-2
done
