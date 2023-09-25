from django.db import models


__all__ = [
    'Brand',
]


class Brand(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'
