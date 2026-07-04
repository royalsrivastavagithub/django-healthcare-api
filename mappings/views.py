from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mappings.models import PatientDoctorMapping
from mappings.serializers import MappingSerializer


class MappingViewSet(viewsets.ModelViewSet):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']

    def retrieve(self, request, pk=None):
        mappings = self.get_queryset().filter(patient_id=pk).select_related('patient', 'doctor')
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)
