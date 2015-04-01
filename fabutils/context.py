# -*- coding: utf-8 -*-
from fabric.colors import green, red
from fabric.state import output
from fabric.utils import fastprint


class CommandMessage(object):
    """
    Context manager that squashes a command output replacing it with the
    given message and the status of the command (OK or ERROR!).

    Usage:
        with CommandMessage('Running some command'):
            run('some command')

    Output:
        Running some command... [OK|ERROR!]

    Parameters:
        - grouped: If True, the given message will not be updated with the
          command status. Defaults to False.
        - dots: If True, the given message will be appended with an
          ellipsis (...). Defaults to True.
        - spaces: The amount of white spaces that sould be prepended to the
          given message. Defaults to 0 (no spaces).
    """
    def __init__(self, message, dots=True, spaces=0, grouped=False):
        self.grouped = grouped
        self.message = '%s%s%s' % (' ' * spaces, message, dots and '...' or '')

        output['running'] = False
        output['stdout'] = False
        output['aborts'] = False

    def __enter__(self):
        end = '\n' if self.grouped else ''
        fastprint(self.message, end=end)

    def __exit__(self, type, value, traceback):
        if not self.grouped:
            if type is None:
                fastprint(green('  OK', True), end='\n')
            else:
                fastprint(red('  ERROR!', True), end='\n\n')


# Alias for the CommandMessage class.
cmd_msg = CommandMessage
