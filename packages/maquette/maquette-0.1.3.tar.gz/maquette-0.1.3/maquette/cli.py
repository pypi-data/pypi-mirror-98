import click
import pandas as pd
import os
import maquette
import shutil
import yaml
import chevron
import fnmatch

from git import Repo

from maquette_lib.__client import Client
from maquette_lib.__user_config import EnvironmentConfiguration

config = EnvironmentConfiguration()
client = Client.from_config(config)


@click.group()
def mq():
    """
    Maquette CLI main routine.
    """
    pass


@mq.group()
def projects():
    """
    Commands for managing projects
    """
    pass


@projects.command("create")
@click.argument('name')
@click.argument('title')
@click.argument('summary')
def projects_init(name, title, summary):
    """
    Initialize a project

    Args:
        name : name of the project

    """
    maquette.project(name,title,summary).create()
    print('# Heureka! You created a project called ' + name + '(‘-’)人(ﾟ_ﾟ)\n'
               '# \n'                                                 
              '# To activate the project type: mq project activate ' + name)


@projects.command("ls")
def projects_list():
    """
    Print the list of projects.

    """
    pd.set_option('display.max_colwidth', None)
    table_df = pd.json_normalize(maquette.projects(to_csv=False))
    print(table_df)


@projects.command("activate")
@click.argument('name')
def activate(name):
    """
    Activate project.

    Args:
        name : name of the project

    """
    project = maquette.project(name).activate()
    config.activate_project(project_name=project.name, project_id=project.id)

    status, response = client.command(cmd='projects environment', args={'name': name})
    if status == 200:
        env_variables = response['data']
        for (env_key, env_value) in env_variables.items():
            config.add_process_env(env_key, env_value)
        if os.name == 'posix':
            print('# You are on a Unix based  system  c[○┬●]כ \n'
                  '# Please copy and run the command: \n'
                  'eval $(unix_env)')
        else:
            for (env_key, env_value) in config.mq_yaml_list['environment'].items():
                os.system("SETX {0} {1}".format(env_key, env_value))
            print('# Congrats you are on a Windows machine \n'
                  '# I activated your project \t\t~~\n'
                  '# Now relax and enjoy a hot cup of coffee \t C|__|')

    else:
        raise RuntimeError('# Ups! Something went wrong (ⓧ_ⓧ)\n'
                           '# status code: ' + str(status) + ', content:\n' + response)


@projects.command("deactivate")
def deactivate():
    """
    Currently only removes the currently activate environment variables from the config, no default env needed or available
    """
    config.remove_process_envs()
    print('Removed Environment from Config')


@projects.command("rm")
@click.argument('name')
def projects_remove(name):
    """
    remove a project

    Args:
        name : name of the project

    """
    maquette.project(name).delete()
    print("# You successfully killed the project " + name + " and removed all evidences (╯°□°)--︻╦╤─ ")

@mq.group()
def code():
    """
    Commands for managing code repositorys
    """
    pass

@code.command("ls")
def code_repositorys_list():
    """
    TODO: as soon as backend supplys list of code repository templates
    """
    print("nothing to see here. Please move on")

@code.command("cl")
@click.argument('template')
@click.argument('target')
def code_repositorys_clone(template, target):
    Repo.clone_from(template, target)
    print("# Repository cloned from git")
    shutil.rmtree(os.path.join(target,".git"))
    if os.path.exists(os.path.join(target, "code_repository.yaml")):

        # Get all file paths
        fnames = []
        for root, d_names, f_names in os.walk(target):
            for f in f_names:
                fnames.append(os.path.join(root, f))

        # access yaml
        with open(os.path.join(target, "code_repository.yaml")) as file:
            code_repo_yaml = yaml.load(file, Loader=yaml.FullLoader)
        print("code_repository.yaml loaded")


        if "templates" in code_repo_yaml:
            print("found template attribute")
            templates = code_repo_yaml["templates"]
            if "filter" in templates:
                filter_list = templates["filter"]
            else:
                print("Nothing to filter, you get the full mustache treatment ( °┏＿┓°) ")

            # reduce fname by filter list
            for filter in filter_list:
                fnames = [x for x in fnames if x not in fnmatch.filter(fnames, filter)]

            print("---------- List of files to be mustached ----------")
            print(fnames)
            print("-----------（°〜～°）-----------")

            if "values" in templates:
                print("")
                value_dict = {}
                for value_item in templates["values"]:
                    # go trough the values list and ask the questions
                    value = click.prompt(value_item["question"], default=value_item["default"])
                    value_dict[value_item["label"]] = value

                    # go through all files per value, very inefficient, thank you for nothing chevron
                    for file in fnames:
                        with open(file) as temp_file:
                            output = chevron.render(temp_file, value_dict)
                        with open(file, "w") as out_file:
                            out_file.write(output)
                        print(file + "has been mustached (•┏∞┓•) ")
            else:
                print("nothing to mustache (￣┏Д┓￣ )")
    else:
        print("No code_repository.yaml found in " + template)


if __name__ == '__main__':
    mq()