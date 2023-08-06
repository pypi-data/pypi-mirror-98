# -*- coding: utf-8 -*-
import click
import base64
from urlparse import urlparse, urlunparse

from testbrain.core.state import State


class URL(click.ParamType):
    name = 'url'

    def convert(self, value, param, ctx):
        if not isinstance(value, tuple):
            value = urlparse(value)
            if value.scheme not in ('http', 'https') or not value.netloc:
                self.fail(
                    '',
                    param,
                    ctx,
                )
        return urlunparse(value)


class ServerToken(click.ParamType):
    name = 'server-token'

    def convert(self, value, param, ctx):
        return base64.b64encode(value.encode()).decode()
