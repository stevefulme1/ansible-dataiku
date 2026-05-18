# -*- coding: utf-8 -*-
# Copyright (c) 2025, Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Ansible module to query Dataiku DSS recipe resources."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: recipe_info
short_description: List or retrieve DSS recipes
description:
    - Retrieve information about Dataiku DSS recipe resources.
version_added: "1.0.0"
author:
    - Steve Fulmer (@stevefulme1)
options:
    project_key:
        description:
            - The project key for the Dataiku DSS resource.
        type: str
    recipe_name:
        description:
            - The recipe name for the Dataiku DSS resource.
        type: str
extends_documentation_fragment:
    - stevefulme1.dataiku.common
requirements:
    - "python >= 3.9"
    - "requests"
"""

EXAMPLES = r"""
- name: List all recipes
  stevefulme1.dataiku.recipe_info:
    api_url: "https://dss.example.dataiku.com"
    api_key: "my-api-key"
"""

RETURN = r"""
recipes:
    description: List of recipe resources.
    returned: always
    type: list
    elements: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.dataiku.plugins.module_utils.api_client import (
    COMMON_ARGS,
    ApiClient,
    HAS_REQUESTS,
)


def main():
    argument_spec = dict(
        project_key=dict(type="str", no_log=False),
        recipe_name=dict(type="str"),
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

    if params.get("project_key"):
        result = client.get(f"/api/v1/recipes/{params['project_key']}")
        module.exit_json(changed=False, recipes=[result] if result else [])
    else:
        result = client.get("/api/v1/recipes")
        items = result if isinstance(result, list) else result.get("data", result.get("items", []))
        module.exit_json(changed=False, recipes=items)


if __name__ == "__main__":
    main()
