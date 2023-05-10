from django.shortcuts import render, redirect
from dotenv import load_dotenv
import os
import requests

load_dotenv()

base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')

def index(request):
    # 현재 상영 영화 인기순으로 5개
    path = '/movie/now_playing'
    params = {
        'api_key': api_key,
        'language': 'ko-kr',
        'region': 'kr'
    }
    playing_movies_response = requests.get(base_url+path, params=params).json()
    playing_movies = sorted(playing_movies_response['results'], key=lambda x: x['popularity'], reverse=True)[:5]

    # 인기영화 5개
    path = '/movie/popular'
    params = {
        'api_key': api_key,
        'language': 'ko-kr',
        'region': 'kr'
    }
    popular_movies_response = requests.get(base_url+path, params=params).json()
    popular_movies = popular_movies_response['results'][:5]

    # 평점 높은 영화
    path = '/movie/top_rated'
    params = {
        'api_key': api_key,
        'language': 'ko-kr',
        'region': 'kr'
    }
    top_movies_response = requests.get(base_url+path, params=params).json()
    top_movies = top_movies_response['results'][:5]

    # 상영예정작(인기 많은 5개 뽑아서 d-day순으로 정렬)
    path = '/movie/upcoming'
    params = {
        'api_key': api_key,
        'language': 'ko-kr',
        'region': 'kr'
    }
    upcoming_movies_response = requests.get(base_url+path, params=params).json()
    upcoming_movies = sorted(upcoming_movies_response['results'], key=lambda x: x['popularity'], reverse=True)[:5]

    context = {
        'playing_movies': playing_movies,
        'popular_movies': popular_movies,
        'top_movies': top_movies,
        'upcoming_movies': sorted(upcoming_movies, key=lambda x: x['release_date'])
    }
    return render(request, 'movies/index.html', context)


def detail(request, movie_id):
    path = f'/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'language': 'ko-kr'
    }
    movie = requests.get(base_url+path, params=params).json()
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)