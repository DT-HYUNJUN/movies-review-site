from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('movies/', include('movies.urls')),
    path('reviews/', include('reviews.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

