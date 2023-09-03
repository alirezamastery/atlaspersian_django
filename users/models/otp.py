from django.db import models


__all__ = [
    'OTP',
]


class OTP(models.Model):
    code = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.mobile} - {self.code}'
