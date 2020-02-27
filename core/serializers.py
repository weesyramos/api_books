from rest_framework import serializers
from rest_framework.response import Response

from .utils import validate_name
from .models import BookModel, AuthorModel


class BookSerializer(serializers.ModelSerializer):    
    class Meta:
        model = BookModel
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorModel
        fields = '__all__'        