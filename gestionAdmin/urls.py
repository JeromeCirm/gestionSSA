from django.urls import path

from . import views

urlpatterns = [
    path("creation",views.creation,name="creation"),

]