from gestionCreneaux.models import *
from gestionCreneaux.settings import *
import datetime

def creation_tournoi(type,categorie,ladate,events,ouvert=True,referents=[]):
    # création d'un tournoi : 
    # il faut un moins un event associé sinon on ne fait rien (plusieurs si AM/PM ou plusieurs jours)
    if len(events)==0: 
        return
    if ouvert:
        gestionnaires=-1
    else:
        gestionnaires=0
    obj=Tournoi(type=type,categorie=categorie)
    obj.save()
    for x in referents:
        obj.referents.add(x)
    laliste=[]
    for (decalage,heuredebut,heurefin,nbterrains,description) in events:
        if description=="":
            description="tournoi "+type+" "+categorie
        laliste.append(Evenement(type=EVENT_TOURNOI,nom=type+" "+categorie[0],description=description,jour=ladate+datetime.timedelta(days=decalage),debut=datetime.time(heuredebut),fin=datetime.time(heurefin),nb_terrains=nbterrains,css='event-tournoi',gestionnaires=gestionnaires))
    Evenement.objects.bulk_create(laliste)
    obj.save()
    Sportive(texte="declaration BVS",tournoi=obj,debut=ladate+datetime.timedelta(days=-20),deadline=ladate+datetime.timedelta(days=-15)).save()
    Sportive(texte="resultats à rentrer",tournoi=obj,debut=ladate+datetime.timedelta(days=0),deadline=ladate+datetime.timedelta(days=3)).save()
    Sportive(texte="prize money à distribuer",tournoi=obj,debut=ladate+datetime.timedelta(days=0),deadline=ladate+datetime.timedelta(days=15)).save()
    Sportive(texte="mail aux participants",tournoi=obj,debut=ladate+datetime.timedelta(days=-7),deadline=ladate+datetime.timedelta(days=-3)).save()

def jolie_date(date):
    return date.strftime('%A %e %B')

def ordonne(la_liste):
    D={}
    for _,value in la_liste.items():
        for x in value["present"]:
            if x in D:
                D[x]+=1
            else:
                D[x]=1
    return sorted(D.items(),key=lambda x : -x[1])

def ouverts(liste):
    proposés=0
    ouverts=0
    for x in liste:
        proposés+=1
        if liste[x]["nb"]>0:
            ouverts+=1
    D={"proposés" : proposés, "ouverts" : ouverts}
    return D

def recupere_stats_fonction(fonction,datedebut,datefin):
    les_events=Evenement.objects.all().filter(jour__gte=datetime.datetime.strptime(datedebut,'%Y-%m-%d')).filter(jour__lte=datetime.datetime.strptime(datefin,'%Y-%m-%d')).order_by('jour','debut')
    present=Inscription.objects.filter(role=ROLE_STAFF)
    res={ x.pk : {"date": jolie_date(x.jour),"intitulé" : x.nom,
    "present" : []} for x in les_events}
    for x in present:
        if x.event.pk in res:
            res[x.event.pk]["present"].append(x.user.first_name+" "+x.user.last_name)
    for x in res:
        res[x]["nb"]=len(res[x]["present"])    
    response={"creneau_et_staff" : res,"staff_en_or" : ordonne(res),"creneaux_stats" : ouverts(res)}
    #print(response)
    return response
