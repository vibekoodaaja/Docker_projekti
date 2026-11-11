---
title: Imaget
order: 20
topic: imaget
description: Imagejen haku, rakentaminen ja rekisteri.
---

# Imaget

Image on paketti, josta kontteja käynnistetään. Imaget koostuvat kerroksista ja niitä säilytetään rekisterissä (esim. Docker Hub).

## Haku ja listaus

| Komento | Mitä tekee |
|---|---|
| `docker pull nginx:1.27-alpine` | hakee imagen |
| `docker images` | paikalliset imaget |
| `docker search postgres` | hakee Docker Hubista |
| `docker image history nginx` | näyttää kerrokset ja koot |
| `docker image inspect nginx` | kaikki tiedot JSONina |

Jos tagia ei anna, käytetään `latest`. Kannattaa käyttää tarkkaa versiota, niin build ei muutu yllättäen.

## Rakentaminen

| Komento | Mitä tekee |
|---|---|
| `docker build .` | rakentaa nykyisen kansion Dockerfilestä |
| `docker build -t sovellus:1.0 .` | antaa nimen ja tagin |
| `docker build -f Dockerfile.dev .` | eri Dockerfile |
| `docker build --no-cache .` | ilman välimuistia |
| `docker build --target build .` | vain tiettyyn vaiheeseen (multi-stage) |

## Rekisteriin

```bash
docker login
docker tag sovellus:1.0 kayttaja/sovellus:1.0
docker push kayttaja/sovellus:1.0
```

## Poisto

| Komento | Mitä tekee |
|---|---|
| `docker rmi nginx` | poistaa imagen |
| `docker image prune` | poistaa nimettömät (dangling) imaget |
| `docker image prune -a` | poistaa kaikki joita mikään kontti ei käytä |
