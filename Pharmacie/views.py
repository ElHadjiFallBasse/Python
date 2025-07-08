# Pharmacie/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Medicament
from .forms import MedicamentForm

# Accueil - Liste des médicaments
def home(request):
    medicaments = Medicament.objects.all()
    return render(request, 'Pharmacie/home.html', {'medicaments': medicaments})

# Ajouter un médicament
def ajouter_medicament(request):
    if request.method == 'POST':
        form = MedicamentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médicament ajouté avec succès !")
            return redirect('home')
    else:
        form = MedicamentForm()
    return render(request, 'Pharmacie/ajouter.html', {'form': form})

# Modifier un médicament
def modifier_medicament(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        form = MedicamentForm(request.POST, instance=medicament)
        if form.is_valid():
            form.save()
            messages.success(request, "Médicament modifié avec succès !")
            return redirect('home')
    else:
        form = MedicamentForm(instance=medicament)
    return render(request, 'Pharmacie/ajouter.html', {'form': form})

# Supprimer un médicament
def supprimer_medicament(request, pk):
    medicament = get_object_or_404(Medicament, pk=pk)
    if request.method == 'POST':
        medicament.delete()
        messages.success(request, "Médicament supprimé avec succès !")
        return redirect('home')
    return render(request, 'Pharmacie/supprimer.html', {'medicament': medicament})
