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
    nom=models.TextField(null=True,blank=True,default="") # nom court pour la vue , indispensable
    description=models.TextField(null=True,blank=True,default="") # nom plus long pour la vue journalière
    jour=models.DateField(null=True,blank=True,default=None) 
    debut=models.TimeField(null=True,blank=True,default=None)
    fin=models.TimeField(null=True,blank=True,default=None)
    nb_terrains=models.IntegerField(null=True,blank=True,default=4)   # les terrains souhaités
    nb_terrains_occupes=models.IntegerField(null=True,blank=True,default=4)  # la réalité !
    css=models.TextField(null=True,blank=True,default="")  # correspond à la classe css à appliquer à l'évènement
    avec_inscription=models.BooleanField(default=False,blank=True)
    inscrits=models.IntegerField(null=True,blank=True,default=0)
    gestionnaires=models.IntegerField(null=True,blank=True,default=0) #-1 pour indiquer une ouverture sans staff
    prioritaire=models.BooleanField(null=True,default=False,blank=True) # prioritaire pour les terrains sur les autres créneaux
    creation=models.ForeignKey(User, null=True,default=None,blank=True,on_delete=models.CASCADE) # qui a créé le créneau ? pour clairifier lors de la validation par exemple
    def __str__(self):
        return "type : "+str(self.type)+", "+self.nom+",id "+str(self.pk)+",jour : "+str(self.jour)+",debut : "+str(self.debut)+",fin : "+str(self.fin)

class Tournoi(models.Model):
    type=models.TextField(null=True,blank=True,default="") # S1, S2, jeunes, championnat mixte
    categorie=models.TextField(null=True,blank=True,default="") # M,F,X,parents_enfant
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
    texte=models.TextField(null=True,blank=True,default="") # description de l'item
    event=models.ManyToManyField(Evenement, blank=True) # liste d'evenements associés si c'est pertinent
    tournoi=models.ForeignKey(Tournoi, on_delete=models.CASCADE) # idem pour un tournoi
    debut=models.DateField(null=True,blank=True,default=None) # date d'apparition dans la liste
    deadline=models.DateField(null=True,blank=True,default=None) # deadline : sert à trier les items 
    resolu=models.OneToOneField(User,null=True,blank=True,on_delete=models.SET_NULL) # indique qui a géré l'item, et la date de gestion
    date_resolution=models.DateField(null=True,blank=True,default=None)
    def __str__(self):
        return "id "+str(self.pk)+",debut : "+str(self.debut)+",fin : "+str(self.deadline)+", "+str(self.tournoi)+", "+self.texte
    
class Inscription(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    event=models.ForeignKey(Evenement, on_delete=models.CASCADE)
    role=models.IntegerField(null=True,blank=True,default=0)

class Reglages(models.Model):
    # nom associé à une chaine ou une valeur, selon les besoins
    # pour l'instant : 
    # types -> entier
    # ordi -> str (la vue par défaut)
    # tel -> str (idem)
    # enattente -> bool (on regarde les créneaux en attente ?)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    nom=models.TextField(null=True,blank=True,default="") 
    str=models.TextField(null=True,blank=True,default="") 
    val=models.IntegerField(null=True,blank=True,default=0)
    bool=models.BooleanField(null=True,default=False,blank=True)

