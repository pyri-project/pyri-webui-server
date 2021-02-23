import RobotRaconteur as RR
from RobotRaconteur.RobotRaconteurPythonUtil import WebFuture
import json
import io
import sys
import zipfile
import os
import importlib

from js import XMLHttpRequest



async def read_url(url):

    # Based on pyodide micropip module

    req = XMLHttpRequest.new()
    req.open("GET", url, True)
    req.responseType = "arraybuffer"

    p = WebFuture()

    def callback(e):
        if req.readyState == 4:
            p.handler(io.BytesIO(req.response),None)

    req.onreadystatechange = callback
    req.send(None)

    return await p

async def download_install_webui_wheel(wheel_name):
    
    wheel_io = await read_url(f"/wheels/{wheel_name}.whl")
    print(wheel_io)
    with zipfile.ZipFile(wheel_io) as zf:
        zf.extractall(WHEEL_BASE)

async def load_wheels(wheels):
    for w in wheels:
        await download_install_webui_wheel(w)

    importlib.invalidate_caches()

async def bootstrap():
    config_json_text = (await read_url("/config")).read()
    config = json.loads(config_json_text)
    await load_wheels(config["wheels"])

    from pyri.webui_browser import PyriWebUIBrowser

    pyri_webui = PyriWebUIBrowser(loop, config)
    loop.call_soon(pyri_webui.run())


for __p in sys.path:
    if __p.endswith('site-packages'):
        WHEEL_BASE = __p
        break

loop = RR.WebLoop()
loop.call_soon(bootstrap())