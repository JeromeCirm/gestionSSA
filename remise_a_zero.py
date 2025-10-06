# ne lancer que la toute première fois : 
# efface complètement la base de données, tous les fichiers, etc...
# et crée uniquement un compte admin
# et un menu permettant d'accéder à l'initialisation 

import os
import shutil

for x in ["gestionSSA","base","gestionAdmin","gestionCreneaux","staff"]:
    path=x+"/migrations"
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)
    f=open(path+'/__init__.py',"w")
    f.close()

try:
    pass
    os.remove('db.sqlite3')
except:
    pass

os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
os.system("python manage.py remise_a_zero_command")     

print("Réinitialisation terminée.")
