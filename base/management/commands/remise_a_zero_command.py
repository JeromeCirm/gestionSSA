from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
import datetime
from gestionCreneaux.models import Menu,Evenement
from base.fonctions import creation_utilisateur
from gestionCreneaux.settings import *
from gestionAdmin.fonctions import creation_tournoi

class Command(BaseCommand):
    help = 'Adds a user to django'

    #def add_arguments(self, parser): # pour ajouter des arguments à la commande
    #    parser.add_argument('admin_login')
    #    parser.add_argument('admin_password')

    def handle(self, *args, **options):
        creation_utilisateur("admin","","","admin",en_attente_confirmation=False,admin=True)
        ## données de base (menu/groupe)

        for nom in ["staff","sportive","creation_jeulibre","creation_tournois","creation_entrainement","creation_entrainement_avalider","creation_event","creation_prioritaire","creation_sportive","admin","validation_entrainement"]:
            Group(name=nom).save()

        liste_menu=[
    ["Jeu Libre","jeulibre",[],[
    ]],
    ["Staff","",["staff","sportive"],[
        ["Récapitulatif","recapitulatif",["staff"]],
        ["Inscrits","inscrits",["staff"]],
        ["Sportive","sportive",["sportive"]]
    ]],      
    ["Gestion","",["creation_jeulibre","creation_tournois","creation_entrainement","creation_entrainement_avalider","creation_event","creation_prioritaire","creation_sportive"],[
        ["Création de créneaux","creationcreneaux",["creation_jeulibre"]],
        ["Gestion de la sportive","gestionsportive",["creation_sportive"]],
    ]], 
    ]

        def creation_menu_site(liste):
                Menu.objects.all().delete()
                ordre=0
                for item in liste:
                    x=Menu(nom=item[0],fonction=item[1])
                    x.ordre=ordre
                    x.parent=0
                    x.save()
                    ordre+=1
                    id=x.pk
                    for y in item[2]:
                        x.groupes.add(Group.objects.get(name=y))                   
                    ordre_s=0
                    for subitem in item[3]:
                        x=Menu(nom=subitem[0],fonction=subitem[1])
                        x.ordre=ordre_s
                        x.parent=id
                        x.save()
                        for y in subitem[2]:
                            x.groupes.add(Group.objects.get(name=y))   
                        ordre_s+=1

        creation_menu_site(liste_menu)
        for login,groupes in [
            ["st1",["staff"]],
            ["st2",["staff"]],
            ["st3",["staff"]],
            ["sp1",["sportive"]],
            ["sp2",["sportive"]],
            ["sp3",["sportive"]],
            ["cj",["creation_jeulibre"]],
            ["cs",["creation_sportive"]],
            ["ce",["creation_entrainement"]],
            ["cea",["creation_entrainement_avalider"]],
            ["ve",["validation_entrainement"]],
            ["ad",["admin","creation_jeulibre","creation_sportive","creation_entrainement","creation_entrainement_avalider","validation_entrainement"]],
            ]:
            user=creation_utilisateur(login,"","","",en_attente_confirmation=False)
            for x in groupes:
                user.groups.add(Group.objects.get(name=x))

        
        ## Quelques créneaux pour voir le site en action (2h): 
        liste=[
            #nom,description, decalage de jour, heure début, terrains, inscription
            ["JL1","",1,12,14,4,False],
            ["JL2","",1,17,19,4,True],
            ["JL3","",3,12,14,4,False],
            ["JL3b","",3,13,14,4,False],
            ["JL4b","",3,18,19,4,True],
            ["JL4","",3,17,19,4,True],
            ["JL3B","",3,9,10,4,False],
            ["JL4B","",3,11,12,4,True],
            ["JL5","",-1,12,14,4,False],
            ["JL6","",1,15,17,2,False],
            ["JL7","",8,12,14,4,False],
            ["JL8","",8,17,19,4,True],
            ["JL9","",40,12,14,4,False],
        ] 
        bulk=[]
        actu=datetime.datetime.now()
        date=datetime.date(year=actu.year,month=actu.month,day=actu.day)
        for nom,desc,decalage,debut,fin,nb_terrains,inscription in liste:
            if inscription:
                css='event-jeulibreinscription'
            else:
                css='event-jeulibre'
            bulk.append(Evenement(type=EVENT_JEULIBRE,nom=nom,description=desc,jour=date+datetime.timedelta(days=decalage),debut=datetime.time(hour=debut),fin=datetime.time(hour=fin),nb_terrains=nb_terrains,avec_inscription=inscription,css=css))
        Evenement.objects.bulk_create(bulk)

        creation_tournoi("S3","X",date,events=[[0,9,17,4,""]])
        creation_tournoi("S1","X",date+datetime.timedelta(days=-15),events=[[0,9,12,4,"Qualif Poules"],[0,12,17,4, "Qualif Barrages"],[1,9,16,4,"Main Draw"]])
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