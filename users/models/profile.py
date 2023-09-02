from django.db import models
from PIL import Image


__all__ = [
    'Profile'
]


class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, primary_key=True)

    first_name = models.CharField(max_length=256, default='', blank=True)
    last_name = models.CharField(max_length=256, default='', blank=True)
    avatar = models.ImageField(upload_to='user/avatar/', null=True, blank=True)
    social_id = models.CharField(max_length=255, blank=True, default='')
    birth_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.first_name} - {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            w = 500
            h = 500
            if img.height > h or img.width > w:
                output_size = (w, h)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
