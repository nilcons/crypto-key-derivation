#!/bin/bash

set -e

SEED="nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst"
for c in btc eth xrp xlm ltc xtz; do
    docker run -it --rm speculos-ledger-cli "$SEED" $c \
        | grep -v "Failed to initialize libusb" \
        | grep -v "UTXOs" \
        | cut -d: -f2- \
        | cut -d')' -f1-2
done
