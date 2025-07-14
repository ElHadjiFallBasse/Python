from django.db import models

class Appartement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=150)
    surface = models.FloatField()
    nombre_chambre = models.IntegerField()
    niveau = models.IntegerField(choices=[(i, f"{i} étoile(s)") for i in range(1, 6)])
    image = models.ImageField(upload_to='appartements/', null=True, blank=True)  # Nouveau champ

    def __str__(self):
        return f"{self.nom} - {self.adresse}"


class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    adresse = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20)
    appartements = models.ManyToManyField(Appartement, related_name='clients')
    image = models.ImageField(upload_to='clients/', null=True, blank=True)  # Nouveau champ

    def __str__(self):
        return f"{self.nom} {self.prenom}"
