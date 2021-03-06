"""
Django settings for settings project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from django.contrib import messages

import const

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = const.secret_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = const.secret_settings.DEBUG

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', const.secret_settings.VPS_IP,
                 'www.clients-notebook.ru', 'clients-notebook.ru']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_registration',
    'apps.front_app',
    'apps.profile_app',
    'apps.services_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'
ADMIN_URL = 'very_secr3t_p4nel/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'front_app/templates',
            'services_app/templates',
            'profile_app/templates',
        ],
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

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default':
            {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'cndb',
                'USER': 'cndbuser',
                'PASSWORD': const.secret_settings.DB_PASSWORD,
                'HOST': 'localhost',
                'PORT': '',
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

ACTIVATION_REQUIRED = const.secret_settings.ACTIVATION_REQUIRED
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True

EMAIL_BACKEND = const.smtp_settings.EMAIL_BACKEND
EMAIL_HOST = const.smtp_settings.EMAIL_HOST
EMAIL_PORT = const.smtp_settings.EMAIL_PORT
EMAIL_HOST_USER = const.smtp_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = const.smtp_settings.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = const.smtp_settings.EMAIL_USE_TLS
SERVER_EMAIL = const.smtp_settings.SERVER_EMAIL
DEFAULT_FROM_EMAIL = const.smtp_settings.DEFAULT_FROM_EMAIL

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = '/profile/login/'
LOGOUT_URL = '/profile/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Messages

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
