"""
Django settings for rfk project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import configparser
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Access configparser to load variable values
config = configparser.SafeConfigParser(
    allow_no_value=True,
    interpolation=None
)
config.read(BASE_DIR / 'rfk' / 'settings.ini')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    'rfk.ee', 'www.rfk.ee', '18.217.179.154',
    'test.valgalinn.ee', '63.33.55.93'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders', # https://github.com/adamchainz/django-cors-headers
    'ajax_select',  # ajax selectväljad https://github.com/crucialfelix/django-ajax-selects
    'main', # RFK sandbox
    'montonio', # montonio sandbox
    'sihtnumber', # postiindeksid
    'rest_framework', # Django REST framework
    'django_filters', # Django filters
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # https://github.com/adamchainz/django-cors-headers
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rfk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.get_cookie_consent_inuse',
            ],
        },
    },
]

WSGI_APPLICATION = 'rfk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static/'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://github.com/adamchainz/django-cors-headers
CORS_ALLOW_ALL_ORIGINS = True

# cookie consent in use?
COOKIE_CONSENT_INUSE = False

# montonio keys
MONTONIO_LIVE = False
if MONTONIO_LIVE:
    MONTONIO_API_SERVER = config['montonio-live']['MONTONIO_API_SERVER']
    MY_ACCESS_KEY = config['montonio-live']['MY_ACCESS_KEY']
    MY_SECRET_KEY = config['montonio-live']['MY_SECRET_KEY']
else:
    MONTONIO_API_SERVER = config['montonio-sandbox']['MONTONIO_API_SERVER']
    MY_ACCESS_KEY = config['montonio-sandbox']['MY_ACCESS_KEY']
    MY_SECRET_KEY = config['montonio-sandbox']['MY_SECRET_KEY']

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}