from django.shortcuts import render
from django.db.models import Count
from reviews.models import Review
import os
import requests
import json
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()
base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')

def review_count(request):
    # 리뷰 개수를 구합니다.
    reviews_count = Review.objects.aggregate(count=Count('id'))['count']

    context = {
        # 기존 context 변수에 추가합니다.
        'reviews_count': reviews_count
    }
    return context


def genre_dict_modal(request):
    
    genre_dict_modal = [
        '액션',
        '어드벤처',
        '애니메이션',
        '코미디',
        '범죄',
        '다큐멘터리',
        '드라마',
        '가족',
        '판타지',
        '역사',
        '공포',
        '음악',
        '미스터리',
        '로맨스',
        'SF',
        'TV',
        '스릴러',
        '전쟁',
        '서부',
    ]
    
    context = {
        'genre_dict_modal': genre_dict_modal,
    }
    return context


def day_trending_movies(request):
    params = {
        'api_key': api_key,
        'language': 'ko-kr',
        'region': 'kr'
    }
    path = '/trending/movie/day'
    day_trending_movies_response = requests.get(base_url+path, params=params).json()
    day_trending_movies = []
    for dtm in day_trending_movies_response['results'][:5]:
        day_trending_movies.append(dtm.get('title'))
    
    context = {
        'day_trending_movies': day_trending_movies,
    }
    return context