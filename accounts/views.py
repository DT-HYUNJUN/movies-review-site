from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views import View #클래스형 뷰


class Signup(View):
    # 로그인 여부
    def is_authenticated(self, request):
        if request.user.is_authenticated:
            return True
        return False
    
    def get(self, request):
        if self.is_authenticated(request):
            
            pass
            # return redirect('메인페이지') <-- 나중에 바꾸기
        
        form = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'form': form})
    
    def post(self, request):
        if self.is_authenticated(request):

            pass
            # return redirect('메인페이지') <-- 나중에 바꾸기

        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            pass
            # return redirect('메인페이지') <-- 나중에 바꾸기


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            return None
            # return redirect('메인페이지') <-- 나중에 바꾸기
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return None
    # return render(request, 'accounts/login.html', context) <-- 나중에 바꾸기


@login_required
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return None
    # return render(request, 'accounts/login.html', context) <-- 나중에 바꾸기
