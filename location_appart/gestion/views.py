from django.shortcuts import render, redirect
from .models import Client, Appartement, Champ
from .forms import ClientForm, AppartementForm, ChampForm

def index(request):
    return render(request, 'gestion/index.html')

# CLIENT
def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'gestion/clients.html', {'clients': clients})

def ajouter_client(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('clients')
    return render(request, 'gestion/form.html', {'form': form, 'titre': 'Ajouter Client'})

# APPARTEMENT
def liste_appartements(request):
    appartements = Appartement.objects.all()
    return render(request, 'gestion/appartements.html', {'appartements': appartements})

def ajouter_appartement(request):
    form = AppartementForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('appartements')
    return render(request, 'gestion/form.html', {'form': form, 'titre': 'Ajouter Appartement'})

# CHAMP
def liste_champs(request):
    champs = Champ.objects.all()
    return render(request, 'gestion/champs.html', {'champs': champs})

def ajouter_champ(request):
    form = ChampForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('champs')
    return render(request, 'gestion/form.html', {'form': form, 'titre': 'Ajouter Champ'})
