from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'collection-field',
                'placeholder': '컬렉션 제목',
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'collection-field',
                'placeholder': '설명 입력하기',
            }
        )
    )
    class Meta:
        model = Collection
        fields = ('title', 'content',)