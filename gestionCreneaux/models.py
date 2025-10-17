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
    #
    # format à vérifier pour les dates (selon local peut-être ?): 
    #  %y/%m/%d %H:%M	2025-10-25 11:44
    #
    type=models.IntegerField(null=True,blank=True,default=None)   # correspond à une constante définie dans setting
    nom=models.CharField(max_length=40) # nom court pour la vue , indispensable
    description=models.CharField(max_length=100,null=True,blank=True,default="") # nom plus long pour la vue journalière
    jour=models.DateField(null=True,blank=True,default=None) 
    debut=models.TimeField(null=True,blank=True,default=None)
    fin=models.TimeField(null=True,blank=True,default=None)
    nb_terrains=models.IntegerField(null=True,blank=True,default=4)   # les terrains souhaités
    nb_terrains_occupes=models.IntegerField(null=True,blank=True,default=4)  # la réalité !
    code_couleur=models.IntegerField(null=True,blank=True,default=None)  # correspond à une constante définie dans setting 
    avec_inscription=models.BooleanField(default=False,blank=True)
    besoin_staff=models.CharField(max_length=40,null=True,blank=True,default="1") # décrit les besoins en staff, la première est le staff d'ouverture : si 0, cela annule la gestion automatique de ouvert/en_attente
    gestion_staff=models.CharField(max_length=40,null=True,blank=True,default="0") # décrit le staff inscrit pour aider
    ouvert=models.BooleanField(null=True,default=False,blank=True) # indique si le créneau est ouvert ou juste en prevision
    prioritaire=models.BooleanField(null=True,default=False,blank=True) # prioritaire pour les terrains sur les autres créneaux
    def __str__(self):
        return "type : "+str(self.type)+", "+self.nom+",id "+str(self.pk)+",jour : "+str(self.jour)+",debut : "+str(self.debut)+",fin : "+str(self.fin)

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
    def __str__(self):
        return self.type+" "+self.categorie+",id "+str(self.pk)

class Sportive(models.Model):
    texte=models.CharField(max_length=200) # description de l'item
    event=models.ManyToManyField(Evenement, blank=True) # liste d'evenements associés si c'est pertinent
    tournoi=models.ForeignKey(Tournoi, on_delete=models.CASCADE) # idem pour un tournoi
    debut=models.DateField(null=True,blank=True,default=None) # date d'apparition dans la liste
    deadline=models.DateField(null=True,blank=True,default=None) # deadline : sert à trier les items 
    resolu=models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL) # indique qui a géré l'item, et la date de gestion
    date_resolution=models.DateField(null=True,blank=True,default=None)
    def __str__(self):
        return "id "+str(self.pk)+",debut : "+str(self.debut)+",fin : "+str(self.deadline)+", "+str(self.tournoi)+", "+self.texte