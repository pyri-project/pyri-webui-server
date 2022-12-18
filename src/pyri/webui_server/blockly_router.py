import sanic.response as res
from sanic.exceptions import NotFound
import re
from pyri.plugins.blockly import get_all_blockly_blocks, get_all_blockly_categories, blockly_block_to_json
import importlib_resources
import json

class PryiWebUIBlocklyBlocksRouteHandler:

    def __init__(self):
        
        pass
         

    def get_block_names(self):
        return list(get_all_blockly_blocks().keys())

    def get_toolbox_json(self):
        blocks_by_category=dict()
        all_blocks = get_all_blockly_blocks()

        for b in all_blocks.values():
            if b.category not in blocks_by_category:
                blocks_by_category[b.category] = [b]
            else:
                blocks_by_category[b.category].append(b)

        toolbox_json_text = importlib_resources.files(__package__).joinpath('blockly_standard_toolbox.json').read_text()
        toolbox_json = json.loads(toolbox_json_text)

        cat = get_all_blockly_categories()
        for c in cat.values():
            c_json = c.blockly_json
            if isinstance(c_json,str):
                c_json = json.loads(c_json)
            c_name = c_json["name"]
            if c_name in blocks_by_category:
                contents = []
                for b in blocks_by_category[c_name]:
                    contents.append(
                        {
                            "kind": "block",
                            "type": b.name
                        }
                    )
                c_json["contents"] = contents
            toolbox_json["contents"].append(c_json)
        return json.dumps(toolbox_json)

    def get_blocks_json(self):
        all_blocks = get_all_blockly_blocks()
        all_blocks_json = []
        for b in all_blocks.values():
            all_blocks_json.append(blockly_block_to_json(b))
        return json.dumps(all_blocks_json)


    async def handler(self, request, path=None):
        if path is None:
            raise NotFound(path)

        if "/" in path or "\\" in path:
            raise NotFound(path)

        if path == "toolbox.json":
            
            # TODO: add additional blocks and categories
            return res.raw(self.get_toolbox_json(), content_type = "application/json")

        if path == "pyri_blocks.json":
            return res.raw(self.get_blocks_json(), content_type = "application/json")


        # blockdef_match = re.match("^blockdef_([0-9a-zA-Z_]+)\\.json$",path)
        # if blockdef_match is not None:
        #     block_name = blockdef_match.group(1)
        #     block = self._blocks.get(block_name, None)
        #     if block is None:
        #         abort(404)
        #     return res.raw(json.dumps(block.blockly_json), content_type = "application/json")

        # blockpygen_match = re.match("^blockpygen_([0-9a-zA-Z_]+)\\.js$",path)
        # if blockpygen_match is not None:
        #     block_name = blockpygen_match.group(1)
        #     block = self._blocks.get(block_name, None)
        #     if block is None:
        #         abort(404)
        #     return res.raw(block.python_generator,content_type="text/javascript")

        raise NotFound()

        