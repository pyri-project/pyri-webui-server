from pyri.plugins.service_node_launch import ServiceNodeLaunch, PyriServiceNodeLaunchFactory

_default_webui_device_manager_url="rr+tcp://{{ HOSTNAME }}:59902?service=device_manager"

def _webui_server_add_args(arg_parser):
    arg_parser.add_argument('--webui-device-manager-url', type=str, default=_default_webui_device_manager_url,\
        required=False,help="Robot Raconteur URL for device manager service for browser connection")

def _webui_server_prepare_args(arg_results):
    args = []
    if arg_results.webui_device_manager_url is not None:
        args.append(f"--device-manager-url={arg_results.webui_device_manager_url}")
    return args

launches = [
    ServiceNodeLaunch("webui_server", "pyri.webui_server", "pyri.webui_server", _webui_server_add_args, _webui_server_prepare_args)
]

class WebUIServerLaunchFactory(PyriServiceNodeLaunchFactory):
    def get_plugin_name(self):
        return "pyri.webui_server"

    def get_service_node_launch_names(self):
        return ["webui_server"]

    def get_service_node_launches(self):
        return launches

def get_service_node_launch_factory():
    return WebUIServerLaunchFactory()

        
