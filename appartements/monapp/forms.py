from django import forms
from .models import Client, Appartement

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'email', 'adresse', 'telephone', 'appartements', 'image']
        widgets = {
            'appartements': forms.CheckboxSelectMultiple(),
        }

class AppartementForm(forms.ModelForm):
    class Meta:
        model = Appartement
        fields = ['nom', 'adresse', 'surface', 'nombre_chambre', 'niveau', 'image']
