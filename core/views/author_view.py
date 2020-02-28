from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from ..utils import validate_name
from ..models import AuthorModel
from ..serializers import AuthorSerializer


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = AuthorModel.objects.all()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name=name)
            return queryset

        paginator = Paginator(queryset, 10)
        page_number = self.request.query_params.get('page')
        return paginator.get_page(page_number)

    def create(self, request, *args, **kwargs):
        name = request.data['name'] if 'name' in request.data else None
        if not name:
            return Response({'error': 'empty name'}, status=204)

        name = validate_name(name)
        if name:
            author = AuthorModel.objects.create(name=name)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        return Response({'error': 'invalid name'}, status=422)

    def update(self, request, pk=None):
        name = request.data['name']
        name = validate_name(name)
        if name:
            try:
                author = AuthorModel.objects.get(pk=pk)
                author.name = name
                author.save()
                serializer = AuthorSerializer(author)
                return Response(serializer.data)
            except:
                return Response({'error': 'author not found'}, status=404)
        return Response({'error': 'invalid name'}, status=422)


    def partial_update(self, request, pk=None):
        name = request.data['name']
        name = validate_name(name)
        if name:
            try:
                author = AuthorModel.objects.get(pk=pk)
                author.name = name
                author.save()
                serializer = AuthorSerializer(author)
                return Response(serializer.data)
            except:
                return Response({'error': 'author not found'}, status=404)
        return Response({'error': 'invalid name'}, status=422)
