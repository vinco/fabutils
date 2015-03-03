# -*- coding: utf-8 -*-
from distutils.util import strtobool


def boolean(value):
    """
    Translate the given value to a boolean object.

    Example:
        >>> boolean(True)
        True

        >>> boolean(0)
        False

        >>> boolean('false')
        False

        >>> boolean('yes')
        True
    """
    if isinstance(value, bool):
        return value

    elif isinstance(value, int):
        return bool(value)

    else:
        return bool(strtobool(str(value)))


def join(*args):
    """
    Return a string composed of the result of applying str() to each one of
    the given args, separated by spaced, but only if the item exists.

    Example:
        >>> join('Hello', False, 1, True, 0, 'world')
        'Hello 1 True world'
    """
    strings = [str(arg) for arg in args if arg]

    return ' '.join(strings)


def arguments(*args, **kwargs):
    """
    Translates the given args and kwargs into a string composed of each one of
    the provided args followed by the key and value of each one of the
    provided kwargs' items in the form key=value, separated by spaces.

    Example:
        >>> arguments('arg1', 'arg2', kwarg1='val1', kwarg2='val2')
        'arg1 arg2 kwarg1=val1 kwarg2=val2'
    """
    named_arguments = ['{0}={1}'.format(*pair) for pair in kwargs.items()]
    arguments = [arg for arg in args] + named_arguments

    return join(*arguments)


def options(**kwargs):
    """
    Translates the given kwargs insto a string composed by the key of each one
    of the provided kwargs items in the form --key only if the corresponding
    value can be avalueated to a boolean True, separated by spaces.

    Example:
        >>> options(option1=True, option2='No', option3=1, option4=False)
        '--option1 --option3'
    """
    options = ['--{0}'.format(k) for k, v in kwargs.items() if boolean(v)]

    return join(*options)
