from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

#회원가입
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'profile_image',)

#회원정보 수정
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email','first_name','last_name', 'birthday', 'profile_image',)

# 비밀번호 수정
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs['placeholder'] = '현재 비밀번호를 입력해 주세요'
        self.fields['new_password1'].widget.attrs['placeholder'] = '새 비밀번호를 입력해 주세요'
        self.fields['new_password2'].widget.attrs['placeholder'] = '새 비밀번호를 다시 입력해 주세요'

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '아이디',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '비밀번호',
            }
        )
    )