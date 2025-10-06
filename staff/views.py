from django.shortcuts import render
from base.fonctions import auth
from gestionCreneaux.fonctions import menu_navigation

@auth(None)
def sportive(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'staff/sportive.html',context)

@auth(None)
def inscrits(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'staff/inscrits.html',context)

@auth(None)
def recapitulatif(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'staff/recapitulatif.html',context)