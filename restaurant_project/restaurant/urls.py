from django.urls import path
from . import views
from .views import home_view


urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.home, name='dashboard'),
    path('ajouter/', views.ajouter_plat, name='ajouter_plat'),
    path('modifier/<int:pk>/', views.modifier_plat, name='modifier_plat'),
    path('supprimer/<int:pk>/', views.supprimer_plat, name='supprimer_plat'),
    path('plats/', views.liste_plats, name='liste_plats'),
    path('inscription/', views.register_view, name='ajouter_utilisateur'),   # ✅ Inscription
    path('password-reset/', views.password_reset_view, name='mot_de_passe_oublie'),  # ✅ Mot de passe
    path('home/', views.home_view, name='home'),  # page d'accueil accessible via /home/
    path('reservation/submit/', views.reservation_submit, name='reservation_submit'),
    path('commander/', views.commander_plat, name='commander_plat'),
    path('mes-commandes/', views.mes_commandes, name='mes_commandes'),
    path('commander/<int:plat_id>/', views.commander_plat, name='commander_plat'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('infos_restaurant/', views.infos_restaurant, name='infos_restaurant'),
    path('paiements/', views.paiements, name='paiements'),
    path('menu/', views.menu, name='menu'),
    path('reservations/', views.reservations, name='reservations'),
    path('horaires/', views.horaires, name='horaires'),
    path('tables/', views.tables, name='tables'),
    path('reserver/', views.reserver_table, name='reserver_table'),
    path('admin_reservations/', views.admin_reservations, name='admin_reservations'),
    path('confirmer_reservation/<int:reservation_id>/', views.confirmer_reservation, name='confirmer_reservation'),

]
