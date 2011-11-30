from django.utils.unittest import TestCase, TestSuite, makeSuite
from django.conf import settings

settings.configure(DEBUG=False, TEMPLATE_DEBUG=False)

import django_zonecache as zonecache


class ZoneCacheTest(TestCase):

    def test_non_zones(self):
        res = zonecache.add('my_key', 'my_value')
        self.assertTrue(res)
        cached_value = zonecache.get('my_key')
        self.assertEqual(cached_value, 'my_value')

        zonecache.delete('my_key')
        cached_value = zonecache.get('my_key')
        self.assertEqual(cached_value, None)

        res = zonecache.add('my_key', 'my_value')
        self.assertTrue(res)
        cached_value = zonecache.get('my_key')
        self.assertEqual(cached_value, 'my_value')

    def test_zones(self):
        zonecache.add('my_key', 'my_value', zone='my_zone')
        cached_value = zonecache.get('my_key', zone='my_zone')
        self.assertEqual(cached_value, 'my_value')

        zonecache.invalidate_zone('my_zone')
        cached_value = zonecache.get('my_key', zone='my_zone')
        self.assertEqual(cached_value, None)

        zonecache.add('my_key', 'my_value', zone='my_zone')
        cached_value = zonecache.get('my_key', zone='my_zone')
        self.assertEqual(cached_value, 'my_value')

    def test_zone_version(self):
        zonecache.invalidate_zone('my_zone')

        zonecache.add('my_key', 'my_value', version=2, zone='my_zone')
        zonecache.add('my_key', 'my_value_2', version=3, zone='my_zone')

        cached_value = zonecache.get('my_key', version=2, zone='my_zone')
        self.assertEqual(cached_value, 'my_value')

        cached_value = zonecache.get('my_key', version=3, zone='my_zone')
        self.assertEqual(cached_value, 'my_value_2')


suite = TestSuite()
suite.addTest(makeSuite(ZoneCacheTest))
