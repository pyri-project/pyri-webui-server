import importlib_resources
import sanic.response as res
from sanic.exceptions import abort
import mimetypes
import re

class PyriWebUIResourceRouteHandler:
    
    def __init__(self, package):
        self._package = package

    async def handler(self,request,path=None):
        if path is not None:
            assert ".." not in path, "relative paths not supported"
            assert "\\" not in path, "path must not contain backslash"
            path_parts = path.split("/")
            for p in path_parts:
                assert re.match(r'^[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)*$',p), "Invalid file path"
        else:
            path = "index.html"
        
        try:
            path2 = importlib_resources.files(self._package) / 'webui_static' / path
            ret = path2.read_bytes()
        except FileNotFoundError:
            abort(404)

        print(f"Got request! {path}")
        mimetype,_=mimetypes.guess_type(path)
        #if path.endswith(".js"):
        #    mimetype = "text/javascript"
        print(mimetype)
        return res.raw(ret,content_type=mimetype)