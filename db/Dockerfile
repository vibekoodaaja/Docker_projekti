FROM postgres:17-alpine

# ajetaan vaan ekalla kerralla kun volume on tyhjä
COPY init.sql /docker-entrypoint-initdb.d/01-init.sql

HEALTHCHECK --interval=5s --timeout=3s --retries=10 CMD pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" || exit 1
