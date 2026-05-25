from django.db import models
from django.conf import settings
from movie.models import Movie

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Movie, on_delete=models.CASCADE)
    raison = models.CharField(max_length=200)

    def __str__(self):
        return f"Reco pour {self.user.username}: {self.film.titre}"