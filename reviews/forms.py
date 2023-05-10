from django import forms
from .models import Review, ReviewComment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'movie', 'content', 'rating')


class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('content',)