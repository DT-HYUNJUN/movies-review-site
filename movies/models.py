from django.db import models
from django.conf import settings
from dotenv import load_dotenv
import os
import requests
load_dotenv()


class MovieLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie_id = models.IntegerField()


class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_collections')
    title = models.CharField(max_length=100)
    content = models.TextField()


class MovieCollection(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    movie_poster = models.CharField(max_length=200, default='', null=True)

    def __str__(self):
        url = f'https://api.themoviedb.org/3/movie/{self.movie_id}'
        api_key = os.getenv('TMDB_API_KEY')
        params = {
            'api_key': api_key,
            'language': 'ko-KR',
        }
        movie = requests.get(url, params=params).json()
        return movie['title']