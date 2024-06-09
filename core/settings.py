import os

import environ

from django.urls import reverse_lazy

env = environ.Env()

environ.Env.read_env()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__),
    ),
)


ADMIN_URL = env("ADMIN_URL", default="admin/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", default=False)  # type: ignore

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default="*").split()  # type: ignore


# Application definition

INSTALLED_APPS = [
    "django_cleanup",
    "ckeditor",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
    "api",
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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


if env("USE_SQLITE", default=True):  # type: ignore
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("DATABASE_NAME"),
            "USER": env("DATABASE_USER"),
            "PASSWORD": env("DATABASE_PASSWORD"),
            "HOST": env("DATABASE_HOST", default="localhost"),  # type: ignore
            "PORT": env("DATABASE_PORT", default="5432"),  # type: ignore
        }
    }

CKEDITOR_UPLOAD_PATH = "uploads/"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

VALIDATORS_PATH = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{VALIDATORS_PATH}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{VALIDATORS_PATH}.MinimumLengthValidator",
    },
    {
        "NAME": f"{VALIDATORS_PATH}.CommonPasswordValidator",
    },
    {
        "NAME": f"{VALIDATORS_PATH}.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "hy"

TIME_ZONE = "Asia/Yerevan"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", default="").split()


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STAKING_WALLET = env("STAKING_WALLET", default="")
STAKING_WALLET_SECRET = env("STAKING_WALLET_SECRET", default="")
