---
title: Miten tämä on tehty
order: 80
topic: toteutus
description: Tämän sivuston rakenne: palvelut, verkot ja API.
---

# Miten tämä on tehty

Komentokirja pyörii Docker Composella. Siinä on neljä palvelua ja lisäksi Adminer, joka käynnistyy vain erikseen pyydettäessä.

| Palvelu | Mitä tekee | Portti |
|---|---|---|
| gateway | nginx, ohjaa pyynnöt oikealle palvelulle | 8080 |
| web | nginx, näyttää nämä sivut | ei julkinen |
| notes-api | Python + FastAPI, käyttäjien lisäykset | ei julkinen |
| db | PostgreSQL, tallentaa lisäykset | ei julkinen |
| adminer | tietokannan selaus, vain `--profile tools` | 8081 |

```text
selain ──► gateway :8080
              ├── /       ──► web
              └── /api/   ──► notes-api ──► db
```

## Mitä Docker-juttuja käytettiin

- jokaiselle palvelulle oma Dockerfile
- multi-stage build: web-palvelussa Markdown muutetaan HTML:ksi Python-kontissa ja valmiit sivut kopioidaan nginxiin
- notes-api ajetaan omalla käyttäjällä eikä rootilla
- healthcheckit ja `depends_on: condition: service_healthy`
- kaksi verkkoa: tietokanta on `internal`-verkossa eikä gateway näe sitä
- tietokannan data volumessa `pgdata`
- tietokannan salasana Docker secretinä
- Adminer omassa profiilissa
- notes-api:n voi skaalata: `docker compose up -d --scale notes-api=3`

## API

| Pyyntö | Mitä tekee |
|---|---|
| `GET /api/notes?topic=kontit` | yhden sivun lisäykset |
| `POST /api/notes` | uusi lisäys |
| `PUT /api/notes/{id}` | muokkaus |
| `DELETE /api/notes/{id}` | poisto |
| `GET /api/health` | terveystarkistus |

Koko rajapinnan dokumentaatio löytyy osoitteesta [/api/docs](/api/docs).

```bash
curl "localhost:8080/api/notes?topic=kontit"
```
