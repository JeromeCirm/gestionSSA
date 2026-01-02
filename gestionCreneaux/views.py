from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from base.fonctions import auth
from .fonctions import *
import json

@auth(None)
def reglages(request):
    try:
        reglages=recupere_reglages(request.user)
        autorises=types_autorises(request.user)
        dico={x : {"nom" : typecreneau[x]["nom"], "checked" : x in reglages["types"]} for x in autorises}
        context={"reglages" : reglages, "types" : dico, "vues" : VUES_PROPOSEEES, "limites" : LIMITES_PROPOSEES,"admin" : is_admin(request.user)}
    except:
        return redirect('/home')
    return render(request,'gestionCreneaux/reglages.html',context)

def aide(request):
    context={"admin" : is_admin(request.user)}
    return render(request,'gestionCreneaux/aide.html',context)

def jeulibre(request):
    context={}
    try:
        reglages=recupere_reglages(request.user)
        creneaux=lecture_creneaux(datetime.datetime.now()+datetime.timedelta(days=-7),fin=datetime.datetime.now()+datetime.timedelta(days=reglages["limite"]),types=reglages["types"],enattente=reglages["enattente"])
        inscriptions=lecture_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7),fin=datetime.datetime.now()+datetime.timedelta(days=reglages["limite"]),types=reglages["types"])
        modifiables=type_event_modifiable(request.user)
        typecreneau_modifiables={ x : typecreneau[x] for x in typecreneau if x in modifiables}
        toutes_inscriptions=lecture_toutes_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7),fin=datetime.datetime.now()+datetime.timedelta(days=reglages["limite"]),types=reglages["types"])
        creneaux=preparation_creneaux(request.user,creneaux,inscriptions,modifiables,toutes_inscriptions)
        context={ "creneaux" : creneaux,"modifiables" : modifiables, "typecreneau" : typecreneau_modifiables, "reglages" : reglages, "admin" : is_admin(request.user), "connecte" : request.user.is_authenticated}
    except:
        pass  
    return render(request,'gestionCreneaux/jeulibre.html',context)

def click(request):
    response_data={}
    if request.POST["cmd"]=="0":
        desinscription(request.user,request.POST["id"])
    elif request.POST["cmd"]=="1":
        inscription(request.user,request.POST["id"])
    return HttpResponse(json.dumps(response_data), content_type="application/json") 

def events(request):
    try:
        reglages=recupere_reglages(request.user)
        creneaux=lecture_creneaux(datetime.datetime.now()+datetime.timedelta(days=-7),fin=datetime.datetime.now()+datetime.timedelta(days=reglages["limite"]),types=reglages["types"],enattente=reglages["enattente"])
        inscriptions=lecture_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7),fin=datetime.datetime.now()+datetime.timedelta(days=reglages["limite"]),types=reglages["types"])
        modifiables=type_event_modifiable(request.user)
        toutes_inscriptions=lecture_toutes_inscription(request.user,datetime.datetime.now()+datetime.timedelta(days=-7),fin=datetime.datetime.now()+datetime.timedelta(days=reglages["limite"]),types=reglages["types"])
        tab=preparation_creneaux(request.user,creneaux,inscriptions,modifiables,toutes_inscriptions)
    except:
        pass
    return HttpResponse(json.dumps(tab), content_type="application/json") 

def checkbox(request):
    Reglages.objects.filter(user=request.user,nom="types",val=request.POST["val"]).delete()
    if request.POST["status"]=="true":
        Reglages(user=request.user,nom="types",val=request.POST["val"]).save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

def enattente(request):
    Reglages.objects.filter(user=request.user,nom="enattente").delete()
    if request.POST["status"]=="true":
        val=True
    else:
        val=False
    Reglages(user=request.user,nom="enattente",bool=val).save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

def ajustevue(request):
    Reglages.objects.filter(user=request.user,nom=request.POST["key"]).delete()
    Reglages(user=request.user,nom=request.POST["key"],str=request.POST["val"]).save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

def changemdp(request):
    user=authenticate(request,username=request.user.username,password=request.POST["old"])
    if user is not None and request.POST["new"]==request.POST["newbis"]: 
        user.set_password(request.POST["new"])
        user.save()
        update_session_auth_hash(request, user)
    return HttpResponse(json.dumps(""), content_type="application/json") 

def ajustelimite(request):
    Reglages.objects.filter(user=request.user,nom="limite").delete()
    Reglages(user=request.user,nom="limite",val=request.POST["val"]).save()
    return HttpResponse(json.dumps(""), content_type="application/json") 
