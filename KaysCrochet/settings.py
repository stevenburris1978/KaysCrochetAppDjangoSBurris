"""
Django settings for KaysCrochet project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
import logging
import sys

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

# Determine if the application is running on Heroku
ON_HEROKU = os.environ.get('ON_HEROKU', None)

DEBUG = True  # DEBUG is True if not on Heroku, use in end (DEBUG = not ON_HEROKU )False if on Heroku

if ON_HEROKU:
    # If on Heroku, use a specific domain or IP address for ALLOWED_HOSTS
    ALLOWED_HOSTS = ["kayscrochet.us", "kayscrochetapp-e13180bf49a3.herokuapp.com", "www.kayscrochet.us"]
else:
    # If not on Heroku, use '' for ALLOWED_HOSTS
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "kayscrochetapp.apps.KayscrochetappConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'KaysCrochet.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'KaysCrochet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# Determine if the application is running on Heroku
ON_HEROKU = os.environ.get('ON_HEROKU', None)

if ON_HEROKU:
    # Use the Heroku database configuration
    DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
else:
    # Use the local SQLite database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Static files (CSS, JavaScript, images)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'kayscrochetappbucket'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_CUSTOM_DOMAIN = f'kayscrochetappbucket.s3.amazonaws.com'
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = 's3v4'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'KaysCrochet.storage_backends.MediaStorage'

AUTH_USER_MODEL = 'auth.User'

# Determine if the application is running on Heroku
ON_HEROKU = os.environ.get('ON_HEROKU', None)

if ON_HEROKU:
    # Use the production static files directory
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'kayscrochetapp/static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
else:
    # Use the local static files directory
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'kayscrochetapp/static')]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_local')

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

if 'test' not in sys.argv and 'collectstatic' not in sys.argv:
    logging.basicConfig(level=logging.DEBUG)

    # Add the following two lines to enable debugging of boto3 (S3 library)
    logging.getLogger('boto3').setLevel(logging.DEBUG)
    logging.getLogger('botocore').setLevel(logging.DEBUG)

    # Add the following line to enable debugging of your code
    logging.getLogger(__name__).setLevel(logging.DEBUG)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Set the desired logging level here
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'kayscrochetapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'boto3': {  # Add boto3 logger configuration
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}