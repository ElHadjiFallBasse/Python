from django.contrib import admin
from .models import Client, Appartement, Location

admin.site.register(Client)
admin.site.register(Appartement)
admin.site.register(Location)