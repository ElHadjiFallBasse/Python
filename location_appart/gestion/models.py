from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom

class Appartement(models.Model):
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.adresse} - {self.ville}"

class Champ(models.Model):
    appartement = models.ForeignKey(Appartement, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    valeur = models.CharField(max_length=200)
    

    def __str__(self):
        return f"{self.nom}: {self.valeur}"

class Location(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    appartement = models.ForeignKey(Appartement, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"{self.client.nom} - {self.appartement.adresse}"
