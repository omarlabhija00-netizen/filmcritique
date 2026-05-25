from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('film', 'auteur', 'note', 'utile', 'statut')
    list_filter = ('note', 'utile', 'statut')
    search_fields = ('contenu', 'auteur__username', 'film__titre')
