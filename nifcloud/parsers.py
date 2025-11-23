"""Parsers for NIFCLOUD API response parsing.

Provides specialized parsers for NIFCLOUD services to handle
service-specific response formats and data conversions.
"""

from botocore import parsers, utils


class ComputingQueryParser(parsers.QueryParser):
    """Parser for NIFCLOUD Computing API responses.

    Handles NIFCLOUD-specific response parsing for Computing service,
    including custom timestamp and integer parsing.
    """

    def __init__(self, timestamp_parser=None, blob_parser=None):
        """Initialize Computing parser with custom timestamp handling.

        Args:
            timestamp_parser: Ignored, uses custom parse_timestamp.
            blob_parser: Optional blob parser.

        """
        super().__init__(self.parse_timestamp, blob_parser)

    def parse_timestamp(self, value):
        """Parse timestamp value with empty string handling.

        Args:
            value: The timestamp string to parse.

        Returns:
            Parsed datetime or None if value is empty.

        """
        if value == "":
            return None
        else:
            return utils.parse_timestamp(value)

    @parsers._text_content
    def _handle_integer(self, shape, text):
        """Handle integer parsing with empty string handling.

        Args:
            shape: The shape definition.
            text: The text to parse as integer.

        Returns:
            Parsed integer or None if text is empty.

        """
        if text == "":
            return None
        return super()._handle_integer(shape, text)


parsers.PROTOCOL_PARSERS.update(
    {
        "computing": ComputingQueryParser,
        "rdb": parsers.QueryParser,
        "nas": parsers.QueryParser,
        "ess": parsers.QueryParser,
        "dns": parsers.RestXMLParser,
    }
)
