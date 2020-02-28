import copy

from rest_framework.test import APIClient
from django.test import TestCase

from .utils import validate_name, validate_year
from .models import AuthorModel, BookModel


class TestValidateEndPintsAuthor(TestCase):
    url = 'http://127.0.0.1:8000/authors/'
    json = {
        "name": "J. K. Rowling"
    }

    def test_empty_name(self):
        json = copy.deepcopy(self.json)
        json.pop('name')
        api_client = APIClient()
        res = api_client.post(self.url, json)
        self.assertEqual(res.data['error'], 'empty name')

    def test_name_with_spaces(self):
        json = copy.deepcopy(self.json)
        json['name'] = '      J. K. Rowling        '
        api_client = APIClient()
        res = api_client.post(self.url, json)
        self.assertEqual(res.data['name'], 'J. K. Rowling')

    def test_invalid_character(self):
        json = copy.deepcopy(self.json)
        json['name'] = 'J. K. Rowling @'
        api_client = APIClient()
        res = api_client.post(self.url, json)
        self.assertEqual(res.data['error'], 'invalid name')

    def test_name_with_number(self):
        json = copy.deepcopy(self.json)
        json['name'] = 'J. K. Rowling 123'
        api_client = APIClient()
        res = api_client.post(self.url, json)
        self.assertEqual(res.data['error'], 'invalid name')