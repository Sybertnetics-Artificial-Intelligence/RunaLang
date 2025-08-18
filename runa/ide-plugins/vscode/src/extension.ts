import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';
import { spawn } from 'child_process';
import * as path from 'path';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    // Language server setup
    const config = vscode.workspace.getConfiguration('runa');
    const lspEnabled = config.get('languageServer.enabled', true);
    
    if (lspEnabled) {
        startLanguageServer();
    }
    
    // Register commands
    const commands = [
        vscode.commands.registerCommand('runa.compileFile', compileFile),
        vscode.commands.registerCommand('runa.runFile', runFile),
        vscode.commands.registerCommand('runa.formatDocument', formatDocument),
        vscode.commands.registerCommand('runa.restartLanguageServer', restartLanguageServer)
    ];
    
    commands.forEach(command => context.subscriptions.push(command));
    
    // Register document formatter
    context.subscriptions.push(
        vscode.languages.registerDocumentFormattingEditProvider('runa', {
            provideDocumentFormattingEdits(document: vscode.TextDocument): vscode.TextEdit[] {
                return formatRunaDocument(document);
            }
        })
    );
    
    // Register hover provider
    context.subscriptions.push(
        vscode.languages.registerHoverProvider('runa', {
            provideHover(document: vscode.TextDocument, position: vscode.Position): vscode.Hover | null {
                return provideRunaHover(document, position);
            }
        })
    );
    
    // Register completion provider
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider('runa', {
            provideCompletionItems(document: vscode.TextDocument, position: vscode.Position): vscode.CompletionItem[] {
                return provideRunaCompletions(document, position);
            }
        }, '.', ' ')
    );
    
    // Status bar item
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.text = "$(check) Runa";
    statusBarItem.tooltip = "Runa Language Support Active";
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
    
    console.log('Runa Language Support activated');
}

function startLanguageServer() {
    const config = vscode.workspace.getConfiguration('runa');
    const host = config.get('languageServer.host', 'localhost');
    const port = config.get('languageServer.port', 8080);
    
    const serverOptions: ServerOptions = {
        host: host,
        port: port
    };
    
    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'runa' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.runa')
        }
    };
    
    client = new LanguageClient(
        'runaLanguageServer',
        'Runa Language Server',
        serverOptions,
        clientOptions
    );
    
    client.start();
}

async function compileFile() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor || activeEditor.document.languageId !== 'runa') {
        vscode.window.showErrorMessage('No active Runa file to compile');
        return;
    }
    
    const filePath = activeEditor.document.fileName;
    const outputChannel = vscode.window.createOutputChannel('Runa Compiler');
    
    try {
        outputChannel.clear();
        outputChannel.show();
        outputChannel.appendLine(`Compiling: ${filePath}`);
        
        // Use Rust-based Runa CLI instead of Python
        const runaCli = getRunaCliPath();
        const runaProcess = spawn(runaCli, ['compile', filePath], {
            cwd: vscode.workspace.rootPath
        });
        
        python.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });
        
        python.stderr.on('data', (data) => {
            outputChannel.append(data.toString());
        });
        
        python.on('close', (code) => {
            if (code === 0) {
                outputChannel.appendLine('\\nCompilation successful!');
                vscode.window.showInformationMessage('Runa file compiled successfully');
            } else {
                outputChannel.appendLine(`\\nCompilation failed with code ${code}`);
                vscode.window.showErrorMessage('Compilation failed');
            }
        });
        
    } catch (error) {
        outputChannel.appendLine(`Error: ${error}`);
        vscode.window.showErrorMessage(`Compilation error: ${error}`);
    }
}

async function runFile() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor || activeEditor.document.languageId !== 'runa') {
        vscode.window.showErrorMessage('No active Runa file to run');
        return;
    }
    
    const filePath = activeEditor.document.fileName;
    const outputChannel = vscode.window.createOutputChannel('Runa Runner');
    
    try {
        outputChannel.clear();
        outputChannel.show();
        outputChannel.appendLine(`Running: ${filePath}`);
        
        // Use Rust-based Runa CLI instead of Python
        const runaCli = getRunaCliPath();
        const runaProcess = spawn(runaCli, ['run', filePath], {
            cwd: vscode.workspace.rootPath
        });
        
        python.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });
        
        python.stderr.on('data', (data) => {
            outputChannel.append(data.toString());
        });
        
        python.on('close', (code) => {
            outputChannel.appendLine(`\\nProcess exited with code ${code}`);
        });
        
    } catch (error) {
        outputChannel.appendLine(`Error: ${error}`);
        vscode.window.showErrorMessage(`Runtime error: ${error}`);
    }
}

async function formatDocument() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor || activeEditor.document.languageId !== 'runa') {
        vscode.window.showErrorMessage('No active Runa file to format');
        return;
    }
    
    const edits = formatRunaDocument(activeEditor.document);
    if (edits.length > 0) {
        const edit = new vscode.WorkspaceEdit();
        edit.set(activeEditor.document.uri, edits);
        await vscode.workspace.applyEdit(edit);
        vscode.window.showInformationMessage('Document formatted');
    }
}

async function restartLanguageServer() {
    if (client) {
        await client.stop();
    }
    startLanguageServer();
    vscode.window.showInformationMessage('Language server restarted');
}

function formatRunaDocument(document: vscode.TextDocument): vscode.TextEdit[] {
    const edits: vscode.TextEdit[] = [];
    let indentLevel = 0;
    
    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        const text = line.text;
        const trimmed = text.trim();
        
        if (trimmed.length === 0) {
            continue;
        }
        
        // Decrease indent for closing keywords
        if (trimmed === 'end' || trimmed === 'else' || trimmed === 'finally' || 
            trimmed === 'catch' || trimmed.startsWith('case ')) {
            indentLevel = Math.max(0, indentLevel - 1);
        }
        
        // Calculate expected indentation
        const expectedIndent = '    '.repeat(indentLevel);
        const currentIndent = text.match(/^\\s*/)?.[0] || '';
        
        // Apply formatting if needed
        if (currentIndent !== expectedIndent) {
            const range = new vscode.Range(
                new vscode.Position(i, 0),
                new vscode.Position(i, currentIndent.length)
            );
            edits.push(vscode.TextEdit.replace(range, expectedIndent));
        }
        
        // Increase indent for opening keywords
        if (trimmed.endsWith(':') || trimmed.startsWith('if ') || 
            trimmed.startsWith('for ') || trimmed.startsWith('while ') ||
            trimmed.startsWith('function ') || trimmed.startsWith('try') ||
            trimmed.startsWith('match ') || trimmed.startsWith('case ')) {
            indentLevel++;
        }
    }
    
    return edits;
}

function provideRunaHover(document: vscode.TextDocument, position: vscode.Position): vscode.Hover | null {
    const range = document.getWordRangeAtPosition(position);
    if (!range) {
        return null;
    }
    
    const word = document.getText(range);
    const hoverText = getHoverText(word);
    
    if (hoverText) {
        return new vscode.Hover(new vscode.MarkdownString(hoverText));
    }
    
    return null;
}

function getHoverText(word: string): string | null {
    const keywords: { [key: string]: string } = {
        'function': 'Define a function that can be called with parameters',
        'let': 'Declare a variable and assign a value to it',
        'if': 'Execute code conditionally based on a boolean expression',
        'for': 'Loop through items in a collection',
        'while': 'Loop while a condition is true',
        'match': 'Pattern matching statement for complex conditionals',
        'try': 'Handle potential errors in a code block',
        'async': 'Define an asynchronous function',
        'await': 'Wait for an asynchronous operation to complete',
        'import': 'Import functionality from another module',
        'export': 'Export functionality to other modules'
    };
    
    const builtins: { [key: string]: string } = {
        'print': 'Print a message to the console',
        'input': 'Get input from the user',
        'length': 'Get the length of a collection or string',
        'type': 'Get the type of a value',
        'convert': 'Convert a value to a different type',
        'range': 'Create a range of numbers',
        'map': 'Apply a function to each item in a collection',
        'filter': 'Filter items in a collection based on a condition',
        'sort': 'Sort items in a collection'
    };
    
    if (keywords[word]) {
        return `**${word}** (keyword)\\n\\n${keywords[word]}`;
    }
    
    if (builtins[word]) {
        return `**${word}** (built-in function)\\n\\n${builtins[word]}`;
    }
    
    return null;
}

function provideRunaCompletions(document: vscode.TextDocument, position: vscode.Position): vscode.CompletionItem[] {
    const completions: vscode.CompletionItem[] = [];
    
    // Keywords
    const keywords = [
        'function', 'let', 'if', 'else', 'for', 'while', 'do', 'return',
        'match', 'case', 'try', 'catch', 'finally', 'throw', 'async', 'await',
        'import', 'export', 'from', 'as', 'and', 'or', 'not', 'in', 'is',
        'true', 'false', 'null', 'end'
    ];
    
    keywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword, vscode.CompletionItemKind.Keyword);
        item.documentation = new vscode.MarkdownString(`Runa keyword: **${keyword}**`);
        completions.push(item);
    });
    
    // Built-in functions
    const builtins = [
        'print', 'input', 'length', 'type', 'convert', 'parse', 'format',
        'range', 'enumerate', 'zip', 'map', 'filter', 'reduce', 'sort',
        'reverse', 'split', 'join', 'replace', 'contains', 'starts_with',
        'ends_with', 'uppercase', 'lowercase', 'trim'
    ];
    
    builtins.forEach(builtin => {
        const item = new vscode.CompletionItem(builtin, vscode.CompletionItemKind.Function);
        item.documentation = new vscode.MarkdownString(`Built-in function: **${builtin}**`);
        completions.push(item);
    });
    
    // Types
    const types = [
        'number', 'string', 'boolean', 'list', 'dictionary', 'function',
        'optional', 'union', 'intersection', 'any', 'void'
    ];
    
    types.forEach(type => {
        const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
        item.documentation = new vscode.MarkdownString(`Runa type: **${type}**`);
        completions.push(item);
    });
    
    return completions;
}

export function deactivate(): Thenable<void> | undefined {
    if (client) {
        return client.stop();
    }
    return undefined;
}