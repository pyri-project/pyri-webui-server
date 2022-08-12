// $(document).ready(function() {
//     var workspace = Blockly.inject('blocklyDiv',
//         {media: './blockly/media/',
//          toolbox: document.getElementById('toolbox')});
// });


var blockly_workspace = null

async function retrieveToolboxJSON()
{
    var response = await fetch("blockly_blocks/toolbox.json", {cache: "no-store"});
    if (response.status != 200)
    {
        throw new Error("Could not read toolbox json");
    }
    const toolbox_json_text = await response.text()
    const toolbox_json = JSON.parse(toolbox_json_text)
    //Blockly.mainWorkspace.updateToolbox(toolbox_json)
    return toolbox_json
}

async function loadBlockly()
{
    // Inject Blockly workspace
    var blocklyArea = document.getElementById('blocklyArea');
    var blocklyDiv = document.getElementById('blocklyDiv');
    const toolbox_json = await retrieveToolboxJSON()
    var workspace = Blockly.inject(blocklyDiv,
        {
            toolbox: toolbox_json,
            zoom:
                {
                    controls: true,
                    wheel: false,
                    startScale: 1.0,
                    maxScale: 3,
                    minScale: 0.3,
                    scaleSpeed: 1.2
                },
            trashcan: true,  
            maxTrashcanContents: 32, // Default 32
            css:true,
            horizontalLayout: false, // Defaul: false
            move:
                {
                    scrollbars: true,
                    drag: true,
                    wheel: false
                },
            media: "/deps/blockly/media/"
        });

    
    // Blockly.Xml.domToWorkspace(document.getElementById('startBlocks'), workspace);
    
    // For resizable workspace
    function onresize_cb(){
        blocklyDiv.style.width = parent_div.offsetWidth-5 + 'px';
        blocklyDiv.style.height = parent_div.offsetHeight-5 + 'px';
        Blockly.svgResize(workspace);
    }
    var table_blockly = document.getElementById('table_BlocklyWorkspace');
    var parent_div = table_blockly.parentNode;
    // console.log(parent_div);
    new ResizeObserver(onresize_cb).observe(parent_div);
    onresize_cb();
    Blockly.svgResize(workspace);


    await loadBlocks()

    blockly_workspace = workspace
    

    // Realtime Code Generation
    /*function myUpdateFunction(event) {
        // var code_js = Blockly.JavaScript.workspaceToCode(workspace);
        // document.getElementById('textareaBlocklyJS').value = code_js;

        var code_py = Blockly.Python.workspaceToCode(workspace);
        document.getElementById('textareaBlocklyPy').value = code_py;
    }
    workspace.addChangeListener(myUpdateFunction);*/


    // var executeBlockly_btn = $('#execute_blockly_btn');
    // executeBlockly_btn.click(function(){
    //     // console.log("Blockly Execute button is clicked!");
    //     // document.getElementById('textareaBlocklyPy').value += "\nBlockly Execute button is clicked!\n";
    //     print_div("<br>Blockly Execute button is clicked!<br><br>");

    //     async function run_blockly(code_text){
    //         // await languagePluginLoader;
    //         // await pyodide.loadPackage(["numpy"]);

    //         // const response_webcam = await fetch("./RR-web_browser-Webcam/client_webcam.py", {cache: "no-store"});
    //         // const client_webcam_py = await response_webcam.text();
    //         // pyodide.runPython(client_webcam_py);
    //         pyodide.runPython(code_text);
    //     }

    //     // code_text = "from js import print_div\nprint_div('HELLO WORLD')";
    //     // code_text = "print_div('HELLO WORLD')\njog_joints(1,+1)";
    //     var code_text = Blockly.Python.workspaceToCode(workspace);
        
    //     run_blockly(code_text);
    // });
};

async function loadBlocks()
{
    var response = await fetch("blockly_blocks/pyri_blocks.json", {cache: "no-store"});
    if (response.status != 200)
    {
        throw new Error("Could not read blockly blocks");
    }
    const blocks_json_text = await response.text();
    const blocks_json = JSON.parse(blocks_json_text);

    new_blocks = []
    blocks_json.forEach(b => {
        new_blocks.push(b.blockly_json);
    })
    Blockly.defineBlocksWithJsonArray(new_blocks)
}

function setBlocklyJson(procedure_json)
{
    Blockly.serialization.workspaces.load(procedure_json, blockly_workspace);
}

function getBlocklyJson()
{
    return Blockly.serialization.workspaces.save(blockly_workspace)
}

function setBlocklyJsonText(procedure_json_text)
{
    setBlocklyJson(JSON.parse(procedure_json_text));
}

function getBlocklyJsonText()
{
    return JSON.stringify(getBlocklyJson());
}

function blocklyReady()
{
    return blockly_workspace !== null
}



$(document).ready(function() {
    loadBlockly()
});