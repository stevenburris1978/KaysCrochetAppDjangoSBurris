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

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'kayscrochetapp/static', 'serviceworker.js')

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "kayscrochetapp.apps.KayscrochetappConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'storages',
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    # Add the origins that you want to allow here
    "https://www.kayscrochet.us",
    "https://kayscrochetapp-e13180bf49a3.herokuapp.com",

]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Service-Worker-Allowed',  # Add this line
]

CORS_EXPOSE_HEADERS = [
    'Service-Worker-Allowed',
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

IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

if IS_HEROKU_APP:
    DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
else:
    # Use the local SQLite database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Set SECURE_SSL_REDIRECT based on whether the app is running on Heroku
if IS_HEROKU_APP:
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

CSRF_COOKIE_SAMESITE = 'Lax'



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
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_QUERYSTRING_AUTH = True
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = 's3v4'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AUTH_USER_MODEL = 'auth.User'

PWA_APP_VERSION = '1.0'
PWA_APP_NAME = "Kay's Crochet"
PWA_APP_DESCRIPTION = 'Crochet Sale'
PWA_APP_THEME_COLOR = 'lavenderblush'
PWA_APP_BACKGROUND_COLOR = 'lavender'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '{% static "kayscrochetapp/images/icon-192x192.png" %}',
        'sizes': '192x192',
        "type": "image/png"
    },
    {
        "src": '{% static "kayscrochetapp/images/icon-256x256.png" %}',
        "sizes": "256x256",
        "type": "image/png"
    },
    {
        "src": '{% static "kayscrochetapp/images/icon-384x384.png" %}',
        "sizes": "384x384",
        "type": "image/png"
    },
    {
        "src": '{% static "kayscrochetapp/images/icon-512x512.png" %}',
        "sizes": "512x512",
        "type": "image/png"
    }
]

PWA_APP_ICONS_APPLE = [
    {
        'src': '{% static "kayscrochetapp/images/icon-160x160.png" %}',
        'sizes': '192x192'
    }
]

PWA_APP_SPLASH_SCREEN = [
    {
        'src': '{% static "kayscrochetapp/images/icon-192x192.png" %}',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_CACHES = [
    {
        'name': 'cache-1',
        'timeout': 60 * 60 * 24 * 7,  # 1 week
        'version': PWA_APP_VERSION,
        'urls': [
            '/',
            '//static/',
            'https://s3.amazonaws.com/kayscrochetbucket/items_images/**',
        ],
        'patterns': [
            '^/static/.*$',
        ],
    },
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# Use the production static files directory
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'kayscrochetapp/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

# Set the email backend
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Set SMTP server details
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT'))
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'True').lower() == 'true'

# Set SMTP username and password
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')

LOGGING_DIR = BASE_DIR / 'logs'
LOGGING_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'error.log',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'info.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'myapp': {
            'handlers': ['info_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
