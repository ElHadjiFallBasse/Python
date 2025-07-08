from django.db import models

class Medicament(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    quantite = models.IntegerField()

    def __str__(self):
        return self.nom
