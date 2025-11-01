from django.urls import path

from . import views

urlpatterns = [
    path("admin", views.admin, name="admin"),
    path("recupere_info", views.recupere_info, name="recupere_info"),
    path("change_info", views.change_info, name="change_info"),
    path("creation_modification", views.creation_modification, name="creation_modification"),

]