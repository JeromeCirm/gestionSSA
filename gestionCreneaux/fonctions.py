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

