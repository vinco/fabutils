# -*- coding: utf-8 -*-
from fabric.api import local, run
from fabric.contrib.project import rsync_project

from .decorators import without_prefixes


# Decorated "local command" to run without command prefixes
ulocal = without_prefixes(local)


# Decorated "rsync_project" command to run without command prefixes
ursync_project = without_prefixes(rsync_project)


# Decorated "run" command to run without command prefixes
urun = without_prefixes(run)
