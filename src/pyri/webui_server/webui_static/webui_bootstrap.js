
async function webui_bootstrap(){
    let pyodide = await loadPyodide();
    await pyodide.loadPackage(["numpy","micropip","Jinja2","RobotRaconteur","pyyaml"]);
    const response = await fetch("webui_bootstrap.py", {cache: "no-store"});
    const webui_bootstrap_py = await response.text();
    pyodide.runPython(webui_bootstrap_py)
}

webui_bootstrap();
