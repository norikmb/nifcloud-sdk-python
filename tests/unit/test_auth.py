"""Unit tests for NIFCLOUD authentication handlers."""

from unittest import mock

import pytest
from botocore import auth as botocore_auth

from nifcloud.auth import SigV2ComputingAuth


class TestSigV2ComputingAuth:
    """Test cases for SigV2ComputingAuth authentication handler."""

    def test_sigv2computing_auth_is_subclass_of_sigv2auth(self):
        """Test SigV2ComputingAuth is a subclass of botocore's SigV2Auth."""
        assert issubclass(SigV2ComputingAuth, botocore_auth.SigV2Auth)

    def test_calc_signature_parameter_mapping(self):
        """Test calc_signature maps AWSAccessKeyId to AccessKeyId."""
        # Create a mock credentials object
        mock_credentials = mock.MagicMock()
        auth_handler = SigV2ComputingAuth(mock_credentials)

        # Create a mock request
        mock_request = mock.MagicMock()
        mock_request.method = "GET"
        mock_request.url = "https://api.example.com/"

        params = {"AWSAccessKeyId": "test_key"}

        # Mock the parent class calc_signature method
        with mock.patch.object(
            botocore_auth.SigV2Auth, "calc_signature", return_value="test_signature"
        ) as mock_parent_calc:
            result = auth_handler.calc_signature(mock_request, params)

        # Verify the parameter was mapped before calling parent
        assert "AccessKeyId" in params
        assert "AWSAccessKeyId" not in params
        assert params["AccessKeyId"] == "test_key"
        # Verify signature was returned
        assert result == "test_signature"

    def test_calc_signature_preserves_other_params(self):
        """Test calc_signature preserves other parameters unchanged."""
        mock_credentials = mock.MagicMock()
        auth_handler = SigV2ComputingAuth(mock_credentials)

        mock_request = mock.MagicMock()
        params = {"AWSAccessKeyId": "test_key", "Action": "DescribeInstances", "Version": "2012-12-12"}

        with mock.patch.object(
            botocore_auth.SigV2Auth, "calc_signature", return_value="test_signature"
        ):
            result = auth_handler.calc_signature(mock_request, params)

        # Verify the parameter was mapped
        assert params["AccessKeyId"] == "test_key"
        assert "AWSAccessKeyId" not in params
        # Verify other params are preserved
        assert params["Action"] == "DescribeInstances"
        assert params["Version"] == "2012-12-12"

    def test_calc_signature_without_aws_access_key(self):
        """Test calc_signature handles params without AWSAccessKeyId."""
        mock_credentials = mock.MagicMock()
        auth_handler = SigV2ComputingAuth(mock_credentials)

        mock_request = mock.MagicMock()
        params = {"Action": "DescribeInstances", "Version": "2012-12-12"}

        with mock.patch.object(
            botocore_auth.SigV2Auth, "calc_signature", return_value="test_signature"
        ):
            result = auth_handler.calc_signature(mock_request, params)

        # Should not raise an error and return signature
        assert result == "test_signature"
        assert "AWSAccessKeyId" not in params
        assert "AccessKeyId" not in params
        # Original params should be unchanged (no AccessKeyId added)
        assert params == {"Action": "DescribeInstances", "Version": "2012-12-12"}

    def test_auth_type_maps_updated(self):
        """Test that v2 auth type is registered in AUTH_TYPE_MAPS."""
        assert "v2" in botocore_auth.AUTH_TYPE_MAPS
        assert botocore_auth.AUTH_TYPE_MAPS["v2"] == SigV2ComputingAuth
