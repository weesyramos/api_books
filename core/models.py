from django.db import models


class AuthorModel(models.Model):
    name = models.CharField(max_length=255) 

    def __str__(self):
        return self.name

    @staticmethod
    def create_author(name):
        """Create a new Author."""
        try:
            AuthorModel.objects.create(name=name)
            print(f'Create a new Author: {name}')
        except Exception as e:
            print(f'error when trying to create author: {e}')


class BookModel(models.Model):
    name = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    publication_year = models.CharField(max_length=4)
    authors = models.ManyToManyField(AuthorModel)

    def __str__(self):
        return self.name

