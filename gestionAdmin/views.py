from django.shortcuts import render
from base.fonctions import auth
from base.models import Utilisateur
from django.http import HttpResponse
import json
from gestionCreneaux.models import Evenement
from gestionCreneaux.settings import typecreneau
from .fonctions import *
from gestionCreneaux.fonctions import is_admin,type_event_modifiable
from dateutil.relativedelta import relativedelta

groupe_admin=1 #pendant la réinitialisation

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
    nom=request.POST["titre"]
    description=request.POST["description"]
    type=type%100
    modifiables=type_event_modifiable(request.user)
    if id==-1:
        # création de créneau
        dt1=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(debut, "%H:%M").time())
        dt2=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(fin, "%H:%M").time())
        if "ouvert" in options:
            gestionnaires=-1
        else:
            gestionnaires=0
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
            if type in modifiables:
                for rep in range(nbrepetition):
                    nouvelle_date = date_obj + deltarepetition*rep
                    jourrep=nouvelle_date.strftime(format_date)
                    Evenement(type=type,nom=nom,description=description,jour=jourrep,debut=debut,fin=fin,nb_terrains=nb_terrains,nb_terrains_occupes=nb_terrains_occupes,gestionnaires=gestionnaires,avec_inscription=avec_inscription,css=css,creation=request.user).save()
            else:
                print("hack") #if True
    else:
        # modification de créneau
        dt1=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(debut, "%H:%M").time())
        dt2=datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(fin, "%H:%M").time())
        if dt2 >=dt1+ datetime.timedelta(minutes=30):
            # à condition que le créneau fasse au moins 30mn
            ev=Evenement.objects.get(id=id)
            if ev.type in modifiables:
                if "ouvert" in options:
                    gestionnaires=-1
                else:
                    gestionnaires=len(Inscription.objects.filter(event=ev,role=ROLE_STAFF))
                Evenement.objects.filter(id=id).update(type=type,nom=nom,description=description,jour=jour,debut=debut,fin=fin,nb_terrains=nb_terrains,nb_terrains_occupes=nb_terrains_occupes,gestionnaires=gestionnaires,avec_inscription=avec_inscription,css=css)
            else:
                print("hack") #if True
    return HttpResponse(json.dumps(res), content_type="application/json") 

def suppression(request):
    modifiables=type_event_modifiable(request.user)
    ev=Evenement.objects.get(id=request.POST['id'])
    if ev.type in modifiables:
        ev.delete()
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
        "username" : user.username,
        "first_name" : user.first_name ,
        "last_name" : user.last_name ,
        "email" : user.email ,
        "lastco" : user.last_login,
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
    if groupe_staff in lesgroups:
        Reglages.objects.filter(user=user,nom="enattente").delete()
        Reglages(user=user,nom="enattente",bool=True).save()
    if groupe_creation_entrainement_avalider or groupe_validation_entrainement in lesgroups:
        lestypes=[x.val for x in Reglages.objects.filter(user=user,nom="types")]
        if EVENT_ENTRAINEMENT_A_VALIDER not in lestypes:
            Reglages(user=user,nom="types",val=EVENT_ENTRAINEMENT_A_VALIDER).save()
    user.save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

@auth([groupe_admin])
def supprime_compte(request):
    user=User.objects.get(id=request.POST["id"])
    if user!=request.user:
        # on interdit la suppression du compte connecté
        user.delete()
    return HttpResponse(json.dumps(""), content_type="application/json") 

@auth([groupe_admin])
def importe(request):
    with open("C://Users//jerom//Desktop//users.json", encoding="utf-8") as f:
        data = json.load(f)
        users={}
        utilisateur={}
        for i,d in enumerate(data) :
            if d['model']=='auth.user':
                users[d['pk']]=d['fields']
            elif d['model']=='base.utilisateur':
                utilisateur[d['pk']]=d['fields']
    for k in utilisateur:
        ut=utilisateur[k]
        if ut["user"] in users :
            us=users[ut["user"]]
            if len(User.objects.filter(username=us["username"]))!=0:
                print("deja présent : ",us["username"])
            else:
                new_user=User.objects.create_user(username=us["username"],first_name=us["first_name"],last_name=us["last_name"],email=us["email"],password="password")
                new_user.password=us["password"]
                new_user.save()
                Utilisateur(user=new_user,telephone=ut["telephone"],csrf_token=ut["csrf_token"],en_attente_confirmation=ut["en_attente_confirmation"],date_demande=ut["date_demande"]).save()
                en_at=DEFAULT_ENATTENTE
                types=DEFAULT_TYPES
                if 1 in us["groups"]:
                    #staff
                    en_at=True
                    new_user.groups.add(groupe_staff)
                Reglages(user=new_user,nom="ordi",str=DEFAULT_ORDI).save()
                Reglages(user=new_user,nom="ordteli",str=DEFAULT_TEL).save()
                Reglages(user=new_user,nom="enattente",bool=en_at).save()
                Reglages(user=new_user,nom="limite",val=DEFAULT_LIMITE).save()
                Reglages(user=new_user,nom="limite_avant",val=DEFAULT_LIMITE_AVANT).save() 
                for x in types:
                    Reglages(user=new_user,nom="types",val=x).save()
    return HttpResponse(json.dumps(""), content_type="application/json") 

