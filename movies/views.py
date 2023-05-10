from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import requests


load_dotenv()


def index(request):
    base_url = 'https://api.themoviedb.org/3/'
    api_key = os.getenv('TMDB_API_KEY')

    # 현재 상영
    path = '/movie/now_playing'
    params = {
        'api_key': api_key,
        'language': 'ko-kr'
    }
    playing_movies = requests.get(base_url+path, params=params).json()

    from pprint import pprint
    pprint(index(playing_movies))