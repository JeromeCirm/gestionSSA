# ne lancer que la toute première fois : 
# efface complètement la base de données, tous les fichiers, etc...
# et crée uniquement un compte admin
# et un menu permettant d'accéder à l'initialisation 

import os
import shutil

admin_login=input("login admin (vide pour admin) : ")
if admin_login=="":
    admin_login="admin"
admin_mdp=input("mot de passe admin (vide pour admin) : ")
if admin_mdp=="":
    admin_mdp="admin"
else:
    confirm_mdp=input("entrer de nouveau le mot de passe : ")
    if confirm_mdp!=admin_mdp:
        print("les deux mots de passe ne coïncident pas")
        exit()

for x in ["gestionSSA","jeulibre","planning","tournois","utilisateurs"]:
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
os.system("python manage.py remise_a_zero_command "+admin_login+" "+admin_mdp)

print("Réinitialisation terminée.")

