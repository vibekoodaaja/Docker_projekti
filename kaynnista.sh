#!/bin/bash
# käynnistää kaiken

cd "$(dirname "$0")"

# tehään salasana jos ei oo
if [ ! -f secrets/db_password.txt ]; then
  mkdir -p secrets
  head -c 24 /dev/urandom | base64 | tr -d '/+=\n' > secrets/db_password.txt
  chmod 644 secrets/db_password.txt  # api ei muuten pysty lukemaan
fi

if [ ! -f .env ]; then
  cp .env.example .env
fi

docker compose up -d --build

echo "http://localhost:8080"
