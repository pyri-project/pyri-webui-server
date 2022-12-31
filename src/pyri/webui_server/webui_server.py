from sanic import Sanic
from sanic import response as res
from .webui_resource_router import PyriWebUIResourceRouteHandler
from .blockly_router import PryiWebUIBlocklyBlocksRouteHandler
from .sandbox_functions_router import PryiWebUISandboxFunctionsRouteHandler
from pyri.plugins.webui_server import get_webui_server_plugin_factories
import appdirs
from pathlib import Path
import urllib.parse
import asyncio
import sys
import mimetypes
import socket


class PyriWebUIServer:
    def __init__(self, device_manager_url: str, host : str='0.0.0.0', port: int =8000, static_data_dir: Path=None):
        self._host = host
        self._port = port
        self._app = Sanic("pyri_webui")
        self._loop = asyncio.get_event_loop()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((host,port))

        # Workaround for invalid js mimetime on Windows
        if mimetypes.guess_type('test.js')[0] != 'text/javascript':
            _mimetype_db = mimetypes.__dict__['_db']
            _mimetype_db.add_type('text/javascript','.js',True)
            _mimetype_db.add_type('text/jsx','.jsx',True)
            assert mimetypes.guess_type('test.js')[0] == 'text/javascript'
            assert mimetypes.guess_type('test.jsx')[0] == 'text/jsx'

        
        if static_data_dir is None:
            static_data_dir = Path(appdirs.user_data_dir(appname="pyri-webui-server", appauthor="pyri-project", roaming=False))
        else:
            if not isinstance(static_data_dir,Path):
                static_data_dir = Path(static_data_dir)

        wheels_dir = static_data_dir.joinpath("wheels")
        deps_dir = static_data_dir.joinpath("deps").joinpath("node_modules")
        pyodide_dir = static_data_dir.joinpath("robotraconteur_pyodide")


        wheels_dir.mkdir(exist_ok=True,parents=True)

        self._wheels_dir = wheels_dir
        
        blockly_block_handler = PryiWebUIBlocklyBlocksRouteHandler()
        self._app.add_route(blockly_block_handler.handler, "/blockly_blocks/<path:path>")
        self._blockly_block_names = blockly_block_handler.get_block_names()

        sandbox_function_handler = PryiWebUISandboxFunctionsRouteHandler()
        self._app.add_route(sandbox_function_handler.handler, "/sandbox_functions/<path:path>")
        self._sandbox_function_names = sandbox_function_handler.get_function_names()

        plugin_route_factories = get_webui_server_plugin_factories()

        self._route_plugin_names = []

        for plugin_route_factory in plugin_route_factories:
            r_name = plugin_route_factory.get_plugin_name()
            r = plugin_route_factory.get_plugin_route_handler()
            self._app.add_route(r,f"/plugins/{r_name}/<path:path>")
            self._route_plugin_names.append(r_name)


        self._app.static('/wheels',str(wheels_dir),name='wheels')
        # self._app.static('/deps',str(deps_dir),name='deps')
        # self._app.static('/robotraconteur_pyodide',str(pyodide_dir),name='robotraconteur_pyodide')
        deps_handler = PyriWebUIResourceRouteHandler("pyri.webui_resources.deps")
        self._app.add_route(deps_handler.handler, '/deps/<path:path>', name="deps")
        pyodide_handler = PyriWebUIResourceRouteHandler("pyri.webui_resources.pyodide")
        self._app.add_route(pyodide_handler.handler,"/robotraconteur_pyodide/<path:path>", name="robotraconteur_pyodide")

        self._app.add_route(self.config_req_handler,"/config")
        main_handler = PyriWebUIResourceRouteHandler(__package__)
        self._app.add_route(main_handler.handler,"/")
        self._app.add_route(main_handler.handler,"/<path:[A-Za-z0-9_]+(?:\\.[A-Za-z0-9_]+)*>")

        self._device_manager_url = device_manager_url



    def config_req_handler(self,request):

        wheel_filenames = [str(w.stem) for w in self._wheels_dir.glob('*.whl')]

        dev_url = self._device_manager_url
        if dev_url.startswith('rr+tcp://localhost'):
            dev_url = dev_url.replace('localhost',urllib.parse.urlsplit("//" + request.host).hostname,1)
        ret = {
            'device_manager_url': dev_url,
            'wheels': wheel_filenames,
            'blockly_block_names': self._blockly_block_names,
            'sandbox_function_names': self._sandbox_function_names,
            'plugin_names': self._route_plugin_names
        }

        return res.json(ret)
        

    async def _run_server(self):
        server = await self._app.create_server(self._host, self._port, return_asyncio_server=True, sock=self._socket)
        await server.startup()
        await server.serve_forever()

    def run(self):
        self._loop.run_until_complete(self._run_server())
        self._loop.run_forever()

    def stop(self):
        self._loop.call_soon_threadsafe(lambda: self._app.stop())
