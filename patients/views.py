from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from patients.models import Patient
from patients.permissions import IsOwner
from patients.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
