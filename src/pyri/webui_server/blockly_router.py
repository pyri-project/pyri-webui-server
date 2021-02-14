import sanic.response as res
from sanic.exceptions import abort
import re
from pyri.plugins.blockly import get_all_blockly_blocks

class PryiWebUIBlocklyBlocksRouteHandler:

    def __init__(self):
        
        all_blocks = get_all_blockly_blocks()

        self._blocks = dict()
        for b in all_blocks.values():
            block_safe_name = re.sub('[^0-9a-zA-Z_]+', '', b.name)   
            self._blocks[block_safe_name] = b             

    async def handler(self, request, path=None):
        if path is None:
            abort(404)

        if "/" in path or "\\" in path:
            abort(404)

        blockdef_match = re.match("^blockdef_([0-9a-zA-Z_]+)\\.json$",path)
        if blockdef_match is not None:
            block_name = blockdef_match.group(1)
            block = self._blocks.get(block_name, None)
            if block is None:
                abort(404)
            return res.json(block.json)

        blockpygen_match = re.match("^blockpygen_([0-9a-zA-Z_]+)\\.js$",path)
        if blockpygen_match is not None:
            block_name = blockpygen_match.group(1)
            block = self._blocks.get(block_name, None)
            if block is None:
                abort(404)
            return res.raw(block.python_generator,content_type="text/javascript")

        abort(404)

        