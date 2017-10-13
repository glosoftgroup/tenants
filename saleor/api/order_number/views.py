from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from ...orders.models import Orders
import random
from rest_framework.decorators import api_view
from .serializers import (
    OrderNumberSerializer,
     )


class Comment(object):
    def __init__(self, number):
        self.number = number


@api_view(['GET', 'POST', ])
def new_order(request):
    number = int(Orders.objects.latest('id').id) + random.randrange(10) + request.user.id
    order_number = Comment(number='RET#'+str(number))
    serializer = OrderNumberSerializer(order_number)
    return Response(serializer.data)


