import os

from .base import *


# Get the secret key from environment variable, with a fallback for safety
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key-only-for-development')

# In production, you want to ensure it's set and raise an error if it's not
if not SECRET_KEY or SECRET_KEY == 'fallback-secret-key-only-for-development':
    raise ValueError("DJANGO_SECRET_KEY environment variable must be set in production!")

DEBUG = True

ALLOWED_HOSTS = [
    'cms.livestauction.com', 
    '127.0.0.1', 
    'localhost'
]

CSRF_TRUSTED_ORIGINS = [
    'https://cms.livestauction.com',
    'http://cms.livestauction.com'
]

try:
    from .local import *
except ImportError:
    pass
