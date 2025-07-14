from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Appartement
from .forms import ClientForm, AppartementForm

def gestion(request):
    clients = Client.objects.all()
    appartements = Appartement.objects.all()

    if request.method == 'POST':
        if 'ajouter_client' in request.POST:
            client_form = ClientForm(request.POST)
            if client_form.is_valid():
                client_form.save()
                return redirect('gestion')
        elif 'ajouter_appart' in request.POST:
            appart_form = AppartementForm(request.POST, request.FILES)  # Ajoute request.FILES ici
            if appart_form.is_valid():
                appart_form.save()
                return redirect('gestion')
    else:
        client_form = ClientForm()
        appart_form = AppartementForm()

    return render(request, 'src/gestion.html', {
        'client_form': client_form,
        'appart_form': appart_form,
        'clients': clients,
        'appartements': appartements,
    })

def detail_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'src/detailsclient.html', {'client': client})

def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('gestion')
    else:
        form = ClientForm(instance=client)
    return render(request, 'src/modifierclient.html', {'form': form})

def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('gestion')

def detail_appart(request, pk):
    appart = get_object_or_404(Appartement, pk=pk)
    return render(request, 'src/detailsappart.html', {'appart': appart})

def modifier_appart(request, pk):
    appart = get_object_or_404(Appartement, pk=pk)
    if request.method == 'POST':
        form = AppartementForm(request.POST, instance=appart)
        if form.is_valid():
            form.save()
            return redirect('gestion')
    else:
        form = AppartementForm(instance=appart)
    return render(request, 'src/modifierappart.html', {'form': form})

def supprimer_appart(request, pk):
    appart = get_object_or_404(Appartement, pk=pk)
    appart.delete()
    return redirect('gestion')
