from django.db import models
from django.conf import settings
from dotenv import load_dotenv
import os
import requests
load_dotenv()


class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_collections')
    title = models.CharField(max_length=100)
    content = models.TextField()


class MovieCollection(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    movie_poster = models.CharField(max_length=200, default='')

    def __str__(self):
        return str(self.movie_id)