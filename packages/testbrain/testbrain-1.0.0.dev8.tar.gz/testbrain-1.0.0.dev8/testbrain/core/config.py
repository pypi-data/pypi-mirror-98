# -*- coding: utf-8 -*-

import os
import json

from abc import abstractmethod, abstractproperty

from configparser import RawConfigParser, NoOptionError
from testbrain.helpers.fs import abspath, join


class ConfigInterface(object):

    @property
    @abstractmethod
    def extension(self):
        pass    # pragma: nocover

    @abstractmethod
    def read_file(self, file_path):
        """
        Parse config file settings from ``file_path``.  Returns True if the
        file existed, and was parsed successfully.  Returns False otherwise.
        Args:
            file_path (str): The path to the config file to parse.
        Returns:
            bool: ``True`` if the file was parsed, ``False`` otherwise.
        """
        pass    # pragma: nocover

    @abstractmethod
    def write_file(self, file_path):
        """
        Write config file settings from ``file_path``.  Returns True if the
        file was saved successfully.  Returns False otherwise.
        Args:
            file_path (str): The path to the config file to parse.
        Returns:
            bool: ``True`` if the file was saved, ``False`` otherwise.
        """
        pass    # pragma: nocover

    @abstractmethod
    def keys(self, section):
        """
        Return a list of configuration keys from ``section``.
        Args:
            section (list): The config section to pull keys from.
        Returns:
            list: A list of keys in ``section``.
        """
        pass    # pragma: nocover

    @abstractmethod
    def get_sections(self):
        """
        Return a list of configuration sections.
        Returns:
            list: A list of config sections.
        """
        pass    # pragma: nocover

    @abstractmethod
    def get_dict(self):
        """
        Return a dict of the entire configuration.
        Returns:
            dict: A dictionary of the entire config.
        """

    @abstractmethod
    def get_section_dict(self, section):
        """
        Return a dict of configuration parameters for ``section``.
        Args:
            section (str): The config section to generate a dict from (using
                that sections' keys).
        Returns:
            dict: A dictionary of the config section.
        """
        pass    # pragma: nocover

    @abstractmethod
    def add_section(self, section):
        """
        Add a new section if it doesn't already exist.
        Args:
            section: The section label to create.
        Returns:
            None
        """
        pass    # pragma: nocover

    @abstractmethod
    def get(self, section, key):
        """
        Return a configuration value based on ``section.key``.  Must honor
        environment variables if they exist to override the config... for
        example ``config['myapp']['foo']['bar']`` must be overridable by the
        environment variable ``MYAPP_FOO_BAR``.... Note that ``MYAPP_`` must
        prefix all vars, therefore ``config['redis']['foo']`` would be
        overridable by ``MYAPP_REDIS_FOO`` ... but
        ``config['myapp']['foo']['bar']`` would not have a double prefix of
        ``MYAPP_MYAPP_FOO_BAR``.
        Args:
            section (str): The section of the configuration to pull key values
                from.
            key (str): The configuration key to get the value for.
        Returns:
            unknown: The value of the ``key`` in ``section``.
        """
        pass    # pragma: nocover

    @abstractmethod
    def set(self, section, key, value):
        """
        Set a configuration value based at ``section.key``.
        Args:
            section (str): The ``section`` of the configuration to pull key
                value from.
            key (str): The configuration key to set the value at.
            value: The value to set.
        Returns:
            None
        """
        pass    # pragma: nocover

    @abstractmethod
    def merge(self, dict_obj, override=True):
        """
        Merges a dict object into the configuration.
        Args:
            dict_obj (dict): The dictionary to merge into the config
            override (bool): Whether to override existing values or not.
        Returns:
            None
        """
        pass    # pragma: nocover

    @abstractmethod
    def has_section(self, section):
        """
        Returns whether or not the section exists.
        Args:
            section (str): The section to test for.
        Returns:
            bool: ``True`` if the configuration section exists, ``False``
                otherwise.
        """
        pass    # pragma: nocover


class ConfigHandler(ConfigInterface):
    """
    Config handler implementation.
    """

    @abstractmethod
    def _read_file(self, file_path):
        """
        Parse a configuration file at ``file_path`` and store it.  This
        function must be provided by the handler implementation (that is
        sub-classing this).
        Args:
            file_path (str): The file system path to the configuration file.
        Returns:
            bool: ``True`` if file was read properly, ``False`` otherwise
        """
        pass    # pragma: nocover

    @abstractmethod
    def _write_file(self, file_path):
        """
        Save a configuration file at ``file_path`` and store it.  This
        function must be provided by the handler implementation (that is
        sub-classing this).
        Args:
            file_path (str): The file system path to the configuration file.
        Returns:
            bool: ``True`` if file was read properly, ``False`` otherwise
        """
        pass    # pragma: nocover

    def read_file(self, file_path=None):
        """
        Ensure we are using the absolute/expanded path to ``file_path``, and
        then call ``self._parse_file`` to parse config file settings from it,
        overwriting existing config settings.
        Developers sub-classing from here should generally override
        ``_parse_file`` which handles just the parsing of the file and leaving
        this function to wrap any checks/logging/etc.
        Args:
            file_path (str): The file system path to the configuration file.
        Returns:
            bool: ``True`` if the given ``file_path`` was parsed, and ``False``
                otherwise.
        """

        if not file_path:
            file_path = join(os.getcwd(), '.testbrain', 'config.{}'.format(self.extension))

        file_path = abspath(file_path)
        if os.path.exists(file_path):
            # LOG.debug('config file "%s" exists, loading settings...' % file_path)
            return self._read_file(file_path)
        else:
            # LOG.debug('config file "%s" does not exist, skipping...' % file_path)
            return False

    def write_file(self, file_path=None):
        """
        Args:
            file_path (str): The file system path to the configuration file.
        Returns:
            bool: ``True`` if the given ``file_path`` was saved, and ``False`` otherwise.
        """

        if not file_path:
            file_path = join(os.getcwd(), '.testbrain', 'config.{}'.format(self.extension))

        file_path = abspath(file_path)

        if not os.path.exists(join(os.getcwd(), '.testbrain')):
            os.mkdir(join(os.getcwd(), '.testbrain'))

        return self._write_file(file_path)


class ConfigParserConfigHandler(ConfigHandler, RawConfigParser):

    """
    This class is an implementation of the :ref:`Config <cement.core.config>`
    interface.  It handles configuration file parsing and the like by
    sub-classing from the standard `ConfigParser
    <http://docs.python.org/library/configparser.html>`_
    library.  Please see the ConfigParser documentation for full usage of the
    class.
    Additional arguments and keyword arguments are passed directly to
    RawConfigParser on initialization.
    """

    def __init__(self, *args, **kwargs):
        default_section = self.default_section
        super(ConfigParserConfigHandler, self).__init__(*args, **kwargs)
        self.add_section(default_section)

    def _read_file(self, file_path):
        """
        Parse a configuration file at ``file_path`` and store it.
        Args:
            file_path (str): The file system path to the configuration file.
        Returns:
            bool: ``True`` if file was read properly, ``False`` otherwise
        """
        self.read(file_path)

        # FIX ME: Should check that file was read properly, however if not it
        # will likely raise an exception anyhow.
        return True

    def merge(self, dict_obj, override=True):
        """
        Merge a dictionary into our config.  If override is True then
        existing config values are overridden by those passed in.
        Args:
            dict_obj (dict): A dictionary of configuration keys/values to merge
                into our existing config (self).
        Keyword Args:
            override (bool):  Whether or not to override existing values in the
                config.
        """
        assert isinstance(dict_obj, dict), "Dictionary object required."

        for section in list(dict_obj.keys()):
            if type(dict_obj[section]) == dict:
                if section not in self.get_sections():
                    self.add_section(section)

                for key in list(dict_obj[section].keys()):
                    if override:
                        self.set(section, key, dict_obj[section][key])
                    else:
                        # only set it if the key doesn't exist
                        if key not in self.keys(section):
                            self.set(section, key, dict_obj[section][key])

                # we don't support nested config blocks, so no need to go
                # further down to more nested dicts.

    def keys(self, section):
        """
        Return a list of keys within ``section``.
        Args:
            section (str): The config section
        Returns:
            list: List of keys in the ``section``.
        """
        return self.options(section)

    def get_dict(self):
        """
        Return a dict of the entire configuration.
        Returns:
            dict: A dictionary of the entire config.
        """
        _config = {}
        for section in self.get_sections():
            _config[section] = self.get_section_dict(section)
        return _config

    def get_sections(self):
        """
        Return a list of configuration sections.
        Returns:
            list: List of sections
        """
        return self.sections()

    def get_section_dict(self, section):
        """
        Return a dict representation of a section.
        Args:
            section: The section of the configuration.
        Returns:
            dict: Dictionary reprisentation of the config section.
        """
        dict_obj = dict()
        for key in self.keys(section):
            dict_obj[key] = self.get(section, key)
        return dict_obj

    def add_section(self, section):
        """
        Adds a block section to the config.
        Args:
            section (str): The section to add.
        """
        return RawConfigParser.add_section(self, section)

    def get(self, section, key, default='', **kwargs):
        try:
            return RawConfigParser.get(self, section, key, **kwargs)
        except NoOptionError:
            return default

    def has_section(self, section):
        return RawConfigParser.has_section(self, section)

    def set(self, section, key, value):
        return RawConfigParser.set(self, section, key, value)


class JsonConfigHandler(ConfigParserConfigHandler):

    """
    This class implements the :ref:`Config` Handler
    interface, and provides the same functionality of
    :ref:`ConfigParserConfigHandler`
    but with JSON configuration files.
    """

    default_section = 'testbrain'
    extension = 'json'

    def _read_file(self, file_path):
        """
        Parse JSON configuration file settings from file_path, overwriting
        existing config settings.  If the file does not exist, returns False.
        Args:
            file_path (str): The file system path to the JSON configuration
            file.
        Returns:
            bool
        """
        with open(file_path, 'r') as f:
            content = f.read()
            if content is not None and len(content) > 0:
                self.merge(json.loads(content))

        return True

    def _write_file(self, file_path):

        with open(file_path, 'w+') as f:
            content = self.get_dict()
            if content is not None and len(content) > 0:
                f.write(json.dumps(content, indent=4))

        return True
