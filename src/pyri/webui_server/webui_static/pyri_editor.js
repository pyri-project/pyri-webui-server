
var editor = null

function loadEditor() {
    // Based on https://jsfiddle.net/developit/bwgkr6uq/ which just works but is based on unpkg.com.
    // Provided by loader.min.js.
    require.config({ paths: { 'vs': '/deps/monaco-editor/min/vs' }});
    window.MonacoEnvironment = { getWorkerUrl: () => proxy };
    let proxy = URL.createObjectURL(new Blob([`
        self.MonacoEnvironment = {
            baseUrl: '/deps/monaco-editor/min'
        };
        importScripts('/deps/monaco-editor/min/vs/base/worker/workerMain.min.js');
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

function gotoline()
{
    editor.trigger('','editor.action.gotoLine')
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

function deleteLeft()
{
    editor.trigger('keyboard', 'deleteLeft')
}

function deleteRight()
{
    editor.trigger('keyboard', 'deleteRight')
}

function deleteLine()
{
    editor.trigger('','editor.action.deleteLines')
}

function moveLineUp()
{
    editor.trigger('','editor.action.moveLinesUpAction')
}

function moveLineDown()
{
    editor.trigger('','editor.action.moveLinesDownAction')
}

function newline()
{
    editor.trigger('keyboard', 'type', {text: "\n"});
}

function selectMore()
{
    editor.trigger('','editor.action.smartSelect.expand')
}

function selectLess()
{
    editor.trigger('','editor.action.smartSelect.shrink')
}

function home()
{
    pos = editor.getPosition()
    // TODO: Find first non-whitespace character
    pos.column = 0
    editor.setPosition(pos)
}

function end()
{
    pos = editor.getPosition()
    // TODO: Find actual length of line
    pos.column = 10000
    editor.setPosition(pos)
}

function commentLine()
{
    editor.trigger('','editor.action.commentLine')
}

function removeCommentLine()
{
    editor.trigger('','editor.action.removeCommentLine')
}

$(document).ready(function() {
    loadEditor()
});