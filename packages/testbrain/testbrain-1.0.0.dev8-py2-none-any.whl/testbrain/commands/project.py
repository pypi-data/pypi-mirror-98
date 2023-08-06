# -*- coding: utf-8 -*-
import click

from testbrain.client.client import APIClient
from testbrain.core.app import cli
from testbrain.core.state import pass_state
from testbrain.core.exceptions import RequestError, HookExistsError
from testbrain.helpers.structures import DotDict
from testbrain.helpers.validators import validate_unique_project_name
from testbrain.helpers.options import RequiredIf
from testbrain.helpers.installers import setup_script_hook


INTEGRATION_TYPE = DotDict({
    'script': 'request_create_script_repository',

})


def get_project_list(client):
    list_resp = client.request_list_project()
    if list_resp.status_code not in [200, 201]:
        raise RequestError(message='Some problem during request project list')

    list_data = DotDict(list_resp.json())
    list_data = list_data.results
    return list_data


def create_project(client, name):
    project_resp = client.request_create_project(project_name=name)

    if project_resp.status_code not in [200, 201]:
        raise RequestError(message='Some problem during request project creation')

    project_data = DotDict(project_resp.json())
    project = DotDict(dict(
        id=project_data.id,
        name=project_data.name,
        slug=project_data.slug,
        organization_id=project_data.organization
    ))

    return project


def create_repository(client, project_id, type):
    request_method = getattr(client, INTEGRATION_TYPE[type])
    repository_resp = request_method(project_id=project_id)

    if repository_resp.status_code not in [200, 201]:
        click.echo(repository_resp.content, err=True)
        raise RequestError(message='Some problem during request repository creation')

    repository_data = DotDict(repository_resp.json())
    repository = DotDict(dict(
        project_id=repository_data.project,
        user_id=repository_data.user,
        name=repository_data.repository_name
    ))

    return repository


@cli.command(init_required=True)
@click.option('--create', 'action', flag_value='create',
              default=True)
@click.option('--list', 'action', flag_value='list')
@click.option('--name', prompt='Project name', cls=RequiredIf, required_if={'action': 'create'},
              callback=validate_unique_project_name)
@click.option('--type', default='script')
@click.option('--repo', prompt=True, default='./.git', cls=RequiredIf,
              required_if={'action': 'create', 'type': 'script'},
              type=click.Path(exists=True, dir_okay=True, resolve_path=True))
@pass_state
@click.pass_context
def project(ctx, state, action, name, type, repo):

    current_project = DotDict(state.config.get('testbrain', 'project'))
    # current_repository = DotDict(state.config.get('testbrain', 'repository'))

    if not current_project.empty:
        message = 'Project already configured: ({}). \n' \
                  'Delete exist project and create new one?'.format(current_project.name)

        if click.confirm(message, abort=True):
            state.config.remove_option('testbrain', 'project')
            state.config.remove_option('testbrain', 'repository')
            state.config.write_file()
            click.echo('Now you can create a project')

    client = APIClient.make_from_state(state=state)

    if action == 'create':

        new_project = create_project(client, name)
        new_repository = create_repository(client, new_project.id, type)

        state.config.set('testbrain', 'project', new_project)
        state.config.set('testbrain', 'repository', new_repository)
        state.config.set('testbrain', 'repo_path', repo)
        state.config.write_file()

        try:
            result = setup_script_hook(state=state)
        except HookExistsError as e:
            click.echo(e, err=True)
            result = False
            message = 'Try re-write hook scripts?'
            if click.confirm(message, abort=True):
                while not result:
                    result = setup_script_hook(state=state, reinstall=True)

    if action == 'list':
        project_list = get_project_list(client)
        if len(project_list) == 0:
            click.echo('No projects found or you are not a project member. \n'
                       'Create a project or log in as a different user.\n"tb project create --name <project name>"')
            return 0

        for item in project_list:
            click.echo('({}):\t{}'.format(item['id'], item['name']))

    click.echo('Success')
