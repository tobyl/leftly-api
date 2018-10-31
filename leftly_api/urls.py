from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from events.views import Events
from posts.views import PostViewSet

admin.autodiscover()

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('events/', Events.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
