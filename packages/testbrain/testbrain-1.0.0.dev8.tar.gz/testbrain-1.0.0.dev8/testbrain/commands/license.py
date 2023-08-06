# -*- coding: utf-8 -*-
import click

from testbrain.core.app import cli
from testbrain.core.state import pass_state
from testbrain.core.exceptions import RequestError, BadCredentialsException, TestbrainError

from testbrain.client.client import APIClient

from testbrain.helpers.params import ServerToken
from testbrain.helpers.options import NotRequiredIf, RequiredIf
from testbrain.helpers.structures import DotDict
from testbrain.helpers.validators import validate_endpoint, \
    validate_server_token, validate_api_token, validate_only_latters


@cli.command(init_required=True)
@click.option('--add', 'action', flag_value='add', default=True)
@click.option('--list', 'action', flag_value='list')
@click.option('--license', cls=RequiredIf, required_if={'action': 'add'}, type=click.File(),
              help='Server license filepath downloaded from server.')
@pass_state
@click.pass_context
def license(ctx, state, action, license):

    client = APIClient.make_from_state(state=state)

    if action == 'add':
        result = client.request_add_license(license=license.read())
        if result.status_code not in [200, 201]:
            raise RequestError(message='[{}] {}'.format(result.status_code, result.content))

    if action == 'list':
        raise click.ClickException(message='Not implemented')

    click.echo('Success')
