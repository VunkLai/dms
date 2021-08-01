"""
Django settings for dms project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Django-environ allows you to configure your Django application by .env file
# https://django-environ.readthedocs.io/en/latest/#indices-and-tables
env_file = BASE_DIR / 'dms' / '.env'
if not env_file.exists():
    raise FileNotFoundError('`.env` file not Found')
env = environ.Env()
environ.Env.read_env(env_file=str(env_file))  # reading .env file

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

GCP_CREDENTIAL = BASE_DIR.parent / '.credential.json'
HEALTH_DECLARATION_SHEET = env.str('HEALTH_DECLARATION_SHEET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'employee',
    'pe',
    'hr',
    'server',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'dms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {'default': env.db('DATABASE_URL')}

# Do not add other databases to DATABASES setting
BPM_DATABASE = env.db('BPM_DATABASE')

NULLABLE = {'default': None, 'null': True, 'blank': True}

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

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

FOUR_ZEROS = {'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email

EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

# Email recipients

EMAIL_JOY = env.str('EMAIL_JOY')

EMAIL_PE_PSMC_OWNER = env.str('EMAIL_PE_PSMC_OWNER')
EMAIL_PE_PSMC_TO = env.list('EMAIL_PE_PSMC_TO')

EMAIL_HR_GATEWAY_OWNER = env.str('EMAIL_HR_GATEWAY_OWNER')
EMAIL_HR_GATEWAY_TO = env.list('EMAIL_HR_GATEWAY_TO')

# Folder

REMOTE_DIR = Path(env.str('REMOTE_DIR'))

CARD_EVENT_DIR = REMOTE_DIR / 'card_event'

# HR Users

HRS = env.list('HRS')
FQDN = env.str('FQDN')
