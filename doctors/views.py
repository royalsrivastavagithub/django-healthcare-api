from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from doctors.models import Doctor
from doctors.permissions import IsCreator
from doctors.serializers import DoctorSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
