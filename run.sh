#!/bin/bash
cd "$(dirname "$0")"
make && exec python3 src/main.py "$@"
