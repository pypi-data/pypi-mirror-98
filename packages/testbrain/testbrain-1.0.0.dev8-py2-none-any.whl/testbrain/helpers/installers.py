# -*- coding: utf-8 -*-
import json
import os
import click
from urlparse import urljoin
from testbrain.core.exceptions import HookSetupError, HookExistsError
from testbrain.client.client import APIClient


def setup_script_hook(state, reinstall=False):
    endpoint = state.endpoint
    api_token = state.api_token

    username = state.config.get('testbrain', 'user').get('username')
    repo_name = state.config.get('testbrain', 'repository').get('name')
    project = state.config.get('testbrain', 'repository').get('project_id')
    repo_path = state.config.get('testbrain', 'repo_path')

    hook_url = urljoin(endpoint, '/api/ssh_v2/hook/{}/'.format(project))

    this_dir, this_filename = os.path.split(__file__)
    template_file_path = os.path.join(this_dir, '..', 'templates', 'script.py-tpl')
    template = open(template_file_path, 'r').read()
    template = template.replace("{{HOOK_URL}}", hook_url)
    template = template.replace("{{USERNAME}}", username)
    template = template.replace("{{REPOSITORY}}", repo_name)
    template = template.replace("{{API_KEY}}", api_token)

    hook_filename = 'testbrain-hook.py'
    hook_wrapper_filename = 'post-receive'
    hook_dir = os.path.join(repo_path, 'hooks')

    if not os.path.exists(hook_dir):
        raise HookSetupError('GIT hook path does not exist.\n'
                             'Maybe need init git: "cd {}; git --bare init"'.format(repo_path))

    if os.path.exists(os.path.join(hook_dir, hook_filename)) and not reinstall:
        raise HookExistsError('GIT Hook file already exist. Please remove old file manually.\n'
                             '{}'.format(os.path.join(hook_dir, hook_filename)))

    hook = open(os.path.join(hook_dir, hook_filename), 'w+')
    hook.write(template)
    hook.close()

    if os.path.exists(os.path.join(hook_dir, hook_wrapper_filename)) and not reinstall:
        raise HookExistsError('"post-receive" hook wrapper already exist. If need add cmd into file manually:\n'
                             '"python {}"'.format(os.path.join('.', 'hooks', hook_filename)))

    hook_wrapper_body = '#!/usr/bin/env bash\npython {} server'.format(os.path.join('.', 'hooks', hook_filename))
    hook_file = open(os.path.join(hook_dir, hook_wrapper_filename), 'w+')
    hook_file.write(hook_wrapper_body)
    hook_file.flush()
    hook_file.close()

    mode = os.stat(os.path.join(hook_dir, hook_wrapper_filename)).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(os.path.join(hook_dir, hook_wrapper_filename), mode)

    client = APIClient.make_from_state(state=state)
    data = json.dumps({
        "repository": {
            "full_name": "{}/{}".format(username, repo_name),
            "name": repo_name,
        }
    })
    resp = client.request_script_hook(project=project, event='install', data=data)
    click.echo('[{}] {}'.format(resp.status_code, resp.content))
    if resp.status_code not in [200, 201]:
        click.echo('{}'.format(resp.content), err=True)
        raise HookSetupError('Some think wrong during hook installation.')

    click.echo('Git hook script installed.\nYou can run command:\n'
               '"cd {}; python {}/hooks/testbrain-hook.py sync -r"'
               ''.format((os.path.abspath(os.path.join(repo_path, os.pardir))), repo_path))

    return True
