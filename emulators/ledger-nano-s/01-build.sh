#!/bin/bash

set -e

# apps
rm -rf apps-out
docker build -f Dockerfile.nanosapps -t nanosapps .
docker run --rm nanosapps tar c /apps-out | tar xv

# speculos emulator with ledger-cli to ask for addresses
docker build -f Dockerfile.speculos -t speculos-ledger-cli .
