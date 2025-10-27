# premier groupe : pour autoriser un créneau pour tout le monde
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
EVENT_JEULIBRE=1
EVENT_ENTRAINEMENT=2
EVENT_TOURNOI=3

# les constantes pour indiquer les rôles 
ROLE_INSCRIT=0
ROLE_STAFF=1