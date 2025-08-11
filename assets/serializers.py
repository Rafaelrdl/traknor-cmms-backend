"""Serializers para os modelos de ativos e estrutura."""

from rest_framework import serializers

from .models import Asset, Company, Sector, Subsection


class CompanySerializer(serializers.ModelSerializer):
    """Serializa o modelo :class:`Company`."""

    class Meta:
        model = Company
        fields = ["id", "name", "code", "status"]


class SectorSerializer(serializers.ModelSerializer):
    """Serializa o modelo :class:`Sector`."""

    class Meta:
        model = Sector
        fields = ["id", "name", "code", "status", "company"]


class SubsectionSerializer(serializers.ModelSerializer):
    """Serializa o modelo :class:`Subsection`."""

    class Meta:
        model = Subsection
        fields = ["id", "name", "code", "status", "sector"]


class AssetSerializer(serializers.ModelSerializer):
    """Serializa o modelo :class:`Asset`."""

    class Meta:
        model = Asset
        fields = [
            "id",
            "code",
            "type",
            "status",
            "brand",
            "model",
            "company",
            "sector",
            "subsection",
            "install_date",
            "maintenance_due_at",
            "criticality",
            "notes",
        ]
