from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet

admin.autodiscover()

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include('rest_framework.urls')),
]
