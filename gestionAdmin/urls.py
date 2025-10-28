from django.urls import path

from . import views

urlpatterns = [
    path("creation_modification",views.creation_modification,name="creation_modification"),
    path("suppression",views.suppression,name="suppression"),

]