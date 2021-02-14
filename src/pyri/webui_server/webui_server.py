from sanic import Sanic
from .webui_resource_router import PyriWebUIResourceRouteHandler
from .blockly_router import PryiWebUIBlocklyBlocksRouteHandler
from pyri.plugins.webui_server import get_all_webui_server_route_handlers

class PyriWebUIServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self._host = host
        self._port = port
        self._app = Sanic("PyRI WebUI")
        
        blockly_block_handler = PryiWebUIBlocklyBlocksRouteHandler()
        self._app.add_route(blockly_block_handler.handler, "/blockly_blocks/<path:path>")

        plugin_routes = get_all_webui_server_route_handlers()

        for r_name, r in plugin_routes.items():
            self._app.add_route(r,f"/plugins/{r_name}/<path:path>")

        main_handler = PyriWebUIResourceRouteHandler(__package__)
        self._app.add_route(main_handler.handler,"/")
        self._app.add_route(main_handler.handler,"/<path:[A-Za-z0-9_]+(?:\\.[A-Za-z0-9_]+)*>")
        

    def run(self):
        self._app.run(self._host, self._port)
