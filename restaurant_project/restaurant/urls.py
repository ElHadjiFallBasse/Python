from django.urls import path
from . import views
from django.urls import path, include


urlpatterns = [
    # Authentification
    path('', views.login_view, name='login'),  # racine = page de connexion
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inscription/', views.register_view, name='inscription'),
    path('password-reset/', views.password_reset_view, name='password_reset'),

    # Accueil / Dashboard
    path('home/', views.accueil_public, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Menus
    path('menu/', views.menu, name='menu'),
    path('ajouter/', views.ajouter_plat, name='ajouter_plat'),
    path('modifier/<int:pk>/', views.modifier_plat, name='modifier_plat'),
    path('supprimer/<int:pk>/', views.supprimer_plat, name='supprimer_plat'),

    # Commandes
    path('commander/', views.commander_plat, name='commander_tous_plats'),
    path('commander/<int:plat_id>/', views.commander_plat, name='commander_un_plat'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),

    # Réservations
    path('reserver/', views.reserver_table, name='reserver_table'),
    path('reservation/submit/', views.reservation_submit, name='reservation_submit'),
    path('reservations/', views.reservations, name='reservations'),
    path('admin_reservations/', views.admin_reservations, name='admin_reservations'),
    path('confirmer_reservation/<int:reservation_id>/', views.confirmer_reservation, name='confirmer_reservation'),

    # Infos Restaurant
    path('infos_restaurant/', views.infos_restaurant, name='infos_restaurant'),
    path('horaires/', views.horaires, name='horaires'),
    path('tables/', views.tables, name='tables'),
    path('paiements/', views.paiements, name='paiements'),

    # Statistiques
    path('statistiques/', views.statistiques, name='statistiques'),


    path('produits/', views.liste_produits, name='liste_produits'),
    path('panier/', views.afficher_panier, name='afficher_panier'),
    path('ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('modifier/<int:item_id>/<str:action>/', views.modifier_quantite, name='modifier_quantite'),
    path('valider/', views.valider_commande, name='valider_commande'),

]
