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

def lecture_creneaux(debut,fin,types=None,vision=None):
    # retourne la liste des créneaux si vision=None
    # retourne une structure html sinon selon la vision demandée
    if types==None:
        liste_brut=Evenement.objects.filter(jour__gte=debut,jour__lte=fin).order_by("jour","debut")
    else:
        liste_brut=Evenement.objects.filter(jour__gte=debut,jour__lte=fin,type__in=types).order_by("jour","debut")
    if vision=="semaine":
        return vision_semaine(liste_brut)
    elif vision=="jour":
        return vision_jour(liste_brut)
    elif vision=="mois":
        return vision_mois(liste_brut)
    return liste_brut

def vision_semaine(liste):
    # retourne le code html à insérer pour une visions par semaine de la liste de créneaux
    return liste

def vision_jour(liste):
    # retourne le code html à insérer pour une visions par jour de la liste de créneaux
    return liste

def vision_mois(liste):
    # retourne le code html à insérer pour une visions par mois de la liste de créneaux
    return liste
