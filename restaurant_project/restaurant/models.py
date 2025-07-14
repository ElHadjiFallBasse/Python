from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
    



class Plat(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='plats/', blank=True, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='plats')
    disponible = models.BooleanField(default=True)  # <-- ajouté

    def __str__(self):
        return self.nom

class Commande(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('livree', 'Livrée'),
    ], default='en_attente')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.plat.nom} ({self.quantite})"

from django.db import models

class Reservation(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    date = models.DateField()
    heure = models.TimeField()
    personnes = models.PositiveIntegerField()
    message = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réservation de {self.nom} pour le {self.date} à {self.heure}"


from django.db import models
from django.contrib.auth.models import User

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class CommandeProduit(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(auto_now_add=True)
    est_validee = models.BooleanField(default=False)

    def __str__(self):
        return f"Commande #{self.id} - Client: {self.client.username}"

    def total(self):
        return sum(item.total() for item in self.items.all())

class ItemCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='items', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    def total(self):
        return self.quantite * self.produit.prix
