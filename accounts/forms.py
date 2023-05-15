from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
# allauth
from allauth.socialaccount.forms import SignupForm

#회원가입
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '아이디'
            }
        ),
    )
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '닉네임'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '이메일'
            }
        ),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '비밀번호'
            }
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control account-field',
                'placeholder': '비밀번호 확인'
            }
        ),
    )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'nickname', 'password1', 'password2',)

#회원정보 수정
class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일',
            }
        ),
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름',
            }
        ),
        required=False,
    )
    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '닉네임',
            }
        ),
        required=False,
    )
    profile_image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        ),
        required=False
    )
    birthday = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
            }
        ),
        required=False
    )
    color = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'id': 'color-picker',
            }
        ),
        required=False,    
    )
# 기본 프로필 색상 설정 & 변경시 출력
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['color'].widget.attrs['value'] = instance.color or '#ffbfd3;'
        else:
            self.fields['color'].widget.attrs['value'] = '#ffbfd3;'


    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'last_name', 'birthday', 'profile_image', 'nickname', 'color')

# 비밀번호 수정
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '기존 비밀번호',
            }
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '새 비밀번호',
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호 확인',
            }
        )
    )
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields['old_password'].widget.attrs['placeholder'] = '현재 비밀번호를 입력해 주세요'
    #     self.fields['new_password1'].widget.attrs['placeholder'] = '새 비밀번호를 입력해 주세요'
    #     self.fields['new_password2'].widget.attrs['placeholder'] = '새 비밀번호를 다시 입력해 주세요'

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


class CustomSocialSignupForm(SignupForm):
    email = forms.EmailField(label='구글 이메일', widget=forms.EmailInput(attrs={
                'class': 'form-control account-field',
                'placeholder': '이메일'
            }), required=False)
    nickname = forms.CharField(required=True, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '닉네임',
            }
        ),  max_length=10, label='닉네임')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nickname'].widget.attrs.update({'autofocus': True})
        # username 숨기고 / 구글에서 받아오는 정보중 sub값 넣음 (의미없는)
        self.fields['username'].widget = forms.HiddenInput()
        self.initial['username'] = self.sociallogin.account.extra_data.get('sub')

    def save(self, request):
        user = super().save(request)
        # 구글 username으로 저장
        user.nickname = self.cleaned_data.get('nickname')
        user.save()
        return user