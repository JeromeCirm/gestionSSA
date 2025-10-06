from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from gestionCreneaux.models import Menu
from django.contrib.auth.models import User,Group
from base.fonctions import creation_utilisateur

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
            ["ad",["admin"]],
            ]:
            user=creation_utilisateur(login,"","","",en_attente_confirmation=False)
            for x in groupes:
                user.groups.add(Group.objects.get(name=x))

        
        ## Quelques créneaux pour voir le site en action : 


        ## des éventuels tests ? 

