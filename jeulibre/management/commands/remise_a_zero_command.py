from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Adds a user to django'

    def add_arguments(self, parser):
        parser.add_argument('admin_login')
        parser.add_argument('admin_password')

    def handle(self, *args, **options):
        # user=creation_compte(options["admin_login"],options["admin_password"],[],True,{})
        # user.is_admin=True
        # user.is_staff=True
        # user.is_superuser=True
        # user.save()
        # user.utilisateur.autorise_modif=False
        # user.utilisateur.doit_changer_mdp=False
        # user.utilisateur.save()
        # creation_menu_site({},[["Initialisation","initialisation",[],[],[]]])

        for name in [
            "staff",  # staff basic pour gestion des créneaux jeu libre
            "jeu_libre", # créateur de créneaux jeu libre
            "tournois", # créateur de créneaux tournois
            "entraînements", # créateur de créneaux entrainements
            "entraînements_a_valider", # créateur de créneaux entrainements à valider
            "event", # créateur de créneaux évènements (entreprise, etc)
            "extérieur", # créateur de créneaux pour ce qui se passe à l'extérieur des terrains SSA
            "sportive", # staff basic sportive
            "creation_sportive", # créateur d'items pour la sportive
            "validation_entrainements", # validation des créneaux entrainements
            "créneau_prioritaire", # autorisé à forcer un créneau prioritaire
            ]:
            Group(name=name).save()

