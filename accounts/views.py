from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model


class Signup(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            pass
            # return redirect('메인페이지') <-- 나중에 바꾸기

        # 양식에 어긋났을때
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {
        'form': form,
        }
        return render(request, 'moives/index.html', context) # <-- 나중에 바꾸기
    
    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            return None
            # return redirect('메인페이지') <-- 나중에 바꾸기
        context = {
        'form': form,
        }
        return None
        # return render(request, 'accounts/login.html', context) <-- 나중에 바꾸기
    

@login_required
def logout(request):
    auth_logout(request)
    return None
    # return render(request, 'accounts/login.html', context) <-- 나중에 바꾸기



# 유저 정보 외에 다른 영화나 리뷰 정보들은 추후에 작업
# 지금은 유저만 넘김
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    
    context = {
        'person': person,    
    }
    return render(request, 'accounts/profile.html', {'person': person})


class ProfileUpdate(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'accounts/update.html', {'form': form})
    
    def post(self, request):
        form = CustomUserChangeForm(request.POST, instance=request.user, files=request.FILES)

        if form.is_valid():
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
            pass
            # return redirect('메인페이지') <-- 나중에 바꾸기


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    # return redirect('메인페이지') <-- 나중에 바꾸기

@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect('accounts:profile', username = you.username)