---
title: Dockerfile
order: 30
topic: dockerfile
description: Dockerfilen ohjeet ja esimerkit.
---

# Dockerfile

Dockerfile on ohje, jonka mukaan `docker build` tekee imagen.

## Ohjeet

| Ohje | Mitä tekee |
|---|---|
| `FROM python:3.13-slim` | pohjaimage |
| `WORKDIR /app` | työkansio |
| `COPY . .` | kopioi tiedostot imageen |
| `RUN pip install -r requirements.txt` | ajetaan buildin aikana |
| `ENV PORT=8000` | ympäristömuuttuja |
| `EXPOSE 8000` | kertoo portin (ei julkaise sitä) |
| `USER app` | millä käyttäjällä ajetaan |
| `HEALTHCHECK CMD curl -f localhost/` | terveystarkistus |
| `CMD ["python", "app.py"]` | komento kun kontti käynnistyy |
| `ENTRYPOINT ["python"]` | kiinteä komento, CMD antaa parametrit |

## Esimerkki: Python-sovellus

```dockerfile
FROM python:3.13-slim
WORKDIR /app

# ensin requirements, niin pip install pysyy välimuistissa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd app
USER app

CMD ["python", "app.py"]
```

## Multi-stage

Ensimmäisessä vaiheessa rakennetaan, toiseen kopioidaan vain valmis lopputulos. Image jää pienemmäksi.

```dockerfile
FROM node:20 AS build
WORKDIR /app
COPY . .
RUN npm ci && npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

## Vinkkejä

- `.dockerignore`-tiedosto, ettei `node_modules` tms. mene build-kontekstiin
- harvoin muuttuvat asiat Dockerfilen alkuun
- ei salasanoja imageen
- ei roottina jos ei ole pakko
