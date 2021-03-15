"""
Django settings for kklogin project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see

https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6=un%_k92bm@j)#wstnhqs)d)pdj$t@_w1ax(ap-xv8^n_t_d!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['dev.khalti.com.np', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kklogin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
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

WSGI_APPLICATION = 'kklogin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
import os
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get(
            'DRYCC_DATABASE_NAME', os.environ.get('DRYCC_DATABASE_USER', 'oauth')),
        'USER': os.environ.get('DRYCC_DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DRYCC_DATABASE_PASSWORD', '123456'),
        'HOST': os.environ.get('DRYCC_DATABASE_SERVICE_HOST', '192.168.6.50'),
        'PORT': os.environ.get('DRYCC_DATABASE_SERVICE_PORT', 5432),
        'CONN_MAX_AGE': 600,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = '/bagaicha/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/login/'
# BASE_URL = 'http://dev.khalti.com.np:8004'
BASE_URL = 'http://g.uucin.com'

# OAuth Specific
CORS_ORIGIN_ALLOW_ALL = True

OAUTH2_PROVIDER = {
    "PKCE_REQUIRED": False,
    "ALLOWED_REDIRECT_URI_SCHEMES": ["http", "https"],
    "ACCESS_TOKEN_EXPIRE_SECONDS": 30*86400, # #30 Days
    "AUTHORIZATION_CODE_EXPIRE_SECONDS": 600, # RFC Recommendation is 10 Secs
    "CLIENT_SECRET_GENERATOR_LENGTH": 64,
    "REFRESH_TOKEN_EXPIRE_SECONDS": 60*86400, # 60 Days
    "ROTATE_REFRESH_TOKEN": True, # New Refresh Token is issued everytime the access token is changed
    "SCOPES": {
        'profile': 'Khalti',
        'balance': 'Available Balance',
        'transactions': 'Fetch Transaction History',
        'payments': 'Allow Payments to be made automatically' ,
    },
    "DEFAULT_SCOPES":['profile', ],
    "DEFAULT_CODE_CHALLENGE_METHOD":'S256',
}

# ALLOWED_REDIRECT_URI_SCHEMES=["http", "https"]
# ACCESS_TOKEN_EXPIRE_SECONDS=30*86400 # #30 Days
# AUTHORIZATION_CODE_EXPIRE_SECONDS=600 # RFC Recommendation is 10 Secs
# CLIENT_SECRET_GENERATOR_LENGTH=64
# REFRESH_TOKEN_EXPIRE_SECONDS=60*86400 # 60 Days
# ROTATE_REFRESH_TOKEN=True # New Refresh Token is issued everytime the access token is changed
# SCOPES={
#         'profile': 'Khalti Id and Basic Profile Info',
#         'balance': 'Available Balance',
#         'transactions': 'Fetch Transaction History',
#         'payments': 'Allow Payments to be made automatically' ,
# }
# DEFAULT_SCOPES=['profile', ]

# DEFAULT_CODE_CHALLENGE_METHOD='S256'
