"""NIFCLOUD SDK for Python.

A data-driven SDK for NIFCLOUD APIs compatible with AWS SDK design patterns.
Supports Computing, RDB, NAS, ESS, DNS, ObjectStorageService, ServiceActivity,
DevOps, and DevOps Runner APIs.

Example:
    >>> from nifcloud import session
    >>> client = session.get_session().create_client(
    ...     'computing',
    ...     region_name='jp-east-1',
    ...     nifcloud_access_key_id='YOUR_KEY',
    ...     nifcloud_secret_access_key='YOUR_SECRET'
    ... )
    >>> response = client.describe_instances()

"""

from . import auth, configprovider, credentials, loaders, parsers, serialize, session  # noqa: F401

__version__ = "1.17.0"
