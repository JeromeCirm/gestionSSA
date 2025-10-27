from django.shortcuts import render
from base.fonctions import auth
from django.http import HttpResponse
from gestionCreneaux.fonctions import menu_navigation
import json

@auth(None)
def creationcreneaux(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'gestionAdmin/creationcreneaux.html',context)

@auth(None)
def gestionsportive(request,numero,context):
    context={"menu" : menu_navigation(request)}
    return render(request,'gestionAdmin/gestionsportive.html',context)

def creation(request):
    res=[]
    print(request.POST)
    return HttpResponse(json.dumps(res), content_type="application/json") 