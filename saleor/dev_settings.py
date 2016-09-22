from .settings import *
import os.path


# SQLITE_DB_URL = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'dev.sqlite')
# DATABASES = {'default': dj_database_url.config(default=SQLITE_DB_URL)}
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


EMAIL_URL = os.environ.get('EMAIL_URL', 'console://')
email_config = dj_email_url.parse(EMAIL_URL)
