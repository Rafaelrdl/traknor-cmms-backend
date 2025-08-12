from django.contrib import admin
from django.urls import path, include
from core.api.routers import OptionalSlashRouter
from core.api.throttling import LoginRateThrottle, AnonymousRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView

from .views import health, trigger_error
from sample.api import ExampleViewSet
from sample.rbac_api import ExampleRBACViewSet
from django.conf import settings
from accounts.api import MeView


class ThrottledLoginView(APIView):
    throttle_classes = [LoginRateThrottle]
    permission_classes = []
    authentication_classes = []
    
    def post(self, request):
        throttle = LoginRateThrottle()
        if not throttle.allow_request(request, self):
            data = {
                "type": "about:blank",
                "title": "Too Many Requests",
                "status": 429,
                "detail": f"Request was throttled. Expected available in {getattr(throttle, 'wait', 60)} seconds."
            }
            return Response(data, status=429, content_type="application/problem+json")
        
        return Response({"detail": "Invalid credentials"}, status=401)


class ThrottledExampleView(APIView):
    throttle_classes = [AnonymousRateThrottle]
    permission_classes = []
    authentication_classes = []
    
    def get(self, request):
        return Response({"message": "success"})


router = OptionalSlashRouter()
router.register("_example", ExampleViewSet, basename="example")
router.register("rbac-examples", ExampleRBACViewSet, basename="rbac-example")

if settings.DEBUG:
    from sandbox.api import ExampleOwnedViewSet
    router.register("sandbox/examples", ExampleOwnedViewSet, basename="sandbox-example")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health, name="health"),
    path("trigger-error", trigger_error, name="trigger-error"),
    path("auth/login", ThrottledLoginView.as_view(), name="auth-login"),
    path("anon-throttle", ThrottledExampleView.as_view(), name="anon-throttle"),
    path("users/me", MeView.as_view(), name="users-me"),
    path("", include(router.urls)),
]
