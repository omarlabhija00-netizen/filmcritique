from django.contrib import admin
from .models import Recommendation

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'raison')
    search_fields = ('user__username', 'film__titre', 'raison')
