"""Views e rotas para gerenciamento de empresas e ativos."""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from core.mixins import RoleRequiredMixin, TenantScopedMixin

from .models import Asset, Company
from .serializers import AssetSerializer, CompanySerializer


class CompanyViewSet(RoleRequiredMixin, TenantScopedMixin, viewsets.ModelViewSet):
    """CRUD básico para o modelo :class:`Company`."""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class AssetViewSet(RoleRequiredMixin, TenantScopedMixin, viewsets.ModelViewSet):
    """CRUD de ativos com suporte mínimo a filtros."""

    queryset = Asset.objects.all().select_related(
        "company", "sector", "subsection"
    )
    serializer_class = AssetSerializer
    filterset_fields = [
        "type",
        "status",
        "brand",
        "model",
        "company",
        "sector",
        "subsection",
    ]
    search_fields = ["code", "brand", "model", "serial_number"]

    @action(detail=True, methods=["get"])
    def utilization(self, request, pk=None):
        """Retorna métricas simples de utilização do ativo.

        Neste MVP os valores são simulados apenas para demonstrar o
        formato esperado pelo front-end.
        """

        data = {
            "series": [],
            "indicators": {
                "avg": 0,
                "min": 0,
                "max": 0,
                "uptime_hours": 0,
                "downtime_hours": 0,
                "observations": 0,
            },
        }
        return Response({"data": data})


class LocationTreeView(APIView):
    """Retorna a árvore Company → Sector → Subsection com contagem de ativos."""

    def get(self, request):
        company_id = request.query_params.get("company_id")
        sector_id = request.query_params.get("sector_id")

        companies = Company.objects.all()
        if company_id:
            companies = companies.filter(id=company_id)

        tree = []
        for company in companies:
            sectors = company.sectors.all()
            if sector_id:
                sectors = sectors.filter(id=sector_id)

            company_node = {
                "company": {"id": str(company.id), "name": company.name},
                "equipment_count": company.assets.filter(is_deleted=False).count(),
                "sectors": [],
            }

            for sector in sectors:
                subsections = sector.subsections.all()
                sector_node = {
                    "id": str(sector.id),
                    "name": sector.name,
                    "equipment_count": sector.assets.filter(is_deleted=False).count(),
                    "subsections": [],
                }

                for subsection in subsections:
                    sub_node = {
                        "id": str(subsection.id),
                        "name": subsection.name,
                        "equipment_count": subsection.assets.filter(is_deleted=False).count(),
                    }
                    sector_node["subsections"].append(sub_node)

                company_node["sectors"].append(sector_node)

            tree.append(company_node)

        return Response({"data": tree})
