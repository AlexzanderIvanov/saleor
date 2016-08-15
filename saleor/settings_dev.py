from .settings import *
import os.path
import dj_database_url


SQLITE_DB_URL = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'dev.sqlite')
DATABASES = {'default': dj_database_url.config(default=SQLITE_DB_URL)}


EMAIL_URL = os.environ.get('EMAIL_URL', 'console://')
email_config = dj_email_url.parse(EMAIL_URL)
