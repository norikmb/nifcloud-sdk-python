"""NIFCLOUD session management with custom SSL context and user agent."""

import ssl

from botocore import __version__ as botocore_version
from botocore import session
from botocore.session import get_session  # noqa: F401

import nifcloud

# for ncl4lb
extra_ciphers = "AES256-SHA256"

ssl_context = ssl.create_default_context()
default_ciphers = ssl_context.get_ciphers()
default_cipher_names = ":".join(c["name"] for c in default_ciphers)
ssl_context.set_ciphers(f"{default_cipher_names}:{extra_ciphers}")


class Session(session.Session):
    """NIFCLOUD session extending botocore.session.Session.

    Configures NIFCLOUD-specific user agent and SSL context for API calls.
    The SSL context includes additional ciphers required by NIFCLOUD services.
    """

    def __init__(self, session_vars=None, event_hooks=None, include_builtin_handlers=True, profile=None):
        """Initialize NIFCLOUD session.

        Args:
            session_vars: Optional session variables dictionary.
            event_hooks: Optional event hooks dictionary.
            include_builtin_handlers: Whether to include built-in event handlers.
            profile: Optional AWS profile name.

        """
        super().__init__(session_vars, event_hooks, include_builtin_handlers, profile)
        self.user_agent_name = "nifcloud"
        self.user_agent_version = nifcloud.__version__
        self.user_agent_extra = f"botocore/{botocore_version}"

    def create_client(
        self,
        service_name,
        region_name=None,
        api_version=None,
        use_ssl=True,
        verify=None,
        endpoint_url=None,
        nifcloud_access_key_id=None,
        nifcloud_secret_access_key=None,
        nifcloud_session_token=None,
        config=None,
    ):
        """Create a NIFCLOUD service client.

        Parameters match AWS SDK but with 'nifcloud_' prefix for credentials.

        Args:
            service_name: The service name (e.g., 'computing', 'rdb').
            region_name: The region name.
            api_version: Optional API version.
            use_ssl: Whether to use SSL (default: True).
            verify: SSL certificate verification (True/False/path).
            endpoint_url: Optional custom endpoint URL.
            nifcloud_access_key_id: NIFCLOUD access key ID.
            nifcloud_secret_access_key: NIFCLOUD secret access key.
            nifcloud_session_token: Optional session token.
            config: Optional client configuration.

        Returns:
            A configured NIFCLOUD service client.

        """
        client = super().create_client(
            service_name,
            region_name=region_name,
            api_version=api_version,
            use_ssl=use_ssl,
            verify=verify,
            endpoint_url=endpoint_url,
            aws_access_key_id=nifcloud_access_key_id,
            aws_secret_access_key=nifcloud_secret_access_key,
            aws_session_token=nifcloud_session_token,
            config=config,
        )

        http_session = client._endpoint.http_session
        if hasattr(http_session, "_manager"):
            http_session._manager.connection_pool_kw["ssl_context"] = ssl_context

        return client


session.Session = Session
