# --- Imports ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail

from .models import Plat, Categorie, Commande, Reservation
from .forms import PlatForm, ReservationForm, CommandeForm, RegisterForm

# --- Vérifie si l'utilisateur est un gestionnaire ---
def est_gestionnaire(user):
    return user.groups.filter(name='Gestionnaire').exists()

# ========================
# === Authentification ===
# ========================

def login_view(request):
    logout(request)  # Déconnecte systématiquement avant un nouveau login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'restaurant/login.html', {'error': 'Identifiants invalides'})
    return render(request, 'restaurant/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'restaurant/inscription.html', {'form': form})

def password_reset_view(request):
    return render(request, 'restaurant/password_reset.html')

# ============================
# === Vue publique accueil ===
# ============================

def accueil_public(request):
    categories = Categorie.objects.prefetch_related('plats').all()
    return render(request, 'restaurant/home.html', {'categories': categories})

# ============================
# === Dashboard & gestion ====
# ============================

@login_required
def dashboard(request):
    plats = Plat.objects.all()
    return render(request, 'restaurant/dashboard.html', {'plats': plats})

@login_required
@user_passes_test(est_gestionnaire)
def ajouter_plat(request):
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Plat ajouté avec succès.")
            return redirect('dashboard')
    else:
        form = PlatForm()
    return render(request, 'restaurant/ajouter_plat.html', {'form': form})

@login_required
def modifier_plat(request, pk):
    plat = get_object_or_404(Plat, pk=pk)
    if request.method == 'POST':
        form = PlatForm(request.POST, request.FILES, instance=plat)
        if form.is_valid():
            form.save()
            messages.success(request, "Plat modifié avec succès.")
            return redirect('dashboard')
    else:
        form = PlatForm(instance=plat)
    return render(request, 'restaurant/modifier_plat.html', {'form': form})

@login_required
def supprimer_plat(request, pk):
    plat = get_object_or_404(Plat, pk=pk)
    if request.method == 'POST':
        plat.delete()
        messages.success(request, "Plat supprimé.")
        return redirect('dashboard')
    return render(request, 'restaurant/supprimer_plat.html', {'plat': plat})

# ============================
# === Vues annexes internes ==
# ============================

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

# ======================
# === Commandes ===
# ======================

def commander_plat(request, plat_id):
    plat = get_object_or_404(Plat, id=plat_id)
    return render(request, 'restaurant/commande.html', {'plat': plat})

@login_required
def mes_commandes(request):
    commandes = Commande.objects.filter(utilisateur=request.user)
    return render(request, 'restaurant/mes_commandes.html', {'commandes': commandes})

# ======================
# === Réservations ===
# ======================

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

def reserver_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            send_mail(
                'Confirmation de votre réservation',
                f"Merci {reservation.nom}, votre réservation pour le {reservation.date} à {reservation.heure} a bien été enregistrée.",
                'elhadjifallbasse@gmail.com',  # Remplacer par DEFAULT_FROM_EMAIL
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
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.confirme = True
    reservation.save()
    send_mail(
        'Votre réservation est confirmée',
        f"Bonjour {reservation.nom}, votre réservation a été confirmée pour le {reservation.date} à {reservation.heure}.",
        'elhadjifallbasse@gmail.com',  # Remplacer par DEFAULT_FROM_EMAIL
        [reservation.email],
        fail_silently=False,
    )
    return redirect('admin_reservations')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produit, Commande, ItemCommande

@login_required
def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'restaurant/liste_produits.html', {'produits': produits})

@login_required
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    commande, created = Commande.objects.get_or_create(client=request.user, est_validee=False)
    item, created = ItemCommande.objects.get_or_create(commande=commande, produit=produit)
    if not created:
        item.quantite += 1
    item.save()
    return redirect('afficher_panier')

@login_required
def afficher_panier(request):
    commande = Commande.objects.filter(client=request.user, est_validee=False).first()
    items = commande.items.all() if commande else []
    total = commande.total() if commande else 0
    return render(request, 'restaurant/panier.html', {'items': items, 'total': total})

@login_required
def modifier_quantite(request, item_id, action):
    item = get_object_or_404(ItemCommande, id=item_id, commande__client=request.user, commande__est_validee=False)
    if action == 'plus':
        item.quantite += 1
        item.save()
    elif action == 'moins':
        if item.quantite > 1:
            item.quantite -= 1
            item.save()
        else:
            item.delete()
    return redirect('afficher_panier')

@login_required
def valider_commande(request):
    commande = Commande.objects.filter(client=request.user, est_validee=False).first()
    if commande and commande.items.exists():
        commande.est_validee = True
        commande.save()
        return render(request, 'restaurant/confirmation.html', {'commande': commande})
    else:
        return redirect('afficher_panier')
