
from pathlib import Path
import os
import environ
    
env = environ.Env(
    DEBUG=(bool,False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


environ.Env.read_env(BASE_DIR/'.env')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(t)u9!s!3!&sh^*f@$nppgdw1ig24@cfb6_c!3-!hs0q7k4e+='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','54.165.130.156']

# CHANGE DEFAULT USER MODEL
AUTH_USER_MODEL = 'account.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'education',
    'food',
    'general',
    'sustainable',
    'crispy_forms',
    'crispy_bootstrap5',
    'storages',
    'django_aws_xray',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django_aws_xray.middleware.XRayMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AWS_XRAY_PATCHES = [
    'django_aws_xray.patches.cache',
    'django_aws_xray.patches.redis',
    'django_aws_xray.patches.db',
    'django_aws_xray.patches.requests',
    'django_aws_xray.patches.templates',
]

ROOT_URLCONF = 'ddac_application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
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

WSGI_APPLICATION = 'ddac_application.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
##LOCAL DATABASE
# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'postgres',
#             'USER': 'admin',
#             'PASSWORD': '',
#             'HOST': 'localhost',
#             'PORT': '5440',image.png
#     }
# }

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ddac_best',
            'USER': 'admin_123',
            'PASSWORD': 'admin_123',
            'HOST': 'ddac-assm.c52e4ck2g5ru.us-east-1.rds.amazonaws.com',
            'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'ddac_application/static'
]

MEDIA_URL = 'media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'custom_login_page'

# ARN_USER= env('ARN_USER')
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_SESSION_TOKEN=env('AWS_SESSION_TOKEN')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')  # e.g., us-east-1
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_S3_HOST = 's3.us-east-1.amazonaws.com'

# # For serving static files directly from S3
# AWS_S3_URL_PROTOCOL = 'https:'
# AWS_S3_USE_SSL = True
# AWS_S3_VERIFY = True
# AWS_S3_FILE_OVERWRITE = False
# AWS_QUERYSTRING_EXPIRE = 5
# # Static and media file configuration
# # STATIC_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/static/'
# # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/media/'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


ARN_USER= env('ARN_USER')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_SESSION_TOKEN=env('AWS_SESSION_TOKEN')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')  # e.g., us-east-1
AWS_S3_CUSTOM_DOMAIN = env('AWS_CLOUDFRONT_DOMAIN')

# For serving static files directly from S3
AWS_S3_URL_PROTOCOL = 'https:'
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True
AWS_S3_FILE_OVERWRITE = False

AWS_CLOUDFRONT_KEY_ID = env.str('AWS_CLOUDFRONT_KEY_ID').strip()
AWS_CLOUDFRONT_KEY = env.str('AWS_CLOUDFRONT_KEY',multiline=True).encode('ascii').strip()

MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}//{AWS_S3_CUSTOM_DOMAIN}/media/'

DEFAULT_FILE_STORAGE = 'ddac_application.custom.ReadOnlyS3Boto3Storage'

AWS_XRAY_TRACING_NAME = 'YOUR_APP_NAME'
AWS_XRAY_SAMPLING_RATE = 100
AWS_XRAY_EXCLUDED_PATHS = []
AWS_XRAY_HOST = '127.0.0.1'
AWS_XRAY_PORT = '2000'