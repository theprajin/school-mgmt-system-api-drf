from .base import *

DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS += [
    "debug_toolbar",
    "silk",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "silk.middleware.SilkyMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

SILKY_PYTHON_PROFILER = True
