from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['film', 'contenu', 'note', 'statut']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 4}),
            'note': forms.Select(choices=[(i, f'{i} ⭐') for i in range(1, 6)]),
            'statut': forms.Select(),
        }