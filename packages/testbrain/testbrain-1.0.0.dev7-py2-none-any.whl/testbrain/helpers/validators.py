# -*- coding: utf-8 -*-
import re
import click

from testbrain.client.client import APIClient
from testbrain.core.state import State
from testbrain.core.exceptions import InputvalidationError, RequestError
from testbrain.helpers.structures import DotDict

from urlparse import urlparse, urlunparse


def validate_endpoint(ctx, param, value):
    value = urlparse(value)
    try:
        if value.scheme not in ('http', 'https') or not value.netloc:
            raise click.BadParameter('Invalid endpoint URL. Please, enter "http(s)://host[:port]"')

        value = urlunparse(value)
        state = ctx.ensure_object(State)
        state.endpoint = value
        return value
    except click.BadParameter as e:
        click.echo(e)
        value = click.prompt(param.prompt)
        return validate_endpoint(ctx=ctx, param=param, value=value)


def validate_server_token(ctx, param, value):
    state = ctx.ensure_object(State)
    endpoint = state.endpoint
    if not endpoint:
        return value
    try:
        client = APIClient(endpoint=endpoint, server_token=value)
        resp = client.request_validate_server_token()
        if resp.status_code == 200:
            state.server_token = value
            return value
        else:
            raise click.BadParameter('Invalid server-token')
    except click.BadParameter as e:
        click.echo(e)
        if click.confirm('Continue without server-token?'):
            value = ''
            return value
        value = click.prompt(param.prompt)
        return validate_server_token(ctx=ctx, param=param, value=value)


def validate_api_token(ctx, param, value):
    state = ctx.ensure_object(State)
    if not param.required and param.prompt is None and not value:
        state.api_token = value
        return value

    endpoint = state.endpoint
    if not endpoint:
        return value

    try:
        client = APIClient(endpoint=endpoint, api_token=value)
        resp = client.request_validate_api_token()
        if resp.status_code == 200:
            state.api_token = value
            return value
        else:
            raise click.BadParameter('Invalid api-token')
    except click.BadParameter as e:
        click.echo(e)
        if click.confirm('Continue without api-token?'):
            if state.server_token != '':
                value = ''
                return value
            else:
                click.echo('No valid server-token specified. Cannot continue without api-token')
        value = click.prompt(param.prompt)
        return validate_api_token(ctx=ctx, param=param, value=value)


def validate_only_latters(value):
    if not re.match(r"^[a-zA-Z\s]+$", value):
        raise InputvalidationError(message='Please enter only "[a-zA-Z\\s]+".')
    else:
        return value


def validate_unique_project_name(ctx, param, value):
    state = ctx.ensure_object(State)
    client = APIClient.make_from_state(state=state)
    list_resp = client.request_list_project()

    if list_resp.status_code not in [200, 201]:
        # raise RequestError(message='Some problem during request project list')
        project_list = []
    else:
        project_list = DotDict(list_resp.json())
        project_list = project_list.results

    project_list = [proj['name'] for proj in project_list]
    try:
        if value in project_list:
            raise click.BadParameter('Project name must be unique.')
        else:
            return value
    except click.BadParameter as e:
        click.echo(e)
        value = click.prompt(param.prompt)
        return validate_unique_project_name(ctx=ctx, param=param, value=value)
