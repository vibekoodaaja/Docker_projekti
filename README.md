# Komentokirja

Pilvipalvelut-kurssin projekti. Docker-komennot aiheittain (cheatsheet) ja jokaiselle sivulle voi lisätä omia komentoja.

## Käynnistys

```
./kaynnista.sh
```

tai

```
head -c 24 /dev/urandom | base64 > secrets/db_password.txt
cp .env.example .env
docker compose up -d --build
```

Sivu: http://localhost:8080
API docs: http://localhost:8080/api/docs
Adminer: `docker compose --profile tools up -d` -> http://localhost:8081

Sammutus: `./lopeta.sh`

## Palvelut

- gateway - nginx, ohjaa / -> web ja /api/ -> notes-api
- web - sivut, tehdään markdownista (web/content)
- notes-api - python + fastapi, käyttäjien lisäämät komennot
- db - postgres
- adminer - valinnainen

## API

- GET /api/notes (?topic= ?author=)
- GET /api/notes/{id}
- POST /api/notes
- PUT /api/notes/{id}
- DELETE /api/notes/{id}
- GET /api/health

## Uusi sivu

Lisää web/content kansioon .md tiedosto ja aja `docker compose up -d --build web`.

Huom: jos kansion nimessä on kaksoispiste niin bind mountit ei toimi, siksi configit on kopioitu imageihin.
