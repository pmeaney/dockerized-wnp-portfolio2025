from .base import *

DEBUG = False

SECRET_KEY = "django-insecure-h3+7&(bxg0y0%-61gre3wb$khtusvqp*bb1w74r0cf1coa=mb6"

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
