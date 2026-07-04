from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping
from patients.models import Patient


class MappingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='map@test.com', name='Mapping User', password='testpass123')
        resp = self.client.post('/api/auth/login/', {'email': 'map@test.com', 'password': 'testpass123'}, format='json')
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.patient = Patient.objects.create(
            user=self.user, name='Test Patient', age=25, gender='Male',
            contact_number='1234567890', address='Addr'
        )
        self.doctor = Doctor.objects.create(
            created_by=self.user, name='Dr. Test', specialization='General',
            contact_number='0987654321', email='dr@test.com', years_of_experience=5
        )

    def test_create_mapping_success(self):
        resp = self.client.post('/api/mappings/', {
            'patient': self.patient.id, 'doctor': self.doctor.id
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn('patient_name', resp.data)
        self.assertIn('doctor_name', resp.data)

    def test_create_mapping_unauthenticated(self):
        self.client.credentials()
        resp = self.client.post('/api/mappings/', {
            'patient': self.patient.id, 'doctor': self.doctor.id
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_duplicate_mapping(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        resp = self.client.post('/api/mappings/', {
            'patient': self.patient.id, 'doctor': self.doctor.id
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_mappings(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        resp = self.client.get('/api/mappings/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_get_mappings_by_patient(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        resp = self.client.get(f'/api/mappings/{self.patient.id}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['patient'], self.patient.id)

    def test_get_mappings_by_patient_empty(self):
        resp = self.client.get(f'/api/mappings/{self.patient.id}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 0)

    def test_delete_mapping(self):
        mapping = PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor)
        resp = self.client.delete(f'/api/mappings/{mapping.id}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PatientDoctorMapping.objects.filter(id=mapping.id).exists())

    def test_delete_nonexistent_mapping(self):
        resp = self.client.delete('/api/mappings/999/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
