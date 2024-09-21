from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .models import RoadSegment, SpeedReading
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone

class TrafficAPITests(TestCase):
    """
    Unit tests for traffic API.
    ---
    This test suite validates the CRUD operations and permissions for road segments
    and speed readings.
    """
    def setUp(self):
        """
        Setup common test data.
        """
        # Set correct URLs for the tests
        self.segment_url = reverse('traffic_speed-list')
        
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass'
        )
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)

        # Create an anonymous user
        self.anon_user = APIClient()

        # Create a test road segment
        self.segmento = SpeedReading.objects.create(
            long_start=103.9460064,
            lat_start=30.75066046,
            long_end=103.9564943,
            lat_end=30.7450801,
            length=1179.207157,
            speed=31.76904762
        )

    def test_anon_user_can_read(self):
        """
        Test if anonymous users can view road segments.
        ---
        Anonymous users should be able to read road segment data.
        """
        response = self.anon_user.get(self.segment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create(self):
        """
        Test if admins can create road segments.
        ---
        Admin users should be able to create new road segments.
        """
        data = {
            'long_start': 104.0,
            'lat_start': 30.8,
            'long_end': 104.1,
            'lat_end': 30.9,
            'length': 1500,
            'speed': 50
        }
        response = self.admin_client.post(self.segment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_update(self):
        """
        Test if admins can update road segments.
        ---
        Admin users should be able to update road segment data.
        """
        update_url = reverse('traffic_speed-detail', args=[self.segmento.id])
        data = {'speed': 60}
        response = self.admin_client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.segmento.refresh_from_db()
        self.assertEqual(self.segmento.speed, 60)

    def test_admin_can_delete(self):
        """
        Test if admins can delete road segments.
        ---
        Admin users should be able to delete road segments.
        """
        delete_url = reverse('traffic_speed-detail', args=[self.segmento.id])
        response = self.admin_client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_anon_user_cannot_create(self):
        """
        Test if anonymous users are prevented from creating road segments.
        ---
        Anonymous users should not be able to create road segments.
        """
        data = {
            'long_start': 104.0,
            'lat_start': 30.8,
            'long_end': 104.1,
            'lat_end': 30.9,
            'length': 1500,
            'speed': 50
        }
        response = self.anon_user.post(self.segment_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_intensity(self):
        """
        Test filtering road segments by traffic intensity.
        ---
        Admin users should be able to filter road segments by traffic intensity.
        """
        filter_url = f"{self.segment_url}?intensity=média"  # Adjust the filter for intensity
        response = self.admin_client.get(filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(
        item['intensity'] == 'média' for item in response.data
    ))

    def test_total_speed_readings_for_segment(self):
        """
        Test if API returns the total number of speed readings for a segment.
        ---
        Admin users should get the total speed readings associated with a road segment.
        """
        response = self.admin_client.get(reverse('traffic_speed-detail', args=[self.segmento.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_speed_readings', response.data)
        self.assertEqual(response.data['total_speed_readings'], 1)
    
    def test_admin_can_create_speed_reading(self):
        """
        Test if admins can create speed readings.
        ---
        Admin users should be able to create new speed readings.
        """
        speed_reading_data = {
            'road_segment': self.segmento.id,
            'speed': 45,
            'timestamp': timezone.now()
        }
        response = self.admin_client.post(reverse('traffic_speedreading-list'), speed_reading_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
