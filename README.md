# 🛡️ Data Anonymiser – Application Flask pour l’Anonymisation de Données CSV

Bienvenue sur **Data Anonymiser**, une application web développée avec **Flask** qui permet aux utilisateurs de **téléverser des fichiers CSV**, **sélectionner les colonnes sensibles**, et **appliquer différentes techniques d’anonymisation**. L’objectif est de protéger les données personnelles tout en gardant leur utilité.

---

## 🚀 Fonctionnalités

- 🔐 **Authentification sécurisée** : Inscription et connexion des utilisateurs.
- 📤 **Téléversement de fichiers CSV** : Interface simple pour importer des fichiers.
- 🧬 **Sélection des colonnes à anonymiser**.
- ✴️ **Techniques d’anonymisation** :
  - **Masquage** : Remplacement par des caractères (ex: `****`).
  - **Généralisation** : Transformation par plages (ex : âge → [20-30]).
  - **Permutation aléatoire** : Mélange des données d’une colonne.
- 📊 **Calcul automatique du pourcentage d’anonymisation**.

---

## 🧪 Exemple d’utilisation

1. Crée un compte ou connecte-toi.
2. Téléverse un fichier CSV contenant des données personnelles.
3. Sélectionne les colonnes à anonymiser.
4. Choisis une méthode d’anonymisation.
5. Visualise les résultats et télécharge le fichier anonymisé.

---

## 🖥️ Installation et Lancement

Assure-toi d’avoir **Python 3.8+** installé, puis exécute :

```bash
git clone https://github.com/ton-profil/data_anonymiser.git
cd data_anonymiser
pip install -r requirements.txt
python app.py

📁 Structure du projet

data_anonymiser/
│
├── app.py                   # Script principal - application Flask
├── Dockerfile               # Fichier pour le déploiement via Docker
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
│   ├── fichier_a_anonymiser.csv        # Fichier exemple (généré avec Mockaroo)
│   └── alifpdf19/           # Répertoire utilisateur avec fichiers anonymisés
│       └── fichier_anonymisé.csv
│
└── README.md                # Documentation du projet



✅ Technologies utilisées
Python & Flask 🐍

Pandas & NumPy 📊

HTML/CSS (Bootstrap) 🎨

SQLite3 (ou autre) pour la gestion des utilisateurs

📌 À venir (Roadmap)
🔐 Authentification OAuth (Google, GitHub)

📥 Export vers Excel ou JSON

📈 Visualisation avancée des impacts de l’anonymisation

📚 Intégration d’une documentation API REST

🤝 Contribuer
Tu veux contribuer ? Super !
Forke ce repo, crée une branche, code, et fais une PR 😄

📄 Licence
Ce projet est sous licence MIT.
Libre à toi de le modifier, le réutiliser ou t’en inspirer.

🧑‍💻 Auteur
ALI SEKANDER Alif					                                     
PROVENT Amaury
ZERROUK Samuel
LAMINE-KONE Mohammed    

