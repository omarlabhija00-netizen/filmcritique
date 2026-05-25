from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('titre', 'realisateur', 'date_sortie', 'genre')
    search_fields = ('titre', 'realisateur', 'genre')
    list_filter = ('genre', 'date_sortie')
