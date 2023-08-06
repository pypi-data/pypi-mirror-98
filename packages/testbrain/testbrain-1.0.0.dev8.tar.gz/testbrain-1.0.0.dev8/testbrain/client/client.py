# -*- coding: utf-8 -*-

import requests
from urlparse import urljoin
from testbrain.client.auth import HTTPCLIAuth, HTTPUserTokenAuth, HTTPAPIAuth


class APIClient(object):

    def __init__(self, endpoint, server_token=None, api_token=None, user_token=None):
        self.endpoint = endpoint
        self.server_token = server_token
        self.api_token = api_token
        self.user_token = user_token

    @classmethod
    def make_from_state(cls, state):
        config = state.config
        endpoint = config.get('testbrain', 'endpoint')
        server_token = config.get('testbrain', 'server_token')
        api_token = config.get('testbrain', 'api_token')
        user_token = config.get('testbrain', 'user_token')
        client = cls(endpoint=endpoint, server_token=server_token, user_token=user_token, api_token=api_token)
        return client

    def update_from_state(self, state):
        config = state.config
        self.endpoint = config.get('testbrain', 'endpoint')
        self.server_token = config.get('testbrain', 'server_token')
        self.api_token = config.get('testbrain', 'api_token')
        self.user_token = config.get('testbrain', 'user_token')
        return self

    def request_validate_server_token(self):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/token/server/')
        resp = session.get(url, auth=HTTPCLIAuth(token=self.server_token))
        return resp

    def request_validate_user_token(self):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/token/user/')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_validate_api_token(self):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/token/api/')
        resp = session.get(url, auth=HTTPAPIAuth(token=self.api_token))
        return resp

    def request_current_organization(self):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/organization/')
        if self.api_token:
            resp = session.get(url, auth=HTTPAPIAuth(token=self.api_token))
        else:
            resp = session.get(url, auth=HTTPCLIAuth(token=self.server_token))
        return resp

    def request_create_from_license(self, license):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/license/init/')
        resp = session.post(url, auth=HTTPCLIAuth(token=self.server_token), data={
            'license_key': license,
        })
        return resp

    def request_create_organization(self, company_name, email, password):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/organization/')
        resp = session.post(url, auth=HTTPCLIAuth(token=self.server_token), data={
            'company_name': company_name,
            'email': email,
            'password': password
        })
        return resp

    def request_user_login(self, email, password):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/account/login/')
        resp = session.post(url, data={
            'email': email,
            'password': password
        })
        return resp

    def request_user_profile(self):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/account/profile/')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_list_project(self):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/projects/?fields=id,name')
        resp = session.get(url, auth=HTTPUserTokenAuth(token=self.user_token))
        return resp

    def request_create_project(self, project_name):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/projects/')
        resp = session.post(url, auth=HTTPUserTokenAuth(token=self.user_token), data={
            'name': project_name,
            'is_public': False,
            'is_active': True
        })
        return resp

    def request_create_script_repository(self, project_id):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/ssh_v2/repository/')
        resp = session.post(url, auth=HTTPUserTokenAuth(token=self.user_token), data={
            'project': project_id
        })
        return resp

    def request_script_hook(self, project, event, data):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/ssh_v2/hook/{}/'.format(project))
        headers = {"X-Git-Event": event, "Content-Type": "application/json"}
        resp = session.post(url, auth=HTTPAPIAuth(token=self.api_token), headers=headers, data=data)
        return resp

    def request_add_license(self, license):
        session = requests.Session()
        url = urljoin(self.endpoint, '/api/cli/license/add/')
        resp = session.post(url, auth=HTTPCLIAuth(token=self.server_token), data={
            'license_key': license,
        })
        return resp
