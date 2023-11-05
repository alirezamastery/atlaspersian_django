import os
from pathlib import Path
from pprint import pprint

from django.core.management import BaseCommand
from django.conf import settings
from django.db.models import *
from django.db.models import Model as DjangoModel
from django.db.models.functions import *
from rest_framework import serializers

from shop.models import *
from shop.api.admin.serializers import *
from utils.slug import unique_slugify
from PIL import Image, UnidentifiedImageError
from shop.api.public.queries import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        # path = './test.jpg'
        # img = Image.open(path)
        # p = Path(path)
        # new_path = path.replace(p.suffix, '.webp')
        # img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        # img.save(new_path, 'webp', optimize=True)
        products = Product.objects.all()
        for product in products:
            path = product.thumbnail.path
            print(f'{path = }')
            pa = Path(path)
            print(pa.suffix)
            if pa.suffix != '.jpg':
                continue
            img = Image.open(path)
            new_path = str(path).replace(pa.suffix, '.webp')
            print(new_path)
            img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            img.save(new_path, 'webp', optimize=True, quality=50)
            new_path = new_path.replace('/home/atlasdjango/media/', '')
            print(new_path)
            product.thumbnail = new_path
            product.save()

            # images = p.images.all()
            # for image in images:
            #     path = os.path.join(settings.MEDIA_ROOT, image.file.path)
            #     print(path)
            #     p = Path(path)
            #     print(p.suffix)
            #     if p.suffix != '.webp':
            #         continue
            #     img = Image.open(path)
            #     new_path = path.replace(p.suffix, '.webp')
            #     img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
            #     img.save(new_path, 'webp', optimize=True, quality=50)
            #     new_path = new_path.replace('/home/atlasdjango/media/', '')
            #     print(new_path)
            #     image.file = new_path
            #     image.save()
