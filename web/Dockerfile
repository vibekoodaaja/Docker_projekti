# 1. vaihe: tehään markdownista html
FROM python:3.13-slim AS build
RUN pip install --no-cache-dir markdown==3.7
WORKDIR /src
COPY . .
RUN python build.py /dist

# 2. vaihe: pelkkä nginx ja valmiit sivut
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /dist /usr/share/nginx/html

HEALTHCHECK --interval=15s --timeout=3s CMD wget -qO- http://127.0.0.1/ || exit 1

EXPOSE 80
