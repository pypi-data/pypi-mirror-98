# -*- coding: utf-8 -*-

import hashlib
from textwrap import TextWrapper
from random import random


def rando(salt=None):
    """
    Generate a random MD5 hash for whatever purpose.  Useful for testing
    or any other time that something random is required.
    Args:
        salt (str): Optional ``salt``, if ``None`` then ``random.random()``
            is used.
    Returns:
        str: Random MD5 hash
    Example:
        .. code-block:: python
            from testbrain.utils.misc import rando
            rando('dAhn49amvnah3m')
    """

    if salt is None:
        salt = random()

    return hashlib.md5(str(salt).encode()).hexdigest()


def is_true(item):
    """
    Given a value, determine if it is one of
    ``[True, 'true', 'yes', 'y', 'on', '1', 1,]`` (note: strings are converted
    to lowercase before comparison).
    Args:
        item: The item to convert to a boolean.
    Returns:
        bool: ``True`` if ``item`` equates to a true-ish value, ``False``
            otherwise
    """
    tstrings = ['true', 'yes', 'y', 'on', '1']
    if isinstance(item, str) and item.lower() in tstrings:
        return True
    elif isinstance(item, bool) and item is True:
        return True
    elif isinstance(item, int) and item == 1:
        return True
    else:
        return False


def wrap(text, width=77, indent='', long_words=False, hyphens=False):
    """
    Wrap text for cleaner output (this is a simple wrapper around
    ``textwrap.TextWrapper`` in the standard library).
    Args:
        text (str): The text to wrap
    Keyword Arguments:
        width (int): The max width of a line before breaking
        indent (str): String to prefix subsequent lines after breaking
        long_words (bool): Whether or not to break on long words
        hyphens (bool): Whether or not to break on hyphens
    Returns:
        str: The wrapped string
    """

    types = [str]
    if type(text) not in types:
        raise TypeError("Argument `text` must be one of [str, unicode].")

    wrapper = TextWrapper(subsequent_indent=indent, width=width,
                          break_long_words=long_words,
                          break_on_hyphens=hyphens)
    return wrapper.fill(text)
