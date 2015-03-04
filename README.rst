fabutils
========

Utilities for creating better fabric tasks.

Install
-------

.. code:: bash

    $ pip install vo-fabutils

Usage
-----

Import the proper fabutils modules inside your fabfile an hack a nice
day.

Examples
--------

Define environments in JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First you must create a JSON file containing your environment
configuration.

.. code:: json

    # /path/to/environments/file.json
    {
        "devel": {
            "user": "devel-user",
            "hosts": ["dev.host.com"],
            "site_dir": "/path/to/devel/site/www/",
            "command_prefixes": [
                "/path/to/devel/site/env/bin/activate"
            ]
        },
        "production": {
            "user": "prod-user",
            "hosts": ["host.com"],
            "site_dir": "/path/to/production/site/www/",
            "command_prefixes": [
                "/path/to/production/site/env/bin/activate"
            ]
        }
    }

Note that:

-  You can define any arbitrary string as env properties and these will be passed to the task's env.
-  Properties with names "reserved" by fabric will be recognized by it and treated with the special meanig that fabric has for them.
-  The only caveat is that if you define an array of ``command_prefixes`` you must only list the path to the script and this will be automatically prepended to with the word 'souce'. For example if you define ``../some_script`` in your command\_prefixes, it will be tranformed to ``source ../some_script``.
-  Every directory path must end with a trailing slash.

Next, import ``fabutils.env.set_env`` in your fabfile and create a task that calls it with the path to your JSON file.

.. code:: python

    # fabfile.py
    from fabric.api import task
    from fabutils.env import set_env


    @task
    def environment(env_name):
        set_env(env_name, '/path/to/environments/file.json')

| Now you can run tasks in the environment by calling
  ``environment:name`` before
| your task.

.. code:: bash

    # Run a task in devel environment
    $ fab environment:devel some_task

    # Run a task in production environment
    $ fab environment:production some_task

Arbitrary options and parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Some times you just need to pass an unknown number of
  options/arguments to a
| command, in this case you can use ``join``, ``options`` and
  ``arguments`` utils to
| translete the pythonic ``*args`` to command arguments and ``**kwargs``
  to
| command options.

.. code:: python

    from fabric.api import task, run
    from fabutils import join, arguments, options


    @task
    def some_task(*args, **kwargs):
        run(join('some_command', arguments(*args, **kwargs))

And then call your task using the fabric's notation

.. code:: bash

    $ fab some_task:arg1,arg2,kwarg1=val1,kwarg2=val2

    # The above will be translated to:
    # some_command arg1 arg2 kwarg1=val1 kwarg2=val2

| If you pass your ``*kwargs`` to ``options`` the keys that are
  evaluated to a boolean
| True will be translated to ``--{key}`` notation.

.. code:: python

    ...

    @task
    def another_task(**kwargs):
        return(join('another_command', options(**kwargs)))

    ...

.. code:: bash

    $ fab another_task:option1=True,option2=No,option3=1,option4=False

    # The above will be translated to:
    # another_command --option1 --option3

Of course, you can combine the two approaches.

.. code:: python

    ...
    from fabutils import boolean

    @task
    def the_task(*args, **kwargs):
        options = {}
        arguments = {}
        
        for k, v in kwargs:
            if boolean(v):
                options[k] = v

            else:
                arguments[k] = v

        run(join('the_command', arguments(*args, **arguments), options(**options)))

    ...

.. code:: bash

    $ fab the_task:arg1,arg2=val2,option1=True

    # The above will be translated to:
    # the_command arg1 arg2=val2 --option1
