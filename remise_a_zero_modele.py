import os
import shutil

def reset_db_sqlite():
    try:
        pass
        os.remove('db.sqlite3')
    except:
        pass

def reset_db_mysql():
    os.system('mysql -u $user -p$passsword -Bse "DROP DATABASE gestionssa;CREATE DATABASE gestionssa;USE gestionssa;GRANT ALL PRIVILEGES ON gestionssa.* TO \'gestionssauser\'@\'localhost\';FLUSH PRIVILEGES;"')

def reset_db():
    for x in ["gestionSSA","base","gestionAdmin","gestionCreneaux","staff"]:
        path=x+"/migrations"
        shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)
        f=open(path+'/__init__.py',"w")
        f.close()
    reset_db_mysql()