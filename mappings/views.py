from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mappings.models import PatientDoctorMapping
from mappings.serializers import MappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]


class MappingManageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        mappings = PatientDoctorMapping.objects.filter(patient_id=pk).select_related('patient', 'doctor')
        serializer = MappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
