from unittest import TestCase
from mock import patch
import throttle


class TestPrioritizer(TestCase):
    def setUp(self):
        self.app = throttle.app.test_client()


