A thin layer for the django cache interface to specify cache zones.

Django cache does not offer the functionality to purge a zone ('group') of
cached objects. This module prefixes all keys for the items within one zone
with a zone key. If the zone should be invalidated then the zone key
is incremented.

All actions take two cache lookups, one for the zone key and one for the
actual value.
