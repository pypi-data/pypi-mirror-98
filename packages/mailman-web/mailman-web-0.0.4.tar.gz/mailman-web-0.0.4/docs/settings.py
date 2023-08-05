# Mailman Web configuration file.
# /etc/mailman3/settings.py

from mailman_web.settings.base import *
from mailman_web.settings.mailman import *


#: Default list of admins who receive the emails from error logging.
ADMINS = (
    ('Mailman Suite Admin', 'root@localhost'),
)

# Postgresql datbase setup.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ‘mailmanweb’,
        'USER': '<db_username>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 'collectstatic' command will copy all the static files here.
# Alias this location from your webserver to `/static`
STATIC_ROOT = '/opt/mailman/web/static'


# Make sure that this directory is created or Django will fail on start.
LOGGING['handlers']['file']['filename'] = '/opt/mailman/web/logs/mailmanweb.log'

#: See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "localhost",  # Archiving API from Mailman, keep it.
    # "lists.your-domain.org",
    # Add here all production domains you have.
]

#: Current Django Site being served. This is used to customize the web host
#: being used to serve the current website. For more details about Django
#: site, see: https://docs.djangoproject.com/en/dev/ref/contrib/sites/
SITE_ID = 1


SECRET_KEY = 'MyVerrySecretKey'
