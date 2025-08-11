from enum import Enum


class Role(str, Enum):
    """Enum simples com os papéis suportados pelo sistema."""

    ADMIN = "admin"
    TECHNICIAN = "technician"
    REQUESTER = "requester"


ROLE_CHOICES = [(role.value, role.value) for role in Role]
