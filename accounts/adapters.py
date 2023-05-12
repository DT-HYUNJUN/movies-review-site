from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=None)
        user.email = sociallogin.account.extra_data['email']
        user.save()
        return user

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
