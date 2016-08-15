from .settings import *
import os.path
import dj_database_url


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ap1shop_test',
        'USER': 'ap1shop_test',
        'PASSWORD': 'Ap1forthewin!',
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'default-character-set': 'utf8',`
    }
}


EMAIL_URL = os.environ.get('EMAIL_URL', 'console://')
email_config = dj_email_url.parse(EMAIL_URL)
