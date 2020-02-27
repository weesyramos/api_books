from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet

from .models import BookModel, AuthorModel
from .serializers import BookSerializer, AuthorSerializer

class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer    

    def get_queryset(self):
        queryset = BookModel.objects.all()
        name = self.request.query_params.get('name', None)
        edition = self.request.query_params.get('edition', None)
        publication_year = self.request.query_params.get('publication_year', None)
        authors = self.request.query_params.get('authors', None)

        if name:
            queryset = queryset.filter(name=name)

        if edition:
            queryset = queryset.filter(edition=edition)

        if publication_year:
            queryset = queryset.filter(publication_year=publication_year)

        if authors:
            queryset = queryset.filter(authors=authors)

        return queryset


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = AuthorModel.objects.all()
        paginator = Paginator(queryset, 2)
        page_number = self.request.query_params.get('page')
        return paginator.get_page(page_number)
