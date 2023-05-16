from django import forms
from .models import Collection, MovieCollection


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


class CollectionMovieDeleteForm(forms.ModelForm):
    delete_movies = forms.ModelMultipleChoiceField(
        # label = '삭제할 영화 선택',
        queryset=MovieCollection.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'text-dark',
            }
        ),
        required=False,
    )
    class Meta:
        model = MovieCollection
        fields = []

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        if instance:
            self.fields['delete_movies'].queryset = instance.moviecollection_set.all()
    
    def save(self, commit=True):
        for movie in self.cleaned_data['delete_movies']:
            movie.delete()