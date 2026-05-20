# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module for managing Dataiku DSS deployment resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: deployment
short_description: Manage DSS API deployments
description:
    - Create, update, and delete Dataiku DSS deployment resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    project_key:
        description:
            - The project key for the Dataiku DSS resource.
        type: str
        required: true
    deployment_id:
        description:
            - The deployment id for the Dataiku DSS resource.
        type: str
        required: true
    endpoint:
        description:
            - The endpoint for the Dataiku DSS resource.
        type: str
    model_version:
        description:
            - The model version for the Dataiku DSS resource.
        type: str
    state:
        description:
            - The desired state of the resource.
        type: str
        choices:
            - present
            - absent
        default: present
extends_documentation_fragment:
    - stevefulme1.dataiku.common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: Create a deployment
  stevefulme1.dataiku.deployment:
    api_url: "https://dss.example.dataiku.com"
    api_key: "my-api-key"
    project_key: "example"
    state: present

- name: Delete a deployment
  stevefulme1.dataiku.deployment:
    api_url: "https://dss.example.dataiku.com"
    api_key: "my-api-key"
    project_key: "example"
    state: absent
"""

RETURN = r"""
deployment:
    description: The deployment resource details.
    returned: On success when state is present.
    type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.dataiku.plugins.module_utils.api_client import (
    COMMON_ARGS,
    ApiClient,
    HAS_REQUESTS,
)


def find_resource(client, params):
    """Find existing resource by identifier."""
    try:
        result = client.get("/public/api/project-deployer/deployments")
        items = result if isinstance(result, list) else result.get("data", result.get("items", []))
        for item in items:
            if item.get("project_key") == params.get("project_key"):
                return item
    except Exception:
        pass
    return None


def create_resource(client, params):
    """Create a new resource."""
    payload = {k: v for k, v in params.items() if v is not None and k not in (
        "api_url", "api_key", "validate_certs", "timeout", "state",
    )}
    return client.post("/public/api/project-deployer/deployments", data=payload)


def update_resource(client, existing, params):
    """Update an existing resource."""
    resource_id = existing.get("id", existing.get("deployment_id", ""))
    payload = {k: v for k, v in params.items() if v is not None and k not in (
        "api_url", "api_key", "validate_certs", "timeout", "state",
    )}
    return client.put(f"/public/api/project-deployer/deployments/{resource_id}/settings", data=payload)


def delete_resource(client, existing):
    """Delete a resource."""
    resource_id = existing.get("id", existing.get("deployment_id", ""))
    client.delete(f"/public/api/project-deployer/deployments/{resource_id}")


def needs_update(params, existing):
    """Check if existing resource needs updating."""
    check_fields = ['endpoint', 'model_version']
    for field in check_fields:
        desired = params.get(field)
        if desired is not None and existing.get(field) != desired:
            return True
    return False


def main():
    argument_spec = dict(
        project_key=dict(type="str", required=True, no_log=False),
        deployment_id=dict(type="str", required=True),
        endpoint=dict(type="str"),
        model_version=dict(type="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )
    argument_spec.update(COMMON_ARGS)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if not HAS_REQUESTS:
        module.fail_json(msg="The 'requests' library is required. Install with: pip install requests")

    client = ApiClient(module)
    params = module.params
    state = params["state"]

    existing = find_resource(client, params)

    if state == "absent":
        if existing is None:
            module.exit_json(changed=False)
        if module.check_mode:
            module.exit_json(changed=True)
        delete_resource(client, existing)
        module.exit_json(changed=True)
        return

    if existing is None:
        if module.check_mode:
            module.exit_json(changed=True)
        resource = create_resource(client, params)
        module.exit_json(changed=True, deployment=resource)
        return

    if needs_update(params, existing):
        if module.check_mode:
            module.exit_json(changed=True)
        resource = update_resource(client, existing, params)
        module.exit_json(changed=True, deployment=resource)
        return

    module.exit_json(changed=False, deployment=existing)


if __name__ == "__main__":
    main()
