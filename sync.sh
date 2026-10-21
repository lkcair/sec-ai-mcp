#!/bin/sh
# Copy sec_finance_ai.py from lkcair/sec-finance-ai, byte for byte. Run before a release.
# Usage: ./sync.sh [ref]   (default main)
set -e
curl -fsSL "https://raw.githubusercontent.com/lkcair/sec-finance-ai/${1:-main}/sec_finance_ai.py" -o sec_finance_ai.py
grep -m1 '^version:' sec_finance_ai.py
