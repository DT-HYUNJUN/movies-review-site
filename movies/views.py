from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import requests


load_dotenv()


def index(request):
    base_url = 'https://api.themoviedb.org/3/'
    api_key = os.getenv('TMDB_API_KEY')

    # 현재 상영 영화 인기순으로 5개
    path = '/movie/now_playing'
    params = {
        'api_key': api_key,
        'language': 'ko-kr'
    }
    playing_movies_response = requests.get(base_url+path, params=params).json()
    playing_movies = sorted(playing_movies_response['results'], key=lambda x: x['popularity'], reverse=True)[:5]

    # 인기영화 10개
    path = ''
    params = {
        'api_key': api_key,
        'language': 'ko-kr'
    }

    context = {
        'playing_movies': playing_movies,
    }
    return render(request, 'movies/index.html', context)


#     from pprint import pprint
#     pprint(playing_movies)
    
# index()