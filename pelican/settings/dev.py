from . import base

for var in dir(base):
    value = getattr(base, var)
    globals()[var] = value

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3', # This is where you put the name of the db file. 
                 # If one doesn't exist, it will be created at migration time.
    }
}