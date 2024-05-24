from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import json
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)

# Charger les données
with open('data_ytb.json', 'r', encoding='utf-8') as f:
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
        # Récupérer les mots clés
        keywords = video.get("keyword",[])
        # Récupérer les tags sans "#"
        tags = video.get("snippet", {}).get("tags", [])
        tags = [tag.lower().lstrip('#') for tag in tags]
        # Récupérer le résumé
        resume = video.get("summary", []) 
        general_key = ['bitcoin', 'howtobitcoin', 'bitcoin fr', 'howtobitcoin.fr', 'btc', 'comprendre bitcoin', 'grand angle', 'crypto monnaie', 'quelle crypto choisir', 'comment marche bitcoin', 'meilleure crypto', 'prédiction prix bitcoin', 'combien vaut bitcoin', 'estimation prix bitcoin', 'prediction prix btc']
        sentence_words = sentence.split()
        sentence_filtered = [word.lower() for word in sentence_words if word not in general_key]
        sentence = ' '.join(sentence_filtered)
                    
        for tag in tags :
            keywords.append(tag)
        if keywords is None or len(keywords) == 0:
            pass
        else :
            keywords = [word.lower() for word in keywords if word not in general_key]
            #keywords = ' '.join(keywords_filtered)
        
        embeddings_1 = model.encode(chaine)
        embeddings_2 = model.encode(channel)
        similarity = embeddings_1 @ embeddings_2.T
        if similarity > 0.8:
            embeddings_3 = model.encode(sentence)
            embeddings_4 = model.encode(title)
            similarite1 = embeddings_3 @ embeddings_4.T
            if similarite1 > 0.5:
                similarite2=100
                liste_vid.append((title, num, similarite2, channel, sentence))
            else :
                if keywords is None or len(keywords) == 0:
                        pass
                else :

                    sentence_words = sentence.split()
                    # Supprimer les mots présents dans les mots clés de sentence
                    sentence_filtered = [word.lower() for word in sentence_words if word not in keywords]
                    sentence = ' '.join(sentence_filtered)
                    #keywords = ' '.join(keywords)
                    embeddings_5 = model.encode(sentence)
                    embeddings_6= model.encode(keywords)
                    similarite1 = embeddings_5 @ embeddings_6.T
                    if any(similarite1) > 0.5 :
                        similarite2=70
                        liste_vid.append((title, num, similarite2, channel,sentence))
                        if resume is None or len(resume) == 0:
                            pass
                        else:
                            embeddings_7 = model.encode(resume)
                            similarite2 = embeddings_5 @ embeddings_7.T
                            if similarite2 > 0.2:
                                similarite2=int(similarite2*100)
                                liste_vid.append((title, num, similarite2, channel,sentence))


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
        message = "Il n'y a pas de résultats associé à votre recherche."
    
    # Afficher les résultats
    return render_template('resultats_ytb.html', resultat=resultat, phrase=phrase,chaine=chaine,message=message)

if __name__ == '__main__':
    app.run(debug=True)
