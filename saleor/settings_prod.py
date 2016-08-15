from .settings import *
import os.path
import dj_database_url


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
