from django.urls import path

from . import views

urlpatterns = [
    path("admin", views.admin, name="admin"),
    path("recupere_info", views.recupere_info, name="recupere_info"),
    path("change_info", views.change_info, name="change_info"),
    path("creation_modification", views.creation_modification, name="creation_modification"),
    path("suppression", views.suppression, name="suppression"),
    path("supprime_compte", views.supprime_compte, name="supprime_compte"),
    path("importe", views.importe, name="importe"),
    path("stats", views.stats, name="stats"),
    path("recupere_stats", views.recupere_stats, name="recupere_stats"),

]