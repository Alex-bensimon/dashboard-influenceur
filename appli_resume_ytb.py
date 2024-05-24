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
def recherche(sentence,chaine):
    liste_vid = []
    
    # Pour chaque vidéo
    for video in tqdm(data, desc="Traitement des transcriptions"): 
        # Récupérer le titre
        title = video.get("snippet", {}).get("title", "")
        # Récupérer l'identififiant
        num = video.get("id", "")
        # Récupérer le nom de la chaine
        channel = video.get("snippet", {}).get("channelTitle", "") 
        # Récupérer le résumé
        resume = video.get("summary", []) 
        
        # Comparaison des nom de chaine
        embeddings_1 = model.encode(chaine)
        embeddings_2 = model.encode(channel)
        similarity = embeddings_1 @ embeddings_2.T
        if similarity > 0.8:

            # Vérification de la contenance des résumés
            if resume is None or len(resume) == 0:
                pass
            else:

                # Comparaison des résumés
                embeddings_3 = model.encode(resume)
                embeddings_4 = model.encode(resume)
                similarite2 = embeddings_3 @ embeddings_4.T
                if similarite2 > 0.5:
                    similarite2=int(similarite2*100)
                    liste_vid.append((title, num, similarite2,channel))
    
    # Trier la liste par similarité décroissante
    liste_vid = sorted(liste_vid, key=lambda x: x[2], reverse=True)

    return liste_vid 

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index_ytb.html')

# Route pour le traitement du formulaire
@app.route('/traitement', methods=['POST'])
def traitement():
    # Récupérer la phrase saisie par l'utilisateur
    phrase = request.form['phrase']
    chaine = request.form['chaine']

    # Appeler la fonction de recherche avec la phrase de l'utilisateur
    resultat = recherche(phrase,chaine)
    # Initialiser le message
    message = None
    if len(resultat)==0:
        message = "Il n'y a pas de chaîne youtube associé à votre recherche."
    
    # Afficher les résultats
    return render_template('resultats_ytb.html', resultat=resultat, phrase=phrase,chaine=chaine,message=message)

if __name__ == '__main__':
    app.run(debug=True)
