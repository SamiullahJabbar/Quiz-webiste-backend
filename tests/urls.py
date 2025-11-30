# tests/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet,TestSummaryViewSet

router = DefaultRouter()
router.register(r'tests', TestViewSet, basename='tests')
router.register(r'test-summary', TestSummaryViewSet, basename='test-summary')

urlpatterns = [
    path('', include(router.urls)),
]
