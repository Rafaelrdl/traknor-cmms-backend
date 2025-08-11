from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .links import build_link_header, update_query_params


@dataclass
class PaginationMeta:
    """Estrutura auxiliar para montar o bloco ``meta``."""

    page: int
    per_page: int
    total_pages: int
    total_items: int


class EnvelopePageNumberPagination(PageNumberPagination):
    """Paginação que segue o padrão de envelope e adiciona headers."""

    page_query_param = "page"
    page_size_query_param = "per_page"
    max_page_size = 100

    def get_paginated_response(self, data: list[Any]) -> Response:
        meta = PaginationMeta(
            page=self.page.number,
            per_page=self.page.paginator.per_page,
            total_pages=self.page.paginator.num_pages,
            total_items=self.page.paginator.count,
        )

        links = self._build_links(meta)

        body: Dict[str, Any] = {
            "data": data,
            "meta": meta.__dict__,
            "links": links,
        }

        response = Response(body)
        self._set_pagination_headers(response, meta, links)
        return response

    # Métodos auxiliares -------------------------------------------------
    def _build_links(self, meta: PaginationMeta) -> Dict[str, str]:
        """Gera os links absolutos para o corpo e para o header Link."""
        request = self.request
        base_url = request.build_absolute_uri()

        def page_url(number: int) -> str:
            return update_query_params(
                base_url,
                page=number,
                per_page=meta.per_page,
            )

        links: Dict[str, str | None] = {
            "self": page_url(meta.page),
            "first": page_url(1),
            "prev": page_url(meta.page - 1) if self.page.has_previous() else None,
            "next": page_url(meta.page + 1) if self.page.has_next() else None,
            "last": page_url(meta.total_pages),
        }
        # Remove entradas None
        return {k: v for k, v in links.items() if v is not None}

    def _set_pagination_headers(self, response: Response, meta: PaginationMeta, links: Dict[str, str]) -> None:
        """Adiciona headers X-Total-* e Link na resposta."""
        response["X-Total-Count"] = str(meta.total_items)
        response["X-Total-Pages"] = str(meta.total_pages)
        response["X-Per-Page"] = str(meta.per_page)
        response["X-Current-Page"] = str(meta.page)
        response["Link"] = build_link_header({k: links.get(k) for k in ["first", "prev", "next", "last"]})
