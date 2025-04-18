"""
Django settings for Littlelemon project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv('.env.local')

# Default to local development settings
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = (os.environ.get('DEBUG') == "True")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
ALLOWED_HOSTS.append('testserver')
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS","https://127.0.0.1").split(",")

# Custom User Model
AUTH_USER_MODEL = "Restaurant.CustomUser"
LOGIN_URL = "login"  # Redirect to login page
LOGIN_REDIRECT_URL = "home"  # Redirect after login
LOGOUT_REDIRECT_URL = "home"  # Redirect after logout

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',
    'rest_framework',
    'rest_framework.authtoken',
    "rest_framework_simplejwt",
    'drf_yasg',
    'Restaurant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # First: Security-related middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Second: Handle sessions (before authentication)
    'django.middleware.common.CommonMiddleware',  # Third: Common middleware (URL handling, etc.)
    'django.middleware.csrf.CsrfViewMiddleware',  # Fourth: CSRF protection (depends on session)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Fifth: Handle authentication (depends on sessions)
    'axes.middleware.AxesMiddleware',  # Sixth: Brute-force protection (after authentication)
    
    # **GZipMiddleware**: Compresses response content (HTML, CSS, JS, JSON) to reduce bandwidth usage and improve performance.
    # It should be placed after session and authentication middleware, but before response is sent to the client.
    'django.middleware.gzip.GZipMiddleware',  # Seventh: Enable GZip compression (for better performance)

    'django.contrib.messages.middleware.MessageMiddleware',  # Eighth: User messages (after authentication)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Ninth: Clickjacking protection (after messages)
]



ROOT_URLCONF = 'Littlelemon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'Littlelemon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = { # MySQL Database
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.getenv('DATABASE_NAME'),
#             'USER': os.getenv('DATABASE_USER'),
#             'PASSWORD': os.getenv('USER_PASSWORD'),
#             'HOST': os.getenv('DATABASE_HOST'),
#             'PORT': os.getenv('DATABASE_PORT'),
#             'TEST': {
#                 'NAME': 'test_db',  # Separate test database
#             },
#         }
#     }

# If you are using MySQL, uncomment the above DATABASES setting and comment the below DATABASES setting. Update your database settings in the .env file or here directly.

DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DATABASE_ENGINE'),
            'NAME': os.environ.get('DATABASE_NAME'),
            'USER': os.environ.get('DATABASE_USER'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),    
            'HOST': os.environ.get('DATABASE_HOST'), # For local development, use 'localhost' or '127.0.0.1'
            'PORT': os.environ.get('DATABASE_PORT'), # Default PostgreSQL port is usually '5432'
            'TEST': {
                'NAME': 'test_db',  # Separate test database
            },
        }
    }

# if ENVIRONMENT == 'development':
#     DATABASES = {
#         'default': {
#             'ENGINE': os.environ.get('DATABASE_ENGINE'),
#             'NAME': os.environ.get('DATABASE_NAME'),
#             'USER': os.environ.get('DATABASE_USER'),
#             'PASSWORD': os.environ.get('DATABASE_PASSWORD'),    
#             'HOST': os.environ.get('DATABASE_HOST'), # For local development, use 'localhost' or '127.0.0.1'
#             'PORT': os.environ.get('DATABASE_PORT'), # Default PostgreSQL port is usually '5432'
#             'TEST': {
#                 'NAME': 'test_db',  # Separate test database
#             },
#         }
#     }

# elif ENVIRONMENT == 'test':  # For GitHub Actions test.yml
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('DATABASE_NAME'),
#             'USER': os.getenv('DATABASE_USER'),
#             'PASSWORD': os.getenv('USER_PASSWORD'),
#             'HOST': os.getenv('DATABASE_HOST'),
#             'PORT': os.getenv('DATABASE_PORT'),
#         }
#     }

# elif ENVIRONMENT == 'production':  # For Render or Heroku
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': os.getenv('DATABASE_NAME'),
#             'USER': os.getenv('DATABASE_USER'),
#             'PASSWORD': os.getenv('USER_PASSWORD'),
#             'HOST': os.getenv('DATABASE_HOST'),
#             'PORT': os.getenv('DATABASE_PORT'),
#         }
#     }



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Required for django-axes (brute force protection)
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication
]


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

# Prevents JavaScript from accessing session cookies, mitigating cross-site scripting (XSS) attacks.
SESSION_COOKIE_HTTPONLY = True 

# Prevents the browser from sending the session cookie along with cross-site requests, mitigating cross-site request forgery (CSRF) attacks.
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# On login, user session will expire after 60 minutes of inactivity and the session will be deleted when the user closes the browser.
SESSION_COOKIE_AGE = 3600  # 60 minutes (3600 seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Rate Limiting Settings (Prevent Brute Force Attacks) 
AXES_FAILURE_LIMIT = 5  # Block user after 1000 failed login attempts
AXES_COOLOFF_TIME = 1  # Lockout time in hours (set 1 for 1 hour)


# Secure Password Settings
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Most secure option
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Fallback option
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',  # Another fallback
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',  # Optional backup
]





# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     BASE_DIR / "Restaurant/static",
# ]



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",  
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework_csv.parsers.CSVParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # Token expires in 1 hour
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh token valid for 7 days
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
