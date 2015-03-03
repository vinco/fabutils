# -*- coding: utf-8 -*-
import json

from fabric.api import env

from .exceptions import EnvironmentNotDefinedError
from .tasks import ulocal


def set_env(env_name, json_path):
    """
    Creates a dynamic environment based on the contents of the given
    json_path. Note that a this task relies on a "vagrant" environment defined
    on your environments json file to populate the task's env with the proper
    Vagrant's identity file.

    This task must be used to create your own envionment task in your fabfile,
    for example:

        # /path/to/my/environments/file.json
        {
            "vagrant": {
                "some_property": "some_value",
                "another_property": "another_value"
            },
            "staging": {
                ...
            }
        }


        # fabfile.py
        from fabric.api import task
        from fabutils.env import set_env


        @task
        def environment(env_name):
            set_env(env_name, '/path/to/my/environments/file.json')

        @task
        def some_task():
            ...


    And call it as follows:

        fab envinronment:vagrant some_task
    """
    with open(json_path, 'r') as data:
        try:
            environment = json.load(data)[env_name]

        except KeyError:
            raise EnvironmentNotDefinedError(
                "The environment '{0}' is not defined in file '{1}'".format(
                    env_name, json_path
                )
            )

    # Update the env with the Vagrant's identity file if the given env_name is
    # "vagrant" and no key_filename property is defined in the current env.
    if env_name == 'vagrant' and 'key_filename' not in environment:
        result = ulocal('vagrant ssh-config | grep IdentityFile', capture=True)
        env.key_filename = result.split()[1].replace('"', '')

    # Prepend the command "source" to each one of the commands defined in the
    # command_prefixes property of the json file.
    prefixes = environment.get('command_prefixes', [])
    sourced_prefixes = map(lambda p: 'source %s' % p, prefixes)
    environment.update(command_prefixes=sourced_prefixes)

    env.update(environment)
