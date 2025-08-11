from typing import Any

from rest_framework.renderers import JSONRenderer


class EnvelopeJSONRenderer(JSONRenderer):
    """Renderer que insere as respostas dentro de um envelope padronizado."""

    media_type = "application/json"
    format = "json"

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: dict | None = None,
    ) -> bytes:
        """Garante que respostas de sucesso estejam dentro de ``data``."""
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")

        # Em caso de erro, o handler já monta o Problem Details
        if response is not None and response.status_code < 400:
            if data is None:
                data = {}
            if not (isinstance(data, dict) and "data" in data):
                # Envolve o payload simples no envelope padronizado
                data = {"data": data}

        return super().render(data, accepted_media_type, renderer_context)
