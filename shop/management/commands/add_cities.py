import json

from django.core.management import BaseCommand

from users.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('./cities.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for row in data:
            p_title = row['province']
            print(p_title)
            province = Province.objects.create(title=p_title)
            for city in row['cities']:
                print(city)
                City.objects.create(province=province, title=city)
