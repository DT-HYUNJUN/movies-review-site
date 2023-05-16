import re
from django.shortcuts import render, redirect, get_object_or_404
from .models import Collection, MovieCollection
from reviews.models import Review, Emote
from .forms import CollectionForm, CollectionMovieDeleteForm
from reviews.models import Review
from reviews.forms import ReviewForm
from dotenv import load_dotenv
from django.utils import timezone
import os
import requests
import pycountry
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.views.decorators.cache import cache_page


load_dotenv()
base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')


def get_average_rating(movies):
    for movie in movies:
        movie_id = movie['id']
        # 리뷰
        reviews = Review.objects.filter(movie=movie_id).order_by('-pk')
        if len(reviews) == 0:
            movie['avg_rating'] = ''
        else:
            # 평점 계산
            movies_rating_dict = {0.0: 0, 0.5: 0, 1.0: 0, 1.5: 0, 2.0: 0, 2.5: 0, 3.0: 0, 3.5: 0, 4.0: 0, 4.5: 0, 5.0: 0}
            for review in reviews:
                movies_rating_dict[review.rating] += 1
            
            sum_ratings = 0
            avg_rating = 0
            rating_people = sum(movies_rating_dict.values())
            for key, value in movies_rating_dict.items():
                sum_ratings += key * value
            if rating_people:
                avg_rating = round((sum_ratings / rating_people), 1)
            movie['avg_rating'] = avg_rating

@cache_page(60 * 5)
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
    playing_movies = sorted(playing_movies_response['results'], key=lambda x: x['popularity'], reverse=True)[:20]
    get_average_rating(playing_movies)
    
    playing_movies_trailers = []
    for movie in playing_movies:
        movie_id = movie['id']
        path = f'/movie/{movie_id}/videos'
        params_trailer = {
            'api_key': api_key,
            'movie_id': movie_id,
        }
        videos = requests.get(base_url+path, params=params_trailer).json()['results']
        for video in videos:
            if video['type'] == 'Trailer':
                video_key = video['key']
                playing_movies_trailers.append(video_key)
                break


    # 인기영화 5개
    path = '/movie/popular'
    popular_movies_response = requests.get(base_url+path, params=params).json()
    popular_movies = popular_movies_response['results'][:20]
    get_average_rating(popular_movies)

    # 평점 높은 영화
    path = '/movie/top_rated'
    top_movies_response = requests.get(base_url+path, params=params).json()
    top_movies = top_movies_response['results'][:20]
    get_average_rating(top_movies)

    # 상영예정작(인기 많은 5개 뽑아서 d-day순으로 정렬)
    path = '/movie/upcoming'
    upcoming_movies_response = requests.get(base_url+path, params=params).json()
    upcoming_movies = sorted(upcoming_movies_response['results'], key=lambda x: x['popularity'], reverse=True)[:20]
    get_average_rating(upcoming_movies)

    context = {
        'playing_movies_trailers': playing_movies_trailers,
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
    
    # 리뷰
    reviews = Review.objects.filter(movie=movie_id).order_by('-pk')
    total_reviews = len(reviews)

    review_info_lst = []
    for review in reviews:
        review_like = Emote.objects.filter(review=review.pk, emotion=1)
        review_dislike = Emote.objects.filter(review=review.pk, emotion=0)
        liked_by_user = False
        for emote in review_like:
            if request.user == emote.user:
                liked_by_user = True
                break
        disliked_by_user = False
        for emote in review_dislike:
            if request.user == emote.user:
                disliked_by_user = True
                break
        review_info_lst.append((review, liked_by_user, disliked_by_user))
    
    # 평점 계산
    rating_dict = {0.0: 0, 0.5: 0, 1.0: 0, 1.5: 0, 2.0: 0, 2.5: 0, 3.0: 0, 3.5: 0, 4.0: 0, 4.5: 0, 5.0: 0}
    for review in reviews:
        rating_dict[review.rating] += 1
    ratings = list(rating_dict.values())
    
    sum_ratings = 0
    avg_rating = 0
    for key, value in rating_dict.items():
        sum_ratings += key * value
    if total_reviews:
        avg_rating = round((sum_ratings / total_reviews), 1)
    
    avg_rating_percent = avg_rating * 0.2 * 100

    # 출연/제작
    path = f'/movie/{movie_id}'
    params = {
        'api_key': api_key,
        'language': 'ko-KR',
    }
    movie = requests.get(base_url+path, params=params).json()
    movie_credits = requests.get(base_url+path+'/credits', params=params).json()
    
    # 메인 예고편
    movie_id = movie['id']
    path = f'/movie/{movie_id}/videos'
    params = {
        'api_key': api_key,
        'movie_id': movie_id,
    }
    videos = requests.get(base_url+path, params=params).json()['results']
    video_key = ''
    for video in videos:
        if video['type'] == 'Trailer':
            video_key = video['key']
            break

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
    for crew in crews:
        crews_tmp = []
        person_id = crew['id']
        path = f'/person/{person_id}'
        params = {
            'api_key': api_key,
            'language': 'ko-KR',
        }
        person = requests.get(base_url+path, params=params).json()
        name = check_korean_name(person, crews_tmp)
        crew['kor_name'] = name

    # 출연진
    casts = movie_credits['cast']
    if len(casts) > 12 - len(crews):
        casts = casts[:12-len(crews)]
    
    for cast in casts:
        casts_tmp = []
        person_id = cast['id']
        path = f'/person/{person_id}'
        params = {
            'api_key': api_key,
            'language': 'ko-KR',
        }
        person = requests.get(base_url+path, params=params).json()
        name = check_korean_name(person, casts_tmp)
        cast['kor_name'] = name
    
    collection_create_form = CollectionForm
    
    context = {
        'avg_rating_percent': avg_rating_percent,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'ratings': ratings,
        'video_key': video_key,
        'year': year,
        'country': country,
        'movie': movie,
        'genres': genres,
        'crews': crews,
        'casts': casts,
        'review_form': review_form,
        'reviews': reviews,
        'review_info_lst': review_info_lst,
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
    name = check_korean_name(person, lst)
    context = {
        'name': name,
        'person': person,
        'category': category.items(),
        'job': '/'.join(job),
    }
    return render(request, 'movies/person_detail.html', context)


def get_name_in_korean(names, lst):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    for name in names:
        result = hangul.sub('', name)
        if result.strip():
            lst.append(result)


def check_korean_name(person, lst):
    name = ''
    names = person['also_known_as']
    if names:
        get_name_in_korean(names, lst)
        if lst:
            name = lst[0]
    else:
        name = person['name']
    return name


def search(request):
    string = request.GET.get('search')
    path = f'/search'
    params = {
        'api_key': api_key,
        'query': string,
        'language': 'ko-KR',
        'region': 'kr',
        'include_adult': 'false'
    }

    # 영화 1페이지
    page            = request.GET.get('page', 1)
    params['page']  = page
    movies_response = requests.get(base_url+path+'/movie', params=params).json()
    movies_pages    = movies_response['total_pages']
    people_response = requests.get(base_url+path+'/person', params=params).json()
    people_pages    = people_response['total_pages']
    total_pages     = max(movies_pages, people_pages)
    total_results   = movies_response['total_results'] + people_response['total_results']

    # 페이지네이터 객체 생성
    paginator = Paginator(range(1, total_pages+1), 1)
    # ex) 1 of 109 page
    pages = paginator.page(page)


    result = movies_response['results'] + people_response['results']
    
    context = {
        'key_word'     : string,
        'results'      : result,
        'total_results': total_results,
        'pages'        : pages,
    }
    return render(request, 'movies/search.html', context)


def api_convert(request):
    return JsonResponse({'api_key': api_key})


@login_required
def create(request, username):
    # 자신의 계정으로만 컬렉션 생성 가능하도록
    if request.user != get_user_model().objects.get(username=username):
        return redirect('accounts:profile', username)
    
    if request.method == 'POST':
        collection_form = CollectionForm(request.POST)
        # js에서 만든 selected_list를 받아옴
        selected_movies_json = request.POST.get('selected_list')
        selected_movies = json.loads(selected_movies_json)

        if collection_form.is_valid():
            collection = collection_form.save(commit=False)
            collection.user = request.user
            collection.save()
            for movie in selected_movies:
                MovieCollection.objects.create(collection=collection, movie_id=movie['id'], movie_poster=movie['poster_path'])

            return redirect('movies:collection_detail', username, collection.pk)
    else:
        collection_form = CollectionForm()
    context = {
        'api_key': api_key,
        'collection_form': collection_form,
    }
    return render(request, 'movies/create.html', context)


def collection_detail(request, username, collection_pk):
    person = get_user_model().objects.get(username=username)
    collection = Collection.objects.get(pk=collection_pk)
    like_users_count = collection.like_users.count()
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
        'person'          : person,
        'collection'      : collection,
        'movies'          : collection_movies,
        'like_users_count': like_users_count,
    }
    return render(request, 'movies/collection_detail.html', context)


@login_required
def update(request, username, collection_pk):
    if request.user != get_user_model().objects.get(username=username):
        return redirect('accounts:profile', username)
    
    collection = Collection.objects.get(pk=collection_pk)
    if request.method == 'POST':
        collection_form = CollectionForm(request.POST, instance=collection)
        movie_delete_form = CollectionMovieDeleteForm(request.POST)

        if collection_form.is_valid() and movie_delete_form.is_valid():
            collection_form.save()
            movie_delete_form.save()
            # js에서 만든 selected_list, deleted_list를 받아옴
            selected_movies_json = request.POST.get('selected_list')
            if selected_movies_json:
                selected_movies = json.loads(selected_movies_json)
                for movie in selected_movies:
                    MovieCollection.objects.create(collection=collection, movie_id=movie['id'], movie_poster=movie['poster_path'])
            return redirect('movies:collection_detail', username, collection.pk)
    else:
        collection_form = CollectionForm(instance=collection)
        movie_delete_form = CollectionMovieDeleteForm(instance=collection)
    context = {
        'collection': collection,
        'collection_form': collection_form,
        'movie_delete_form': movie_delete_form,
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


def get_average_rating(movies):
    for movie in movies:
        movie_id = movie['id']
        # 리뷰
        reviews = Review.objects.filter(movie=movie_id).order_by('-pk')
        if len(reviews) == 0:
            movie['avg_rating'] = ''
        else:
            # 평점 계산
            movies_rating_dict = {0.0: 0, 0.5: 0, 1.0: 0, 1.5: 0, 2.0: 0, 2.5: 0, 3.0: 0, 3.5: 0, 4.0: 0, 4.5: 0, 5.0: 0}
            for review in reviews:
                movies_rating_dict[review.rating] = movies_rating_dict.get(0, 1) + 1
            
            sum_ratings = 0
            avg_rating = 0
            rating_people = sum(movies_rating_dict.values())
            for key, value in movies_rating_dict.items():
                sum_ratings += key * value
            if rating_people:
                avg_rating = round((sum_ratings / rating_people), 1)
            movie['avg_rating'] = avg_rating


def genre_movies(request, genre_name):
    # 장르별 딕셔너리
    genre_dict = {
        '액션'         : '28',
        '어드벤처'     : '12',
        '애니메이션'   : '16',
        '코미디'       : '35',
        '범죄'         : '80',
        '다큐멘터리'   : '99',
        '드라마'       : '18',
        '가족'         : '10751',
        '판타지'       : '14',
        '역사'         : '36',
        '공포'         : '27',
        '음악'         : '10402',
        '미스터리'     : '9648',
        '로맨스'       : '10749',
        'SF'           : '878',
        'TV'           : '10770',
        '스릴러'       : '53',
        '전쟁'         : '10752',
        '서부'         : '37'
    }
    
    # 페이지 정보를 받아올 URL
    params = {
        'api_key'    : api_key,
        'language'   : 'ko-KR',
        'region'     : 'kr',
        'with_genres': genre_dict[genre_name]
    }
    path = '/discover/movie'

    # JSON 응답에서 총 페이지 수를 추출
    response = requests.get(base_url + path, params=params).json()
    
    # 파라미터 가져오기
    page    = request.GET.get('page', 1)
    # 기본: 인기순
    sort_by = request.GET.get('sort_by', 'popularity.desc')

    movies            = []
    params['page']    = page
    params['sort_by'] = sort_by
    response          = requests.get(base_url + path, params=params).json()
    total_pages       = response['total_pages']
    total_results     = response['total_results']
    
    # 페이지네이터 객체 생성
    paginator = Paginator(range(1, total_pages+1), 1)
    # ex) 1 of 109 page
    pages = paginator.page(page)

    movies += response['results']
    
    context = {
        'genre_name'   : genre_name,
        'movies'       : movies,
        'pages'        : pages,
        'total_results': total_results,
    }

    return render(request, 'movies/genre_movies.html', context)


@login_required
def like_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    
    if request.user in collection.like_users.all():
        collection.like_users.remove(request.user)
        liked = False
    else:
        collection.like_users.add(request.user)
        liked = True
        
    return JsonResponse({'is_liked': liked, 'like_users_count': collection.like_users.count()})