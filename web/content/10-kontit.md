---
title: Kontit
order: 10
topic: kontit
description: Konttien käynnistys, hallinta ja lokit.
---

# Kontit

Kontti on imagesta käynnistetty prosessi. Kontti pysyy päällä niin kauan kuin sen pääprosessi on käynnissä.

## Käynnistys

| Komento | Mitä tekee |
|---|---|
| `docker run nginx` | käynnistää kontin, terminaali jää kiinni |
| `docker run -d nginx` | käynnistää taustalle |
| `docker run -it ubuntu bash` | interaktiivinen shell |
| `docker run --rm alpine echo moi` | poistaa kontin kun se loppuu |
| `docker run --name web nginx` | antaa kontille nimen |
| `docker run -p 8080:80 nginx` | julkaisee portin, kone:kontti |
| `docker run -e NIMI=arvo alpine env` | ympäristömuuttuja |
| `docker run -v data:/data alpine` | volume kontin polkuun /data |

Esimerkki, nginx taustalle porttiin 8080:

```bash
docker run -d --name web -p 8080:80 nginx:1.27-alpine
curl localhost:8080
```

## Tila ja hallinta

| Komento | Mitä tekee |
|---|---|
| `docker ps` | käynnissä olevat kontit |
| `docker ps -a` | kaikki, myös pysähtyneet |
| `docker stop web` | pysäyttää |
| `docker start web` | käynnistää uudestaan |
| `docker restart web` | stop + start |
| `docker rm web` | poistaa (pitää olla pysäytetty) |
| `docker rm -f web` | pysäyttää ja poistaa |

## Sisälle konttiin

| Komento | Mitä tekee |
|---|---|
| `docker logs web` | lokit |
| `docker logs -f --tail 50 web` | seuraa, 50 viimeistä riviä |
| `docker exec -it web sh` | shell käynnissä olevaan konttiin |
| `docker exec web cat /etc/nginx/nginx.conf` | yksittäinen komento |
| `docker cp web:/etc/nginx/nginx.conf .` | kopioi tiedoston koneelle |
| `docker attach web` | liittyy kontin pääprosessiin |

<div class="tip"><code>docker attach</code> ja Ctrl+C pysäyttää kontin. Ctrl+P Ctrl+Q irrottaa ilman pysäytystä.</div>
