#!/bin/bash
# sammuttaa, data jää volumeen
# ./lopeta.sh --kaikki poistaa myös datan

cd "$(dirname "$0")"

if [ "$1" == "--kaikki" ]; then
  docker compose --profile tools down -v
else
  docker compose --profile tools down
fi
