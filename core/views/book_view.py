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
        name = request.data['name'] if 'name' in request.data else None
        edition = request.data['edition'] if 'edition' in request.data else None
        publication_year = request.data['publication_year'] if 'publication_year' in request.data else None
        authors = request.data['authors'] if 'authors' in request.data else None

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
            return Response({'error': 'invalid publication_year'}, status=422)

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

    def update(self, request, pk=None):
        name = request.data['name'] if 'name' in request.data else None
        edition = request.data['edition'] if 'edition' in request.data else None
        publication_year = request.data['publication_year'] if 'publication_year' in request.data else None
        authors = request.data['authors'] if 'authors' in request.data else None
        if name and edition and publication_year and authors:

            try:
                book = BookModel.objects.get(pk=pk)
            except:
                return Response({'error': 'book not found'}, status=404)
            
            verify_authors = AuthorModel.objects.filter(pk__in=authors)
            if not len(verify_authors) == len(authors):
                return Response({'error': 'one or more authors not found'}, status=404)

            if not validate_year(publication_year):
                return Response({'error' : 'invalid publication_year'}, status=422)

            book.name = name
            book.edition = edition
            book.publication_year = publication_year
            book.name = name
            book.save()

            book.authors.set(authors)
            book.save()
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response({'error': 'incomplete information'}, status=422)

    def partial_update(self, request, pk=None):
        name = request.data['name'] if 'name' in request.data else None
        edition = request.data['edition'] if 'edition' in request.data else None
        publication_year = request.data['publication_year'] if 'publication_year' in request.data else None
        authors = request.data['authors'] if 'authors' in request.data else None

        try:
            book = BookModel.objects.get(pk=pk)
        except:
            return Response({'error': 'book not found'}, status=404)

        if authors or authors == '':
            if authors != '' and len(authors) != 0: 
                verify_authors = AuthorModel.objects.filter(pk__in=authors)
                if not len(verify_authors) == len(authors):
                    return Response({'error': 'one or more authors not found'}, status=404)
                book.authors.set(authors)
            else:
                return Response({'error' : 'invalid authors'}, status=422)
        
        if name or name == '': 
            if name != '':
                book.name = name
            else:
                return Response({'error' : 'invalid name'}, status=422)

        if edition or edition == '': 
            if edition != '':
                book.edition = edition
            else:
                return Response({'error' : 'invalid edition'}, status=422)

        if publication_year or publication_year == '': 
            if validate_year(publication_year):
                book.publication_year = publication_year
            else:
                return Response({'error' : 'invalid publication_year'}, status=422)
        book.save()

        serializer = BookSerializer(book)
        return Response(serializer.data)