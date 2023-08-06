import logging
import shutil
import tempfile
import webbrowser

import tornado.ioloop
import tornado.web
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_server.services.kernels.handlers import (
    KernelHandler,
    MainKernelHandler,
    ZMQChannelsHandler,
)
from jupyter_server.services.kernels.kernelmanager import MappingKernelManager
from jupyter_server.services.kernelspecs.handlers import MainKernelSpecHandler
from traitlets import Integer, Unicode, default
from traitlets import Dict as tDict
from traitlets.config.application import Application
import logging
import jinja2
from .handlers import ROOT, TEMPLATE_ROOT, DEFAULT_STATIC_ROOT, MODULE_MODE
from .handlers import (
    MainEntryHandler,
    MainModuleHandler,
    StartupCodeHandler,
    Default404Handler,
)

ENTRY_POINT = {MODULE_MODE.SINGLE: "main.html", MODULE_MODE.MULTIPLE: "index.html"}

_kernel_id_regex = r"(?P<kernel_id>\w+-\w+-\w+-\w+-\w+)"


class CosappModuleServer(Application):
    name = "cosapp_module"
    description = Unicode(
        """ 
        This launches a stand-alone server for CoSApp application.
        """
    )
    option_description = Unicode(
        """
        """
    )

    startup_code = Unicode(
        """
        """
    )

    args_list = Unicode("[]")

    title = Unicode(
        """
        CoSApp application
        """
    )

    file = Unicode("file", config=True)

    port = Integer(6789, config=True, help="Port of the CoSApp server. Default 6789.")
    static_root = Unicode(
        str(DEFAULT_STATIC_ROOT),
        config=True,
        help="Directory holding static assets (HTML, JS and CSS files).",
    )
    aliases = {
        "port": "CosappModuleServer.port",
        "p": "CosappModuleServer.port",
        "static": "CosappModuleServer.static_root",
        "f": "CosappModuleServer.file",
    }
    connection_dir_root = Unicode(
        config=True,
        help=(
            "Location of temporary connection files. Defaults "
            "to system `tempfile.gettempdir()` value."
        ),
    )
    connection_dir = Unicode()

    all_module_data = tDict({}, help="Content of CoSApp module json file")

    module_mode = Integer(
        0, help="Module mode, 0 for single module, 1 for multiple modules"
    )

    @default("connection_dir_root")
    def _default_connection_dir(self):
        return tempfile.gettempdir()

    @default("log_level")
    def _default_log_level(self):
        return logging.INFO

    def start(self):
        connection_dir = tempfile.mkdtemp(
            prefix="cosapp_module_", dir=self.connection_dir_root
        )

        kernel_spec_manager = KernelSpecManager(parent=self)
        kernel_manager = MappingKernelManager(
            parent=self,
            kernel_spec_manager=kernel_spec_manager,
            connection_dir=connection_dir,
            cull_idle_timeout=600,
            cull_interval=600,
            cull_connected=True,
        )
        if len(self.title) == 0:
            self.title = "CoSApp Application"
        handlers = [
            (
                r"/cosapp/code",
                StartupCodeHandler,
                {
                    "code": self.startup_code,
                    "title": self.title,
                    "args": self.args_list,
                    "all_module_data": self.all_module_data,
                },
            ),
            (
                r"/module/([^/]+)",
                MainModuleHandler,
                {
                    "all_module_data": self.all_module_data,
                    "module_mode": self.module_mode,
                },
            ),
            (
                r"/api/kernels",
                MainKernelHandler,
            ),
            (r"/api/kernels/%s" % _kernel_id_regex, KernelHandler),
            (r"/api/kernels/%s/channels" % _kernel_id_regex, ZMQChannelsHandler),
            (r"/api/kernelspecs", MainKernelSpecHandler),
            (
                r"/static/(.*)",
                tornado.web.StaticFileHandler,
                {"path": self.static_root},
            ),
            (
                r"/",
                MainEntryHandler,
                {
                    "all_module_data": self.all_module_data,
                    "module_mode": self.module_mode,
                },
            ),
        ]

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_ROOT))
        app = tornado.web.Application(
            handlers,
            kernel_manager=kernel_manager,
            kernel_spec_manager=kernel_spec_manager,
            autoreload=False,
            jinja2_env=env,
            compress_response=False,
            allow_remote_access=True,
            default_handler_class=Default404Handler,
        )
        app.listen(self.port)
        self.log.info(f"CoSApp server listening on port {self.port}.")
        try:
            webbrowser.open(f"http://127.0.0.1:{self.port}")
            logging.getLogger("tornado.access").disabled = True
            tornado.ioloop.IOLoop.current().start()

        finally:
            self.log.info("Remove connection files")
            shutil.rmtree(connection_dir)


launch_server = CosappModuleServer.launch_instance

if __name__ == "__main__":
    CosappModuleServer.startup_code = ""
    CosappModuleServer.title = ""
    CosappModuleServer.module_mode = MODULE_MODE.MULTIPLE
    CosappModuleServer.launch_instance()
