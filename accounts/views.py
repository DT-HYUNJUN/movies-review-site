import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View 
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import requests
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from reviews.models import Review
from movies.models import Collection, MovieLike
from reviews.models import Emote, Review
from movies.models import Collection

load_dotenv()
base_url = 'https://api.themoviedb.org/3'
api_key = os.getenv('TMDB_API_KEY')


class Signup(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('movies:index')

        # 양식에 어긋났을때
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})


class Login(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        context = {
        'form': form,
        }
        return render(request, 'accounts/login.html', context) # <-- 나중에 바꾸기
    
    def post(self, request):
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
        context = {
        'form': form,
        }
        return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')


# 유저 정보 외에 다른 영화나 리뷰 정보들은 추후에 작업
# 지금은 유저만 넘김
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    collections = Collection.objects.filter(user=person).prefetch_related('moviecollection_set').order_by('-pk')
    reviews = Review.objects.filter(user_id=person.id).order_by('-pk')
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
        
    like_movies = MovieLike.objects.filter(user=person).order_by('-pk')
    like_movies_info = []
    params = {
        'api_key': api_key,
        'language': 'ko-KR',
    }
    for movie in like_movies:
        path = f'/movie/{movie.movie_id}'
        movie = requests.get(base_url+path, params=params).json()
        like_movies_info.append(movie)
    
    context = {
        'reviews': reviews,
        'person': person,
        'collections': collections,
        'like_movies': like_movies_info,
        'review_info_lst': review_info_lst,
    }
    return render(request, 'accounts/profile.html', context)


class ProfileUpdate(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'accounts/update.html', {'form': form})

    def post(self, request):
        print('post pass')
        form = CustomUserChangeForm(request.POST, instance=request.user, files=request.FILES)

        if form.is_valid():
            print('form valid pass')
            form.save()
            return redirect('accounts:profile', request.user)
        
        context = {
        'form': form,
        }
        return render(request, 'accounts/update.html', {'form': form})


class ChangePassword(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = CustomPasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})
    
    def post(self, request):
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 로그인 유지
            update_session_auth_hash(request, user)
            return redirect('movies:profile')


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user
    if you != me:
        if you.followers.filter(pk=request.user.pk).exists():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', you.user_pk)