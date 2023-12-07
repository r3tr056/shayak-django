
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DocumentViewSet,
    DocumentContentViewSet,
    DocumentSearchView
)

router = DefaultRouter()

router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'documentcontents', DocumentContentViewSet, basename='documentcontent')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', DocumentSearchView.as_view(), name='document-search'),
]