from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,User
import datetime
from gestionCreneaux.models import Menu,Evenement,Inscription
from base.fonctions import creation_utilisateur
from gestionCreneaux.settings import *
from gestionAdmin.fonctions import creation_tournoi
from gestionCreneaux.fonctions import inscription
try:
    from .remise_perso import *
except:
    from .remise_modele import *

class Command(BaseCommand):
    help = 'Adds a user to django'

    #def add_arguments(self, parser): # pour ajouter des arguments à la commande
    #    parser.add_argument('admin_login')
    #    parser.add_argument('admin_password')

    def handle(self, *args, **options):
        creation_utilisateur(LOGIN_ADMIN,"","",MDP_ADMIN,en_attente_confirmation=False,admin=True)
        
        ## données de base (groupes)

        for nom in ["staff","sportive","creation_jeulibre","creation_tournois","creation_entrainement","creation_entrainement_avalider","creation_event","creation_prioritaire","creation_sportive","admin","validation_entrainement"]:
            Group(name=nom).save()

        if BIDON:
            for login,groupes,types,enattente in [
                ["j1",[],DEFAULT_TYPES,DEFAULT_ENATTENTE],
                ["j2",[],DEFAULT_TYPES,DEFAULT_ENATTENTE],
                ["j3",[],DEFAULT_TYPES,DEFAULT_ENATTENTE],
                ["st1",["staff"],DEFAULT_TYPES,True],
                ["st2",["staff"],DEFAULT_TYPES,True],
                ["st3",["staff"],DEFAULT_TYPES,True],
                ["sp1",["sportive"],DEFAULT_TYPES,DEFAULT_ENATTENTE],
                ["sp2",["sportive"],DEFAULT_TYPES,DEFAULT_ENATTENTE],
                ["sp3",["sportive"],DEFAULT_TYPES,DEFAULT_ENATTENTE],
                ["cj",["creation_jeulibre"],DEFAULT_TYPES,True],
                ["cs",["creation_sportive"],DEFAULT_TYPES,True],
                ["ce",["creation_entrainement"],[EVENT_ENTRAINEMENT],True],
                ["cea",["creation_entrainement_avalider"],[EVENT_ENTRAINEMENT_A_VALIDER],True],
                ["ct",["creation_tournois"],[EVENT_TOURNOI],True],
                ["ve",["validation_entrainement"],[EVENT_ENTRAINEMENT_A_VALIDER],True],
                ["ad",["admin","staff","sportive","creation_jeulibre","creation_sportive","creation_tournois","creation_entrainement","creation_entrainement_avalider","validation_entrainement"],[EVENT_JEULIBRE,EVENT_ENTRAINEMENT,EVENT_TOURNOI,EVENT_ENTRAINEMENT_A_VALIDER],True],
                ]:
                user=creation_utilisateur(login,login,login,"",en_attente_confirmation=False,types=types,en_attente=enattente)
                for x in groupes:
                    user.groups.add(Group.objects.get(name=x))

            ## Quelques créneaux pour voir le site en action : 
            liste=[
                #type,decalage de jour, heure début, terrains, avec inscription,gestionnaires, inscrits
                [EVENT_JEULIBRE,-1,12,14,4,False,0,[]],
                [EVENT_JEULIBRE,1,12,14,4,False,0,["st1"]],
                [EVENT_JEULIBRE,1,17,19,4,True,-1,["j1"]],
                [EVENT_JEULIBRE,1,15,17,2,False,0,[]],
                [EVENT_ENTRAINEMENT,2,12,14,3,False,-1,[]],
                [EVENT_JEULIBRE_ADHERENTS,2,12,14,1,False,0,["st1","st2"]],
                [EVENT_ENTRAINEMENT,2,17,19,2,True,-1,["st1","j3","j1"]],
                [EVENT_JEULIBRE_ADHERENTS,2,17,19,2,True,0,["st1","st2","st3","sp2","sp1","j3","j2","j1"]],
                [EVENT_JEULIBRE,2,9,10,4,False,-1,[]],
                [EVENT_JEULIBRE,2,11,12,4,True,-1,[]],
                [EVENT_JEULIBRE,8,12,14,4,False,-1,[]],
                [EVENT_JEULIBRE,8,17,19,4,True,0,[]],
                [EVENT_JEULIBRE,40,12,14,4,False,-1,[]],
            ] 
            actu=datetime.datetime.now()
            date=datetime.date(year=actu.year,month=actu.month,day=actu.day)
            for type,decalage,debut,fin,nb_terrains,avecinscription,gestionnaires,inscrits in liste:
                if avecinscription:
                    css=typecreneau[type]["cssins"]
                    description=typecreneau[type]["descriptionins"]
                else:
                    css=typecreneau[type]["css"]
                    description=typecreneau[type]["description"]
                type=type%100
                for duplicate in range(50):
                    ev=Evenement(type=type,nom=typecreneau[type]["titre"],description=description,jour=date+datetime.timedelta(days=decalage+duplicate*4),debut=datetime.time(hour=debut),fin=datetime.time(hour=fin),nb_terrains=nb_terrains,avec_inscription=avecinscription,css=css,gestionnaires=gestionnaires)
                    ev.save()
                    for x in inscrits:
                        inscription(User.objects.get(username=x),ev.id)

            creation_tournoi("S3","X",date,events=[[0,9,17,4,""]])
            creation_tournoi("S1","X",date+datetime.timedelta(days=4),events=[[0,9,12,4,"Qualif Poules"],[0,12,17,4, "Qualif Barrages"],[1,9,16,4,"Main Draw"]])
            creation_tournoi("S2","Jeunes",date+datetime.timedelta(days=8),events=[[0,9,17,4,""]])

            ## des éventuels tests ? 

            from gestionCreneaux.fonctions import lecture_creneaux
            liste=lecture_creneaux(date,date+datetime.timedelta(days=3))
            print("tous les évenements sur 3 jours : ")
            for x in liste:
                print(x)
            print("juste les tournois : ")
            liste=lecture_creneaux(date,date+datetime.timedelta(days=3),types=[EVENT_TOURNOI])
            for x in liste:
                print(x)