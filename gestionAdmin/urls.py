from django.urls import path

from . import views

urlpatterns = [
    path("admin", views.admin, name="admin"),
    path("creation_modification", views.creation_modification, name="creation_modification"),

]