"""
Throttling customizado para diferentes endpoints
"""
from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle


class LoginRateThrottle(SimpleRateThrottle):
    """Rate limiting específico para login"""
    scope = "login"
    
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class AnonymousRateThrottle(AnonRateThrottle):
    """Rate limiting para usuários anônimos"""
    scope = "anon"
