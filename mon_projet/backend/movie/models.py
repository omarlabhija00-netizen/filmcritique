from django.db import models

class Movie(models.Model):
    titre = models.CharField(max_length=200)
    realisateur = models.CharField(max_length=100)
    acteurs = models.TextField()
    synopsis = models.TextField()
    date_sortie = models.DateField()
    duree = models.IntegerField()
    genre = models.CharField(max_length=100)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

    def __str__(self):
        return self.titre