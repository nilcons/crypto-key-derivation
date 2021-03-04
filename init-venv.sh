#!/bin/bash

set -e

rm -rf venv
python3.9 -m venv venv
. venv/bin/activate
pip install -U pip wheel
echo $PWD >venv/lib/python3.9/site-packages/crypto-key-derivation.pth
pip install -r requirements.txt
touch venv/lib/python3.9/site-packages/electrum/py.typed
touch venv/lib/python3.9/site-packages/electrum_ltc/py.typed

# pytezos hard depends on outdated version 1 of base58 pip package,
# but we need version 2 features for XRP.  Somebody should help the
# pytezos guys update...
curl -sL -o venv/lib/python3.9/site-packages/base58_2.py  https://github.com/keis/base58/raw/5077d046107cbdda9f5e5aecc3da97c559d486e7/base58/__init__.py
