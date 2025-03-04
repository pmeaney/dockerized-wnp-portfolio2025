from .base import *

# Turn off debug in production
DEBUG = False

# Explicitly set allowed hosts
ALLOWED_HOSTS = [
    'cms.livestauction.com',
    # Add any other production domains
]

# Add trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://cms.livestauction.com',
    # Add any other trusted origins
]

# Use a secure, production-specific secret key (set via environment variable)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Production-specific email backend (optional)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Ensure you're not inheriting development settings
try:
    from .local import *
except ImportError:
    pass