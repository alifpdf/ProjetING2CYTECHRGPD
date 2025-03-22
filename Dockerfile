# Base image Python 3.11
FROM python:3.11-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances nécessaires
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie des fichiers du projet
COPY . .

# Création du dossier uploads (pour fichiers CSV)
RUN mkdir -p uploads

# Exposition du port Flask (5000 par défaut)
EXPOSE 5000

# Commande pour lancer l'application Flask
CMD ["python", "app.py"]
