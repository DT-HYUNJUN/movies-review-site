from django import forms
from .models import Review, ReviewComment

class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'placeholder': '이 작품에 대한 생각을 자유롭게 표현해주세요',
            'class': 'form-control',
        })
    )
    class Meta:
        model = Review
        fields = ('content', 'is_spoiler',)



class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ('content',)