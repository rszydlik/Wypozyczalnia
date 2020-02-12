import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'iq_q7_e*%e7$jwlqvvqw2a34f12u^-u6fukwq(6m-=kcb7a5l8'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wypozyczalnia',
        'USER': 'postgres',
        'PASSWORD': 'darkomen2',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Messing with static path because of multiple os
if os.name == 'nt':
    STATIC_ROOT = ''
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join('static'),)
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Gdzie przekierowuje gdy trzeba byc zalogowanym
LOGIN_URL = 'login'
