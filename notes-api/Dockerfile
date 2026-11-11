FROM python:3.13-slim AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# requirements ensin niin cache toimii
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.13-slim

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# ei ajeta roottina
RUN useradd --system --uid 10001 app

COPY --from=builder /opt/venv /opt/venv
WORKDIR /srv
COPY app ./app

USER app
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
