from django.db import models
from django.core.validators import MaxValueValidator


__all__ = [
    'Comment',
    'Question',
]


class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='comments')
    accepted = models.BooleanField(default=False)

    text = models.TextField(default='')

    quality_score = models.PositiveSmallIntegerField(default=5, validators=[MaxValueValidator(5)])
    worth_buy_score = models.PositiveSmallIntegerField(default=5, validators=[MaxValueValidator(5)])

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='questions')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    answer = models.TextField(default='', blank=True)
    accepted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
