"""
Django settings for idesignweb project.
Strict compliance: Flat styling, no gradients, no emoji, no icon fonts/SVGs, no em dashes.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-+rz26ne259ic%2=tb*3s&#be%w6qj!e9qs0r)hf26o%amg8!&#')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allowed hosts configuration
allowed_hosts_raw = os.getenv('ALLOWED_HOSTS', '*').strip()
if not allowed_hosts_raw or allowed_hosts_raw == '*':
    ALLOWED_HOSTS = ['*']
else:
    raw_hosts = [h.strip() for h in allowed_hosts_raw.split(',') if h.strip()]
    ALLOWED_HOSTS = []
    for h in raw_hosts:
        # Strip scheme (http:// or https://) and path if entered by mistake
        h_clean = h.replace('https://', '').replace('http://', '').split('/')[0].strip()
        if h_clean.startswith('*.'):
            h_clean = h_clean[1:]  # Convert *.domain.com to .domain.com for Django wildcard
        if h_clean and h_clean not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(h_clean)

# Automatically ensure domain fallbacks and local loopbacks are allowed
for default_h in ['idesignweb.echowithin.xyz', '.echowithin.xyz', 'localhost', '127.0.0.1', 'testserver']:
    if default_h not in ALLOWED_HOSTS and '*' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(default_h)

# Traefik Reverse Proxy & HTTPS Configuration for Dokploy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
csrf_origins_env = os.getenv('CSRF_TRUSTED_ORIGINS', '').strip()
if csrf_origins_env:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins_env.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []

for default_csrf in [
    'https://idesignweb.echowithin.xyz',
    'https://*.echowithin.xyz',
    'http://idesignweb.echowithin.xyz',
    'http://*.echowithin.xyz',
]:
    if default_csrf not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(default_csrf)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Internal project apps
    'apps.core',
    'apps.public',
    'apps.portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Member portal headers enforcement (noindex, nofollow)
    'apps.portal.middleware.PortalSecurityMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Relational side-store for auth, sessions, and Django admin
db_path = os.getenv('DATABASE_PATH')
if db_path:
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
else:
    db_file = BASE_DIR / 'db.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': db_file,
    }
}

# MongoDB Storage Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'idesignweb_db')

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/portal/'
LOGOUT_REDIRECT_URL = '/'
