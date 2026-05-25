from django.shortcuts import render, get_object_or_404
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    genre = request.GET.get('genre')
    annee = request.GET.get('annee')
    if genre:
        movies = movies.filter(genre__icontains=genre)
    if annee:
        movies = movies.filter(date_sortie__year=annee)
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    return render(request, 'movie/movie_list.html', {
        'movies': movies,
        'genres': genres,
    })

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = movie.reviews.all()
    return render(request, 'movie/movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
    })