"""Documentation generation for NIFCLOUD API reference.

Provides custom documenters for API documentation generation with
NIFCLOUD-specific branding and service-specific documentation links.
"""

import re

from botocore import docs
from botocore.docs import client, service

NIFCLOUD_DOC_BASE = "https://pfs.nifcloud.com/api"


class ClientDocumenter(client.ClientDocumenter):
    """Documenter for NIFCLOUD client API.

    Extends botocore's ClientDocumenter to add NIFCLOUD-specific
    documentation links and branding.
    """

    def _add_model_driven_method(self, section, method_name):
        """Add operation documentation with NIFCLOUD links.

        Args:
            section: The documentation section to add to.
            method_name: The method name.

        """
        super()._add_model_driven_method(section, method_name)
        operation_name = self._client.meta.method_to_api_mapping[method_name]
        if self._service_name == "computing":
            replace = rf"\1<{NIFCLOUD_DOC_BASE}/cp/{operation_name}.htm>\2"
        elif self._service_name == "storage":
            replace = rf"\1<{NIFCLOUD_DOC_BASE}/object-storage-service/{operation_name}.htm>\2"
        else:
            replace = rf"\1<{NIFCLOUD_DOC_BASE}/{self._service_name}/{operation_name}.htm>\2"
        method_intro = section.get_section("method-intro")
        replaced_text = re.sub(r"([\s\S]+)<.+>(.+)$", replace, method_intro.getvalue().decode("utf8")).replace(
            "AWS", "NIFCLOUD"
        )
        method_intro.clear_text()
        method_intro.push_write(replaced_text)


class ServiceDocumenter(service.ServiceDocumenter):
    """Documenter for NIFCLOUD service API.

    Extends botocore's ServiceDocumenter to generate NIFCLOUD service
    documentation with proper branding and links.
    """

    def __init__(self, service_name, session, root_docs_path):
        """Initialize service documenter.

        Args:
            service_name: The NIFCLOUD service name.
            session: The NIFCLOUD session object.
            root_docs_path: Root path for documentation output.

        """
        self._session = session
        self._service_name = service_name
        self._root_docs_path = root_docs_path

        self._client = self._session.create_client(
            service_name, region_name="jp-east-1", nifcloud_access_key_id="foo", nifcloud_secret_access_key="bar"
        )
        self._event_emitter = self._client.meta.events

        self.sections = ["title", "table-of-contents", "client-api", "client-exceptions", "paginator-api", "waiter-api"]


docs.ServiceDocumenter = ServiceDocumenter
service.ClientDocumenter = ClientDocumenter
