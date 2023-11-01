from django.db.models import Model as DjangoModel
from rest_framework.viewsets import ModelViewSet

from .serializer import serializer_factory


def viewset_factory(model_: type(DjangoModel), *, mixins: list[type] | None = None):
    mixin_list = mixins if mixins is not None else []

    class ViewSet(ModelViewSet, *mixin_list):
        queryset = model_.objects.all()
        serializer_class = serializer_factory(model_)

    return ViewSet

