from django.shortcuts import render
from movie.models import Movie
from reviews.models import Review
from recommendations.models import Recommendation

def dashboard(request):
    total_films = Movie.objects.count()
    total_reviews = Review.objects.count()
    total_recos = Recommendation.objects.count()
    derniers_films = Movie.objects.order_by('-id')[:4]
    return render(request, 'dashboard/dashboard.html', {
        'total_films': total_films,
        'total_reviews': total_reviews,
        'total_recos': total_recos,
        'derniers_films': derniers_films,
    })