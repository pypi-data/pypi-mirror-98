from django.test import TestCase

from employee_info.models import Resource, Employment, Function
from tests.test_data import TestData

load = TestData()


class ResourceTestCase(TestCase):
    def setUp(self) -> None:
        load.load_test_data()

    def testLoadData(self):
        function = Function.objects.get(value=120)
        self.assertEqual('Administrasjon', function.description)

    def testMainPosition(self):
        resource = Resource.objects.get(resourceId=53453)
        main = resource.main_position()
        self.assertIsInstance(main, Employment)

    def testManages(self):
        resource = Resource.objects.get(resourceId=53453)
        self.assertEqual(resource.manages_list(), [])
