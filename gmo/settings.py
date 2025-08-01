"""
Django settings for gmo project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

""" 
collected static files
 """

from pathlib import Path  
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ei9s=@j)=ielp2(=_i3xoye_*p#i9sld8_--wxjf+@3gbh^nrl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gmo.urls'  



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

WSGI_APPLICATION = 'gmo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'login_view'

MEDIA_URL = 'media/'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # e.g., smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'eddymutugik@gmail.com'
EMAIL_HOST_PASSWORD = 'yxbdzcdikhaehcae'



# Jazzmin UI Settings
JAZZMIN_SETTINGS = {
    # Title on the brand (19 chars max)
    "site_brand": "AgriVerify",
    "site_logo": "images/logo.png",  # Path to your logo (should be in static files)
    
    # Welcome text on the login screen
    "welcome_sign": "Welcome to AgriVerify Administration",
    
    # Copyright on the footer
    "copyright": "AgriVerify Ltd",
    
    # Field name on user model that contains avatar image
    "user_avatar": None,
    
    # Top Menu #
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        
        # external url that opens in a new window (Permissions can be added)
        {"name": "Live Site", "url": "/", "new_window": True},
        
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
        
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "agriverify"},
    ],
    
    # Side Menu #
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # Custom icons for side menu apps/models
    "icons": {
        "auth": "ri-shield-user-line",
        "auth.user": "ri-user-line",
        "auth.Group": "ri-group-line",
        "agriverify.GMOProduct": "ri-seedling-line",
        "agriverify.ChatMessage": "ri-chat-1-line",
        "agriverify.EducationalResource": "ri-book-line",
        "agriverify.VerificationRequest": "ri-qr-scan-line",
    },
    
    # Icons that are used when one is not manually specified
    "default_icon_parents": "ri-arrow-right-s-line",
    "default_icon_children": "ri-arrow-right-s-line",
    
    # UI Tweaks
    "related_modal_active": True,  # Use modal windows for related items
    "custom_css": "css/admin.css",  # Custom admin CSS
    "custom_js": "js/admin.js",  # Custom admin JS
    
    # Show UI customizer on the sidebar
    "show_ui_builder": True,
    
    # Change view #
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs"
    },
    
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "agriverify": [{
            "name": "Make Reports", 
            "url": "make_report", 
            "icon": "ri-file-chart-line",
            "permissions": ["agriverify.view_report"]
        }]
    },
    
    # Customize the order of apps/models
    "order_with_respect_to": [
        "agriverify",
        "auth",
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}