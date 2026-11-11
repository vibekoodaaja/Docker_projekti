---
title: Verkot
order: 50
topic: verkot
description: Konttien väliset verkot ja portit.
---

# Verkot

Kontit samassa itse tehdyssä verkossa löytävät toisensa nimellä. Oletus-bridge-verkossa nimet eivät toimi.

## Komennot

| Komento | Mitä tekee |
|---|---|
| `docker network ls` | listaa verkot |
| `docker network create oma` | uusi bridge-verkko |
| `docker network create --internal sisa` | verkko ilman yhteyttä ulos |
| `docker run -d --network oma --name db postgres` | kontti verkkoon |
| `docker network connect oma web` | lisää käynnissä oleva kontti verkkoon |
| `docker network disconnect oma web` | poistaa verkosta |
| `docker network inspect oma` | ketkä ovat verkossa |
| `docker network rm oma` | poistaa verkon |

## Verkkotyypit

| Tyyppi | Käyttö |
|---|---|
| bridge | oletus, yhden koneen sisäinen verkko |
| host | kontti käyttää suoraan koneen verkkoa |
| none | ei verkkoa |
| overlay | monen koneen verkko (Swarm) |

## Testaus

Väliaikainen kontti samaan verkkoon:

```bash
docker run --rm -it --network oma alpine sh
/ # ping db
/ # nc -zv db 5432
```

## Portit

`-p 8080:80` julkaisee kontin portin 80 koneen porttiin 8080. Konttien välillä käytetään aina kontin omaa porttia, ei julkaistua.
