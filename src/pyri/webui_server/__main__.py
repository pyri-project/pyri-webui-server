from .webui_server import PyriWebUIServer
import argparse

def main():
    parser = argparse.ArgumentParser(description="PyRI WebUI Server")
    parser.add_argument("--http-host", type=str, default='0.0.0.0',help="Host to listen for connections")
    parser.add_argument("--http-port",type=int,default=8000,help="Port to listen for connections")

    args, _ = parser.parse_known_args()

    server = PyriWebUIServer(args.http_host,args.http_port)
    server.run()

if __name__ == "__main__":
    main()