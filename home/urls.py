from django.urls import path, include
from home.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('<slug:slug>/', blog_detail, name='blog_detail'),
    path("category/<str:slug>/", category, name="category"),
    path('<slug:slug>/add_comment/', add_comment, name='add_comment'),
    path('/blog', blog, name='blog'),
    path('/about', about, name='about'),
    path('/contact', contact, name='contact'),
    path('/search', search, name='search'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)