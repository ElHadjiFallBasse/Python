# restaurant/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from .models import Plat
from .forms import PlatForm


# Vérifie si l'utilisateur est dans le groupe 'Gestionnaire'
def est_gestionnaire(user):
    return user.groups.filter(name='Gestionnaire').exists()


# Vue Login

from django.contrib.auth import logout

def login_view(request):
    logout(request)  # Déconnecte toujours l'utilisateur au début

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'restaurant/login.html', {'error': 'Identifiants invalides'})

    return render(request, 'restaurant/login.html')


# Vue Déconnexion
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Page Accueil (Dashboard)
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    plats = Plat.objects.all()
    return render(request, 'restaurant/dashboard.html', {'plats': plats})



# Liste des plats
@login_required
def liste_plats(request):
    plats = Plat.objects.all()
    return render(request, 'restaurant/liste_plats.html', {'plats': plats})


# Ajouter plat (Gestionnaire uniquement)
@login_required
@user_passes_test(est_gestionnaire)
def ajouter_plat(request):
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PlatForm()
    return render(request, 'restaurant/ajouter_plat.html', {'form': form})


# Modifier plat
@login_required
def modifier_plat(request, pk):
    plat = get_object_or_404(Plat, pk=pk)
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES, instance=plat)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PlatForm(instance=plat)
    return render(request, 'restaurant/modifier_plat.html', {'form': form})


# Supprimer plat
@login_required
def supprimer_plat(request, pk):
    plat = get_object_or_404(Plat, pk=pk)
    if request.method == 'POST':
        plat.delete()
        return redirect('dashboard')
    return render(request, 'restaurant/supprimer_plat.html', {'plat': plat})

from .forms import InscriptionForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = InscriptionForm()
    
    return render(request, 'restaurant/inscription.html', {'form': form})

def password_reset_view(request):
    return render(request, 'restaurant/password_reset.html')


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'restaurant/inscription.html', {'form': form})

from django.shortcuts import render
from .models import Categorie

def home_view(request):
    categories = Categorie.objects.prefetch_related('plats').all()
    return render(request, 'restaurant/home.html', {'categories': categories})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReservationForm

def reservation_submit(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre réservation a bien été prise en compte. Merci !")
            return redirect('home')
    else:
        form = ReservationForm()

    return render(request, 'restaurant/reservation_form.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plat, Commande
from .forms import CommandeForm

from django.shortcuts import render, get_object_or_404
from .models import Plat

def commander_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    return render(request, 'restaurant/commande.html', {'plat': plat})

@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(utilisateur=request.user)
    return render(request, 'restaurant/mes_commandes.html', {'commandes': commandes})

# restaurant/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'restaurant/dashboard.html')

@login_required
def statistiques(request):
    return render(request, 'restaurant/statistiques.html')

@login_required
def infos_restaurant(request):
    return render(request, 'restaurant/infos_restaurant.html')

@login_required
def paiements(request):
    return render(request, 'restaurant/paiements.html')

@login_required
def menu(request):
    return render(request, 'restaurant/menu.html')

@login_required
def reservations(request):
    return render(request, 'restaurant/reservations.html')

@login_required
def horaires(request):
    return render(request, 'restaurant/horaires.html')

@login_required
def tables(request):
    return render(request, 'restaurant/tables.html')


from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Reservation
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

def reserver_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            # Envoi d'email de confirmation
            send_mail(
                'Confirmation de votre réservation',
                f"Merci {reservation.nom}, votre réservation pour le {reservation.date} à {reservation.heure} a bien été enregistrée.",
                'elhadjifallbasse@gmail.com',
                [reservation.email],
                fail_silently=False,
            )
            return render(request, 'restaurant/reservation_confirmation.html', {'reservation': reservation})
    else:
        form = ReservationForm()
    return render(request, 'restaurant/reserver_table.html', {'form': form})

@login_required
def admin_reservations(request):
    reservations = Reservation.objects.all().order_by('-date')
    return render(request, 'restaurant/admin_reservations.html', {'reservations': reservations})

@login_required
def confirmer_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.confirme = True
    reservation.save()
    # Email de confirmation au client
    send_mail(
        'Votre réservation est confirmée',
        f"Bonjour {reservation.nom}, votre réservation a été confirmée pour le {reservation.date} à {reservation.heure}.",
        'votre_email@example.com',
        [reservation.email],
        fail_silently=False,
    )
    return redirect('admin_reservations')
