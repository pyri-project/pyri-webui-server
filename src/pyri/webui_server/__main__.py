from .webui_server import PyriWebUIServer
import argparse

def main():
    parser = argparse.ArgumentParser(description="PyRI WebUI Server")
    parser.add_argument('--device-manager-url', type=str, default=None,required=True,help="Robot Raconteur URL for device manager service (required)")
    parser.add_argument("--http-host", type=str, default='0.0.0.0',help="Host to listen for connections")
    parser.add_argument("--http-port",type=int,default=8000,help="Port to listen for connections")
    parser.add_argument("--wheels-dir",type=str,default=None,help="Directory to store Python Wheel files for WebUI Pyodide")

    args, _ = parser.parse_known_args()

    server = PyriWebUIServer(args.device_manager_url,args.http_host,args.http_port,args.wheels_dir)
    server.run()

if __name__ == "__main__":
    main()