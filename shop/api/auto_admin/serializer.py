from django.db.models import Model as DjangoModel
from rest_framework.serializers import ModelSerializer


def serializer_factory(
        model_: type(DjangoModel),
        *,
        depth_: int = 1,
        fields_: list[str] | None = None
):
    class ClsSerializer(ModelSerializer):
        class Meta:
            model = model_
            depth = depth_
            fields = '__all__' if fields_ is None else fields_

    return ClsSerializer
