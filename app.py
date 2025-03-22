import os
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Utilisateur déjà existant")

        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            return redirect(url_for('upload'))

        return render_template('login.html', error="Identifiants incorrects")

    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('upload.html', error="Veuillez sélectionner un fichier.")

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)
        return render_template('column_selection.html', columns=df.columns.tolist(), filename=file.filename)

    return render_template('upload.html')

@app.route('/process_csv', methods=['POST'])
def process_csv():
    filename = request.form.get('filename')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath).sample(frac=1).reset_index(drop=True)

    generalize_cols = request.form.getlist('generalize_cols')

    for col in generalize_cols:
        interval_size_str = request.form.get(f'interval_{col}')

        try:
            interval_size = float(interval_size_str)
            if interval_size <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return render_template('column_selection.html', columns=df.columns.tolist(),
                                   filename=filename, error=f"Intervalle invalide pour '{col}'.")

        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            col_min = np.floor(df[col].min() / interval_size) * interval_size
            col_max = np.ceil(df[col].max() / interval_size) * interval_size
            if col_min == col_max:
                col_max += interval_size
            bins = np.arange(col_min, col_max + interval_size, interval_size)
            labels = [f"[{int(bins[i])}; {int(bins[i+1])})" for i in range(len(bins)-1)]
            df[col] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)

    mask_cols = request.form.getlist('mask_cols')
    for col in mask_cols:
        if col in df.columns:
            df[col] = "****"

    return render_template('table.html', tables=[df.to_html(classes='table table-striped', index=False)])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
