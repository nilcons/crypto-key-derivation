#!/bin/bash

set -e

rm -rf down
mkdir -p down
curl -o down/proxy.py https://raw.githubusercontent.com/LedgerHQ/speculos/master/tools/ledger-live-http-proxy.py
curl -o down/ledger-live -L https://download-live.ledger.com/releases/latest/download/linux
chmod a+x down/*
npm install ledger-live
rm -f package-lock.json package.json
