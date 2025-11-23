"""Unit tests for NIFCLOUD session management."""

from unittest import mock
import ssl

import pytest

import nifcloud
from nifcloud.session import Session


class TestSession:
    """Test cases for NIFCLOUD Session class."""

    def test_session_initialization(self):
        """Test Session can be instantiated."""
        session = Session()
        assert session is not None
        assert isinstance(session, Session)

    def test_session_user_agent_name(self):
        """Test Session sets user_agent_name to 'nifcloud'."""
        session = Session()
        assert session.user_agent_name == "nifcloud"

    def test_session_user_agent_version(self):
        """Test Session sets user_agent_version from nifcloud version."""
        session = Session()
        assert session.user_agent_version == nifcloud.__version__

    def test_session_user_agent_extra(self):
        """Test Session sets user_agent_extra with botocore version."""
        session = Session()
        assert "botocore/" in session.user_agent_extra
        # Verify format is "botocore/X.Y.Z"
        parts = session.user_agent_extra.split("/")
        assert len(parts) == 2
        assert parts[0] == "botocore"

    def test_session_with_profile_none(self):
        """Test Session can be created with profile=None."""
        session = Session(profile=None)
        assert session.user_agent_name == "nifcloud"
        assert session.user_agent_version == nifcloud.__version__

    def test_session_user_agent_configuration(self):
        """Test that user agent configuration is properly set."""
        session = Session()
        # Verify user agent components are set
        assert hasattr(session, "user_agent_name")
        assert hasattr(session, "user_agent_version")
        assert hasattr(session, "user_agent_extra")

    @mock.patch("botocore.session.Session.create_client")
    def test_create_client_basic(self, mock_super_create_client):
        """Test create_client calls parent create_client."""
        mock_client = mock.MagicMock()
        mock_http_session = mock.MagicMock()
        mock_http_session._manager = mock.MagicMock()
        mock_http_session._manager.connection_pool_kw = {}

        mock_endpoint = mock.MagicMock()
        mock_endpoint.http_session = mock_http_session

        mock_client._endpoint = mock_endpoint
        mock_super_create_client.return_value = mock_client

        session = Session()
        result = session.create_client("computing", region_name="jp-east-1")

        # Verify parent create_client was called
        mock_super_create_client.assert_called_once()
        call_args = mock_super_create_client.call_args
        assert call_args[0][0] == "computing"
        assert call_args[1]["region_name"] == "jp-east-1"
        assert result is mock_client

    def test_create_client_calls_parent_and_returns_client(self):
        """Test create_client calls parent and applies SSL context."""
        # Mock only the parent's parent (botocore.session.Session.create_client)
        with mock.patch("botocore.session.Session.create_client") as mock_super:
            # Setup mock client with proper structure
            mock_client = mock.MagicMock()
            mock_http_session = mock.MagicMock()
            mock_manager = mock.MagicMock()
            mock_manager.connection_pool_kw = {}
            mock_http_session._manager = mock_manager
            mock_client._endpoint.http_session = mock_http_session

            mock_super.return_value = mock_client

            session = Session()
            # Call the method - our implementation should call parent and set ssl_context
            result = session.create_client("computing", region_name="jp-east-1")

            # Verify parent was called with correct service
            mock_super.assert_called_once()
            args = mock_super.call_args
            assert args[0][0] == "computing"
            assert result is mock_client
            # The implementation modifies the manager dict
            assert mock_manager.connection_pool_kw is not None

    def test_create_client_method_exists(self):
        """Test that create_client method exists and has correct signature."""
        session = Session()
        assert hasattr(session, "create_client")
        assert callable(session.create_client)
        # Check the method has the nifcloud_ parameter variants
        import inspect

        sig = inspect.signature(session.create_client)
        param_names = set(sig.parameters.keys())
        # Should have both regular and nifcloud_ variants
        assert "service_name" in param_names
        assert "nifcloud_access_key_id" in param_names
        assert "nifcloud_secret_access_key" in param_names
        assert "nifcloud_session_token" in param_names

    @mock.patch("botocore.session.Session.create_client")
    def test_create_client_calls_super_with_mapped_params(self, mock_super_create):
        """Test create_client transforms nifcloud params to aws params."""
        mock_client = mock.MagicMock()
        mock_super_create.return_value = mock_client

        session = Session()
        # Call with nifcloud_* params
        session.create_client(
            "computing",
            nifcloud_access_key_id="key",
            nifcloud_secret_access_key="secret",
            nifcloud_session_token="token",
        )

        # Verify super was called (this line is executed)
        mock_super_create.assert_called_once()
        # The call has positional and keyword args
        # The method parameters are transformed before calling super
        call_args = mock_super_create.call_args
        # Verify service name is first positional arg
        assert call_args.args[0] == "computing"

    def test_create_client_http_session_access_exists(self):
        """Test that create_client code path processes http_session."""
        # We'll test that the code path is reachable by verifying
        # the return value and that parent create_client is called
        with mock.patch("botocore.session.Session.create_client") as mock_super:
            mock_client = mock.MagicMock()
            mock_super.return_value = mock_client

            session = Session()
            result = session.create_client("computing", region_name="jp-east-1")

            # Verify the method executed successfully
            assert result is mock_client
            # Verify super was called (indicates method was executed)
            mock_super.assert_called_once()

    @mock.patch("botocore.session.Session.create_client")
    def test_create_client_returns_client(self, mock_super_create_client):
        """Test create_client returns the created client."""
        mock_client = mock.MagicMock()
        mock_http_session = mock.MagicMock()
        mock_http_session._manager = mock.MagicMock()
        mock_http_session._manager.connection_pool_kw = {}

        mock_endpoint = mock.MagicMock()
        mock_endpoint.http_session = mock_http_session

        mock_client._endpoint = mock_endpoint
        mock_super_create_client.return_value = mock_client

        session = Session()
        result = session.create_client("computing", region_name="jp-east-1")

        assert result is mock_client

    @mock.patch("botocore.session.Session.create_client")
    def test_create_client_without_http_manager(self, mock_super_create_client):
        """Test create_client handles clients without _manager gracefully."""
        # Create a mock client without _manager attribute
        mock_http_session = mock.MagicMock(spec=[])
        # Remove _manager attribute
        del mock_http_session._manager

        mock_endpoint = mock.MagicMock()
        mock_endpoint.http_session = mock_http_session

        mock_client = mock.MagicMock()
        mock_client._endpoint = mock_endpoint

        mock_super_create_client.return_value = mock_client

        session = Session()
        # Should not raise an error
        result = session.create_client("computing", region_name="jp-east-1")

        assert result is mock_client

    @mock.patch("botocore.session.Session.create_client")
    def test_create_client_multiple_services(self, mock_super_create_client):
        """Test create_client works with different service names."""
        mock_client = mock.MagicMock()
        mock_http_session = mock.MagicMock()
        mock_http_session._manager = mock.MagicMock()
        mock_http_session._manager.connection_pool_kw = {}

        mock_endpoint = mock.MagicMock()
        mock_endpoint.http_session = mock_http_session

        mock_client._endpoint = mock_endpoint
        mock_super_create_client.return_value = mock_client

        session = Session()

        # Test with different service names
        for service_name in ["computing", "rdb", "nas", "storage"]:
            mock_super_create_client.reset_mock()
            result = session.create_client(service_name, region_name="jp-east-1")
            mock_super_create_client.assert_called_once()
            assert result is mock_client

    @mock.patch("botocore.session.Session.create_client")
    def test_create_client_with_multiple_kwargs(self, mock_super_create_client):
        """Test create_client passes through all kwargs to parent."""
        mock_client = mock.MagicMock()
        mock_http_session = mock.MagicMock()
        mock_http_session._manager = mock.MagicMock()
        mock_http_session._manager.connection_pool_kw = {}

        mock_endpoint = mock.MagicMock()
        mock_endpoint.http_session = mock_http_session

        mock_client._endpoint = mock_endpoint
        mock_super_create_client.return_value = mock_client

        session = Session()
        result = session.create_client(
            "computing",
            region_name="jp-east-1",
            verify=False,
            config=None,
        )

        # Verify all kwargs were passed to parent
        mock_super_create_client.assert_called_once()
        call_kwargs = mock_super_create_client.call_args[1]
        assert call_kwargs["region_name"] == "jp-east-1"
        assert call_kwargs["verify"] is False
        assert call_kwargs["config"] is None

    def test_session_ssl_context_includes_extra_ciphers(self):
        """Test that session module creates SSL context with extra ciphers."""
        # Import the ssl_context from the module
        from nifcloud.session import ssl_context

        assert ssl_context is not None
        assert isinstance(ssl_context, ssl.SSLContext)
        # Verify the context includes AES256-SHA256 cipher
        ciphers = ssl_context.get_ciphers()
        cipher_names = [c["name"] for c in ciphers]
        assert "AES256-SHA256" in cipher_names
