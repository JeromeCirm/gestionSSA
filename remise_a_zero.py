# ne lancer que la toute première fois : 
# efface complètement la base de données, tous les fichiers, etc...
# et crée uniquement un compte admin
# et un menu permettant d'accéder à l'initialisation 

import os

try:
    from remise_a_zero_perso import reset_db
except:
    from remise_a_zero_modele import reset_db

reset_db()

os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py remise_a_zero_command")   #lance la "vrai réinitialisation" : ingérable ici car on n'a pas accès aux modèles par exemple  

print("Réinitialisation terminée.")
