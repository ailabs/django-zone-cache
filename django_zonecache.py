"""A thin layer for the django cache interface to specify cache zones.

Django cache does not offer the functionality to purge a zone ('group') of
cached objects. This module prefixes all keys for the items within one zone
with a zone key. If the zone should be invalidated then the zone key
is incremented.

All actions take two cache lookups, one for the zone key and one for the
actual value.

"""
from django.core.cache import cache


def add(key, value, timeout=None, version=None, zone=None):
    key, version = make_zone_key(key, version, zone)
    return cache.add(key, value, timeout, version=version)


def get(key, default=None, version=None, zone=None):
    key, version = make_zone_key(key, version, zone)
    return cache.get(key, default, version)


def set(key, value, timeout=None, version=None, zone=None, refreshed=False):
    key, version = make_zone_key(key, version, zone)
    return cache.set(key, value, timeout, version)


def delete(key, version=None, zone=None):
    key, version = make_zone_key(key, version, zone)
    return cache.delete(key, version)


def invalidate_zone(zone):
    """ Invalidates all cache keys belonging to zone """
    key, version = _zone_metadata(zone)
    try:
        cache.incr(key)
    except ValueError:
        cache.add(key, version)
        cache.incr(key)


def make_zone_key(key, version=None, zone=None):
    """Create the unique zone key"""
    if zone:
        zone_key, zone_version = _zone_metadata(zone, version)
        if version:
            key = '%d:%s' % (version, key)
        key = '%s:%s' % (zone, key)
        return key, zone_version
    return key, version


def _zone_metadata(zone, version=None):
    """ This can be useful sometimes if you're doing a very large number
        of operations and you want to avoid all of the extra cache hits.
    """
    zone_key = '_:zone_version::%s' % zone
    if version:
        zone_key += ':%d' % version
    zone_version = cache.get(zone_key, default=1)
    return zone_key, zone_version
