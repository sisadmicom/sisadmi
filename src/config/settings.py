import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializa el entorno
env = environ.Env(
    DEBUG=(bool, False)
)

# Carga el archivo .env desde la raíz del proyecto
#environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
environ.Env.read_env(os.path.join(BASE_DIR, "..", ".env"))

# Variables de entorno
SECRET_KEY = env("SECRET_KEY", default="fallback-secret")
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

# Application definition
INSTALLED_APPS = [
    "people",
    "companies",
    "users",
    "core",
    "inventory",
    
    "purchases",
    "documents",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smart_selects',
    # terceros
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    
    
    
    #"accounting",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # 👇 Esto es lo importante:
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # ✅ Coloca tu middleware DESPUÉS
    'core.middleware.ActiveCompanyMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.CurrentUserMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'sisadmi'),
        'USER': os.getenv('POSTGRES_USER', 'sisadmi'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'passisadmi'),
        'HOST': os.getenv('POSTGRES_HOST', 'db'),
        #'HOST': 'db',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#AUTH_USER_MODEL = "users.User"

AUTH_USER_MODEL = 'users.User'

from datetime import timedelta

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}
