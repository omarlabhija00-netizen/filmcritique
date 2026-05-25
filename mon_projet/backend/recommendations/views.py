from django.shortcuts import render
from .models import Recommendation

def recommendation_list(request):
    recommendations = Recommendation.objects.all()
    return render(request, "recommendations/recommendation_list.html", {"recommendations": recommendations})