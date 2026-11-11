---
title: Compose
order: 40
topic: compose
description: Monen kontin ympäristö yhdellä tiedostolla.
---

# Docker Compose

Compose käynnistää monta konttia kerralla `docker-compose.yml`-tiedoston perusteella.

## Komennot

| Komento | Mitä tekee |
|---|---|
| `docker compose up` | käynnistää kaiken |
| `docker compose up -d` | taustalle |
| `docker compose up -d --build` | rakentaa imaget ensin |
| `docker compose up -d web` | vain yksi palvelu |
| `docker compose ps` | palvelujen tila |
| `docker compose logs -f api` | yhden palvelun lokit |
| `docker compose exec db psql -U notes` | komento palvelun konttiin |
| `docker compose restart web` | uudelleenkäynnistys |
| `docker compose stop` | pysäyttää, ei poista |
| `docker compose down` | poistaa kontit ja verkot |
| `docker compose down -v` | poistaa myös volumet |
| `docker compose config` | näyttää lopullisen configin |
| `docker compose up -d --scale api=3` | kolme instanssia |
| `docker compose --profile tools up -d` | käynnistää myös profiilin palvelut |

## Esimerkki yml

```yaml
services:
  api:
    build: ./api
    environment:
      DB_HOST: db
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]

volumes:
  pgdata:

secrets:
  db_password:
    file: ./db_password.txt
```

## Muistettavaa

- palvelun nimi toimii hostnamena, esim. `db:5432`
- pelkkä `depends_on` ei odota että palvelu on valmis, tarvitaan `condition: service_healthy` ja healthcheck
- `.env`-tiedosto luetaan automaattisesti, muuttujat `${PORTTI:-8080}`
