import uuid

from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework import serializers
from PIL import Image, UnidentifiedImageError

from shop.models import *


__all__ = [
    'ImageReadSerializer',
    'ImageUploadSerializerAdmin',
]


class ImageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'url', 'is_main', 'description']

    def get_absolute_url(self, obj):
        if not obj.file:
            return None
        url = obj.file.url
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(url)
        if (host := self.context.get('host')) is not None:
            return f'{host}{url}'
        return url


class ImageUploadSerializerAdmin(serializers.Serializer):
    image = serializers.ImageField()

    def validate(self, attrs):
        image = attrs.get('image')
        valid_extension = self.context.get('valid_extensions', ['jpg', 'jpeg', 'png'])

        if not image:
            raise serializers.ValidationError('no file')

        parts = image.name.split('.')
        if len(parts) == 0:
            raise serializers.ValidationError('no file extension')

        extension = parts[-1]
        if extension.lower() not in valid_extension:
            raise serializers.ValidationError('unacceptable file format for image')
        attrs['extension'] = extension

        return attrs

    def save(self, **kwargs):
        save_path = self.context.get('save_path')
        assert bool(save_path), 'save path not specified'

        image = self.validated_data.get('image')
        extension = self.validated_data.get('extension')
        new_name = f'{uuid.uuid4().hex}.{extension}'
        path = f'{save_path}{new_name}'

        from PIL import ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        try:
            img = Image.open(image)
            if img.mode in ['RGBA', 'P']:
                img = img.convert('RGB')
            img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
            img.save(f'{settings.MEDIA_ROOT}/{path}', optimize=True, quality=50)

        except UnidentifiedImageError:
            return None

        # saved_file = default_storage.save(path, image)

        return {
            'file_address': path
        }
