import datetime
from re import U
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from django.db.models.functions import Lower
from .models import *
from .settings import *
from base.settings import TITRE_SITE
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
    
def autorise_menu(user,menu):
    # teste si on autorise ce menu pour l'utilisateur 
    lesgroupes=user.groups.all()
    if user.is_superuser:
        return True
    for x in menu.groupes.all():
        if x in lesgroupes:
            return True
    return False

def menu_navigation(request):
    # liste des menus accessibles à l'utilisateur connecté
    liste=Menu.objects.all().order_by('ordre')
    tableau=[]
    for item in liste : 
        if item.parent==0 and (item.nom=="Jeu Libre" or autorise_menu(request.user,item)):
            subtableau=[]
            for subitem in liste : 
                if subitem.parent==item.id and autorise_menu(request.user,subitem):
                    subtableau.append((subitem.nom,subitem.id,subitem.fonction,False))
            tableau.append((item.nom,item.id,item.fonction,subtableau))
    return tableau

def lecture_creneaux(debut,fin=None,types=None):
    # retourne la liste des créneaux 
    liste_brut=Evenement.objects.filter(jour__gte=debut).order_by("jour","debut")
    if types!=None:
        liste_brut=liste_brut.filter(type__in=types)
    if fin!=None:
        liste_brut=Evenement.objects.filter(jour__lte=fin)
    return liste_brut

def lecture_inscription(user,debut,fin=None,types=None):
    # retourne un dictionnaire {id : [liste de rôle]}
    if not user.is_authenticated:
        return defaultdict(list)
    liste_brut=Inscription.objects.filter(user=user,event__jour__gte=debut)
    if types!=None:
        liste_brut=liste_brut.filter(event__type__in=types)
    if fin!=None:
        liste_brut=Evenement.objects.filter(event__jour__lte=fin)
    res=defaultdict(list)
    for x in liste_brut:
        res[x.event.id].append(x.role)
    return res

def preparation_creneaux(user,creneaux,inscriptions):
    # création d'une liste d'event pour FullCalendar à partir de creneaux
    res=[]
    gestionnaire=gestion(user)
    for x in creneaux:
        dico={}
        dico["title"]=x.nom
        # format YYYY-MM-DDTHH:MM:SS,   ex : 2025-10-25T09:00:00
        dico["start"]=f"{x.jour.year:04d}-{x.jour.month:02d}-{x.jour.day:02d}T{x.debut.hour:02d}:{x.debut.minute:02d}:00"
        dico["end"]=f"{x.jour.year:04d}-{x.jour.month:02d}-{x.jour.day:02d}T{x.fin.hour:02d}:{x.fin.minute:02d}:00"
        # la classe de l'évent pour changer la couleur de fond par exemple
        if x.gestionnaires==0:
            dico["classNames"]=['event-enattente']
        else:
            dico["classNames"]=[x.css]
        dico["id"]=x.id
        # le contenu du corps du modal lors du click sur l'event
        dico["body"]=x.description+f"<br>{x.nb_terrains_occupes} terrains disponibles, {x.gestionnaires} gestionnaires, id: {x.id}"
        # faire apparaitre le bouton d'inscription ? oui si non vide
        if x.gestionnaires!=-1:
            if gestionnaire:
                # bouton pour gestionnaire
                if (ROLE_INSCRIT not in inscriptions[x.id]) or (ROLE_STAFF not in inscriptions[x.id]): 
                    dico["inscription"]="s'inscrire"
                    dico["cmd"]=1
                else:
                    dico["inscription"]="se désinscrire"
                    dico["cmd"]=0
            elif (x.avec_inscription and x.gestionnaires!=0):
                # bouton pour simple utilisateur
                if ROLE_INSCRIT in inscriptions[x.id]:
                    dico["inscription"]="se désinscrire"
                    dico["cmd"]=0
                else:
                    dico["inscription"]="s'inscrire"
                    dico["cmd"]=1
        res.append(dico)
    return res

def gestion(user,event=None):
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
    return res

def desinscription(user,id):
    event=Evenement.objects.get(id=id)
    liste=Inscription.objects.filter(user=user,event=event)
    if len(liste)>0:
        liste.delete()
        event.gestionnaires=len(Inscription.objects.filter(event=event,role=ROLE_STAFF))
        event.inscrits=len(Inscription.objects.filter(event=event,role=ROLE_INSCRIT))
        event.save()
        return True
    return False
