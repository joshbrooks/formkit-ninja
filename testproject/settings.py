"""
Django settings for testproject project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import importlib
from importlib.util import find_spec
from os import environ
from pathlib import Path

from django.conf.locale import LANG_INFO
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-uq^#m^-8-k+f%jag(2kv$p#45%o!#au!877xby@c_tu*ccdr%f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "formkit_ninja",
    "ninja",
    "pgtrigger",
    "pghistory",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "testproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "testproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# Note:
# If you have no database running yet
# maybe start one with `docker run -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres`
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "localhost",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
EXTRA_LANG_INFO = {
    "tet": {
        "bidi": False,  # right-to-left
        "code": "tet",
        "name": "Tetum",
        "name_local": "Tetum",
    }
}
LANG_INFO.update(EXTRA_LANG_INFO)
LANGUAGE_CODE = environ.get("DJANGO_LANGUAGE_CODE", "en")

TIME_ZONE = "Asia/Dili"

LANGUAGES = [
    ("tet", _("Tetum")),
    ("en", _("English")),
    ("pt", _("Portuguese")),
]


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG and find_spec("django_extensions"):
    # "pip install django-extensions"
    INSTALLED_APPS.append("django_extensions")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "rich.logging.RichHandler" if importlib.util.find_spec("rich") else "logging.StreamHandler",
        }
    },
    "loggers": {
        "formkit_ninja": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
    },
}
