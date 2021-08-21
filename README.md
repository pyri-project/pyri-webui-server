<p align="center">
<img src="./doc/figures/pyri_logo_web.svg" height="200"/>
</p>

## PyRI Open Source Teach Pendant WebUI Server

This package is part of the PyRI project. See https://github.com/pyri-project/pyri-core#documentation for documentation. This package is included in the `pyri-robotics-superpack` Conda package.

The `pyri-webui-server` package contains the WebUI HTTP server service, which is the server for the WebUI browser.

## Service

Standalone service command line example:

```
pyri-webui-server
```

The `pyri-variable-storage` and `pyri-device-manager` services must be running before use.

Command line options:

| Option | Type | Required | Description |
| ---    | ---  | ---      | ---         |
| `--device-manager-url=` | Robot Raconteur URL | Yes | Robot Raconteur URL of device manager service to pass to the web browser |
| `--http-host=` | Hostname | No | The hostname to start the server on. Defaults to `0.0.0.0` for all local adapters |
| `--http-port=` | uint16 | No | The TCP port to listen for incoming HTTP connections. Defaults to 8000 |
| `--static-data-dir=` | Directory | No | Directory to store static data |

This service is started automatically by `pyri-core`, and does not normally need to be started manually.

This service does not run a Robot Raconteur node.

The `--device-manager-url=` is passed to the web browser, to allow the web application to connect to the device manager service. This URL is run through a Jinja2 template expansion before being used. This allows the web browser to use the current hostname or IP address to connect to the device manager. This assumes that the device manager and WebUI server are running on the same computer.

The WebUI adds the `--web-ui-device-manager-url=` command line option to `pyri-core`. This option has the default value:

```
rr+tcp://{{ HOSTNAME }}:59902?service=device_manager
```

This URL will work correctly in most cases, and the user does not need to worry about this option.

## Static Data Directory

The WebUI requires a large number of static files to be loaded from the WebUI HTTP server. These files fall into the rough categories:

* Pyodide Runtime
* JavaScript library dependencies
* WebUI Python Wheels

The `pyri-robotics-superpack` includes all these files automatically.

If the WebUI is cloned, it is necessary to install these dependencies. The location of the static data directory is set using the `PYRI_WEBUI_STATIC_DATA_DIR` environmental variable. If not set, the location defaults to the following on different platforms:

| Platform | Directory |
| ---      | ---       |
| Windows | %LOCALAPPDATA%\pyri-project\pyri-webui-service |
| Linux | ~/.local/share/pyri-webui-server |

The static data directory has three subdirectories:

| Directory | Contents |
| ---       | ---      |
| robotraconteur_pyodide | Robot Raconteur Pyodide runtime files |
| deps | JavaScript dependencies, contained in a `node_modules` NPM directory format |
| wheels | WebUI Python Wheels installed into the WebUI Pyodide environment during startup |

Configuring the static data is done automatically by the `init_workspace_packages` script in the developers script repo. See https://github.com/pyri-project/pyri-core/blob/master/doc/development_env_setup.md#clone-and-initialize . Wheels can be installed using the `install_webui_browser_wheels.py` script.

## Acknowledgment

This work was supported in part by Subaward No. ARM-TEC-19-01-F-24 from the Advanced Robotics for Manufacturing ("ARM") Institute under Agreement Number W911NF-17-3-0004 sponsored by the Office of the Secretary of Defense. ARM Project Management was provided by Christopher Adams. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of either ARM or the Office of the Secretary of Defense of the U.S. Government. The U.S. Government is authorized to reproduce and distribute reprints for Government purposes, notwithstanding any copyright notation herein.

This work was supported in part by the New York State Empire State Development Division of Science, Technology and Innovation (NYSTAR) under contract C160142. 

![](doc/figures/arm_logo.jpg) ![](doc/figures/nys_logo.jpg)

PyRI is developed by Rensselaer Polytechnic Institute, Wason Technology, LLC, and contributors.
