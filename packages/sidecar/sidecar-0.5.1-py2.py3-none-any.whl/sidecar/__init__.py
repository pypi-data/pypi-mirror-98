#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Project Jupyter.
# Distributed under the terms of the Modified BSD License.

from .sidecar import Sidecar
from ._version import __version__, version_info


def _jupyter_labextension_paths():
    return [{
        'src': 'labextension',
        'dest': '@jupyter-widgets/jupyterlab-sidecar'
    }]
