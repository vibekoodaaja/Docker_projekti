---
title: Etusivu
order: 0
topic:
---

# Komentokirja

Docker-komennot, joita tarvittiin Pilvipalvelut-kurssilla, koottuna yhteen paikkaan. Jokaisen komennon kohdalla on lyhyt selitys, ja sivujen alaosaan voi lisätä omia komentoja.

<div class="stats">
  <div class="stat"><b>{{total}}</b><span>komentoa</span></div>
  <div class="stat"><b>{{topics}}</b><span>aihetta</span></div>
  <div class="stat"><b id="stat-notes">…</b><span>käyttäjien lisäystä</span></div>
</div>

## Aiheet

<!-- cards -->

## Yleisimmät

| Komento | Mitä tekee |
|---|---|
| `docker run -d -p 8080:80 nginx` | käynnistää nginxin taustalle porttiin 8080 |
| `docker ps` | näyttää käynnissä olevat kontit |
| `docker logs -f <kontti>` | seuraa kontin lokeja |
| `docker exec -it <kontti> sh` | avaa shellin konttiin |
| `docker compose up -d --build` | rakentaa ja käynnistää compose-ympäristön |
| `docker compose down` | sammuttaa sen |
