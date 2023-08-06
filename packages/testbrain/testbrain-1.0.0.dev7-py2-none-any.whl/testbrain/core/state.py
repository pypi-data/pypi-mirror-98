# -*- coding: utf-8 -*-

import click
from testbrain.core.config import JsonConfigHandler


class State(object):
    _instance = None

    def __init__(self):
        self.verbosity = 0
        self.debug = False
        self.force = False
        self.config = JsonConfigHandler()
        self.initialized = self.config.read_file()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def endpoint(self):
        return self.config.get('testbrain', 'endpoint')

    @endpoint.setter
    def endpoint(self, value):
        self.config.set('testbrain', 'endpoint', value)

    @property
    def server_token(self):
        return self.config.get('testbrain', 'server_token')

    @server_token.setter
    def server_token(self, value):
        self.config.set('testbrain', 'server_token', value)

    @property
    def api_token(self):
        return self.config.get('testbrain', 'api_token')

    @api_token.setter
    def api_token(self, value):
        self.config.set('testbrain', 'api_token', value)

    @property
    def user_token(self):
        return self.config.get('testbrain', 'user_token')

    @user_token.setter
    def user_token(self, value):
        self.config.set('testbrain', 'user_token', value)


pass_state = click.make_pass_decorator(State, ensure=True)


def callback_to_state(ctx, param, value):
    state = ctx.ensure_object(State)
    setattr(state, param.name, value)
    return value
