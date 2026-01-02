
from django.contrib.auth.models import Group

try:  # pour ne pas bloquer lors de la réinitialisation
    # le staff
    groupe_staff=Group.objects.get(name="staff")
    groupe_sportive=Group.objects.get(name="sportive")

    # les créateurs de créneaux
    
    groupe_creation_jeulibre=Group.objects.get(name="creation_jeulibre")
    groupe_creation_tournois=Group.objects.get(name="creation_tournois")
    groupe_creation_entrainement=Group.objects.get(name="creation_entrainement")
    groupe_creation_entrainement_avalider=Group.objects.get(name="creation_entrainement_avalider")
    groupe_creation_event=Group.objects.get(name="creation_event")
    groupe_creation_prioritaire=Group.objects.get(name="creation_prioritaire")

    # gesion de la sportive

    groupe_creation_sportive=Group.objects.get(name="creation_sportive")

    # admin/validateurs
    groupe_admin=Group.objects.get(name="admin")
    groupe_validation_entrainement=Group.objects.get(name="validation_entrainement")
except:
    pass

# les constantes pour indiquer le type d'évenement
# penser à modifier la fonction type_event_modifiable en cas d'ajout d'event
EVENT_JEULIBRE=0
EVENT_ENTRAINEMENT=1
EVENT_TOURNOI=2
EVENT_ENTRAINEMENT_A_VALIDER=3
# idem mais juste pour faciliter la création de créneau : transformé en autre event ensuite : on ne garde que le modulo 100
EVENT_JEULIBRE_ADHERENTS=100 # devient EVENT_JEULIBRE
# dictionnaire associé avec nom et classe CSS en mode classique/avec inscription
# titre et description pré-remplissent le formulaire de création
typecreneau={
    EVENT_JEULIBRE : { "nom" : "jeu libre", "css" : "event-jeulibre","cssins" : "event-jeulibreinscription","titre" : "jeu libre", "description" : "séance de jeu libre ouverte à tout le monde", "descriptionins" : "séance de jeu libre ouverte sur inscription. La séance peut être annulée s'il n'y a pas assez de personnes inscrites", "ouvert"  : False, "inscription" : False}, 
    EVENT_ENTRAINEMENT : { "nom" : "entrainement", "css" : "event-entrainement","cssins" : "event-entrainement","titre" : "entrainement", "description" : "séance d'entrainement", "descriptionins" : "", "ouvert"  : True, "inscription" : False},
    EVENT_TOURNOI : { "nom" : "tournoi", "css" : "event-tournoi","cssins" : "event-tournoi","titre" : "tournoi", "description" : "tournoi : venez encourager les équipes. Inscription au tournoi sur le site du BVS", "descriptionins" : "", "ouvert"  : True, "inscription" : False},
    EVENT_ENTRAINEMENT_A_VALIDER : { "nom" : "entrainement à valider", "css" : "event-entrainement","cssins" : "event-entrainement","titre" : "entrainement", "description" : "entrainement", "descriptionins" : "", "ouvert"  : True, "inscription" : False},
    EVENT_JEULIBRE_ADHERENTS : { "nom" : "jeu libre adhérents", "css" : "event-jeulibre","cssins" : "event-jeulibreinscription","titre" : "jeu libre", "description" : "séance de jeu libre réservée aux adhérent(e)s", "descriptionins" : "séance de jeu libre réservée aux adhérent(e)s et sur inscription. La séance peut être annulée s'il n'y a pas assez de personnes inscrites", "ouvert"  : False, "inscription" : False}, 
}

# les constantes pour indiquer les rôles 
ROLE_INSCRIT=0
ROLE_STAFF=1

# les types par défaut pour un nouvel utilisateur à l'inscription ou pour quelqu'un de déconnecté, 
# penser  à modifier la fonction de création si on ajoute un réglage
DEFAULT_TYPES=[EVENT_JEULIBRE,EVENT_TOURNOI]
DEFAULT_TEL="TimeGridThreeDay"
DEFAULT_ORDI="timeGridWeek"
DEFAULT_ENATTENTE=False
DEFAULT_LIMITE=31

VUES_PROPOSEEES = [
    {"label" : "1 jour", "nom" : "timeGridDay"},
    {"label" : "3 jours ", "nom" : "TimeGridThreeDay"},
    {"label" : "7 jours", "nom" : "timeGridWeek"},
    {"label" : "1 mois", "nom" : "dayGridMonth"},
    ]

LIMITES_PROPOSEES= [
    {"label" : "1 semaine", "val" : 7},
    {"label" : "15 jours", "val" : 14},
    {"label" : "1 mois", "val" : 31},
    {"label" : "2 mois", "val" : 61},
    {"label" : "6 mois", "val" : 183},
    ]
