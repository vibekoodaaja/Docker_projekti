-- notes = käyttäjien lisäämät komennot
-- title = komento, body = selitys, topic = sivu
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    author VARCHAR(50) NOT NULL,
    topic VARCHAR(50) NOT NULL DEFAULT 'yleinen',
    title VARCHAR(200) NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- testidataa
INSERT INTO notes (author, topic, title, body) VALUES
  ('aapo', 'kontit', 'docker run -it --rm python:3.13 python', 'nopea python-tulkki ilman asennusta'),
  ('aapo', 'compose', 'docker compose logs -f --tail 20', 'kaikkien palvelujen lokit, 20 viimeistä riviä'),
  ('aapo', 'siivous', 'docker ps -aq | xargs docker rm -f', 'poistaa kaikki kontit');
