from django.shortcuts import render
from base.fonctions import auth
from django.http import HttpResponse
import json
from gestionCreneaux.models import Evenement
from gestionCreneaux.settings import typecreneau
from .fonctions import *
from gestionCreneaux.fonctions import is_admin
from dateutil.relativedelta import relativedelta

@auth([groupe_admin])
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
        dt1=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(debut, "%H:%M").time())
        dt2=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(fin, "%H:%M").time())
        if dt2 >=dt1+ datetime.timedelta(minutes=30):
            typerepetition=request.POST["typerepetition"]
            nbrepetition=int(request.POST["nbrepetition"])
            if nbrepetition<1 or nbrepetition>50:
                nbrepetition=1
            if typerepetition=="jour":
                deltarepetition=datetime.timedelta(days=1)
            elif typerepetition=="semaine":
                deltarepetition=datetime.timedelta(weeks=1)
            elif typerepetition=="mois":
                deltarepetition=relativedelta(months=1)
            format_date = "%Y-%m-%d"
            date_obj = datetime.datetime.strptime(jour, format_date)
            for rep in range(nbrepetition):
                nouvelle_date = date_obj + deltarepetition*rep
                jourrep=nouvelle_date.strftime(format_date)
                Evenement(type=type,nom=nom,description=description,jour=jourrep,debut=debut,fin=fin,nb_terrains=nb_terrains,nb_terrains_occupes=nb_terrains_occupes,gestionnaires=gestionnaires,avec_inscription=avec_inscription,css=css).save()
    else:
        # modification de créneau
        dt1=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(debut, "%H:%M").time())
        dt2=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(fin, "%H:%M").time())
        if dt2 >=dt1+ datetime.timedelta(minutes=30):
            # à condition que le créneau fasse au moins 30mn
            Evenement.objects.filter(id=id).update(type=type,nom=nom,description=description,jour=jour,debut=debut,fin=fin,nb_terrains=nb_terrains,nb_terrains_occupes=nb_terrains_occupes,gestionnaires=gestionnaires,avec_inscription=avec_inscription,css=css)
    return HttpResponse(json.dumps(res), content_type="application/json") 

@auth([groupe_admin])
def suppression(request):
    Evenement.objects.filter(id=request.POST['id']).delete()
    res=[]
    return HttpResponse(json.dumps(res), content_type="application/json") 

@auth([groupe_admin])
def admin(request):
    # on exclut les super_admin (pas les admin au sens des groupes de l'appli)
    context={ "adherents" : User.objects.all().exclude(is_staff=True),"admin" : is_admin(request.user)}
    return render(request,'gestionAdmin/admin.html',context)

@auth([groupe_admin])
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

@auth([groupe_admin])
def change_info(request):
    user=User.objects.get(id=request.POST["id"])
    group_names=json.loads(request.POST["groupes"])
    lesgroups = Group.objects.filter(name__in=group_names)
    user.groups.set(lesgroups)    
    user.save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

