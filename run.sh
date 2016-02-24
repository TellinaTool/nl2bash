#!/bin/bash
cd "$(dirname "$0")"
make && exec python src/main.py "$@"
