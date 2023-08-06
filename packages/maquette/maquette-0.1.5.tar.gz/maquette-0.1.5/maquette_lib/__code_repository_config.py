import os
import yaml

class CodeRepositoryConfiguration:
    code_repo = None
    cr_yaml_list = []

    def __init__(self, code_repository_path: str = None):
        if code_repository_path:
            self.code_repo = code_repository_path
        else:
            self.code_repo = "code_repository.yaml"
        if os.path.exists(self.code_repo):
            with open(self.code_repo) as file:
                self.cr_yaml_list = yaml.load(file, Loader=yaml.FullLoader)

    def get_train_script(self) -> str:
        return self.cr_yaml_list.get('train_script')