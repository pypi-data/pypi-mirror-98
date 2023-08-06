import click

from .init import init_project
from .add_gitignore import add_gitignore_lines
from .add_pipelines import add_pipeline_files


@click.group()
def project_group():
    """
    Manage machine learning projects
    """
    pass


project_group.add_command(init_project, 'init')
project_group.add_command(add_gitignore_lines, 'add-gitignore')
project_group.add_command(add_pipeline_files, 'add-pipelines')
