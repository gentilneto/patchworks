"""
Django settings for patchworks project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-lij(r(q-dw(x7b+5xn7$o9bau9myl$ue33)(sqvg&#2x(x*hno)',
)

DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = [
    h.strip()
    for h in os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '').split(',')
    if o.strip()
]

INSTALLED_APPS = [
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'patchworks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'patchworks.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'patchworks'),
        'USER': os.getenv('MYSQL_USER', 'patchworks'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
        'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Melhor Envio / loja (usados no Passo 3)
STORE_CEP = os.getenv('STORE_CEP', '07094000')
STORE_ADDRESS = os.getenv(
    'STORE_ADDRESS',
    'Av. Dr. Timoteo Penteado, 1874 - Vila Hulda, Guarulhos - SP',
)
MELHOR_ENVIO_TOKEN = os.getenv('MELHOR_ENVIO_TOKEN', '')
MELHOR_ENVIO_USER_AGENT = os.getenv(
    'MELHOR_ENVIO_USER_AGENT',
    'Patch Works e Afins (gentilc.neto@gmail.com)',
)
MELHOR_ENVIO_BASE_URL = os.getenv(
    'MELHOR_ENVIO_BASE_URL',
    'https://sandbox.melhorenvio.com.br',
)
MELHOR_ENVIO_CLIENT_ID = os.getenv('MELHOR_ENVIO_CLIENT_ID', '')
MELHOR_ENVIO_CLIENT_SECRET = os.getenv('MELHOR_ENVIO_CLIENT_SECRET', '')
MELHOR_ENVIO_REDIRECT_URI = os.getenv(
    'MELHOR_ENVIO_REDIRECT_URI',
    'https://127.0.0.1:8000/api/melhorenvio/callback/',
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
