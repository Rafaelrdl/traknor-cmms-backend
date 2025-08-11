from __future__ import annotations

from uuid import uuid4
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """Modelo base com campos comuns.

    Inclui chave primária UUID e timestamps de criação e atualização.
    Também fornece suporte simples a *soft delete* através dos campos
    ``is_deleted`` e ``deleted_at``.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Marca o registro como removido sem apagá-lo do banco."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])


class Company(BaseModel):
    """Representa uma empresa dentro do tenant."""

    STATUS_CHOICES = [
        ("active", "active"),
        ("inactive", "inactive"),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - representação simples
        return self.name


class Sector(BaseModel):
    """Setor pertencente a uma :class:`Company`."""

    STATUS_CHOICES = Company.STATUS_CHOICES

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="sectors")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [
            models.Index(fields=["company", "name"]),
            models.Index(fields=["company", "code"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="uniq_sector_code",
                condition=models.Q(code__isnull=False),
            )
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.company} / {self.name}"


class Subsection(BaseModel):
    """Subseção dentro de um :class:`Sector`."""

    STATUS_CHOICES = Company.STATUS_CHOICES

    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="subsections")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        indexes = [
            models.Index(fields=["sector", "name"]),
            models.Index(fields=["sector", "code"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["sector", "code"],
                name="uniq_subsection_code",
                condition=models.Q(code__isnull=False),
            )
        ]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.sector} / {self.name}"


class Asset(BaseModel):
    """Recurso físico instalado em um local específico."""

    TYPE_CHOICES = [
        ("ahu", "ahu"),
        ("chiller", "chiller"),
        ("split", "split"),
        ("vrf", "vrf"),
        ("fan_coil", "fan_coil"),
        ("cooling_tower", "cooling_tower"),
        ("pump", "pump"),
        ("boiler", "boiler"),
        ("other", "other"),
    ]
    STATUS_CHOICES = [
        ("active", "active"),
        ("in_maintenance", "in_maintenance"),
        ("down", "down"),
        ("decommissioned", "decommissioned"),
    ]
    CRITICALITY_CHOICES = [
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="assets")
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="assets")
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name="assets")

    code = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    brand = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    install_date = models.DateField(null=True, blank=True)
    maintenance_due_at = models.DateField(null=True, blank=True)
    criticality = models.CharField(
        max_length=10, choices=CRITICALITY_CHOICES, default="low"
    )
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["company", "sector", "subsection"]),
            models.Index(fields=["maintenance_due_at"]),
        ]

    def __str__(self) -> str:  # pragma: no cover
        return self.code
