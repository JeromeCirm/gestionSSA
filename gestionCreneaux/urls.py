from django.urls import path

from . import views

urlpatterns = [
    path("reglages", views.reglages, name="reglages"),
    path("aide", views.aide, name="aide"),
    path("click",views.click,name="click"),
    path("events",views.events,name="events"),
    path("jeulibre",views.jeulibre,name="jeulibre"),
    path("checkbox",views.checkbox,name="checkbox"),
    path("enattente",views.enattente,name="enattente"),
    path("ajustevue",views.ajustevue,name="ajustevue"),
    path("changemdp",views.changemdp,name="changemdp"),
    path("ajustelimite",views.ajustelimite,name="ajustelimite"),
]