from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer
import json
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)

# Charger les données
with open('barthez.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Charger le modèle de SentenceTransformer
model = SentenceTransformer("BAAI/bge-m3")

# Fonction de recherche
def recherche(sentence):
    liste_vid = []
    # Pour chaque vidéo
    for video in tqdm(data, desc="Traitement des transcriptions"): 
        # Récupérer le titre
        title = video.get("snippet", {}).get("localized", {}).get("title", "")
        # Récupérer l'identififiant
        num = video.get("id", "") 
        # Récupérer la transcription
        transcription = video.get("summary", []) 

        if transcription is None or len(transcription) == 0:
            pass
        else:
            embeddings_1 = model.encode(sentence)
            embeddings_2 = model.encode(transcription)
            similarity = embeddings_1 @ embeddings_2.T
            if similarity > 0.5:
                liste_vid.append((title, num, similarity))

    # Trier la liste par similarité décroissante
    liste_vid = sorted(liste_vid, key=lambda x: x[2], reverse=True)

    return liste_vid

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index_htb.html')

# Route pour le traitement du formulaire
@app.route('/traitement', methods=['POST'])
def traitement():
    # Récupérer la phrase saisie par l'utilisateur
    phrase = request.form['phrase']

    # Appeler la fonction de recherche avec la phrase de l'utilisateur
    resultat = recherche(phrase)

    # Afficher les résultats
    return render_template('resultats_htb.html', resultat=resultat, phrase=phrase)

if __name__ == '__main__':
    app.run(debug=True)
