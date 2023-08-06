"""
Module for Terraform Cloud API Endpoint: Run Triggers.
"""

from .endpoint import TFCEndpoint
from ._constants import MAX_PAGE_SIZE

class TFCRunTriggers(TFCEndpoint):
    """
    `Run Triggers API Docs \
        <https://www.terraform.io/docs/cloud/api/run-triggers.html>`_
    """
    def __init__(self, instance_url, org_name, headers, well_known_paths, verify, log_level):
        super().__init__(instance_url, org_name, headers, well_known_paths, verify, log_level)
        self._endpoint_base_url = f"{self._api_v2_base_url}/run-triggers"
        self._ws_api_v2_base_url = f"{self._api_v2_base_url}/workspaces"

    def required_entitlements(self):
        return []

    def terraform_cloud_only(self):
        return False

    def terraform_enterprise_only(self):
        return False

    def create(self, workspace_id, payload):
        """
        ``POST /workspaces/:workspace_id/run-triggers``

        `Run Triggers Create API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-triggers.html#create-a-run-trigger>`_

        `Create Sample Payload \
            <https://www.terraform.io/docs/cloud/api/run-triggers.html#sample-payload>`_
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/run-triggers"
        return self._create(url, payload)

    def list(self, workspace_id, filters=None, page=None, page_size=None):
        """
        ``GET /workspaces/:workspace_id/run-triggers``

        `Run Triggers List API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-triggers.html#list-run-triggers>`_

        Query Parameter(s) (`details \
            <https://www.terraform.io/docs/cloud/api/run-triggers.html#query-parameters>`_):
            - ``filter[run-trigger][type]`` (Required)
            - ``page_size`` (Optional)

        Example filter(s):

        .. code-block:: python

            filters = [
                {
                    "keys": ["run-trigger", "type"],
                    "value": "foo"
                }
            ]
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/run-triggers"
        return self._list(url, filters=filters, page=page, page_size=page_size)

    def list_all(self, workspace_id, filters=None):
        """
        This function does not correlate to an endpoint in the TFC API Docs specifically,
        but rather is a helper function to wrap the `list` endpoint, which enumerates out
        every page so users do not have to implement the paging logic every time they just
        want to list every run trigger for a workspace.

        Returns an array of objects.
        """
        url = f"{self._ws_api_v2_base_url}/{workspace_id}/run-triggers"

        current_page_number = 1
        run_triggers_resp = \
            self._list(url, page=current_page_number, page_size=MAX_PAGE_SIZE, filters=filters)
        total_pages = run_triggers_resp["meta"]["pagination"]["total-pages"]

        run_triggers = []
        while current_page_number <= total_pages:
            run_triggers_resp = \
                self._list(url, page=current_page_number, page_size=MAX_PAGE_SIZE, filters=filters)
            run_triggers += run_triggers_resp["data"]
            current_page_number += 1

        return run_triggers

    def show(self, run_trigger_id):
        """
        ``GET /run-triggers/:run_trigger_id``

        `Run Triggers Show API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-triggers.html#show-a-run-trigger>`_
        """
        url = f"{self._endpoint_base_url}/{run_trigger_id}"
        return self._show(url)

    def destroy(self, run_trigger_id):
        """
        ``DELETE /run-triggers/:run_trigger_id``

        `Run Triggers Destroy API Doc Reference \
            <https://www.terraform.io/docs/cloud/api/run-triggers.html#delete-a-run-trigger>`_
        """
        url = f"{self._endpoint_base_url}/{run_trigger_id}"
        return self._destroy(url)
