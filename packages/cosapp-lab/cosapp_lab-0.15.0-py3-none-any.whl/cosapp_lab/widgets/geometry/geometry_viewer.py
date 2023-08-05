#!/usr/bin/env python
# coding: utf-8

# Copyright (c) CoSApp Team.


"""
Widget container as geometry viewer panel
"""

from typing import Dict, List, Any
from weakref import ref

from cosapp.systems import System
from cosapp_lab._frontend import module_name, module_version
from cosapp_lab.widgets.utils import CosappObjectParser, OccParser
from ipywidgets import Box
from traitlets import CaselessStrEnum
from traitlets import Dict as tDict
from traitlets import Int, Unicode

from ..sysexplorer.component.geometry_component import GeometryView


class GeometryViewer(Box):
    """Widget container as GeometryViewer panel.

    If more than one children is given, they will be appended top to bottom.

    Attributes
    ----------
    title: str, optional
        Tab title for the GeometryViewer; default "GeometryViewer"
    anchor: str - one of ['split-right', 'split-left', 'split-top', 'split-bottom', 'tab-before', 'tab-after', 'right']
        Position of the GeometryViewer; default "split-right"
    children: list of Widget
        List of widget to insert in the GeometryViewer
    """

    _model_name = Unicode("GeometryViewerModel").tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode("GeometryViewerView").tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    title = Unicode("GeometryViewer").tag(sync=True)
    anchor = CaselessStrEnum(
        [
            "split-right",
            "split-left",
            "split-top",
            "split-bottom",
            "tab-before",
            "tab-after",
            "right",
        ],
        default_value="split-right",
        allow_none=False,
    ).tag(sync=True)
    system_data = tDict(default_value={"key": "None"}, allow_none=False).tag(sync=True)

    update_signal = Int(default_value=0, allow_none=False).tag(sync=True)
    notification_msg = tDict(
        default_value={"update": 0, "msg": "", "log": ""}, allow_none=False
    ).tag(sync=True)

    def __init__(self, data: System = None, **kwargs):
        """Initialize class from input system

        Attributes
        ----------
        self._system : ReferenceType
            The weak reference of input system

        self.add_shape : Callable
            The helper function used to get geometry from system.
            If it is not provided, self.default_add_shape will
            be used.

        self.title : str
            The title of widget tab.

        self.update_signal : int
            The signal which is observed in frontend, it is incremented each time
            the main driver is computed

        self.time_step : int
            The counter for time step


        self.notification_msg : Dict
            The message which is sent to frontend after each time step.

        """

        self._system = ref(data)
        self.add_shape = kwargs.get("add_shape", None)

        self.geo_source = kwargs.get("source", None)
        self.title = f"{data.name} - GeometryViewer {module_version}"

        self.time_step = 0

        self.__init_data(data)
        self.__init_connection()
        super().__init__(**kwargs)

    def __init_data(self, data: System):
        """Parse cosapp System and return list of sub-systems,
        list of ports...

        """
        self.sys_data = CosappObjectParser(data)
        self.component = GeometryView(self._system, self.sys_data, self.send)

    def __init_connection(self) -> None:
        """Initialize the connection between fontend - backend and
        between input system with the callbacks.
        """
        self.sys_data.connect_main_driver(self.computed_notification)
        self.on_msg(self._handle_button_msg)

    def computed_notification(self) -> None:
        """Callback function used to update geometry data from buffer
        and to emit update signal to front end.
        """
        self.component.computed_notification()

    def _handle_button_msg(self, model: Any, content: Dict, buffers: List) -> None:
        self.component._handle_button_msg(model, content, buffers)
