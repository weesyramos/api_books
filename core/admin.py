from django.contrib import admin
from .models import AuthorModel, BookModel

admin.site.register(AuthorModel)
admin.site.register(BookModel)

