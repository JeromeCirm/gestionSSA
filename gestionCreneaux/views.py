from django.shortcuts import render
from django.http import HttpResponse
from .fonctions import *
from gestionAdmin.views import creationcreneaux,gestionsportive
from staff.views import recapitulatif,inscrits,sportive
from .menus import *

@auth(None)
def menu(request,numero):
    context={"menu":menu_navigation(request)}
    context["titresite"]=TITRE_SITE
    if True : #try:
        lemenu=Menu.objects.get(pk=numero) 
        if autorise_menu(request.user,lemenu):
            nom_fonction=str(lemenu.fonction)
            if nom_fonction in liste_menus_defaut:
                return globals()[str(nom_fonction)](request,numero,context)
        return redirect('/home')
    #except: 
        debug('erreur dans la fonction : enlever try except de la fonction menu de views.py')
        return redirect('/home')

def reglages(request):
    context={"menu" : menu_navigation(request)}
    return render(request,'gestionCreneaux/reglages.html',context)

def jeulibre(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'gestionCreneaux/jeulibre.html',context)
