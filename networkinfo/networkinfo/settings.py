"""
Django settings for networkinfo project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from pathlib import Path
import environ

env = environ.Env()
env.read_env('.env')
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_users',
    'programmers',
    'create_user',
    'main_page',
    'telephone_billing',
    'psycopg2'
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

ROOT_URLCONF = 'networkinfo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates'))],
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

WSGI_APPLICATION = 'networkinfo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT')
    },
    "kav": {
        "ENGINE": "mssql",
        "NAME": env('SQL_DB'),
        "USER": env('SQL_USER'),
        "PASSWORD": env('SQL_PASSWORD'),
        "HOST": env('SQL_HOST'),
        "PORT": "",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server"
                    },
    },
    "spsql": {
        "ENGINE": "mssql",
        "NAME": env('SPSQL_DATABASE'),
        "USER": env('SPSQL_UID'),
        "PASSWORD": env('SPSQL_PASSWORD'),
        "HOST": env('SPSQL_SERVER'),
        "PORT": "",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server"
                    },
    },
    'freeswitchdb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('FREESWITCH_DB'),
        'USER': env('FREESWITCH_USER'),
        'PASSWORD': env('FREESWITCH_PASSWORD'),
        'HOST': env('FREESWITCH_HOST'),
        'PORT': env('FREESWITCH_PORT')
    },
    'statisticdb': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('STATISTIC_DB'),
        'USER': env('STATISTIC_USER'),
        'PASSWORD': env('STATISTIC_PASSWORD'),
        'HOST': env('STATISTIC_HOST'),
        'PORT': env('STATISTIC_PORT')
    },
}

# ORACLE DB

ORACLE_USER = env('ORACLE_USER')
ORACLE_PASSWORD = env('ORACLE_PASSWORD')
DB_STRING = env('DB_STRING')


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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'app_users.backends.LDAPBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'

# LDAP CONNECTIONS SETTINGS

LDAP_USERNAME = env('LDAP_USERNAME')
LDAP_PASSWORD = env('LDAP_PASSWORD')
LDAP_SERVER = env('LDAP_SERVER')

# SKUD MYSQL CONFIGURATION

skud_config = {
    'host': env('SKUD_HOST'),
    'port': env('SKUD_PORT'),
    'database': env('SKUD_DATABASE'),
    'user': env('SKUD_USER'),
    'password': env('SKUD_PASSWORD'),
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True,
}

# ADMIN LDAP

AD_SERVER = env('ad_server')
AD_USER = env('ad_user')
AD_PASSWORD = env('ad_password')

TRANSLIT_DICT = {' ': '_', '??': 'a', '??': 'b', '??': 'v', '??': 'g', '??': 'd', '??': 'e', '??': 'e', '??': 'zh', '??': 'z',
                 '??': 'i', '??': 'i', '??': 'k', '??': 'l', '??': 'm', '??': 'n', '??': 'o', '??': 'p', '??': 'r', '??': 's',
                 '??': 't', '??': 'u', '??': 'f', '??': 'h', '??': 'c', '??': 'ch', '??': 'sh', '??': 'shch', '??': 'y',
                 '??': 'iu',
                 '??': 'ya', '??': 'A', '??': 'B', '??': 'V', '??': 'G', '??': 'D', '??': 'E', '??': 'E', '??': 'Zh', '??': 'Z',
                 '??': 'I', '??': 'I', '??': 'K', '??': 'L', '??': 'M', '??': 'N', '??': 'O', '??': 'P', '??': 'R', '??': 'S',
                 '??': 'T', '??': 'U', '??': 'F', '??': 'H', '??': 'C', '??': 'Ch', '??': 'Sh', '??': 'Shch', '??': 'Y',
                 '??': 'E',
                 '??': 'Iu', '??': 'Ya', '??': '', '??': '', '??': '', '??': '', '.': '', '1': '1', '2': '2', '3': '3',
                 '4': '4',
                 '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0'}
