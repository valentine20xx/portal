import os
from django.contrib.messages import constants


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "s%u&15u2zkg&$c)md$(6a63gg0fc85@ec=f4gnc#thfs%(w4-9"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': True
        },
    },
]

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    "converter",
    "authorization",
)

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "portal.urls"
WSGI_APPLICATION = "portal.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
    # 'default': {
    # 'ENGINE': "django.db.backends.postgresql_psycopg2",
    # 'NAME': 'djangodb',
    # 'USER': 'postgres',
    # 'PASSWORD': 'postgres',
    # 'HOST': '127.0.0.1',
    # 'PORT': '5432',
    # }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# AUTOCOMMIT = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "common-static"),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# print("BASE_DIR" + BASE_DIR)
MEDIA_URL = '/media/'

STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"
MESSAGE_LEVEL = constants.DEBUG

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S"
        },
    },
    "handlers": {
        "file_django": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/django.log",
            "formatter": "verbose"
        },
        "file_converter": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/converter.log",
            "formatter": "verbose"
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_django"],
            "propagate": True,
            "level": "DEBUG",
        },
        "converter": {
            "handlers": ["file_converter"],
            "propagate": True,
            "level": "DEBUG",
        },
    }
}