from __future__ import annotations

from typing import Any, Dict, List

from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

PROBLEM_BASE = "https://traknor.dev/problems/"


def _build_validation_errors(detail: Any) -> List[Dict[str, str]]:
    """Normaliza o payload de ValidationError em uma lista de erros."""
    errors: List[Dict[str, str]] = []
    if isinstance(detail, dict):
        for field, messages in detail.items():
            if isinstance(messages, (list, tuple)):
                for msg in messages:
                    errors.append({"name": field, "reason": str(msg)})
            else:
                errors.append({"name": field, "reason": str(messages)})
    elif isinstance(detail, list):
        for msg in detail:
            errors.append({"name": "non_field_errors", "reason": str(msg)})
    else:
        errors.append({"name": "non_field_errors", "reason": str(detail)})
    return errors


PROBLEM_TYPE_MAP = {
    status.HTTP_400_BAD_REQUEST: PROBLEM_BASE + "bad-request",
    status.HTTP_401_UNAUTHORIZED: PROBLEM_BASE + "unauthorized",
    status.HTTP_403_FORBIDDEN: PROBLEM_BASE + "forbidden",
    status.HTTP_404_NOT_FOUND: PROBLEM_BASE + "not-found",
    status.HTTP_409_CONFLICT: PROBLEM_BASE + "conflict",
    status.HTTP_422_UNPROCESSABLE_ENTITY: PROBLEM_BASE + "validation-error",
    status.HTTP_500_INTERNAL_SERVER_ERROR: PROBLEM_BASE + "internal-error",
}


def problem_exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """Transforma exceções em respostas Problem Details."""
    request = context.get("request")

    if isinstance(exc, exceptions.ValidationError):
        errors = _build_validation_errors(exc.detail)
        data = {
            "type": PROBLEM_TYPE_MAP[status.HTTP_422_UNPROCESSABLE_ENTITY],
            "title": "Validation Error",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": "There were validation errors",
            "instance": request.get_full_path() if request else "",
            "errors": errors,
        }
        response = Response(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        response = drf_exception_handler(exc, context)
        status_code = response.status_code if response else status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = getattr(exc, "detail", str(exc))
        if isinstance(detail, (list, dict)):
            detail = str(detail)
        data = {
            "type": PROBLEM_TYPE_MAP.get(status_code, "about:blank"),
            "title": status.HTTP_STATUS_CODES.get(status_code, "Error"),
            "status": status_code,
            "detail": detail,
            "instance": request.get_full_path() if request else "",
        }
        if response is None:
            response = Response(data, status=status_code)
        else:
            response.data = data

    response["Content-Type"] = "application/problem+json"
    return response
