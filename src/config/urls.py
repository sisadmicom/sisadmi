#config/urls
"""
URL configuration for config project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("core/", include("core.urls")),
    path('chaining/', include('smart_selects.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Added JWT auth and company context endpoints
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
try:
    from users.api.views import SelectCompanyAPIView, ContextAPIView
except Exception:
    # In case import path differs, avoid crash; user should adapt import if necessary
    SelectCompanyAPIView = None
    ContextAPIView = None

urlpatterns += [
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/select-company/', SelectCompanyAPIView.as_view(), name='select_company'),
    path('api/auth/context/', ContextAPIView.as_view(), name='auth_context'),
]


# Memberships API
from users.api.views import MembershipViewSet
membership_list = MembershipViewSet.as_view({'get': 'list', 'post': 'create'})
membership_detail = MembershipViewSet.as_view({'delete': 'destroy'})

urlpatterns += [
    path('api/memberships/', membership_list, name='memberships-list'),
    path('api/memberships/<int:pk>/', membership_detail, name='memberships-detail'),
]


# config/urls.py
from core.views import test_context

urlpatterns += [
    path("api/test-context/", test_context),
    path("core/", include("core.urls")),
]

