from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

class BaseViewTests(TestCase):
    def test_algus_view(self):
        time_start = datetime.now()
        response = self.client.get(reverse('index'))
        time_stopp = datetime.now() - time_start
        self.assertEqual(response.status_code, 200)
        self.assertTrue(time_stopp.seconds < 3)

    def test_info_view(self):
        time_start = datetime.now()
        response = self.client.get(reverse('sandbox'))
        time_stopp = datetime.now() - time_start
        self.assertEqual(response.status_code, 200)
        self.assertTrue(time_stopp.seconds < 3)
