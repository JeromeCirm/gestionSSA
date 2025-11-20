from django.contrib import admin
from .models import *

# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    pass

class EvenementAdmin(admin.ModelAdmin):
    pass

class SportiveAdmin(admin.ModelAdmin):
    pass

class TournoiAdmin(admin.ModelAdmin):
    pass

class InscriptionAdmin(admin.ModelAdmin):
    pass

class ReglagesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Reglages,ReglagesAdmin)
admin.site.register(Inscription,InscriptionAdmin)
admin.site.register(Tournoi,TournoiAdmin)
admin.site.register(Sportive,SportiveAdmin)
admin.site.register(Evenement,EvenementAdmin)
admin.site.register(Menu,MenuAdmin)