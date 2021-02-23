
async function webui_bootstrap(){
    await languagePluginLoader;
    await pyodide.loadPackage(["numpy","micropip"]);
    const response = await fetch("webui_bootstrap.py", {cache: "no-store"});
    const webui_bootstrap_py = await response.text();
    pyodide.runPython(webui_bootstrap_py)
}
webui_bootstrap();
