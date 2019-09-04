
import os
import dj_database_url
import os.path
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

WSGI_APPLICATION = 'SpotWrk.wsgi.application'
SECRET_KEY = '63y!+)$(#vi$6a3y-74hdpo)wd1$v*(v3+o+hj4xwk^invnpti'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'SpotWrkApp.apps.SpotWrkAppConfig',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'social_django',
    'employer',
    #'cities_light',
     'django_inlinecss',
     'django_cleanup'
]

from django.conf import settings

FILE_STORAGE = getattr(
    settings, 'FU_FILE_STORAGE', 'django.core.files.storage.DefaultStorage'
)

#CITIES_LIGHT_TRANSLATION_LANGUAGES = ['in', 'en']
#CITIES_LIGHT_INCLUDE_COUNTRIES = ['IN','US']
#CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PCLF','PPL',]

# Application definition

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'SpotWrk.urls'

PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]


LOGIN_URL = '/'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '192259400309-4pc90ajcqq143r8887l2mimutri127s1.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '_MCA6Q81jkrZdPVHFML50HS0'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '815m1l2vtrz24o'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = '6VJ60uLT4qACY3Au'


#1426932694089704
#cc9c5661e9f9f22a64f68fb61e454767

SOCIAL_AUTH_FACEBOOK_KEY = '258157754676012'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '1169d1a2416ff63bb7de70a1930d2da6'  # App Secret


AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""
    'SpotWrkAppdb': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'employerdb': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':os.path.join(BASE_DIR, 'employer_db.sqlite3'),
    }
"""


#DATABASE_ROUTERS = ['employer.dbRouter.employerDBRouter', 'SpotWrkApp.dbRouter.SpotWrkAppDBRouter']

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PROFILE_MODULE = 'accounts.Profile'

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_USE_TLS = True

#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
#MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'Fjwsjd616'
EMAIL_HOST_USER = 'tannai.odin@gmail.com'
EMAIL_PORT = 587
#EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
