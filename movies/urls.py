from django.contrib import admin
from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('search/', views.search, name='search'),
    path('like/<int:movie_id>/', views.like, name='like'),
    path('collection/create/<str:username>/', views.create, name='create'),
    path('collection/<str:username>/<int:collection_pk>/', views.collection_detail, name='collection_detail'),
    path('collection/update/<str:username>/<int:collection_pk>/', views.update, name='update'),
    path('collection/delete/<str:username>/<int:collection_pk>/', views.delete, name='delete'),
    path('collections/<int:collection_pk>/like/', views.like_collection, name='like_collection'),
    path('collections/add/<int:collection_pk>/<int:movie_id>/', views.add_collection_movie, name='add_collection_movie'),
    path('api/key/', views.api_convert, name='api_convert'),
    # 장르별 영화조회
    path('genre/<str:genre_name>/', views.genre_movies, name='genre_movies'),
]
