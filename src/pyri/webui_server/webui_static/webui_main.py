import RobotRaconteur as RR
from RobotRaconteur.RobotRaconteurPythonUtil import WebFuture
import micropip
import json
import io
import sys
import zipfile
import os

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

async def main():
    config_json_text = (await read_url("/config")).read()
    config = json.loads(config_json_text)
    await load_wheels(config["wheels"])

    print(os.listdir("/lib/python3.8/site-packages"))

for __p in sys.path:
    if __p.endswith('site-packages'):
        WHEEL_BASE = __p
        break

loop = RR.WebLoop()
loop.call_soon(main())