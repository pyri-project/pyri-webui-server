from .webui_server import PyriWebUIServer
import argparse
import pyri.util.wait_exit as wait_exit

def main():
    parser = argparse.ArgumentParser(description="PyRI WebUI Server")
    parser.add_argument('--device-manager-url', type=str, default=None,required=True,help="Robot Raconteur URL for device manager service (required)")
    parser.add_argument("--http-host", type=str, default='0.0.0.0',help="Host to listen for connections")
    parser.add_argument("--http-port",type=int,default=8000,help="Port to listen for connections")
    parser.add_argument("--static-data-dir",type=str,default=None,help="Directory to store WebUI static data (Pyodide, wheels, deps)")
    parser.add_argument("--wait-signal",action='store_const',const=True,default=True, help="wait for SIGTERM or SIGINT")

    args, _ = parser.parse_known_args()

    server = PyriWebUIServer(args.device_manager_url,args.http_host,args.http_port,args.static_data_dir)
    wait_exit.wait_exit_callback(lambda: server.stop())
    server.run()

if __name__ == "__main__":
    main()