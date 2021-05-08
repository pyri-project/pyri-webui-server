import sanic.response as res
from sanic.exceptions import abort
import re
from pyri.plugins.sandbox_functions import get_all_plugin_sandbox_functions
import importlib_resources
import json
import inspect

class PryiWebUISandboxFunctionsRouteHandler:

    def __init__(self):
        
        all_functions = get_all_plugin_sandbox_functions()

        self._functions = dict()
        for f,v in all_functions.items():
            function_safe_name = re.sub('[^0-9a-zA-Z_]+', '', f)   
            self._functions[function_safe_name] = v

    def get_function_names(self):
        return list(self._functions.keys())

    def get_function_signatures(self):
        ret_list = []
        for f,v in self._functions.items():
            ret_list.append({
                "name": f,
                "full_signature": v.__name__ + str(inspect.signature(v))
            })

        return {"function_signatures": ret_list}

    def get_all_functions(self):
        ret_list = []
        for f,v in self._functions.items():
            ret_list.append({
                "name": f,
                "full_signature": v.__name__ + str(inspect.signature(v)),
                "docstring": inspect.getdoc(v) or ""
            })

        return {"all_functions": ret_list}

    async def handler(self, request, path=None):
        if path is None:
            abort(404)

        if "/" in path or "\\" in path:
            abort(404)

        if path == "function_signatures.json":
            return res.json(self.get_function_signatures())

        if path == "all_functions.json":
            return res.json(self.get_all_functions())

        sandbox_function_match = re.match("^sandbox_function_([0-9a-zA-Z_]+)\\.json$",path)
        if sandbox_function_match is not None:
            function_name = sandbox_function_match.group(1)
            f = self._functions.get(function_name, None)
            if f is None:
                abort(404)

            f_info = {
                "name": f.__name__,
                "signature": str(inspect.signature(f)),
                "docstring": inspect.getdoc(f) or ""
            }
            #return res.raw(block.json, content_type = "application/json")
            return res.json(f_info)

        abort(404)

        