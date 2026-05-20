> **EXPERIMENTAL** - This collection is a proof of concept and is not production ready.
> Modules may use placeholder API endpoints and have not been validated against real infrastructure.
> Do not use in production environments.

        # stevefulme1.dataiku

        Ansible Collection for **Dataiku DSS**.

        ## Modules

        - `stevefulme1.dataiku.project` -- Manage DSS projects
- `stevefulme1.dataiku.project_info` -- List or retrieve DSS projects
- `stevefulme1.dataiku.dataset` -- Manage DSS datasets
- `stevefulme1.dataiku.dataset_info` -- List or retrieve DSS datasets
- `stevefulme1.dataiku.recipe` -- Manage DSS recipes
- `stevefulme1.dataiku.recipe_info` -- List or retrieve DSS recipes
- `stevefulme1.dataiku.model` -- Manage DSS saved models
- `stevefulme1.dataiku.model_info` -- List or retrieve DSS saved models
- `stevefulme1.dataiku.deployment` -- Manage DSS API deployments
- `stevefulme1.dataiku.deployment_info` -- List or retrieve DSS deployments
- `stevefulme1.dataiku.scenario` -- Manage DSS scenarios
- `stevefulme1.dataiku.scenario_info` -- List or retrieve DSS scenarios
- `stevefulme1.dataiku.managed_folder` -- Manage DSS managed folders
- `stevefulme1.dataiku.managed_folder_info` -- List or retrieve DSS managed folders
- `stevefulme1.dataiku.code_env` -- Manage DSS code environments
- `stevefulme1.dataiku.code_env_info` -- List or retrieve DSS code environments

        ## Roles

        - `dss_install` -- Install and configure Dataiku DSS
- `project_deploy` -- Deploy DSS projects with automation
- `model_promote` -- Promote models through DSS deployment pipeline

        ## EDA Event Source

        - `stevefulme1.dataiku.dss_events` -- Poll Dataiku DSS for events

        ## Requirements

        - Python >= 3.9
        - `requests` library
        - ansible-core >= 2.16

        ## Installation

        ```bash
        ansible-galaxy collection install stevefulme1.dataiku
        ```

        ## License

        GPL-3.0-or-later
