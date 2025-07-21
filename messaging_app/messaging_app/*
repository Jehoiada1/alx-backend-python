# messaging_app/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',          # Add this for DRF
    'chats',                   # Add your app
]

# Add this REST_FRAMEWORK configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Update these for security (add your domain when deploying)
ALLOWED_HOSTS = ['*']

# Add at the bottom for static files
STATIC_URL = '/static/'
