from django.contrib import admin
from .models import *

# Register your models here.
class MenuAdmin(admin.ModelAdmin):
    pass

class EvenementAdmin(admin.ModelAdmin):
    pass

class SportiveAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sportive,SportiveAdmin)
admin.site.register(Evenement,EvenementAdmin)
admin.site.register(Menu,MenuAdmin)