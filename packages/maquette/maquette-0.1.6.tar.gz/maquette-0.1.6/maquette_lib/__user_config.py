import pathlib
import os
import yaml

class EnvironmentConfiguration:

    #TODO authentication only implemented for stupid(s), implement the other 2
    mq_config: str = None
    mq_yaml_list = []

    def __init__(self, mq_home: str = None):
        if mq_home:
            self.mq_config = os.path.join(mq_home, "config.yaml")
        else:
            self.mq_config = os.path.join(pathlib.Path.home(), ".mq", "config.yaml")
        if os.path.exists(self.mq_config):
            with open(self.mq_config) as file:
                self.mq_yaml_list = yaml.load(file, Loader=yaml.FullLoader)

    def get_url(self) -> str:
        url = self.mq_yaml_list.get('url', 'http://localhost:9042')

        if not (url.endswith('/api/') or url.endswith('/api')):
            url = f"{url}/api/"

        if not url.endswith('/'):
            url = f"{url}/"

        return os.environ.get('MQ_BASE_URL', url)

    def get_user(self) -> str:
        if 'authentication' in self.mq_yaml_list:
            user =  self.mq_yaml_list['authentication'].get('username', 'alice')
        else:
            user = 'alice'
        return os.environ.get('MQ_USERNAME', user)

    def get_roles(self):
        if 'authentication' in self.mq_yaml_list:
            roles = self.mq_yaml_list['authentication'].get('roles', ['a-team', 'b-team'])
            roles = ','.join(roles)
        else:
            roles = 'a-team, b-team'
        return os.environ.get('MQ_ROLES', roles).split(",")

    def get_project(self) -> str:
        if 'project' in self.mq_yaml_list:
            project_id = self.mq_yaml_list['project'].get('id', None)
        else:
            project_id = None
        return os.environ.get('MQ_PROJECT_ID', project_id)

    def get_project_name(self) -> str:
        if 'project' in self.mq_yaml_list:
            project_name = self.mq_yaml_list['project'].get('name', None)
        else:
            project_name = None
        return os.environ.get('MQ_PROJECT_NAME', project_name)

    def get_process_env(self):
        if 'environment' in self.mq_yaml_list:
            return self.mq_yaml_list['environment'].items()
        else:
            return None

    def activate_project(self, project_name, project_id):
        if self.mq_config:
            self.mq_yaml_list["project"]["id"] = project_id
            self.mq_yaml_list["project"]["name"] = project_name
            with open(self.mq_config, 'w') as file:
                yaml.dump(self.mq_yaml_list, file)


    def add_process_env(self, key, value):
        if 'environment' in self.mq_yaml_list:
            self.mq_yaml_list['environment'][key] = value
        else:
            self.mq_yaml_list['environment'] = {}
            self.mq_yaml_list['environment'][key] = value
        if self.mq_config:
            with open(self.mq_config, 'w') as file:
                yaml.dump(self.mq_yaml_list, file)

    def remove_process_envs(self):
        self.mq_yaml_list.pop('environment', None)
        if self.mq_config:
            with open(self.mq_config, 'w') as file:
                yaml.dump(self.mq_yaml_list, file)
