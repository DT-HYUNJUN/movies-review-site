from django import forms
from .models import Collection, MovieCollection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('title', 'content',)