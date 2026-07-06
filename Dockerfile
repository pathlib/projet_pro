FROM python:3.13

WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les packages
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Lancer l'API
CMD ["uvicorn", "api.api:app", "--host", "0.0.0.0", "--port", "8000"]
