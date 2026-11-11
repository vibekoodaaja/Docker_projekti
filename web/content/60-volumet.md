---
title: Volumet
order: 60
topic: volumet
description: Pysyvä data, bind mountit ja varmuuskopiot.
---

# Volumet

Kontin sisällä oleva data häviää kun kontti poistetaan. Pysyvä data laitetaan volumeen tai bind mountiin.

## Komennot

| Komento | Mitä tekee |
|---|---|
| `docker volume ls` | listaa volumet |
| `docker volume create data` | uusi volume |
| `docker volume inspect data` | missä data on koneella |
| `docker volume rm data` | poistaa |
| `docker volume prune` | poistaa käyttämättömät |
| `docker run -v data:/var/lib/postgresql/data postgres` | nimetty volume |
| `docker run -v "$PWD":/app node` | bind mount nykyiseen kansioon |
| `docker run -v "$PWD/conf":/etc/conf:ro nginx` | vain luku |

## Volume vai bind mount

| | Nimetty volume | Bind mount |
|---|---|---|
| Missä | Dockerin hallinnoima | koneen kansio |
| Käyttö | tietokannat | konfigit, koodi kehityksessä |
| Esimerkki | `pgdata:/var/lib/postgresql/data` | `./nginx.conf:/etc/nginx/nginx.conf` |

<div class="tip">Jos polussa on kaksoispiste, <code>-v</code> ei toimi koska se käyttää kaksoispistettä erottimena.</div>

## Varmuuskopio

```bash
# postgres
docker compose exec db pg_dump -U notes notes > backup.sql

# koko volume tar-tiedostoksi
docker run --rm -v pgdata:/data -v "$PWD":/backup alpine tar czf /backup/pgdata.tgz -C /data .
```
