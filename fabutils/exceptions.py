# -*- coding: utf-8 -*-


class Error(Exception):
    """
    Base error exception for this module.
    """
    pass


class EnvironmentNotDefinedError(Error):
    """
    Exception that must be raised when a environment is not defined in the
    environments json file.
    """
    pass
