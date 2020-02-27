from django.test import TestCase
from .utils import validate_name, validate_year
from .models import AuthorModel, BookModel


class TestValidateFields(TestCase):
    """Validation Model Fields."""
    def test_name_with_spaces(self):
        name = '  Weslley  '
        self.assertEqual(validate_name(name), 'Weslley')

    def test_invalid_character(self):
        name = 'weslley@'
        self.assertEqual(validate_name(name), None)

    def test_name_with_number(self):
        name = 'weslley14'
        self.assertEqual(validate_name(name), None)

    def test_year_less_than_or_equal_to_4(self):
        publication_year = '20020'
        self.assertEqual(validate_year(publication_year), None)

    def test_different_year_of_numbers(self):
        publication_year = 'abcd'
        self.assertEqual(validate_year(publication_year), None)

