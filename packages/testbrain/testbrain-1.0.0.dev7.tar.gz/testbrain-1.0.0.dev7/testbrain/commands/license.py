# -*- coding: utf-8 -*-
import click

from testbrain.core.app import cli
from testbrain.core.state import pass_state
from testbrain.core.exceptions import RequestError, BadCredentialsException

from testbrain.client.client import APIClient

from testbrain.helpers.params import ServerToken
from testbrain.helpers.options import NotRequiredIf
from testbrain.helpers.structures import DotDict
from testbrain.helpers.validators import validate_endpoint, \
    validate_server_token, validate_api_token, validate_only_latters


@cli.command(init_required=False)
@click.option('--endpoint', required=True, prompt=True, callback=validate_endpoint,
              help='Server endpoint URL. ("http(s)://host[:port]")')
@click.option('--server-token', required=False, prompt=True, default='', type=ServerToken(),
              callback=validate_server_token)
@click.option('--api-token', prompt=True, default='', cls=NotRequiredIf, not_required_if='server_token',
              callback=validate_api_token)
@pass_state
@click.pass_context
def init(ctx, state, endpoint, server_token, api_token):

    state.config.set('testbrain', 'endpoint', endpoint)
    state.config.set('testbrain', 'server_token', server_token)
    state.config.set('testbrain', 'api_token', api_token)

    client = APIClient(endpoint=endpoint, server_token=server_token, api_token=api_token)

    current_organization_response = client.request_current_organization()

    if current_organization_response.status_code >= 500:
        raise RequestError('Some error during request')

    if current_organization_response.status_code == 401:
        if server_token != '' and not api_token:
            raise BadCredentialsException('Please set or check required param "--server-token"')
        raise BadCredentialsException('Check if endpoint or server-token/api-token is correct')

    if current_organization_response.status_code == 404:
        click.echo('There are no organizations on this server. Please create a new one.')
        if server_token == '':
            server_token = click.prompt('Please enter valid server-token', default='', value_proc=validate_server_token)
        company = click.prompt('Please enter a organization name', type=str, value_proc=validate_only_latters)
        company = str(company).capitalize()

        user_email = click.prompt('Please enter a first user (email)', type=str)
        user_password = click.prompt('Please enter a first user (password)', type=str,
                                     hide_input=True, confirmation_prompt=True)

        organization_response = client.request_create_organization(
            company_name=company,
            email=user_email,
            password=user_password
        )

        if organization_response.status_code not in [200, 201]:
            raise RequestError(message='Some problem during the creation of the organization \n'
                                       'and the first user in the system')

        organization_data = DotDict(organization_response.json())

        state.config.set('testbrain', 'api_token', organization_data.api_token)
        state.config.set('testbrain', 'user_token', organization_data.user_token)

    if current_organization_response.status_code in [200, 201, ]:
        click.echo('An organization exists on the server. Enter the details of an existing user or create a new one.')

        user_email = click.prompt('Please enter a email (ex. name@domain.com)', type=str)
        user_password = click.prompt('Please enter a password', type=str, hide_input=True)

        user_response = client.request_user_login(email=user_email, password=user_password)
        if user_response.status_code not in [200, 201]:
            raise RequestError(message='Some problem during request user login')

        user_data = DotDict(user_response.json())

        state.config.set('testbrain', 'user_token', user_data.key)

    client.update_from_state(state=state)

    profile_response = client.request_user_profile()
    if profile_response.status_code not in [200, 201]:
        raise RequestError(message='Some problem during request user profile')

    profile_data = DotDict(profile_response.json())

    state.config.set('testbrain', 'api_token', profile_data.api_key)
    state.config.set('testbrain', 'user', DotDict({
        'id': profile_data.id,
        'username': profile_data.username,
        'email': profile_data.email
    }))

    state.config.write_file()

    click.echo('Success')


@cli.command(init_required=False)
@click.option('--endpoint', required=True, prompt=True, callback=validate_endpoint,
              help='Server endpoint URL. ("http(s)://host[:port]")')
@click.option('--server-token', required=False, prompt=True, default='', type=ServerToken(),
              callback=validate_server_token)
@click.option('--license', required=True, type=click.File(),
              help='Server license filepath downloaded from server.')
@pass_state
@click.pass_context
def initialize(ctx, state, endpoint, server_token, license):

    state.config.set('testbrain', 'endpoint', endpoint)
    state.config.set('testbrain', 'server_token', server_token)

    client = APIClient(endpoint=endpoint, server_token=server_token)

    create_response = client.request_create_from_license(license=license.read())

    if create_response.status_code not in [200, 201]:
        raise RequestError(message='Some problem during the creation of the organization \n'
                                   'and the first user in the system')

    organization_data = DotDict(create_response.json())

    state.config.set('testbrain', 'api_token', organization_data.api_token)
    state.config.set('testbrain', 'user_token', organization_data.user_token)

    client.update_from_state(state=state)

    profile_response = client.request_user_profile()
    if profile_response.status_code not in [200, 201]:
        raise RequestError(message='Some problem during request user profile')

    profile_data = DotDict(profile_response.json())

    state.config.set('testbrain', 'user', DotDict({
        'id': profile_data.id,
        'username': profile_data.username,
        'email': profile_data.email
    }))

    state.config.write_file()

    click.echo('Success')
