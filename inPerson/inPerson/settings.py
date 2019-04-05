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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6l)tm(+9my#y0=t7v3+8_%1p%yhu*-8i00zh6)gu+2@w2ec(6x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'schedule',
    'users'
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

ROOT_URLCONF = 'inPerson.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'inPerson.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
        # 'default': dj_database_url.config(default='postgres://dtrstrpwyxmxer:4c93c1cba1869c88beda4741002847546676002ca179097a490de298d5df9765@ec2-23-21-106-241.compute-1.amazonaws.com:5432/dsrsgr2k2redd')
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #     'HOST': 'ec2-23-21-106-241.compute-1.amazonaws.com',
        #     'PASSWORD': '4c93c1cba1869c88beda4741002847546676002ca179097a490de298d5df9765',
        #     'USER': 'dtrstrpwyxmxer',
        #     'NAME': 'dsrsgr2k2redd',
        #     'PORT': '',
        #     'TEST': {
        #         'NAME': 'test_dsrsgr2k2redd',
        #     }
        # },

        ## USE THIS FOR TESTING MODELS LOCALLY
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': 'localhost',
            'PASSWORD': 'password',
            'USER': 'inPerson_admin',
            'NAME': 'inperson_db',
            'PORT': '',
            'TEST': {
                'NAME': 'inPerson_db_test',
            }
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

STATIC_URL = '/static/'
django_heroku.settings(locals())

# Login Redirection
LOGIN_REDIRECT_URL = '/'
