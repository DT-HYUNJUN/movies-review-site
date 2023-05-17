from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('create/', views.review_create, name='review_create'),
    path('<int:movie_id>/<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:review_pk>/emotes/<int:emotion>/', views.review_emote, name='review_emote'),
    path('<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:review_pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:review_pk>/comments/<int:comment_pk>/emotes/<int:emotion>/', views.comment_emote, name='comment_emote'),
]