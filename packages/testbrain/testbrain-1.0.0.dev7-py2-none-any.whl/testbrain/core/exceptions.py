# -*- coding: utf-8 -*-
import click


class TestbrainError(click.ClickException):
    def __init__(self):
        super(TestbrainError, self).__init__(message=self.message)


class ConfigLoadError(TestbrainError):
    message = 'Configfile could not load.'


class NotInitializedError(TestbrainError):
    message = 'This directory has not been set up with the TB CLI\nYou must first run "tb init".'


class AlreadyInitializedError(TestbrainError):
    message = 'Current directory already initialized.\nPlease re-init CLI "tb init --force"'


class InputvalidationError(click.ClickException):
    pass


class RequestError(click.ClickException):
    pass


class HookSetupError(click.ClickException):
    pass


class HookExistsError(click.ClickException):
    pass


class BadCredentialsException(click.ClickException):
    pass


class PermissionDeniedException(click.ClickException):
    pass
