from .webui_server import PyriWebUIServer
import argparse
import pyri.util.wait_exit as wait_exit
import os

def main():
    parser = argparse.ArgumentParser(description="PyRI WebUI Server")
    parser.add_argument('--device-manager-url', type=str, default=None,required=True,help="Robot Raconteur URL for device manager service (required)")
    parser.add_argument("--http-host", type=str, default='0.0.0.0',help="Host to listen for connections")
    parser.add_argument("--http-port",type=int,default=8000,help="Port to listen for connections")
    parser.add_argument("--static-data-dir",type=str,default=None,help="Directory to store WebUI static data (Pyodide, wheels, deps)")

    args, _ = parser.parse_known_args()

    static_data_dir = None
    if args.static_data_dir is not None:
        static_data_dir = args.static_data_dir
    elif "PYRI_WEBUI_STATIC_DATA_DIR" in os.environ:
        static_data_dir = os.environ["PYRI_WEBUI_STATIC_DATA_DIR"]

    server = PyriWebUIServer(args.device_manager_url,args.http_host,args.http_port,static_data_dir)
    wait_exit.wait_exit_callback(lambda: server.stop())
    server.run()

if __name__ == "__main__":
    main()