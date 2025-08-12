"""
Renderer que envelopa responses em formato padronizado
"""
from typing import Any
from rest_framework.renderers import JSONRenderer


class EnvelopedJSONRenderer(JSONRenderer):
    """
    Renderer que envelopa dados em formato {data, meta, links}
    """
    media_type = "application/json"
    charset = "utf-8"
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context:
            return super().render(data, accepted_media_type, renderer_context)
            
        resp = renderer_context["response"]
        status_code = resp.status_code
        
        # Se for erro 4xx/5xx, não envelopa (deve usar Problem Details)
        if status_code >= 400:
            return super().render(data, accepted_media_type, renderer_context)
        
        # Se já for problem+json, não envelopa
        if (resp.get("Content-Type") == "application/problem+json" or 
            (isinstance(data, dict) and {"title", "status", "detail"} <= set(data.keys()))):
            return super().render(data, accepted_media_type, renderer_context)
        
        # Envelopar detail/create/retrieve
        if isinstance(data, dict) and "results" not in data and "count" not in data:
            data = {"data": data}
        
        # Paginação DRF -> meta/links
        if isinstance(data, dict) and "results" in data:
            results = data.pop("results")
            meta = {
                "page": data.get("page", 1),
                "size": data.get("page_size", None),
                "total": data.get("count", None),
            }
            links = {k: v for k, v in data.items() if k in {"next", "previous", "self"}}
            data = {"data": results, "meta": meta, "links": links}
        
        return super().render(data, accepted_media_type, renderer_context)


# Manter compatibilidade com nome antigo
EnvelopeJSONRenderer = EnvelopedJSONRenderer
