from django.urls import path
from . import views

urlpatterns = [
    path('', views.gestion, name='gestion'),
    path('client/<int:pk>/', views.detail_client, name='detail_client'),
    path('client/modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    path('client/supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),
    path('appart/<int:pk>/', views.detail_appart, name='detail_appart'),
    path('appart/modifier/<int:pk>/', views.modifier_appart, name='modifier_appart'),
    path('appart/supprimer/<int:pk>/', views.supprimer_appart, name='supprimer_appart'),
]
