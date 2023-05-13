from django import forms
from .models import Collection, MovieCollection


class CollectionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '컬렉션 제목',
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '설명 입력하기',
            }
        )
    )
    class Meta:
        model = Collection
        fields = ('title', 'content',)


class MovieCollectionForm(forms.ModelForm):
    class Meta:
        model = MovieCollection
        fields = ('movie_id',)

