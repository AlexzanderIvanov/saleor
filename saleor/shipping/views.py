from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from saleor.shipping.models import ShippingOffice


# @login_required
def get_offices(request, city):
    offices = ShippingOffice.objects.filter(city__external_id=city)
    refs = list(map(to_reference, offices))
    return JsonResponse(refs, safe=False)


def to_reference(T):
    return {'name': T.name, 'address': T.address, 'id': T.external_id}
