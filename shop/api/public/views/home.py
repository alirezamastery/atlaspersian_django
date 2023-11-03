from django.db.models import *
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import *
from shop.api.public.serializers import *
from shop.api.public.queries import *
from utils.drf.permissions import ReadOnly


__all__ = [
    'HomePageDataView',
]


class HomePageDataView(APIView):
    permission_classes = [ReadOnly]

    def get(self, request):
        prefetch_variants = get_prefetch_variants()
        total_inv_subq = get_total_inventory_subq()
        price_min_subq = get_price_min_subq(filters={'inventory__gt': 0})

        discounted = (Product.objects
                      .select_related('brand')
                      .select_related('category')
                      .prefetch_related(prefetch_variants)
                      .filter(is_active=True)
                      .annotate(max_discount=Max('variants__discount_percent', filter=Q(variants__inventory__gt=0)))
                      .annotate(total_inventory=Coalesce(Subquery(total_inv_subq), Value(0)))
                      .annotate(price_min=Coalesce(Subquery(price_min_subq), Value(0)))
                      .filter(total_inventory__gt=0)
                      .order_by('-max_discount', '-created_at')[:15])

        highest_sale = (Product.objects
                        .select_related('brand')
                        .select_related('category')
                        .prefetch_related(prefetch_variants)
                        .filter(is_active=True)
                        .annotate(sale_sum=Sum('variants__sale_count'))
                        .annotate(max_discount=Max('variants__discount_percent', filter=Q(variants__inventory__gt=0)))
                        .annotate(total_inventory=Coalesce(Subquery(total_inv_subq), Value(0)))
                        .annotate(price_min=Coalesce(Subquery(price_min_subq), Value(0)))
                        .filter(total_inventory__gt=0)
                        .order_by('-sale_sum', '-created_at')[:15])

        home_slides = HomeSlide.objects.all().order_by('-created_at')

        serializer_context = {'request': request}
        response = {
            'discounted':   ProductListSerializerPublic(discounted, many=True, context=serializer_context).data,
            'highest_sale': ProductListSerializerPublic(highest_sale, many=True, context=serializer_context).data,
            'home_slides':  HomeSlideReadSerializerPublic(home_slides, many=True, context=serializer_context).data,
        }

        return Response(response)
