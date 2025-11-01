from django.shortcuts import render
from base.fonctions import auth
from django.http import HttpResponse
import json
from gestionCreneaux.models import Evenement
from gestionCreneaux.settings import typecreneau
from .fonctions import *

def creation_modification(request):
    res=[]
    id=int(request.POST["id"])
    options=json.loads(request.POST["options"])
    type=int(request.POST["type"])
    jour=request.POST["date"]
    debut=request.POST["debut"]
    fin=request.POST["fin"]
    nb_terrains=request.POST["nb_terrains"]
    nb_terrains_occupes=nb_terrains
    avec_inscription="avec_inscription" in options
    if avec_inscription:
        css=typecreneau[type]["cssins"]
    else:
        css=typecreneau[type]["css"]    
    if "ouvert" in options:
        gestionnaires=-1
    else:
        gestionnaires=0
    nom=request.POST["titre"]
    description=request.POST["description"]
    type=type%100
    if id==-1:
        # création de créneau
        Evenement(type=type,nom=nom,description=description,jour=jour,debut=debut,fin=fin,nb_terrains=nb_terrains,nb_terrains_occupes=nb_terrains_occupes,gestionnaires=gestionnaires,avec_inscription=avec_inscription,css=css).save()
    else:
        # modification de créneau
        Evenement.objects.filter(id=id).update(type=type,nom=nom,description=description,jour=jour,debut=debut,fin=fin,nb_terrains=nb_terrains,nb_terrains_occupes=nb_terrains_occupes,gestionnaires=gestionnaires,avec_inscription=avec_inscription,css=css)
    return HttpResponse(json.dumps(res), content_type="application/json") 

def suppression(request):
    Evenement.objects.filter(id=request.POST['id']).delete()
    res=[]
    return HttpResponse(json.dumps(res), content_type="application/json") 

def admin(request):
    context={ "adherents" : User.objects.all().exclude(is_staff=True)}
    return render(request,'gestionAdmin/admin.html',context)

def recupere_info(request):
    user=User.objects.get(id=request.POST["id"])
    res={
        "id" : user.id,
        "first_name" : user.first_name ,
        "last_name" : user.last_name ,
        "email" : user.email ,
        "groupes" : [x.name for x in user.groups.all()],
        "touslesgroupes" : [x.name for x in Group.objects.all().order_by("-name")]
    }
    return HttpResponse(json.dumps(res), content_type="application/json") 

def change_info(request):
    user=User.objects.get(id=request.POST["id"])
    group_names=json.loads(request.POST["groupes"])
    lesgroups = Group.objects.filter(name__in=group_names)
    user.groups.set(lesgroups)    
    user.save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

