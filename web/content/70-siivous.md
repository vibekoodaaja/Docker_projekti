---
title: Siivous ja vianetsintä
order: 70
topic: siivous
description: Levytilan siivous ja yleisimmät virheet.
---

# Siivous ja vianetsintä

## Siivous

| Komento | Mitä tekee |
|---|---|
| `docker system df` | paljonko tilaa imaget, kontit ja volumet vievät |
| `docker container prune` | poistaa pysähtyneet kontit |
| `docker image prune -a` | poistaa käyttämättömät imaget |
| `docker builder prune` | tyhjentää build-välimuistin |
| `docker system prune` | kaikki ylläolevat (ei volumeja) |
| `docker system prune -a --volumes` | kaikki, myös volumet (varovasti!) |

## Vianetsintä

| Komento | Mitä tekee |
|---|---|
| `docker ps -a` | onko kontti kaatunut (Exited) |
| `docker logs <kontti>` | miksi kaatui |
| `docker inspect <kontti>` | kaikki tiedot: verkot, volumet, env |
| `docker inspect --format '{{.State.Health.Status}}' <kontti>` | healthcheckin tila |
| `docker stats` | CPU ja muisti |
| `docker top <kontti>` | prosessit kontissa |
| `docker events` | mitä dockerissa tapahtuu |

## Yleisiä virheitä

| Virhe | Syy |
|---|---|
| `port is already allocated` | portti on jo käytössä, vaihda portti |
| `502 Bad Gateway` | proxyn takana oleva palvelu ei vastaa |
| kontti sammuu heti | CMD loppuu tai kaatuu, katso lokit |
| `connection refused` | väärä hostname tai portti, tai eri verkko |
| muutos ei näy | image pitää rakentaa uudestaan (`--build`) |
| `invalid volume specification` | polussa kaksoispiste tai väärä muoto |
