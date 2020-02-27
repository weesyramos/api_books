import csv
import os

from django.core.management.base import BaseCommand, CommandError

from core.models import AuthorModel


class Command(BaseCommand):
    """commando to import and create new authors."""
    help = "importing and creating authors"

    def handle(self, *args, **options):
        try:
            with open(f'{os.path.dirname(os.path.abspath(__file__))}\\authors.csv', 'r', encoding='utf-16') as file:
                reader = csv.DictReader(file)
                for line in reader:
                    AuthorModel.create_author(name=line['name'])
            
        except Exception as e:
            print(f'error when executing command: {e}')