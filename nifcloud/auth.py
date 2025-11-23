"""Custom authentication handler for NIFCLOUD API."""

from botocore import auth


class SigV2ComputingAuth(auth.SigV2Auth):
    """SigV2 authentication with NIFCLOUD-specific parameter mapping.

    This class handles the parameter name mapping between AWS SDK's
    'AWSAccessKeyId' and NIFCLOUD API's 'AccessKeyId'.
    """

    def calc_signature(self, request, params):
        """Calculate signature with NIFCLOUD parameter mapping.

        Converts 'AWSAccessKeyId' to 'AccessKeyId' before calculating
        the signature, as required by NIFCLOUD API.

        Args:
            request: The request object.
            params: The request parameters dictionary.

        Returns:
            The calculated signature string.

        """
        if "AWSAccessKeyId" in params:
            params["AccessKeyId"] = params["AWSAccessKeyId"]
            del params["AWSAccessKeyId"]
        return super().calc_signature(request, params)


auth.AUTH_TYPE_MAPS.update({"v2": SigV2ComputingAuth})
