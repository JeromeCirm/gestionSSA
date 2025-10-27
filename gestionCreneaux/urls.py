from django.urls import path

from . import views

urlpatterns = [
    path('menu/<int:numero>',views.menu,name='menu'),
    path("reglages", views.reglages, name="reglages"),
    path("click",views.click,name="click"),
    path("events",views.events,name="events"),
]