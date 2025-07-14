from django import forms
from .models import Client, Appartement, Champ

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class AppartementForm(forms.ModelForm):
    class Meta:
        model = Appartement
        fields = '__all__'

class ChampForm(forms.ModelForm):
    class Meta:
        model = Champ
        fields = '__all__'
