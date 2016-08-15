import os.path

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ap1shop_saleor',
        'USER': 'ap1shop_saleor',
        'PASSWORD': 'Ap1forthewin!',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'default-character-set': 'utf8',
    }
}

EMAIL_URL = 'smtp://orders@ap1shop.com:ap1forthewin@mail.ap1shop.com:25'  # os.environ.get('EMAIL_URL', 'console://')
email_config = dj_email_url.parse(EMAIL_URL)

GOOGLE_ANALYTICS_TRACKING_ID = os.environ.get('GOOGLE_ANALYTICS_TRACKING_ID', 'UA-82439832-1')

DEFAULT_FROM_EMAIL = 'orders@ap1shop.com'  # os.environ.get('DEFAULT_FROM_EMAIL')
REPORT_EMAIL = 'orders@ap1shop.com'  # os.environ.get('DEFAULT_FROM_EMAIL')

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
