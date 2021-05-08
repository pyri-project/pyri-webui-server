
var editor = null

function loadEditor() {
    // Based on https://jsfiddle.net/developit/bwgkr6uq/ which just works but is based on unpkg.com.
    // Provided by loader.min.js.
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.20.0/min/vs' }});
    window.MonacoEnvironment = { getWorkerUrl: () => proxy };
    let proxy = URL.createObjectURL(new Blob([`
        self.MonacoEnvironment = {
            baseUrl: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.20.0/min'
        };
        importScripts('https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.20.0/min/vs/base/worker/workerMain.min.js');
    `], { type: 'text/javascript' }));
    require(["vs/editor/editor.main"], function () {
        editor = monaco.editor.create(document.getElementById('container'), {
            value: "",
            language: 'python',
            theme: 'vs-dark',
            automaticLayout: true
        });
    });
}

function getValue()
{
    return editor.getModel().getValue()
}

function setValue(program_text)
{
    editor.getModel().setValue(program_text)
}

function editorReady()
{
    return editor !== null
}

function indentLines()
{
    editor.trigger('', 'editor.action.indentLines', null)
}

function outdentLines()
{
    editor.trigger('', 'editor.action.outdentLines', null)
}

function cursorRight()
{
    pos = editor.getPosition()
    pos.column = pos.column + 1
    editor.setPosition(pos)
}

function cursorLeft()
{
    pos = editor.getPosition()
    pos.column = pos.column - 1
    editor.setPosition(pos)
}

function cursorUp()
{
    pos = editor.getPosition()
    pos.lineNumber = pos.lineNumber - 1
    editor.setPosition(pos)
}

function cursorDown()
{
    pos = editor.getPosition()
    pos.lineNumber = pos.lineNumber + 1
    editor.setPosition(pos)
}


function replace()
{
    editor.trigger('',"editor.action.startFindReplaceAction",null)
}

function find()
{
    editor.trigger('',"actions.find",null)
}

function undo()
{
    editor.trigger('',"undo",null)
}

function redo()
{
    editor.trigger('',"redo",null)
}

function insertText(text)
{
    editor.trigger('keyboard', 'type', {text: text});
}

$(document).ready(function() {
    loadEditor()
});