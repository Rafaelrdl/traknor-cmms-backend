"""Configuração da aplicação core."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configurações da app core."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
