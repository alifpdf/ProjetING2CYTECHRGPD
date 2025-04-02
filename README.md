Anonymisation de Données CSV – Application Flask

Cette application web permet aux utilisateurs de téléverser un fichier CSV, d'appliquer des techniques d’anonymisation (masquage, généralisation, permutation), puis de visualiser les résultats et le pourcentage d’anonymisation.

Fonctionnalités:
  -Authentification (inscription / connexion)
  -Téléversement de fichiers CSV
  -Sélection de colonnes à anonymiser :
  -Masquage (****)
  -Généralisation par intervalle (pd.cut)
  -Permutation aléatoire
  -Calcul du pourcentage d’anonymisation

Lancement dans le terminal:
  -pip install -r requirements.txt
  -python app.py
