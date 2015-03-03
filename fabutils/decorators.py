# -*- coding: utf-8 -*-
from fabric.api import env


def without_prefixes(task):
    """
    Decorator that strips the ```command_prefixes``` attribute from the given
    task env to run it without calling those prefixes.

    This decorator is intended to create tasks that does not need to call the
    command_prefixes defined in the current env, for example if you have
    prefixes that need to be called inside a VM but not in your local machine.
    """
    def wrapper(*args, **kwargs):
        # Save the current env's command_prefixes and remove it from env
        command_prefixes = env.get('command_prefixes', [])
        env.command_prefixes = []

        # Call the given task
        result = task(*args, **kwargs)

        # Restore the original command_prefixes
        env.command_prefixes = command_prefixes

        return result

    return wrapper
