from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from shop.models import *
from shop.api.public.serializers.question import QuestionWriteSerializerPublic
from utils.drf.permissions import IsAuthenticated


__all__ = [
    'QuestionViewSetPublic',
]


class QuestionViewSetPublic(mixins.CreateModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionWriteSerializerPublic
    permission_classes = [IsAuthenticated]
