import datetime
from re import U
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.db.models.functions import Lower
from .models import *
from .settings import *
from base.fonctions import auth
from gestionSSA.settings import DEBUG
from collections import defaultdict

if DEBUG:
    def debug(*args):
        print(*args)
else:
    def debug(*args):
        pass

#fonctions générales
def jolie_date(date):
    return date.strftime('%A %e %B')

def lecture_creneaux(debut,fin=None,types=None,enattente=False):
    # retourne la liste des créneaux 
    liste_brut=Evenement.objects.filter(jour__gte=debut).order_by("jour","debut")
    if not enattente:
        liste_brut=liste_brut.exclude(gestionnaires=0)
    if types!=None:
        liste_brut=liste_brut.filter(type__in=types)
    if fin!=None:
        liste_brut=liste_brut.filter(jour__lte=fin)
    return liste_brut

def lecture_inscription(user,debut,fin=None,types=None):
    # retourne un dictionnaire {id : [liste de rôle]}
    if not user.is_authenticated:
        return defaultdict(list)
    liste_brut=Inscription.objects.filter(user=user,event__jour__gte=debut)
    if types!=None:
        liste_brut=liste_brut.filter(event__type__in=types)
    if fin!=None:
        liste_brut=liste_brut.filter(event__jour__lte=fin)
    res=defaultdict(list)
    for x in liste_brut:
        res[x.event.id].append(x.role)
    return res

def lecture_toutes_inscription(user,debut,fin=None,types=None):
    # retourne un dictionnaire {id : [liste de rôle]}
    if not gestion(user):
        return []
    liste_brut=Inscription.objects.filter(event__jour__gte=debut)
    if types!=None:
        liste_brut=liste_brut.filter(event__type__in=types)
    if fin!=None:
        liste_brut=liste_brut.filter(event__jour__lte=fin)
    res=defaultdict(list)
    for x in liste_brut:
        res[x.event.id].append((x.user.id,x.role))
    return res

def preparation_creneaux(user,creneaux,inscriptions,modifiables,toutes_inscriptions):
    # création d'une liste d'event pour FullCalendar à partir de creneaux
    res=[]
    gestionnaire=gestion(user)  # à gérer par event éventuellement ? staff pour l'instant
    for x in creneaux:
        dico={}
        dico["id"]=x.id
        dico["nom"]=x.nom
        if x.avec_inscription:
            dico["title"]=x.nom+', '+str(x.inscrits)+' ins, '+str(x.nb_terrains_occupes)+"T"
        else:
            dico["title"]=x.nom+', '+str(x.nb_terrains_occupes)+"T"
        # format YYYY-MM-DDTHH:MM:SS,   ex : 2025-10-25T09:00:00
        dico["start"]=f"{x.jour.year:04d}-{x.jour.month:02d}-{x.jour.day:02d}T{x.debut.hour:02d}:{x.debut.minute:02d}:00"
        dico["end"]=f"{x.jour.year:04d}-{x.jour.month:02d}-{x.jour.day:02d}T{x.fin.hour:02d}:{x.fin.minute:02d}:00"
        # la classe de l'évent pour changer la couleur de fond par exemple
        if x.gestionnaires==0:
            dico["classNames"]=['event-enattente']
        else:
            dico["classNames"]=[x.css]
        # faire apparaitre le bouton d'inscription ?
        if (x.avec_inscription and x.gestionnaires!=0):
            if (ROLE_INSCRIT not in inscriptions[x.id]) or (gestionnaire and x.gestionnaires!=-1 and (ROLE_STAFF not in inscriptions[x.id])): 
                    dico["inscription"]="s'inscrire"
                    dico["cmd"]=1
            else:
                    dico["inscription"]="se désinscrire"
                    dico["cmd"]=0
        elif gestionnaire and x.gestionnaires!=-1:
            if ROLE_STAFF not in inscriptions[x.id]: 
                    dico["inscription"]="s'inscrire"
                    dico["cmd"]=1
            else:
                    dico["inscription"]="se désinscrire"
                    dico["cmd"]=0
        # on peut modifier le créneau ?
        dico["creneaux_modifiable"]=x.type in modifiables
        # les champs à afficher/utiles pour la modif
        dico["description"]=x.description
        dico["nb_terrains"]=x.nb_terrains
        dico["avec_inscription"]=x.avec_inscription
        s=""
        if gestionnaire:
            if x.gestionnaires!=-1:
                s="<br>en gestion : "
                for id,role in toutes_inscriptions[x.id]:
                    if role==ROLE_STAFF:
                        ungestionnaire=User.objects.get(id=id)
                        s+=ungestionnaire.first_name+' '+ungestionnaire.last_name+' '
            if x.avec_inscription:
                s+="<br>inscrit(e)s : "
                for id,role  in toutes_inscriptions[x.id]:
                    if role==ROLE_INSCRIT:
                        ungestionnaire=User.objects.get(id=id)
                        s+=ungestionnaire.first_name+' '+ungestionnaire.last_name+', '
        else:
            if x.avec_inscription:
                s='<br>'+str(x.inscrits)+" inscrit(e)s"
        dico["lesinscrits"]=s
        dico["ouvert"]=x.gestionnaires==-1
        dico["type"]=x.type
        res.append(dico)
    return res

def gestion(user,event=None):
    # print : la première ligne n'est utile que pour la remise_a_zero car les groupes ne sont pas importés
    groupe_staff=Group.objects.get(name="staff")
    return user.is_authenticated and (groupe_staff in user.groups.all())

def inscription(user,id):
    event=Evenement.objects.get(id=id)
    liste=Inscription.objects.filter(user=user,event__id=id)
    res=False
    if gestion(user,event):
        if event.gestionnaires!=-1 and len(liste.filter(role=ROLE_STAFF))==0:
            Inscription(user=user,event=event,role=ROLE_STAFF).save()
            event.gestionnaires=len(Inscription.objects.filter(event=event,role=ROLE_STAFF))
            event.save()
            res=True
    if len(liste.filter(role=ROLE_INSCRIT))==0:
            Inscription(user=user,event=event,role=ROLE_INSCRIT).save()
            event.inscrits=len(Inscription.objects.filter(event=event,role=ROLE_INSCRIT))
            event.save() 
            res=True
    return res # print - try  .   inutilisé pour l'instant

def desinscription(user,id):
    event=Evenement.objects.get(id=id)
    liste=Inscription.objects.filter(user=user,event=event)
    if len(liste)>0:
        liste.delete()
        if event.gestionnaires!=-1:
            event.gestionnaires=len(Inscription.objects.filter(event=event,role=ROLE_STAFF))
        event.inscrits=len(Inscription.objects.filter(event=event,role=ROLE_INSCRIT))
        event.save()
        return True
    return False # print - try  .  inutilisé pour l'instant

def type_event_modifiable(user):
    # retourne la liste des créneaux que la personne peut créer
    res=[]
    for x in user.groups.all():
        if x==groupe_creation_jeulibre:
            res.append(EVENT_JEULIBRE)
            res.append(EVENT_JEULIBRE_ADHERENTS)
        if x==groupe_creation_entrainement:
            res.append(EVENT_ENTRAINEMENT)
        if x==groupe_creation_tournois:
            res.append(EVENT_TOURNOI)
        if x==groupe_creation_entrainement_avalider:
            res.append(EVENT_ENTRAINEMENT_A_VALIDER)
    return res

def recupere_reglages(user):
    res={"types" : DEFAULT_TYPES, "ordi" : DEFAULT_ORDI, "tel" : DEFAULT_TEL, "enattente" : DEFAULT_ENATTENTE,"limite" : DEFAULT_LIMITE, "limite_avant" : DEFAULT_LIMITE_AVANT}
    if not user.is_authenticated:
        return res
    reglages=Reglages.objects.filter(user=user)
    res["types"]=[]
    for x in reglages:
        if x.nom=="types":
            res["types"].append(x.val)
        elif x.nom=="ordi":
            res["ordi"]=x.str
        elif x.nom=="tel":
            res["tel"]=x.str
        elif x.nom=="enattente":
            res["enattente"]=x.bool
        elif x.nom=="limite":
            res["limite"]=x.val
        elif x.nom=="limite_avant":
            res["limite_avant"]=x.val
    return res

def is_admin(user):
    if user.is_authenticated:
        return groupe_admin in user.groups.all()
    return False

def types_autorises(user):
    # renvoie les types de créneau que la personne a le droit de voir
    return [EVENT_JEULIBRE,EVENT_ENTRAINEMENT,EVENT_TOURNOI]
