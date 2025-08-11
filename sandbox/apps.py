from django.apps import AppConfig


class SandboxConfig(AppConfig):
    """Configuração do app de sandbox."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "sandbox"
