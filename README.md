# Data Anonymiser – Application Flask pour l’Anonymisation de Données CSV

Data Anonymiser est une application web développée avec Flask qui permet aux utilisateurs de téléverser des fichiers CSV, de sélectionner les colonnes sensibles, et d’appliquer différentes techniques d’anonymisation. L’objectif est de protéger les données personnelles tout en conservant leur utilité pour l’analyse.

---

## Fonctionnalités

- Authentification sécurisée : inscription et connexion des utilisateurs.
- Téléversement de fichiers CSV.
- Sélection des colonnes à anonymiser.
- Techniques d’anonymisation disponibles :
  - Masquage (remplacement des données par des caractères tels que ****).
  - Généralisation (ex : transformation d’un âge en tranche comme [20-30]).
  - Permutation aléatoire des données d’une colonne.
- Calcul automatique du pourcentage d’anonymisation.
- Téléchargement du fichier anonymisé.

---

## Exemple d’utilisation

1. Crée un compte ou connecte-toi.
2. Téléverse un fichier CSV contenant des données personnelles.
3. Sélectionne les colonnes à anonymiser.
4. Choisis une méthode d’anonymisation.
5. Visualise les résultats et télécharge le fichier anonymisé.

---

## Installation et Lancement

Assure-toi d’avoir Python 3.8 ou supérieur installé, puis exécute :

```bash
git clone https://github.com/ton-profil/data_anonymiser.git
cd data_anonymiser
pip install -r requirements.txt
python app.py

Structure du projet
data_anonymiser/
│
├── app.py                   # Script principal - application Flask
├── requirements.txt         # Liste des dépendances Python
│
├── instance/
│   └── users.db             # Base de données SQLite (utilisateurs)
│
├── templates/               # Templates HTML (frontend)
│   ├── index.html           # Page d’accueil
│   ├── login.html           # Page de connexion
│   ├── register.html        # Page d’inscription
│   ├── upload.html          # Téléversement du fichier CSV
│   ├── column_selection.html# Choix des colonnes et masque
│   ├── table.html           # Affichage des données
│   └── archives.html        # Liste des fichiers anonymisés
│
├── uploads/                 # Dossiers des fichiers téléversés
│   ├── MOCK_DATA.csv        # Fichier exemple (généré avec Mockaroo)
│   └── alifpdf19/           # Répertoire utilisateur avec fichiers anonymisés
│       └── anonymized_*.csv
│
└── README.md                # Documentation du projet


Technologies utilisées
langages de programmation : Python, HTML, CSS

Bibliothèques python
Pandas & NumPy

framework
SQLite3, bootstap, flask

Auteurs :
Amaury Provent
Samuel Zerrouk
Alif Ali Sekander
Mohamed Lamine Koné
