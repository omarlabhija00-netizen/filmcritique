from django.db import models
from django.conf import settings
from movie.models import Movie

class Review(models.Model):
    film = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    note = models.IntegerField()
    utile = models.BooleanField(default=False)
    statut = models.CharField(max_length=20, choices=[("vu", "Vu"), ("a_voir", "À voir")])

    def __str__(self):
        return f"{self.auteur.username} - {self.film.titre}"