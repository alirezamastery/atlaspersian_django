from django.db import models


__all__ = [
    'UserOTP',
    'MobileOTP',
]


class UserOTP(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id} - {self.code}'


class MobileOTP(models.Model):
    mobile = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.mobile} - {self.code}'
