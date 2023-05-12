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

    # ---------------collection---------------------
    # path('create/', views.create, name='create'),
    # path('update/<int:collection_pk>/', views.update, name='update'),
]
