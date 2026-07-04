from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsOwner
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return Doctor.objects.filter(created_by=self.request.user)
        return Doctor.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
