"""
Django settings for drf_api project.

Generated by 'django-admin startproject' using Django 3.2.23.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
import re

if os.path.exists('env.py'):
    import env

CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}

# The code below is standard django folder to store media files like images, now setting know where to put our image files
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# To make this distinction, I’ll set  ‘DEV’ to ‘1’ in the env.py file.
# Next, we can use this value to check  whether we’re in Development or Production,  
# and authenticate using sessions  or tokens respectively. https://jwt.io/ is the website for JSON web tokens.
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [(
        'rest_framework.authentication.SessionAuthentication'
        if 'DEV' in os.environ
        else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    )],
    # Pagination is really easy to set up  with REST Framework. In settings.py, 
    # I’ll set it to PageNumberPagination with the page  size set to ten inside the REST_FRAMEWORK object.
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE' : 10,
    # e.g 02 Aug 2024 https://www.django-rest-framework.org/api-guide/settings/#date-and-time-formatting
    # https://docs.python.org/3/library/time.html#time.strftime
    'DATETIME_FORMAT' : '%d %b %Y'
}

# Another thing to get out of the way  is to set the default renderer to JSON  
# for the production environment. What this means is  that we want this nice, in-browser interface to be  
# available in development only. All the frontend  app cares about is JSON, and nothing else,  
# so it would be pointless to send html. Here’s how to do it in settings.py.
# If the ‘DEV’ environment variable is NOT present,  I’ll set the rest framework’s default renderer  
# classes attribute to JSONRenderer inside a list. FRONTEND only just need JSON data notthong else
if 'DEV' not in os.environ:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]


# To enable token authentication, we’ll  also have to set REST_USE_JWT to True.  
# To make sure they’re sent over HTTPS only,  we will set JWT_AUTH_SECURE to True as well.
# We also need to declare the cookie names for the  access and refresh tokens, as we’ll be using both.
REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
# To be able to have the front end app and the API deployed to different platforms,
# set the JWT_AUTH_SAMESITE attribute to 'None'. Without this the cookies would be blocked
JWT_AUTH_SAMESITE = 'None'

# let’s overwrite the default USER_DETAILS_SERIALIZER in settings.py.
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'drf_api.serializers.CurrentUserSerializer'
}

# TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = 'DEV' in os.environ

ALLOWED_HOSTS = ['8000-mbilalqures-reactdjango-qd5jaotagrv.ws-us107.gitpod.io',os.environ.get('ALLOWED_HOST'),]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'corsheaders',
    'profiles',
    'posts',
    'comments',
    'likes',
    'followers',
]

SITE_ID = 1
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Here the allowed origins are set for the network requests made to the server. 
# The API will use the CLIENT_ORIGIN variable, which is the front end app's url. 
# We haven't deployed that project yet, but that's ok. If the variable is not present,
# that means the project is still in development, so then the regular expression in the
#  else statement will allow requests that are coming from your IDE.

if 'CLIENT_ORIGIN' in os.environ:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN')
    ]
# else:
#     CORS_ALLOWED_ORIGIN_REGEXES = [
#         r"^https://.*\.gitpod\.io$",
#     ]
'''
Above else is removed and below if is put because:
In order to make our application more secure and accommodate the way Gitpod works by changing the workspace URL regularly, the below code has been provided for you to add to your project.

The following code works as follows:
a) When the CLIENT_ORIGIN_DEV environment variable is defined, the unique part of your gitpod preview URL is extracted.
b) It is then included in the regular expression provided by us so that the gitpod workspace is still connected to our API when gitpod rotates the workspace URL.
'''
if 'CLIENT_ORIGIN_DEV' in os.environ:
    extracted_url = re.match(r'^.+-', os.environ.get('CLIENT_ORIGIN_DEV', ''), re.IGNORECASE).group(0)
    CORS_ALLOWED_ORIGIN_REGEXES = [
        rf"{extracted_url}(eu|us)\d+\w\.gitpod\.io$",
    ]

# Enable sending cookies in cross-origin requests so that users can get authentication functionality
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'drf_api.urls'

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

WSGI_APPLICATION = 'drf_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
         'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
