"""
URL configuration for traknor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import LoginView, health, trigger_error
from sample.api import ExampleViewSet
from django.conf import settings

router = SimpleRouter()
router.register("_example", ExampleViewSet, basename="example")

if settings.DEBUG:
    from sandbox.api import ExampleOwnedViewSet

    router.register("sandbox/examples", ExampleOwnedViewSet, basename="sandbox-example")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health, name="health"),
    path("_error", trigger_error, name="_error"),
    path("auth/login", LoginView.as_view(), name="auth-login"),
]

urlpatterns += router.urls
