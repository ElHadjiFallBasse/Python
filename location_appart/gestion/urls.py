from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('clients/', views.liste_clients, name='clients'),
    path('clients/ajouter/', views.ajouter_client, name='ajouter_client'),

    path('appartements/', views.liste_appartements, name='appartements'),
    path('appartements/ajouter/', views.ajouter_appartement, name='ajouter_appartement'),

    path('champs/', views.liste_champs, name='champs'),
    path('champs/ajouter/', views.ajouter_champ, name='ajouter_champ'),
]
