import sanic.response as res
from sanic.exceptions import abort
import re
from pyri.plugins.blockly import get_all_blockly_blocks, get_all_blockly_categories
import importlib_resources
import json

class PryiWebUIBlocklyBlocksRouteHandler:

    def __init__(self):
        
        all_blocks = get_all_blockly_blocks()

        self._blocks = dict()
        for b in all_blocks.values():
            block_safe_name = re.sub('[^0-9a-zA-Z_]+', '', b.name)   
            self._blocks[block_safe_name] = b   

    def get_block_names(self):
        return list(self._blocks.keys())

    def get_toolbox_json(self):
        toolbox_json_text = importlib_resources.files(__package__).joinpath('blockly_standard_toolbox.json').read_text()
        toolbox_json = json.loads(toolbox_json_text)

        cat = get_all_blockly_categories()
        for c in cat.values():
            toolbox_json["contents"].append(json.loads(c.json))
        return json.dumps(toolbox_json)


    async def handler(self, request, path=None):
        if path is None:
            abort(404)

        if "/" in path or "\\" in path:
            abort(404)

        if path == "toolbox.json":
            
            # TODO: add additional blocks and categories
            return res.raw(self.get_toolbox_json(), content_type = "application/json")

        blockdef_match = re.match("^blockdef_([0-9a-zA-Z_]+)\\.json$",path)
        if blockdef_match is not None:
            block_name = blockdef_match.group(1)
            block = self._blocks.get(block_name, None)
            if block is None:
                abort(404)
            return res.raw(block.json, content_type = "application/json")

        blockpygen_match = re.match("^blockpygen_([0-9a-zA-Z_]+)\\.js$",path)
        if blockpygen_match is not None:
            block_name = blockpygen_match.group(1)
            block = self._blocks.get(block_name, None)
            if block is None:
                abort(404)
            return res.raw(block.python_generator,content_type="text/javascript")

        abort(404)

        