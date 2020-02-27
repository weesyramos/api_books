from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.views.author_view import AuthorViewSet
from core.views.book_view import BookViewSet


router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
