"""
Django settings for app_support project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

#import django_heroku
from django.core.mail import EmailMessage

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!f=4z(wp*cqg^ic&%nhpq5vm6i=wt*p$non*i7=c24h)1=33%q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend" ,

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend" ,
)

ACCOUNT_FORMS = {
    # "login": "users.forms.CustomLoginForm"
    'signup': 'users.forms.UserCreationForm' ,
    # 'signup': 'users.forms.CustomuserPasswordReset',
    'login': 'allauth.account.forms.LoginForm' ,
    'add_email': 'allauth.account.forms.AddEmailForm' ,
    'change_password': 'allauth.account.forms.ChangePasswordForm' ,
    'set_password': 'allauth.account.forms.SetPasswordForm' ,
    'reset_password': 'allauth.account.forms.ResetPasswordForm' ,
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm' ,
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm' ,

}

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 3600
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'
SITE_ID = 1
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/ticket/list/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = '/ticket/list'
ACCOUNT_LOGOUT_REDIRECT_URL = '/ticket/list'

SESSION_EXPIRE_SECONDS = 3600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True


SILENCED_SYSTEM_CHECKS = ['auth.E003', 'auth.W004']


# Application definition

INSTALLED_APPS = [
    'django_cleanup' ,
    'django.contrib.admin' ,
    'django.contrib.auth' ,
    'django.contrib.contenttypes' ,
    'django.contrib.sessions' ,
    'django.contrib.messages' ,
    'django.contrib.staticfiles' ,
    'django.contrib.sites' ,  # new

    # 3rd party
    'allauth' ,  # new
    'allauth.account' ,  # new
    'allauth.socialaccount' ,  # new
    'crispy_forms' ,
    'django_crispy_bulma' ,
    'ckeditor',

    # Local
    'tickets.apps.TicketsConfig' ,
    'users.apps.UsersConfig' ,  # new
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware' ,
    'django.contrib.sessions.middleware.SessionMiddleware' ,
    'django.middleware.common.CommonMiddleware' ,
    'django.middleware.csrf.CsrfViewMiddleware' ,
    'django.contrib.auth.middleware.AuthenticationMiddleware' ,
    'django.contrib.messages.middleware.MessageMiddleware' ,
    'django.middleware.clickjacking.XFrameOptionsMiddleware' ,
]
AUTH_USER_MODEL = 'users.User'  # new

ROOT_URLCONF = 'app_support.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates' ,
        'DIRS': [os.path.join(BASE_DIR , 'templates')] ,
        # 'DIRS': [],
        'APP_DIRS': True ,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug' ,
                'django.template.context_processors.request' ,
                'django.contrib.auth.context_processors.auth' ,
                'django.contrib.messages.context_processors.messages' ,
            ] ,
        } ,
    } ,
]

WSGI_APPLICATION = 'app_support.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2' ,
        'NAME': 'infohub_db' ,
        'DATABASE_SCHEMA': 'infohub_db' ,
        'options': '-c search_path=django, public' ,
        'USER': '' ,
        'PASSWORD': '' ,
        'HOST': '' ,
        'PORT': '' ,
    } ,

    'ticket': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2' ,
        'NAME': 'infohub_db' ,
        'options': '-c search_path=django, ticket' ,
        'USER': '' ,
        'PASSWORD': '' ,
        'HOST': '' ,
        'PORT': '' ,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' ,
    } ,
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' ,
    } ,
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' ,
    } ,
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' ,
    } ,
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR , "static") ,
]

CRISPY_ALLOWED_TEMPLATE_PACKS = (
    "bulma",
    "bootstrap4"
)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR , 'media')
MEDIA_URL = '/media/'
CRISPY_TEMPLATE_PACK = 'bulma'
LOGIN_URL = 'accounts/login'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# CKEDITOR_BASEPATH = "/my_static/ckeditor/ckeditor/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = MEDIA_ROOT

CKEDITOR_CONFIGS = {
    'default': {
        'height': 300,
        'width': 600,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}


# Configure Django App for Heroku.
#django_heroku.settings(locals())
#del DATABASES['default']['OPTIONS']['sslmode']

