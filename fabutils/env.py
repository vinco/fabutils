# -*- coding: utf-8 -*-
import json

from fabric.api import env

from jsonschema import validate

from .exceptions import EnvironmentNotDefinedError


def set_env_from_json_file(json_path, property_name=None, schema_path=None):
    """
    Creates a dynamic environment given a json_path to an environment file,
    using property_name as the initial node to start reading, validating
    against a json schema file if given any


    @task
    def environment(env_name):
        set_env('/path/to/my/environments/file.json', property_name)

    @task
    def some_task():
        ...

    And call it as follows:

        fab envinronment:vagrant some_task
    """
    if schema_path:  # if schema_path is provided
        with open(schema_path, 'r') as schema_file:
            json_schema = json.load(schema_file)
    else:
        json_schema = None

    with open(json_path, 'r') as data:

        if property_name:
            try:
                set_env_from_json(json.load(data)[property_name], json_schema)

            except KeyError:
                raise EnvironmentNotDefinedError(
                    "The property_name '{0}' is not defined in file '{1}'".format(
                        property_name, json_path
                    )
                )
        else:
            set_env_from_json(json.load(data), json_schema)


def set_env_from_json(json_object, json_schema=None):
    """
    Creates a dynamic environment based on the contents of the given
    json_object and validates againts a json_schema object if given any.

    If 'command_prefixes' is available it adds it to the environment prepending
    'source' to the given paths.


    # fabfile.py
    from fabric.api import task
    from fabutils.env import set_env_from_json

    @task
    def some_task():
        with open('/path/to/json', 'r') as json_object, \
                open('/path/to/schema') as json_schema:

        set_env_from_json(json_object, json_schema)


    """
    if json_schema:
        validate(json_object, json_schema)

    environment = json_object

    # Prepend the command "source" to each one of the commands defined in the
    # command_prefixes property of the json file.
    prefixes = environment.get('command_prefixes', [])
    sourced_prefixes = map(lambda p: 'source %s' % p, prefixes)
    environment.update(command_prefixes=sourced_prefixes)

    env.update(environment)
