"""
Settings específicos para testes
Elimina redirects 301 e configura handlers apropriados
"""
from .base import *

DEBUG = False
APPEND_SLASH = False                # evita 301 para adicionar "/"
SECURE_SSL_REDIRECT = False         # evita 301 http->https nos testes
USE_X_FORWARDED_HOST = False

ALLOWED_HOSTS = ["*", "testserver", "acme.localhost", "beta.localhost", "oth.localhost", "gamma.localhost"]

# Configuração do REST Framework para testes
REST_FRAMEWORK.update({
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "EXCEPTION_HANDLER": "core.api.problem_details.exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "core.api.renderers.EnvelopedJSONRenderer",
    ],
    "DEFAULT_PAGINATION_CLASS": "core.api.pagination.EnvelopedPageNumberPagination",
    "PAGE_SIZE": 20,
})

# Throttling para testes
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
    "rest_framework.throttling.AnonRateThrottle",
    "rest_framework.throttling.UserRateThrottle",
]
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "5/minute",
    "user": "60/minute",
    "login": "3/minute",  # usado por throttle custom de login
}
