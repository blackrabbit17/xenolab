from django.test import TestCase, Client
from django.urls import reverse
from sunlight.models import Sunlight
from wind.models import Wind
from temphumidity.models import TempHumidityReading


class APIEndpointTests(TestCase):
    """Test suite for API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample sunlight data
        Sunlight.objects.create(
            status=Sunlight.STATUS_SUNLIGHT_ON,
            r=0.8,
            g=0.6,
            b=0.4,
            brightness=0.7
        )
        
        # Create sample wind data
        Wind.objects.create(
            status=Wind.STATUS_WIND_ON,
            speed=1.5
        )
        
        # Create sample temperature/humidity data
        TempHumidityReading.objects.create(
            temperature=25.5,
            humidity=68.7
        )
        
        # Set up the test client
        self.client = Client()
    
    def test_wind_endpoint(self):
        """Test the wind endpoint"""
        response = self.client.get(reverse('wind_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertTrue('timestamp' in data[0])
        self.assertTrue('status' in data[0])
    
    def test_sunlight_endpoint(self):
        """Test the sunlight endpoint"""
        response = self.client.get(reverse('sunlight_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertTrue('timestamp' in data[0])
        self.assertTrue('r' in data[0])
        self.assertTrue('g' in data[0])
        self.assertTrue('b' in data[0])
        self.assertTrue('brightness' in data[0])
        self.assertTrue('status' in data[0])
    
    def test_temphumidity_endpoint(self):
        """Test the temperature/humidity endpoint"""
        response = self.client.get(reverse('temphumidity_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        self.assertTrue('timestamp' in data[0])
        self.assertTrue('temperature' in data[0])
        self.assertTrue('humidity' in data[0])
    
    def test_lifeform_endpoint(self):
        """Test the lifeform endpoint with different types"""
        # Test venus type
        response = self.client.get(reverse('get_lifeform_data') + '?type=venus')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['lifeform'], 'DIONAEA MUSCIPULA')
        
        # Test pitcher type
        response = self.client.get(reverse('get_lifeform_data') + '?type=pitcher')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['lifeform'], 'HELIAMPHORA FOLLICULATA')
        
        # Test sundew type
        response = self.client.get(reverse('get_lifeform_data') + '?type=sundew')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['lifeform'], 'DROSERA SNYDERRI')
    
    def test_map_endpoint(self):
        """Test the map endpoint"""
        response = self.client.get(reverse('map_png') + '?type=venus')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
    
    def test_atmospherics_endpoint(self):
        """Test the atmospherics endpoint"""
        response = self.client.get(reverse('get_atmospherics'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue('sunlight' in data)
        self.assertTrue('wind' in data)
        self.assertEqual(data['sunlight']['status'], 1)  # ON from our test data
        self.assertEqual(data['wind']['status'], 1)  # ON from our test data