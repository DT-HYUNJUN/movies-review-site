from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('update/', views.ProfileUpdate.as_view(), name='update'),
    path('password/', views.ChangePassword.as_view(), name='change_password'),
    path('delete/', views.delete, name='delete'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]
