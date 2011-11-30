"""A thin layer for the django cache interface to specify cache zones.

Django cache does not offer the functionality to purge a group ('zone') of
cached objects. This module prefixes all keys for the items within one zone
with a zone key. If the zone should be invalidated then the zone key
is incremented.

All actions take two cache lookups, one for the zone key and one for the
actual value.


TODO: all references of `group` should be renamed to `zone`.

"""
from django.core.cache import cache


def add(key, value, timeout=None, version=None, group=None):
    key, version = make_group_key(key, version, group)
    return cache.add(key, value, timeout, version=version)


def get(key, default=None, version=None, group=None):
    key, version = make_group_key(key, version, group)
    return cache.get(key, default, version)


def set(key, value, timeout=None, version=None, group=None, refreshed=False):
    key, version = make_group_key(key, version, group)
    return cache.set(key, value, timeout, version)


def delete(key, version=None, group=None):
    key, version = make_group_key(key, version, group)
    return cache.delete(key, version)


def invalidate_group(group):
    """ Invalidates all cache keys belonging to group """
    key, version = _group_metadata(group)
    try:
        cache.incr(key)
    except ValueError:
        cache.add(key, version)
        cache.incr(key)


def make_group_key(key, version=None, group=None):
    """Create the unique zone key"""
    if group:
        group_key, group_version = _group_metadata(group, version)
        if version:
            key = '%d:%s' % (version, key)
        key = '%s:%s' % (group, key)
        return key, group_version
    return key, version


def _group_metadata(group, version=None):
    """ This can be useful sometimes if you're doing a very large number
        of operations and you want to avoid all of the extra cache hits.
    """
    group_key = '_:group_version::%s' % group
    if version:
        group_key += ':%d' % version
    group_version = cache.get(group_key, default=1)
    return group_key, group_version
