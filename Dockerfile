FROM python:3.12-slim

WORKDIR /app

# Installera dependencies först (för bättre cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera resten av koden
COPY . .

ENV PORT=5000
EXPOSE 5000

# Kör med gunicorn i container
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]