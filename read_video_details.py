# affiche tous les titres des vidéos du fichier json mis en paramètre
# le code passé en commentaires affiche les informations d'un fichier contenant une seule video que l'utilsateur à demandé

import json 

filename="UCjlxqqxeG5HtvKR5zX88Y1w.json"

def open_file(filename):
    with open(filename, 'r') as read_json_file:
        data=json.load(read_json_file)
    return data

data=open_file(filename)

for video in data:
    # Accéder au titre de la vidéo dans le snippet
    titre_video = video["snippet"]["title"]
    print(titre_video)
    


"""
items=data['items']

if items:
    video=items[0]
    
    #------------------informations sur la vidéo-------------------
    snippet=video["snippet"]
    
    publishedAt=snippet["publishedAt"]
    #channelId=snippet["channelId"]
    title=snippet["title"]
    description=snippet["description"]
    #thumbnails=snippet["thumbnails"]
    channelTitle=snippet["channelTitle"]
    tags=snippet["tags"]
    #categoryId=snippet["categoryId"]
    #liveBroadcastContent=snippet["liveBroadcastContent"]
    #localized=snippet["localized"]

    
    #-----------------statistiques de la vidéo-------------------
    statistics=video["statistics"]

    viewCount=statistics["viewCount"]
    likeCount=statistics["likeCount"]
    favoriteCount=statistics["favoriteCount"]
    commentCount=statistics["commentCount"]

else:
    print("Aucune vidéo dans le fichier demandé")


continuer=input("Souhaitez-vous obtenir des informations sur la video ? [y/n]")

while continuer=="y":
    print("\nInformations disponibles:\n1. Titre de la vidéo\n2. Description\n3. Nom de la chaine\n4. Tags de la vidéo\n5. Nombre de vues\n6. Nombre de likes\n7. Nombre de favoris\n8. Nombre de commentaires")
    print("\nQue souhaitez vous obtenir (entrez le chiffre correspondant)")


    demande=input()

    if demande == "1":
        print("le titre de la vidéo est : ",title)
    elif demande == "2":
        print("la description de la vidéo est : ",description)
    elif demande == "3":
        print("le nom de la chaine est : ",channelTitle)
    elif demande == "4":
        print("les tags de la vidéo sont : ",tags)
    elif demande == "5":
        print("la video compte ",viewCount,' vues')
    elif demande == "6":
        print("la vidéo a ",likeCount," likes")
    elif demande == "7":
        print("la vidéo a été mise ",favoriteCount," fois en favoris")
    elif demande == "8":
        print("la vidéo compte ",commentCount," commentaires")
    else:
        print("erreur dans le chiffre demandé")

    continuer=input("Souhaitez-vous d'autres informations ? [y/n]")



"""