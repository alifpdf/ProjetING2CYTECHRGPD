import os  # Module pour interagir avec le système de fichiers (création, suppression, chemins)
import numpy as np  # Bibliothèque pour les calculs numériques, utilisée ici pour les intervalles
import pandas as pd  # Librairie de manipulation de données tabulaires (fichiers CSV)
from flask import Flask, request, render_template, redirect, url_for, session  # Outils principaux de Flask pour créer des routes, gérer les sessions, les formulaires, etc.
from flask_sqlalchemy import SQLAlchemy  # ORM pour interagir avec une base de données relationnelle
from pandas.core.dtypes.common import is_numeric_dtype #Vérification du type numérique
from werkzeug.security import generate_password_hash, check_password_hash  # Pour hasher et vérifier les mots de passe de manière sécurisée

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clé secrète nécessaire pour sécuriser les sessions utilisateur

# Configuration de l'application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Utilisation d'une base SQLite stockée localement
app.config['UPLOAD_FOLDER'] = 'uploads'  # Répertoire où les fichiers CSV téléversés seront stockés
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Crée le répertoire s'il n'existe pas déjà

# Connexion de la base de données à l'application
db = SQLAlchemy(app)

# Définition du modèle User pour la table utilisateurs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Clé primaire, ID unique
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nom d'utilisateur unique et requis
    email = db.Column(db.String(120), unique=True, nullable=False)  # Adresse email unique et requise
    password = db.Column(db.String(200), nullable=False)  # Mot de passe hashé

# Réinitialisation de la base de données à chaque lancement (utile pour développement)
with app.app_context():
    db_path = os.path.join(app.root_path, 'users.db')  # Chemin vers le fichier de base
    if os.path.exists(db_path):  # Si la base existe, on la supprime
        os.remove(db_path)  # Suppression du fichier de base
        print("✅ Base de données supprimée proprement")
    db.create_all()  # Création des tables selon les modèles définis
    print("✅ Base recréée, on repart sur de bonnes bases 😎")

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')  # Renvoie le template HTML de la page d'accueil

# Route d'inscription d'un nouvel utilisateur
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Si le formulaire est soumis
        username = request.form['username']  # Récupère le nom d'utilisateur
        email = request.form['email']  # Récupère l'email
        password = request.form['password']  # Récupère le mot de passe

        if User.query.filter_by(username=username).first():  # Vérifie si le pseudo existe déjà
            return render_template('register.html', error="Ce pseudo existe déjà")

        hashed_password = generate_password_hash(password)  # Hash le mot de passe pour le stocker en sécurité
        new_user = User(username=username, email=email, password=hashed_password)  # Crée l'utilisateur
        db.session.add(new_user)  # L'ajoute à la session
        db.session.commit()  # Sauvegarde en base
        print(f"✅ {username} inscrit avec succès !")
        return redirect(url_for('login'))  # Redirige vers la page de connexion

    return render_template('register.html')  # Affiche le formulaire d'inscription

# Route de connexion utilisateur
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Si le formulaire est soumis
        username = request.form['username']  # Récupère le pseudo
        password = request.form['password']  # Récupère le mot de passe

        user = User.query.filter_by(username=username).first()  # Cherche l'utilisateur en base
        if user and check_password_hash(user.password, password):  # Vérifie que le mot de passe est correct
            session['username'] = user.username  # Stocke le nom d'utilisateur en session
            print(f"✅ {username} connecté avec succès")
            return redirect(url_for('upload'))  # Redirige vers l'upload

        return render_template('login.html', error="Identifiants incorrects 🤮")  # Message d'erreur

    return render_template('login.html')  # Affiche le formulaire de connexion

# Route pour téléverser un fichier CSV
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:  # Vérifie que l'utilisateur est connecté
        return redirect(url_for('login'))  # Redirige vers la connexion

    if request.method == 'POST':  # Si le formulaire est soumis
        file = request.files.get('file')  # Récupère le fichier
        if not file or file.filename == '':  # Si aucun fichier n'est sélectionné
            return render_template('upload.html', error="Fichier manquant... tu veux pas envoyer un CSV là ? 😅")

        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])  # Répertoire propre à l'utilisateur
        os.makedirs(user_folder, exist_ok=True)  # Crée le dossier si besoin

        filepath = os.path.join(user_folder, file.filename)  # Chemin complet vers le fichier
        file.save(filepath)  # Sauvegarde du fichier
        print(f"✅ Fichier {file.filename} reçu de {session['username']}")

        df = pd.read_csv(filepath)  # Charge le CSV en DataFrame
        # Ajout d'une colonne 'id' si elle n'existe pas
        if 'id' not in df.columns:
            df.insert(0, 'id', range(1, len(df) + 1))
            df.to_csv(filepath, index=False)  # Mise à jour du fichier CSV avec la colonne id
        return render_template('column_selection.html', columns=df.columns.tolist(), filename=file.filename)  # Affiche les colonnes pour l'utilisateur

    return render_template('upload.html')  # Affiche le formulaire d'upload

# Traitement du CSV pour anonymisation
@app.route('/process_csv', methods=['POST'])
def process_csv():
    if 'username' not in session:  # Sécurité : vérifie l'identité
        return redirect(url_for('login'))

    filename = request.form.get('filename')  # Nom du fichier à traiter
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])  # Dossier utilisateur
    filepath = os.path.join(user_folder, filename)  # Chemin complet du fichier
    df_original = pd.read_csv(filepath)
    df = pd.read_csv(filepath).sample(frac=1).reset_index(drop=True)  # Mélange aléatoire des lignes

    # Traitement des colonnes à généraliser
    generalize_cols = request.form.getlist('generalize_cols')  # Liste des colonnes à généraliser
    for col in generalize_cols:
        interval_str = request.form.get(f'interval_{col}')  # Récupère l'intervalle fourni
        try:
            interval = float(interval_str)  # Conversion en float
            if interval <= 0:
                raise ValueError()  # Vérifie que l'intervalle est valide
        except (ValueError, TypeError):
            return render_template('column_selection.html', columns=df.columns.tolist(),
                                   filename=filename, error=f"Intervalle pour {col} incorrect")

        if col in df.columns and is_numeric_dtype(df[col]):  # Si la colonne est numérique
            col_min = np.floor(df[col].min() / interval) * interval  # Début de l'intervalle
            col_max = np.ceil(df[col].max() / interval) * interval  # Fin de l'intervalle
            if col_min == col_max:
                col_max += interval  # Évite les intervalles vides
            bins = np.arange(col_min, col_max + interval, interval)  # Crée les bornes
            labels = [f"[{int(bins[i])}; {int(bins[i+1])})" for i in range(len(bins) - 1)]  # Étiquettes d'intervalle
            df[col] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)  # Remplace les valeurs par leurs intervalles


    # Masquage des colonnes demandées
    mask_cols = request.form.getlist('mask_cols')  # Liste des colonnes à masquer
    for col in mask_cols:
        if col in df.columns:
            df[col] = "****"  # Remplace les valeurs par des étoiles

    # Permutation aléatoire de toutes les colonnes restantes
    for col in df.columns:
        df[col] = np.random.permutation(df[col].values)
    archive_filename = f"anonymized_{filename}"
    archive_path = os.path.join(user_folder, archive_filename)  # Chemin complet de sortie
    df.to_csv(archive_path, index=False)  # Sauvegarde du DataFrame modifié en CSV
    print(f" Fichier anonymisé sauvegardé sous {archive_filename}")

    # Fusion des DataFrames original et anonymisé en utilisant les index pour aligner les lignes
    merged_df = pd.merge(df_original, df, left_index=True, right_index=True, suffixes=('_orig', '_anon'))

    # Calcul du nombre total de cellules dans le DataFrame original
    total_rows, total_columns = df_original.shape


    # Séparation des deux DataFrames fusionnés pour comparaison facile
    original_values = merged_df.iloc[:, :total_columns].values
    anonymized_values = merged_df.iloc[:, total_columns:].values

    # Vérification cellule par cellule (True si identique, False si différent)
    comparison_array = (original_values == anonymized_values)
    print(comparison_array)

    # Une ligne est considérée anonymisée si elle a au maximum UNE cellule identique
    fully_anonymized_rows = (comparison_array.sum(axis=1) <= 1).sum()

    # Calcul du nouveau pourcentage d'anonymisation selon cette règle
    anonymization_percentage = (fully_anonymized_rows / total_rows) * 100 if total_rows else 0

    print(f" Pourcentage de lignes correctement anonymisées (tolérance 1 cellule) : {anonymization_percentage:.2f}%")

    return render_template('table.html',
                           tables=[df.to_html(classes='table table-striped', index=False)],
                           anonymization_percentage=round(anonymization_percentage, 2))# Affiche le résultat

# Route pour voir la liste des fichiers anonymisés
@app.route('/archives')
def archives():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])  # Dossier utilisateur
    os.makedirs(user_folder, exist_ok=True)
    files = os.listdir(user_folder)  # Liste les fichiers
    anonymized_files = [f for f in files if f.startswith('  anonymized_')]  # Garde seulement les anonymisés
    return render_template('archives.html', files=anonymized_files)  # Affiche la liste

# Route pour visualiser un fichier anonymisé
@app.route('/view_archive/<filename>')
def view_archive(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['username'])  # Dossier utilisateur
    filepath = os.path.join(user_folder, filename)  # Chemin vers le fichier

    if not os.path.exists(filepath):  # Vérifie que le fichier existe
        return "Oups... Fichier introuvable", 404

    df = pd.read_csv(filepath)  # Lecture du fichier
    return render_template('table.html', tables=[df.to_html(classes='table table-striped', index=False)])  # Affiche le contenu

# Déconnexion de l'utilisateur
@app.route('/logout')
def logout():
    session.pop('username', None)  # Supprime l'utilisateur de la session
    return redirect(url_for('index'))  # Retour à l'accueil





# Démarrage de l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Exécution du serveur en mode debug
