from gestionCreneaux.models import *
from gestionCreneaux.settings import *
import datetime

def creation_tournoi(type,categorie,ladate,referents=[],events=[]):
    obj=Tournoi(type=type,categorie=categorie)
    obj.save()
    for x in referents:
        obj.referents.add(x)
    laliste=[]
    for (decalage,heuredebut,heurefin,nbterrains,description) in events:
        if description=="":
            description="tournoi "+type+" "+categorie
        laliste.append(Evenement(type=EVENT_TOURNOI,nom=type+" "+categorie[0],description=description,jour=ladate+datetime.timedelta(days=decalage),debut=datetime.time(heuredebut),fin=datetime.time(heurefin),nb_terrains=nbterrains,code_couleur=COULEUR_TOURNOI,besoin_staff="0"))
    Evenement.objects.bulk_create(laliste)
    obj.save()
    Sportive(texte="declaration BVS",tournoi=obj,debut=ladate+datetime.timedelta(days=-20),deadline=ladate+datetime.timedelta(days=-15)).save()
    Sportive(texte="resultats à rentrer",tournoi=obj,debut=ladate+datetime.timedelta(days=0),deadline=ladate+datetime.timedelta(days=3)).save()
    Sportive(texte="prize money à distribuer",tournoi=obj,debut=ladate+datetime.timedelta(days=0),deadline=ladate+datetime.timedelta(days=15)).save()
    Sportive(texte="mail aux participants",tournoi=obj,debut=ladate+datetime.timedelta(days=-7),deadline=ladate+datetime.timedelta(days=-3)).save()
