from . import base

for var in dir(base):
    value = getattr(base, var)
    globals()[var] = value

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DEBUG = False

ALLOWED_HOSTS = ['0.0.0.0']