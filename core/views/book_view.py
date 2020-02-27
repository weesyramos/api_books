from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from ..utils import validate_year
from ..models import BookModel, AuthorModel
from ..serializers import BookSerializer


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

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        edition = request.data['edition']
        publication_year = request.data['publication_year']
        authors = request.data['authors']

        if not name:
            return Response({'error': 'empty name'}, status=204)

        if not edition:
            return Response({'error': 'empty edition'}, status=204)

        if not publication_year:
            return Response({'error': 'empty publication_year'}, status=204)

        if not authors:
            return Response({'error': 'empty authors'}, status=204)

        publication_year = validate_year(publication_year)
        if not publication_year:
            return Response({'error': 'publication_year invalid'}, status=422)

        try:
            AuthorModel.objects.filter(pk__in=authors)
        except:
            return Response({'error': 'one or more authors not found'}, status=404)

        book = BookModel()
        book.name = name
        book.edition = edition
        book.publication_year = publication_year
        book.save()

        authors = ','.join(str(i) for i in authors)
        book.authors.add(authors)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    # def update(self, request, pk=None):
    #     name = request.data['name']
    #     name = validate_name(name)
    #     if name:
    #         try:
    #             author = AuthorModel.objects.get(pk=pk)
    #             author.name = name
    #             author.save()
    #             serializer = AuthorSerializer(author)
    #             return Response(serializer.data)
    #         except:
    #             return Response({'error': 'author not found'}, status=404)
    #     return Response({'error': 'name invalid'}, status=422)


    # def partial_update(self, request, pk=None):
    #     name = request.data['name']
    #     name = validate_name(name)
    #     if name:
    #         try:
    #             author = AuthorModel.objects.get(pk=pk)
    #             author.name = name
    #             author.save()
    #             serializer = AuthorSerializer(author)
    #             return Response(serializer.data)
    #         except:
    #             return Response({'error': 'author not found'}, status=404)
    #     return Response({'error': 'name invalid'}, status=422)