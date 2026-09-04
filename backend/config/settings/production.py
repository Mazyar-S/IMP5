
from .base import *

DEBUG = False

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", "").split(",")

CSRF_TRUSTED_ORIGINS = [
    value for value in env("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if value
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True