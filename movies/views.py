import re
from django.shortcuts import render, redirect
from .models import Collection, MovieCollection
from reviews.models import Review
from .forms import CollectionForm, MovieCollectionForm
from reviews.forms import ReviewForm
from dotenv import load_dotenv
from django.utils import timezone
import os
import requests
import pycountry
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Avg


load_dotenv()
base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')


def index(request):
    # 현재 시간
    now_time = timezone.now()

    params = {
        'api_key': api_key,
        'language': 'ko-kr',
        'region': 'kr'
    }

    # 현재 상영 영화 인기순으로 5개
    path = '/movie/now_playing'
    playing_movies_response = requests.get(base_url+path, params=params).json()
    playing_movies = sorted(playing_movies_response['results'], key=lambda x: x['popularity'], reverse=True)[:5]


    # 인기영화 5개
    path = '/movie/popular'
    popular_movies_response = requests.get(base_url+path, params=params).json()
    popular_movies = popular_movies_response['results'][:5]

    # 평점 높은 영화
    path = '/movie/top_rated'
    top_movies_response = requests.get(base_url+path, params=params).json()
    top_movies = top_movies_response['results'][:5]

    # 상영예정작(인기 많은 5개 뽑아서 d-day순으로 정렬)
    path = '/movie/upcoming'
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
        'language': 'ko-KR'
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
        'language': 'ko-KR',
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

    #  한글 이름 출력
    lst = []
    name = ''
    names = person['also_known_as']
    if names:
        i_am_korean(names, lst)
        if lst:
            name = lst[0]
    else:
        name = person['name']
    context = {
        'name': name,
        'person': person,
        'category': category.items(),
        'job': '/'.join(job),
    }
    return render(request, 'movies/person_detail.html', context)

def i_am_korean(names, lst):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    for name in names:
        result = hangul.sub('', name)
        if result.strip():
            lst.append(result)
            
def search(request):
    string = request.GET.get('search')
    path = f'/search'
    params = {
        'api_key': api_key,
        'query': string,
        'language': 'ko-KR',
        'region': 'kr'
    }

    # 영화/인물 검색 데이터 1page ~ 존재하는 page까지 인기순 정렬
    total_movies = []
    page = 1
    while 1:
        params['page'] = page
        movies_response = requests.get(base_url+path+'/movie', params=params).json()
        if len(movies_response['results']) == 0:
            break
        movies = sorted(movies_response['results'], key=lambda x: x['popularity'], reverse=True)
        total_movies += movies
        page += 1

    total_people = []
    page = 1
    while 1:
        params['page'] = page
        people_response = requests.get(base_url+path+'/person', params=params).json()
        if len(people_response['results']) == 0:
            break
        people = sorted(people_response['results'], key=lambda x: x['popularity'], reverse=True)
        for person in people:
            if person['known_for_department'] in {'Acting', 'Actors'}:
                person['job'] = '배우'
            elif person['known_for_department'] == 'Directing':
                person['job'] = '감독'
            elif person['known_for_department'] == 'Writing':
                person['job'] = '작가'
            elif person['known_for_department'] == 'Production':
                person['job'] = '프로듀서'
            else:
                person['job'] = '스탭'
            new = []
            cnt = 0
            for movie in sorted(person['known_for'], key=lambda x: x['popularity'], reverse=True):
                if cnt == 2:
                    break
                if movie['media_type'] == 'movie':
                    new.append(movie)
                    cnt += 1
            person['known_for'] = new

        total_people += people
        page += 1

    context = {
        'key_word': string,
        'movies': total_movies,
        'people': total_people,
    }
    return render(request, 'movies/search.html', context)


@login_required
def create(request, username):
    # 자신의 계정으로만 컬렉션 생성 가능하도록
    if request.user != get_user_model().objects.get(username=username):
        return redirect('accounts:profile', username)
    
    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)
        movie_form = MovieCollectionForm(request.POST)
        if collection_form.is_valid() and movie_form.is_valid():
            collection = collection_form.save(commit=False)
            collection.user = request.user
            collection.save()
            movies = movie_form.save(commit=False)
            movies.collection = collection
            movies.save()
            return redirect('accounts:profile', username)
    else:
        collection_form = CollectionForm()
        movie_form = MovieCollectionForm()
    context = {
        'collection_form': collection_form,
        'movie_form': movie_form,
    }
    return render(request, 'movies/create.html', context)


def collection_detail(request, username, collection_pk):
    person = get_user_model().objects.get(username=username)
    collection = Collection.objects.get(pk=collection_pk)
    movies = collection.moviecollection_set.all()
    collection_movies = []
    params = {
        'api_key': api_key,
        'language': 'ko-KR'
    }
    for movie in movies:
        path = f'/movie/{movie.movie_id}'
        movie_info = requests.get(base_url+path, params=params).json()
        movie_avg = Review.objects.filter(movie=movie.movie_id).aggregate(avg=(Avg('rating')))
        movie_info['avg'] = movie_avg['avg'] if movie_avg['avg'] != None else 0
        collection_movies.append(movie_info)
    context = {
        'person': person,
        'collection': collection,
        'movies': collection_movies,
    }
    return render(request, 'movies/collection_detail.html', context)


@login_required
def update(request, username, collection_pk):
    if request.user != get_user_model().objects.get(username=username):
        return redirect('accounts:profile', username)
    
    collection = Collection.objects.get(pk=collection_pk)
    if request.method == 'POST':
        collection_form = CollectionForm(request.POST, instance=collection)
        movie_form = MovieCollectionForm(request.POST, instance=collection)
        if collection_form.is_valid() and movie_form.is_valid():
            collection_form.save()
            movie_form.save()
            return redirect('movies:collection_detail', collection.pk)
    else:
        collection_form = CollectionForm(instance=collection)
        movie_form = MovieCollectionForm(instance=collection)
    context = {
        'collection': collection,
        'collection_form': collection_form,
        'movie_form': movie_form,
    }
    return render(request, 'movies/update.html', context)


@login_required
def delete(request, username, collection_pk):
    if request.user != get_user_model().objects.get(username=username):
        return redirect('accounts:profile', username)
    
    collection = Collection.objects.get(pk=collection_pk)
    movies = collection.moviecollection_set.all()
    for movie in movies:
        movie.delete()
    collection.delete()
    return redirect('accounts:profile', username)