import os
import re
import sys
import click
import tempfile
import subprocess
from shutil import copyfile

from energinetml.core.project import Project

from ..utils import discover_project


GIT_CLONE_URLS = {
    'ssh': 'git@ssh.dev.azure.com:v3/energinet/AnalyticsOps/PipelineTemplates',
    'https': 'https://energinet@dev.azure.com/energinet/AnalyticsOps/_git/PipelineTemplates',
}


FILES_TO_COPY = (
    (
        os.path.join('examples', 'provision-resources-example-pipeline.yml'),
        'provision-resources.yml',
    ),
    (
        os.path.join('examples', 'destroy-resources-example-pipeline.yml'),
        'destroy-resources.yml',
    ),
    (
        os.path.join('examples', 'deploy-model-example-pipeline.yml'),
        'deploy-model.yml',
    ),
)


# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_project()
def add_pipeline_files(project):
    """
    Add DevOps pipelines to project.
    \f

    :param Project project:
    """

    # -- Project short name --------------------------------------------------

    click.echo((
        'Provisioning cloud resources requires a short name for your '
        'which contains 11 (or less) characters. This name is used as part '
        'of the resource names, can only contain lower case letters '
        'and numbers, and must start with a letter.'
    ))

    project_short_name_valid = False

    while not project_short_name_valid:
        project_short_name = click.prompt(
            text='Please enter a project short name',
            type=click.STRING,
        )

        if not re.findall(r'^[a-z][a-z0-9]{,10}$', project_short_name):
            click.echo('Invalid short name provided')
        else:
            project_short_name_valid = True

    # -- Clone repo ----------------------------------------------------------

    click.echo('-' * 79)
    click.echo((
        'NOTICE: We need to clone a Git repository containing the '
        'necessary pipeline templates. You may be prompted to enter '
        'your password to Energinet\'s Azure DevOps. '
    ))
    click.echo()
    click.echo('Make sure you have access to the repository before continuing.')
    click.echo()
    click.echo((
        'The repository is located here: '
        'https://dev.azure.com/energinet/AnalyticsOps/_git/PipelineTemplates'
    ))
    click.echo('-' * 79)

    # -- Choose SSH / HTTPS --------------------------------------------------

    clone_type = click.prompt(
        text='Would you like to clone repository using SSH or HTTPS?',
        type=click.Choice(GIT_CLONE_URLS.keys()),
    )

    clone_url = GIT_CLONE_URLS[clone_type]

    # -- Clone repo ----------------------------------------------------------

    click.echo('Cloning %s' % clone_url)

    with tempfile.TemporaryDirectory() as temp_path:
        try:
            subprocess.check_call(
                args=['git', 'clone', clone_url, temp_path],
                stdout=sys.stdout,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            raise click.Abort()

        click.echo('-' * 79)

        pipelines_path = os.path.join(project.path, 'pipelines')

        if not os.path.isdir(pipelines_path):
            os.makedirs(pipelines_path)

        for src, dst in FILES_TO_COPY:
            src_path = os.path.join(temp_path, src)
            dst_path = os.path.join(pipelines_path, dst)
            _copy_template_file(
                project=project,
                project_short_name=project_short_name,
                src_path=src_path,
                dst_path=dst_path,
            )


def _copy_template_file(project, project_short_name, src_path, dst_path):
    """
    :param Project project:
    :param str project_short_name:
    :param str src_path:
    :param str dst_path:
    """
    if os.path.exists(dst_path):
        click.echo('File already exists: %s' % dst_path)
        fn = os.path.split(dst_path)[1]
        if not click.confirm('Really override existing %s?' % fn):
            click.echo('Skipping %s' % fn)
            return

    copyfile(src_path, dst_path)

    with open(dst_path, 'r') as f:
        s = f.read() \
            .replace('Enter Project Name', project.name) \
            .replace('Enter Project Short Name', project_short_name)\
            .replace('Enter Resource Group', project.resource_group)

    with open(dst_path, 'w') as f:
        f.write(s)

    click.echo('Created file: %s' % dst_path)
