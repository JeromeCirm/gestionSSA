from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.

class Menu(models.Model):
    nom=models.CharField(max_length=40)
    parent=models.IntegerField(blank=True)  # 0 pour un menu principal
    fonction=models.CharField(max_length=50,blank=True,default="")  #  fonction à appeler : vide s'il y des sous-menus
    groupes=models.ManyToManyField(Group,blank=True)
    ordre=models.IntegerField(default=0) # ordre dans le sous-menu

    def __str__(self):
        return self.nom+",id "+str(self.pk)+", parent "+str(self.parent)+",ordre "+str(self.ordre)+" "+str(self.fonction)

    class Meta : 
        ordering=['parent','ordre']

class Evenement(models.Model):
    type=models.IntegerField(null=True,blank=True,default=None)   # correspond à une constante définie dans setting
    nom=models.CharField(max_length=40) # nom court pour la vue mensuelle
    description=models.CharField(max_length=100) # nom plus long pour la vue journalière
    datedebut=models.DateTimeField(null=True,blank=True,default=None) # date et heure
    datefin=models.DateTimeField(null=True,blank=True,default=None)
    nb_terrains=models.IntegerField(null=True,blank=True,default=None) 
    code_couleur=models.IntegerField(null=True,blank=True,default=None) 
    avec_inscription=models.BooleanField(default=False,blank=True)
    besoin_staff=models.CharField(max_length=40) # décrit les besoins en staff, la première est le staff d'ouverture : si 0, cela annule la gestion automatique de ouvert/en_attente
    gestion_staff=models.CharField(max_length=40) # décrit le staff inscrit pour aider
    ouvert=models.BooleanField(null=True,default=False,blank=True) # indique si le créneau est ouvert ou juste en prevision
    prioritaire=models.BooleanField(null=True,default=False,blank=True) # prioritaire pour les terrains sur les autres créneaux

class Tournoi(models.Model):
    type=models.CharField(max_length=40) # S1, S2, jeunes, championnat mixte
    categorie=models.CharField(max_length=40) # M,F,X,parents_enfant
    referents=models.ManyToManyField(User,blank=True) # liste de référents
    declare=models.BooleanField(null=True,default=False,blank=True)
    inscriptions_closes=models.BooleanField(null=True,default=False,blank=True)
    resultats_rentres=models.BooleanField(null=True,default=False,blank=True)
    prize_money_distribue=models.BooleanField(null=True,default=False,blank=True)
    photos_envoyees=models.BooleanField(null=True,default=False,blank=True)
    events=models.ManyToManyField(Evenement,blank=True) # liste d'évenemnts associés (plusieurs si plusieurs jours ou bien matin/AM)

class Sportive(models.Model):
    texte=models.CharField(max_length=200) # description de l'item
    event=models.ManyToManyField(Evenement, null=True,blank=True) # liste d'evenements associés si c'est pertinent
    tournoi=models.OneToOneField(Tournoi, on_delete=models.CASCADE) # idem pour un tournoi
    debut=models.DateField(null=True,blank=True,default=None) # date d'apparition dans la liste
    deadline=models.DateField(null=True,blank=True,default=None) # deadline : sert à trier les items 
    resolu=models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL) # indique qui a géré l'item, et la date de gestion
    date_resolution=models.DateField(null=True,blank=True,default=None)
