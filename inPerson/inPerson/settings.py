"""
Django settings for inPerson project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6l)tm(+9my#y0=t7v3+8_%1p%yhu*-8i00zh6)gu+2@w2ec(6x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party applications
    'rest_framework',
    'friendship',
    'django_filters',
    'uniauth',

    # Applications created within this project
    'schedule',
    'users',
    'followrequests',

    # For connection to frontend
    'corsheaders',
    'django_react_templatetags'
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'uniauth.backends.CASBackend',
]

# Specify uniauth settings
LOGIN_URL = "/accounts/login/"
UNIAUTH_LOGIN_DISPLAY_STANDARD = False
UNIAUTH_LOGOUT_CAS_COMPLETELY = True
UNIAUTH_LOGIN_REDIRECT_URL = 'home'
UNIAUTH_LOGOUT_REDIRECT_URL = 'home'

CORS_ORIGIN_ALLOW_ALL = True

# CSRF_COOKIE_NAME = "XSRF-TOKEN" #TEST

# CSRF_COOKIE_NAME = "csrftoken"
# CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ['nperson.herokuapp.com', '127.0.0.1:8000']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'inPerson.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(os.path.dirname(BASE_DIR), 'build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_react_templatetags.context_processors.react_context_processor',
            ],
        },
    },
]


# CORS_ORIGIN_WHITELIST = (
#        'localhost:3000',
# )

ALLOWED_HOSTS = ['nperson.herokuapp.com', '127.0.0.1:8000']

WSGI_APPLICATION = 'inPerson.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'inpersondb.c7xstdrblfzl.us-east-2.rds.amazonaws.com',
            'USER': 'inperson_admin',
            'PASSWORD': 'password',
            'NAME': 'inpersondb',
            'PORT': '',
            'TEST': {
                'HOST': 'localhost',
                'USER': 'inperson_admin',
                'PASSWORD': 'password',
                'USER': 'inperson_admin',
                'NAME': 'inperson_db',
                'PORT': '',
            },
        },


}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

TIME_INPUT_FORMATS = [
    #'%I:%M:%S %p',  # 6:22:44 PM
    '%I:%M %p',  # 6:22 PM
    '%I %p',  # 6 PM
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
  # '/build/',
  # '/static/',
  os.path.join(FRONTEND_DIR, 'build/static'),
)
django_heroku.settings(locals())
