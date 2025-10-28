from django.shortcuts import render
from django.http import HttpResponse
from .fonctions import *
from gestionAdmin.views import creationcreneaux,gestionsportive
from staff.views import recapitulatif,inscrits,sportive
from .menus import *
import json

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
    creneaux=lecture_creneaux(datetime.datetime.now()+datetime.timedelta(days=-7))
    inscriptions=lecture_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7))
    modifiables=type_event_modifiable(request.user)
    typecreneau_modifiables={ x : typecreneau[x] for x in typecreneau if x in modifiables}
    creneaux=preparation_creneaux(request.user,creneaux,inscriptions,modifiables)
    context={"menu" : menu_navigation(request), "creneaux" : creneaux,"modifiables" : modifiables, "typecreneau" : typecreneau_modifiables}
    return render(request,'gestionCreneaux/jeulibre.html',context)

def click(request):
    response_data={}
    modifie=False
    if request.POST["cmd"]=="0":
        modifie=desinscription(request.user,request.POST["id"])
    elif request.POST["cmd"]=="1":
        modifie=inscription(request.user,request.POST["id"])
    if modifie:
        creneaux=lecture_creneaux(datetime.datetime.now()+datetime.timedelta(days=-7))
        inscriptions=lecture_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7))
        modifiables=type_event_modifiable(request.user)
        response_data["events"]=preparation_creneaux(request.user,creneaux,inscriptions,modifiables)
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

def events(request):
    creneaux=lecture_creneaux(datetime.datetime.now()+datetime.timedelta(days=-7))
    inscriptions=lecture_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7))
    modifiables=type_event_modifiable(request.user)
    tab=preparation_creneaux(request.user,creneaux,inscriptions,modifiables)
    return HttpResponse(json.dumps(tab), content_type="application/json") 
