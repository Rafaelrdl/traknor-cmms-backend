"""Configurações principais do projeto Django."""

from pathlib import Path
import environ

# Diretórios base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent  # src
ROOT_DIR = BASE_DIR.parent  # backend

# Carrega variáveis de ambiente do arquivo .env, se existir
env = environ.Env(
    DEBUG=(bool, False),
)
if (ROOT_DIR / ".env").exists():
    environ.Env.read_env(ROOT_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Configurações do banco de dados utilizando DATABASE_URL
DATABASES = {
    "default": env.db_url("DATABASE_URL", default="sqlite:///db.sqlite3")
}

# Aplicativos instalados
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "core",
]

# Middlewares padrão e WhiteNoise para servir estáticos
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

# Configurações do DRF
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

# Configurações do drf-spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "TrakNor API",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Configurações de arquivos estáticos
STATIC_URL = "/static/"
STATIC_ROOT = ROOT_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Localização
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
