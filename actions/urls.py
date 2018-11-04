from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from actions.views import (
    PublishView, PostView, MessageActionsView, MessageOptionsView
)

urlpatterns = [
    path('publish/', PublishView.as_view()),
    path('post/', PostView.as_view()),
    path('message-actions/', MessageActionsView.as_view()),
    path('message-options/', MessageOptionsView.as_view()),
]
