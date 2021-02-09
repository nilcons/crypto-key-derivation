#!/bin/bash

set -e

mypy --allow-redefinition lib/utils.py lib/mbp32.py tools/xkeydump.py bip39.py
