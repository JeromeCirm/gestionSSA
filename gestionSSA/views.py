from utilisateurs.fonctions import *
from django.http import HttpResponse

@auth(None)
def home(request):
        return HttpResponse("Hello, world. <a href='utilisateurs/deconnexion' class='creation-btn'>  " \
        "You're at the global index.")
