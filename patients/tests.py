from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from patients.models import Patient


class PatientTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='pat@test.com', name='Patient Owner', password='testpass123')
        resp = self.client.post('/api/auth/login/', {'email': 'pat@test.com', 'password': 'testpass123'}, format='json')
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def _create_patient(self, **overrides):
        data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male',
            'contact_number': '1234567890',
            'address': '123 Main St',
            'medical_history': 'None',
        }
        data.update(overrides)
        return self.client.post('/api/patients/', data, format='json')

    def test_create_patient_success(self):
        resp = self._create_patient()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], 'John Doe')
        self.assertEqual(resp.data['age'], 30)

    def test_create_patient_unauthenticated(self):
        self.client.credentials()
        resp = self._create_patient()
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_own_patients(self):
        self._create_patient(name='Patient A')
        self._create_patient(name='Patient B')
        resp = self.client.get('/api/patients/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_list_only_own_patients(self):
        self._create_patient(name='Mine')
        other = User.objects.create_user(email='other@test.com', name='Other', password='testpass123')
        Patient.objects.create(user=other, name='Theirs', age=40, gender='Female', contact_number='0', address='Elsewhere')
        resp = self.client.get('/api/patients/', format='json')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['name'], 'Mine')

    def test_get_patient_detail(self):
        create_resp = self._create_patient()
        pid = create_resp.data['id']
        resp = self.client.get(f'/api/patients/{pid}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'John Doe')

    def test_get_other_users_patient_returns_404(self):
        other = User.objects.create_user(email='other2@test.com', name='Other', password='testpass123')
        other_patient = Patient.objects.create(user=other, name='Theirs', age=40, gender='Female', contact_number='0', address='Elsewhere')
        resp = self.client.get(f'/api/patients/{other_patient.id}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_patient(self):
        create_resp = self._create_patient()
        pid = create_resp.data['id']
        resp = self.client.put(f'/api/patients/{pid}/', {
            'name': 'Updated Name', 'age': 35, 'gender': 'Male',
            'contact_number': '0987654321', 'address': 'New Address', 'medical_history': 'Updated'
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Updated Name')

    def test_delete_patient(self):
        create_resp = self._create_patient()
        pid = create_resp.data['id']
        resp = self.client.delete(f'/api/patients/{pid}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(id=pid).exists())

    def test_delete_other_users_patient_returns_404(self):
        other = User.objects.create_user(email='other3@test.com', name='Other', password='testpass123')
        other_patient = Patient.objects.create(user=other, name='Theirs', age=40, gender='Female', contact_number='0', address='Elsewhere')
        resp = self.client.delete(f'/api/patients/{other_patient.id}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_validate_age_range(self):
        resp = self._create_patient(age=-1)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp = self._create_patient(age=151)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_gender(self):
        resp = self._create_patient(gender='Alien')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_contact_number(self):
        resp = self._create_patient(contact_number='abc')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
