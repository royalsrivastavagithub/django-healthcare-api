from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from doctors.models import Doctor


class DoctorTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='doc1@test.com', name='Doctor Creator', password='testpass123')
        self.user2 = User.objects.create_user(email='doc2@test.com', name='Other User', password='testpass123')

        resp = self.client.post('/api/auth/login/', {'email': 'doc1@test.com', 'password': 'testpass123'}, format='json')
        self.token1 = resp.data['access']

        resp = self.client.post('/api/auth/login/', {'email': 'doc2@test.com', 'password': 'testpass123'}, format='json')
        self.token2 = resp.data['access']

    def _create_doctor(self, client=None, **overrides):
        if client is None:
            client = self.client
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        data = {
            'name': 'Dr. Smith',
            'specialization': 'Cardiology',
            'contact_number': '1112223333',
            'email': 'smith@hospital.com',
            'years_of_experience': 10,
        }
        data.update(overrides)
        return client.post('/api/doctors/', data, format='json')

    def test_create_doctor_success(self):
        resp = self._create_doctor()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['name'], 'Dr. Smith')

    def test_create_doctor_unauthenticated(self):
        self.client.credentials()
        resp = self.client.post('/api/doctors/', {
            'name': 'Dr. NoAuth', 'specialization': 'Cardiology',
            'contact_number': '1112223333', 'email': 'no@auth.com',
            'years_of_experience': 10
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_all_doctors(self):
        self._create_doctor(name='Dr. A')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        self._create_doctor(name='Dr. B')
        resp = self.client.get('/api/doctors/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_get_doctor_detail(self):
        create_resp = self._create_doctor()
        did = create_resp.data['id']
        resp = self.client.get(f'/api/doctors/{did}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_own_doctor(self):
        create_resp = self._create_doctor()
        did = create_resp.data['id']
        resp = self.client.put(f'/api/doctors/{did}/', {
            'name': 'Dr. Updated', 'specialization': 'Cardiology',
            'contact_number': '1112223333', 'email': 'smith@hospital.com',
            'years_of_experience': 15
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Dr. Updated')

    def test_update_other_users_doctor_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        create_resp = self._create_doctor()
        did = create_resp.data['id']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        resp = self.client.put(f'/api/doctors/{did}/', {
            'name': 'Dr. Hacked', 'specialization': 'Cardiology',
            'contact_number': '1112223333', 'email': 'smith@hospital.com',
            'years_of_experience': 15
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_doctor(self):
        create_resp = self._create_doctor()
        did = create_resp.data['id']
        resp = self.client.delete(f'/api/doctors/{did}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(id=did).exists())

    def test_delete_other_users_doctor_returns_403(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')
        create_resp = self._create_doctor()
        did = create_resp.data['id']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        resp = self.client.delete(f'/api/doctors/{did}/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_validate_years_of_experience(self):
        resp = self._create_doctor(years_of_experience=-1)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp = self._create_doctor(years_of_experience=71)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_contact_number(self):
        resp = self._create_doctor(contact_number='abc')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
