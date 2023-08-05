#!/usr/bin/env python
# coding: utf-8


from ._version import __version__, version_info
import json
import os.path as osp

HERE = osp.abspath(osp.dirname(__file__))

with open(osp.join(HERE, "lab_static", "package.json")) as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{"src": "lab_static", "dest": data["name"]}]
