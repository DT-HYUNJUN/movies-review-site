from django import forms
from .models import Review, ReviewComment

class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'id': 'review-field',
                'placeholder': '이 작품에 대한 생각을 자유롭게 표현해주세요',
                'class': 'review-form w-100 border-0',
            }
        ),
    )
    class Meta:
        model = Review
        fields = ('content',)



class ReviewCommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'id': 'comment-field',
                'placeholder': '',
                'class': 'review-form w-100 border-0',
            }
        ),
    )

    class Meta:
        model = ReviewComment
        fields = ('content',)