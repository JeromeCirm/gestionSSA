from django.shortcuts import render
from base.fonctions import auth
from gestionCreneaux.fonctions import menu_navigation

@auth(None)
def creationcreneaux(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'gestionAdmin/creationcreneaux.html',context)

@auth(None)
def gestionsportive(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'gestionAdmin/gestionsportive.html',context)