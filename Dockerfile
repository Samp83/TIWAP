FROM python:3.9-slim

# Appliquer les correctifs de securite de l'image de base (exigence du scan Trivy)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer les dependances d'abord pour profiter du cache de layers Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
