"""
Router que aceita URLs com ou sem trailing slash
"""
from rest_framework.routers import DefaultRouter


class OptionalSlashRouter(DefaultRouter):
    """Router que aceita tanto /endpoint quanto /endpoint/"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = '/?'  # aceita /endpoint e /endpoint/
