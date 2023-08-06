import os
import click

from energinetml.core.project import Project
from energinetml.settings import GITIGNORE_PATH

from ..utils import discover_project


# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_project()
def add_gitignore_lines(project):
    """
    Add ML specific lines to .gitignore file.
    \f

    :param Project project:
    """
    fp = os.path.join(project.path, '.gitignore')

    with open(GITIGNORE_PATH, 'r') as src, open(fp, 'a') as dst:
        dst.writelines(src.readlines())
