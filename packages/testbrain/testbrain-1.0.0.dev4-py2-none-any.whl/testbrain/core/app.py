# -*- coding: utf-8 -*-

import click
import os
import inspect
import importlib

from click.exceptions import UsageError, ClickException
from testbrain.core.exceptions import AlreadyInitializedError, NotInitializedError
from testbrain.core.state import State, callback_to_state


class TestbrainCommand(click.Command):

    def __init__(self, name, context_settings=None, callback=None, params=None, help=None, epilog=None, short_help=None,
                 options_metavar="[OPTIONS]", add_help_option=True, no_args_is_help=False, hidden=False,
                 deprecated=False, init_required=False):
        super(TestbrainCommand, self).__init__(name, context_settings, callback, params, help, epilog, short_help,
                                               options_metavar, add_help_option, no_args_is_help, hidden, deprecated)

        self.init_required = init_required

    def get_force_option(self, ctx):
        return click.Option(
            ('--force', ),
            is_flag=True,
            is_eager=False,
            expose_value=False,
            callback=callback_to_state,
            help='Flag to enforce the command',
        )

    def get_params(self, ctx):
        rv = super(TestbrainCommand, self).get_params(ctx=ctx)
        force_option = self.get_force_option(ctx=ctx)
        if force_option is not None:
            rv = rv + [force_option]
        return rv

    def invoke(self, ctx):
        state = ctx.ensure_object(State)
        if self.init_required and not state.initialized:
            raise NotInitializedError()
        if not self.init_required and state.initialized:
            if not state.force:

                raise AlreadyInitializedError()
            else:
                raise ClickException('Sorry, but at the moment this feature is not implemented')
        return super(TestbrainCommand, self).invoke(ctx=ctx)


class TestbrainGroup(click.Group):
    plugin_folder = os.path.join(os.path.dirname(__file__), '..', 'commands')

    def command(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a command to
        the group.  This takes the same arguments as :func:`command` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        from click.decorators import command

        kwargs['cls'] = TestbrainCommand

        def decorator(f):
            cmd = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        return decorator

    def group(self, *args, **kwargs):
        """A shortcut decorator for declaring and attaching a group to
        the group.  This takes the same arguments as :func:`group` but
        immediately registers the created command with this instance by
        calling into :meth:`add_command`.
        """
        from click.decorators import group

        kwargs['cls'] = TestbrainGroup

        def decorator(f):
            cmd = group(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        return decorator

    def load_commands(self, ctx):
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith('.py') and not filename.startswith('__init__'):
                mod = importlib.import_module('testbrain.commands.{name}'.format(name=filename[:-3]))
                for _, cmd in inspect.getmembers(mod):
                    if isinstance(cmd, TestbrainCommand):
                        self.add_command(cmd, name=cmd.name)

    def list_commands(self, ctx):
        self.load_commands(ctx)
        return self.commands

    def get_command(self, ctx, cmd_name):
        self.load_commands(ctx)
        cmd = super(TestbrainGroup, self).get_command(ctx, cmd_name)
        return cmd


@click.group(cls=TestbrainGroup, invoke_without_command=False)
@click.pass_context
def cli(ctx):
    pass


app = cli
