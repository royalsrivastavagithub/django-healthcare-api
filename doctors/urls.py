from django.urls import path, include
from rest_framework.routers import DefaultRouter

from doctors.views import DoctorViewSet

router = DefaultRouter()
router.register('', DoctorViewSet, basename='doctors')

urlpatterns = [
    path('', include(router.urls)),
]
