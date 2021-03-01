#!/bin/bash

set -e

get_addresses() {
    for c in btc eth xrp xlm ltc xtz; do
        docker run -it --rm speculos-ledger-cli "$1" $c \
            | grep -v "Failed to initialize libusb" \
            | grep -v "UTXOs" \
            | cut -d: -f2- \
            | cut -d')' -f1-2
    done
}

echo "Addresses for our test seed without passphrase:"
get_addresses "nation grab van ride cloth wash endless gorilla speed core dry shop raise later wedding sweet minimum rifle market inside have ill true analyst"

# Unfortunately the speculos doesn't provide passphrase feature, so we
# have to trust at least the BIP39 part of our project and we can't
# test it directly with the emulator. :(
echo
echo "Addresses for our test seed with passphrase:"
get_addresses "hex:a5190ce0b41c519b44087fdfe997cf1c511a135d3bf02b8a0e7ddad1e972fe2a863962f26ed62f8c03d1f768c51cf97084fd9e2490384173ae437027949331d9"
