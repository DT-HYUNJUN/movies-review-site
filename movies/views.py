from django.shortcuts import render, redirect
from .forms import CollectionForm, MovieCollectionForm
from reviews.forms import ReviewForm
from dotenv import load_dotenv
from django.utils import timezone
import os
import requests
import pycountry

load_dotenv()
base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')


def index(request):
    # 현재 시간
    now_time = timezone.now()

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
        'now_time': now_time,
        'playing_movies': playing_movies,
        'popular_movies': popular_movies,
        'top_movies': top_movies,
        'upcoming_movies': sorted(upcoming_movies, key=lambda x: x['release_date'])
    }
    
    return render(request, 'movies/index.html', context)


def detail(request, movie_id):
    # 리뷰 폼
    review_form = ReviewForm()

    path = f'/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'language': 'ko-kr'
    }
    movie = requests.get(base_url+path, params=params).json()
    movie_credits = requests.get(base_url+path+'/credits', params=params).json()
    
    # 개봉연도
    year = movie['release_date'][:4]
    
    # 장르 불러오기
    genres_list = movie['genres']
    tmp = []
    for genre in genres_list:
        tmp.append(genre['name'])
    genres = '/'.join(tmp)
    
    # 국가 코드
    country_code = movie['production_countries'][0]['iso_3166_1']
    try:
        country = pycountry.countries.get(alpha_2=country_code).name
    except AttributeError:
        pass

    # 감독
    crews = []
    for crew in movie_credits['crew']:
        if crew['job'] == 'Director':
            crews.append(crew)

    # 출연진
    casts = movie_credits['cast']
    if len(casts) > 12 - len(crews):
        casts = casts[:12-len(crews)]
    
    context = {
        'year': year,
        'country': country,
        'movie': movie,
        'genres': genres,
        'crews': crews,
        'casts': casts,
        'review_form': review_form,
    }
    return render(request, 'movies/detail.html', context)


def person_detail(request, person_id):
    path = f'/person/{person_id}'
    params = {
        'api_key': api_key,
        'language': 'ko-kr',
    }
    person = requests.get(base_url+path, params=params).json()

    # 카테고리 별 영화 리스트(최신순 정렬)
    info = requests.get(base_url+path+'/movie_credits', params=params).json()
    category = {'감독': [], '출연': [], '각본': []}
    if info.get('cast', False):
        category['출연'] = sorted(info['cast'], key=lambda x: x['release_date'], reverse=True)
    if info.get('crew', False):
        for movie in info['crew']:
            if movie['job'] == 'Director':
                category['감독'].append(movie)
            elif movie['job'] == 'Writer':
                category['각본'].append(movie)
        category['감독'].sort(key=lambda x: x['release_date'], reverse=True)
        category['각본'].sort(key=lambda x: x['release_date'], reverse=True)

    # 인물 직업
    job = []
    for key, movies in category.items():
        if movies:
            if key == '출연':
                job.append('배우')
            elif key == '각본':
                job.append('작가')
            else:
                job.append('감독')

    context = {
        'person': person,
        'category': category.items(),
        'job': '/'.join(job),
    }
    return render(request, 'movies/person_detail.html', context)


# ---------------collection---------------------
# def create(request):
#     if request.method == 'POST':
#         pass
#     else:
#         collection_form = CollectionForm()
#         movie_form = MovieCollectionForm()
#     context = {
#         'collection_form': collection_form,
#         'movie_form': movie_form,
#     }


# def update(request, collection_pk):
#     pass