"""
Commande Django pour importer 20 films populaires depuis l'API TMDB.

Utilisation :
    python manage.py import_movies

Placement du fichier :
    movie/management/commands/import_movies.py
"""

import requests
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from movie.models import Movie

TMDB_API_KEY = "e4d5d56cdf08e1d86a32d851cd3df858"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


class Command(BaseCommand):
    help = "Importe 20 films populaires depuis l'API TMDB"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO("\n🎬 Démarrage de l'import TMDB...\n"))

        # 1. Récupérer les films populaires
        url = f"{TMDB_BASE_URL}/movie/popular"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "fr-FR",
            "page": 1,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f"Erreur API TMDB : {response.status_code}"))
            return

        films = response.json().get("results", [])[:20]
        self.stdout.write(f"  {len(films)} films récupérés depuis TMDB\n")

        importes = 0
        ignores = 0

        for film_data in films:
            titre = film_data.get("title", "Titre inconnu")

            # Éviter les doublons
            if Movie.objects.filter(titre=titre).exists():
                self.stdout.write(f"  ⏭  Ignoré (déjà existant) : {titre}")
                ignores += 1
                continue

            # 2. Récupérer les détails complets du film (réalisateur, acteurs, durée)
            film_id = film_data["id"]
            detail_url = f"{TMDB_BASE_URL}/movie/{film_id}"
            credits_url = f"{TMDB_BASE_URL}/movie/{film_id}/credits"

            detail_params = {"api_key": TMDB_API_KEY, "language": "fr-FR"}

            detail_resp = requests.get(detail_url, params=detail_params)
            credits_resp = requests.get(credits_url, params=detail_params)

            detail = detail_resp.json() if detail_resp.status_code == 200 else {}
            credits = credits_resp.json() if credits_resp.status_code == 200 else {}

            # Réalisateur
            realisateur = "Inconnu"
            for membre in credits.get("crew", []):
                if membre.get("job") == "Director":
                    realisateur = membre.get("name", "Inconnu")
                    break

            # Acteurs (les 5 premiers)
            acteurs_list = credits.get("cast", [])[:5]
            acteurs = ", ".join([a.get("name", "") for a in acteurs_list]) or "Non renseigné"

            # Autres champs
            synopsis = film_data.get("overview", "") or "Aucun synopsis disponible."
            date_sortie = film_data.get("release_date") or "2000-01-01"
            duree = detail.get("runtime") or 90
            genres = detail.get("genres", [])
            genre = genres[0]["name"] if genres else "Divers"

            # 3. Créer l'objet Movie
            movie = Movie(
                titre=titre,
                realisateur=realisateur,
                acteurs=acteurs,
                synopsis=synopsis,
                date_sortie=date_sortie,
                duree=duree,
                genre=genre,
            )

            # 4. Télécharger l'affiche
            poster_path = film_data.get("poster_path")
            if poster_path:
                try:
                    img_url = f"{TMDB_IMAGE_BASE}{poster_path}"
                    img_response = requests.get(img_url, timeout=10)
                    if img_response.status_code == 200:
                        filename = f"{film_id}.jpg"
                        movie.image.save(
                            filename,
                            ContentFile(img_response.content),
                            save=False,
                        )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  ⚠  Affiche non téléchargée pour {titre} : {e}"))

            movie.save()
            importes += 1
            self.stdout.write(self.style.SUCCESS(f"  ✅ Importé : {titre} ({genre}, {date_sortie[:4]})"))

        # Résumé final
        self.stdout.write("\n" + "─" * 50)
        self.stdout.write(self.style.SUCCESS(f"  ✅ {importes} films importés avec succès"))
        if ignores:
            self.stdout.write(self.style.WARNING(f"  ⏭  {ignores} films ignorés (déjà en base)"))
        self.stdout.write("─" * 50 + "\n")