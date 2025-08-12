"""
Exception handler que retorna Problem Details (RFC 7807)
"""
from rest_framework.views import exception_handler as drf_handler
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied as DRFPermissionDenied, Throttled
from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response


def _problem(status_code, title, detail, type_="about:blank", extra=None):
    """Cria resposta Problem Details padronizada"""
    data = {"type": type_, "title": title, "status": status_code, "detail": detail}
    if extra: 
        data.update(extra)
    return Response(data, status=status_code, content_type="application/problem+json")


def exception_handler(exc, context):
    """
    Exception handler customizado que retorna Problem Details
    """
    # Throttling (429)
    if isinstance(exc, Throttled):
        response = _problem(429, "Too Many Requests", 
                           f"Request was throttled. Expected available in {exc.wait} seconds.")
        # Força o renderer a não envelopar  
        response["Content-Type"] = "application/problem+json"
        return response
    
    # Validação (422)
    if isinstance(exc, ValidationError):
        response = _problem(422, "Validation Error", "Validation failed", 
                           extra={"errors": exc.detail})
        response["Content-Type"] = "application/problem+json"
        return response
    
    # Not Found (404)
    if isinstance(exc, (NotFound, Http404)):
        response = _problem(404, "Not Found", "Resource not found")
        response["Content-Type"] = "application/problem+json"
        return response
    
    # Permission Denied (403)
    if isinstance(exc, (PermissionDenied, DRFPermissionDenied)):
        response = _problem(403, "Forbidden", 
                           "You do not have permission to perform this action.")
        response["Content-Type"] = "application/problem+json"
        return response
    
    # Delega para DRF handler padrão
    resp = drf_handler(exc, context)
    
    # Se DRF não conseguiu tratar, retorna 500
    if resp is None:
        response = _problem(500, "Internal Server Error", "An unexpected error occurred.")
        response["Content-Type"] = "application/problem+json"
        return response
    
    # Garante content-type problem+json para respostas DRF de erro
    resp["Content-Type"] = "application/problem+json"
    return resp
