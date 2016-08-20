import logging

from django.conf import settings
from django.utils.translation import get_language
from django.utils import translation

from . import analytics, get_country_by_ip, get_currency_for_country
from ..discount.models import Sale

logger = logging.getLogger(__name__)


class GoogleAnalytics(object):
    def process_request(self, request):
        client_id = analytics.get_client_id(request)
        path = request.path
        language = get_language()
        headers = request.META
        # FIXME: on production you might want to run this in background
        try:
            analytics.report_view(client_id, path=path, language=language,
                                  headers=headers)
        except Exception:
            logger.exception('Unable to update analytics')


class DiscountMiddleware(object):
    def process_request(self, request):
        discounts = Sale.objects.all()
        discounts = discounts.prefetch_related('products', 'categories')
        request.discounts = discounts


class CountryMiddleware(object):

    def process_request(self, request):
        if 'REMOTE_ADDR' in request.META:
            request.country = get_country_by_ip(request.META['REMOTE_ADDR'])
        else:
            request.country = None


class CurrencyMiddleware(object):

    def process_request(self, request):
        if hasattr(request, 'country') and request.country is not None:
            request.currency = get_currency_for_country(request.country)
        else:
            request.currency = settings.DEFAULT_CURRENCY


class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']
