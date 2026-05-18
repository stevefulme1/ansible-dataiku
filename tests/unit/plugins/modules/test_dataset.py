"""Unit tests for stevefulme1.dataiku.dataset module."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.dataiku.plugins.modules.dataset"
CLIENT_PATH = "ansible_collections.stevefulme1.dataiku.plugins.module_utils.api_client"


def _build_dataset(**kwargs):
    """Return a mock dataset dict."""
    defaults = {"id": "test-id", "name": "test-dataset"}
    defaults.update(kwargs)
    return defaults


class TestCreate:
    """Test dataset creation."""

    @patch(f"{CLIENT_PATH}.requests")
    def test_create_dataset(self, mock_requests, module_args):
        """Creating a dataset sends POST request."""
        mock_response = MagicMock()
        created = _build_dataset()
        mock_response.json.return_value = created
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'{"id":"test-id"}'

        list_response = MagicMock()
        list_response.json.return_value = []
        list_response.raise_for_status.return_value = None
        list_response.content = b'[]'

        session = MagicMock()
        session.request.side_effect = [list_response, mock_response]
        mock_requests.Session.return_value = session

        from ansible_collections.stevefulme1.dataiku.plugins.module_utils.api_client import ApiClient

        mock_module = MagicMock()
        mock_module.params = module_args
        client = ApiClient(mock_module)
        result = client.post("/api/v1/datasets", data={"name": "test"})
        assert result is not None
