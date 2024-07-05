from pathlib import Path
from dotenv import load_dotenv
import os

from django.urls import reverse_lazy


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'DjangoSecretKey')

DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
    'allauth',
    'allauth.account',

    # Optional -- requires install using `django-allauth[socialacocunt]`.
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # My apps
    'Tinytalefactory.common',
    'Tinytalefactory.generate_stories',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third party middlewares
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'Tinytalefactory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Tinytalefactory.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'default'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static | Media files configurations
STATIC_URL = 'staticfiles/'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles/']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_EMAIL')
EMAIL_HOST = 'live.smtp.mailtrap.io'
EMAIL_HOST_USER = 'api'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_PORT = '587'
EMAIL_USE_TLS = True

# Login | Logout default configurations
LOGIN_REDIRECT_URL = reverse_lazy('account_login')
LOGIN_URL = reverse_lazy('account_login')
LOGOUT_URL = reverse_lazy('account_logout')


# allauth configurations
ACCOUNT_ADAPTER = 'Tinytalefactory.users.adapter.RedirectToIndexAdapter'
ACCOUNT_FORMS = {
    'login': 'Tinytalefactory.allauth.forms.CustomLoginForm',
    'add_email': 'Tinytalefactory.allauth.forms.CustomAddEmailForm',
    'set_password': 'Tinytalefactory.allauth.forms.CustomSetPasswordForm',
    'change_password': 'Tinytalefactory.allauth.forms.CustomChangePasswordForm',
    'reset_password': 'Tinytalefactory.allauth.forms.CustomResetPasswordForm',
    'reset_password_from_key': 'Tinytalefactory.allauth.forms.CustomResetPasswordKeyForm',
    'signup': 'Tinytalefactory.allauth.forms.CustomSignUpForm',
}
