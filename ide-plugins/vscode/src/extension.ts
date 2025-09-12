import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions } from 'vscode-languageclient/node';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';

let client: LanguageClient | undefined;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('Activating Runa Language Support...');
    
    // Create output channel
    outputChannel = vscode.window.createOutputChannel('Runa');
    outputChannel.appendLine('=== RUNA EXTENSION ACTIVATION STARTED ===');
    context.subscriptions.push(outputChannel);
    
    // Language server is disabled by default to prevent networking issues
    const config = vscode.workspace.getConfiguration('runa');
    if (config.get('languageServer.enabled', false)) {
        outputChannel.appendLine('Language server enabled in settings - attempting to start');
        initializeLanguageServer(context);
    } else {
        outputChannel.appendLine('Language server disabled - using basic syntax highlighting only');
    }
    
    // Register all commands
    registerCommands(context);
    
    // Register language providers
    registerLanguageProviders(context);
    
    // Create status bar item
    createStatusBarItem(context);
    
    // Listen for configuration changes
    vscode.workspace.onDidChangeConfiguration(event => {
        if (event.affectsConfiguration('runa')) {
            handleConfigurationChange();
        }
    });
    
    outputChannel.appendLine('Runa Language Support activated successfully');
    vscode.window.showInformationMessage('Runa Language Support is now active!');
}

function initializeLanguageServer(context: vscode.ExtensionContext) {
    outputChannel.appendLine('🎯 Initializing Runa Language Server...');
    
    try {
        // Find the runa-lsp executable
        const lspPath = findLspExecutable();
        if (!lspPath) {
            outputChannel.appendLine('❌ Runa LSP executable not found');
            showLspNotFoundMessage();
            return;
        }
        
        outputChannel.appendLine(`✅ Found Runa LSP at: ${lspPath}`);
        
        // Configure server options to use the LSP executable
        const serverOptions: ServerOptions = {
            command: lspPath,
            args: [],
            options: {
                env: { ...process.env }
            }
        };
        
        // Configure client options
        const clientOptions: LanguageClientOptions = {
            documentSelector: [
                { scheme: 'file', language: 'runa' },
                { scheme: 'untitled', language: 'runa' }
            ],
            synchronize: {
                fileEvents: vscode.workspace.createFileSystemWatcher('**/*.runa')
            },
            outputChannel: outputChannel,
            initializationOptions: {},
            initializationFailedHandler: (error) => {
                outputChannel.appendLine(`❌ LSP initialization failed: ${error.message}`);
                return false;
            }
        };
        
        // Create and start the language client
        client = new LanguageClient(
            'runaLanguageServer',
            'Runa Language Server',
            serverOptions,
            clientOptions
        );
        
        outputChannel.appendLine('🚀 Starting Runa Language Server...');
        
        client.start().then(() => {
            outputChannel.appendLine('✅ Runa Language Server started successfully');
            vscode.window.showInformationMessage(
                '🎉 Runa Language Server is now running! Enjoy intelligent code assistance.',
                'Open Output'
            ).then(selection => {
                if (selection === 'Open Output') {
                    outputChannel.show();
                }
            });
        }).catch(error => {
            outputChannel.appendLine(`❌ Failed to start Runa Language Server: ${error.message}`);
            showLspErrorMessage(error);
        });
        
        context.subscriptions.push(client);
        
    } catch (error) {
        outputChannel.appendLine(`❌ Error initializing language server: ${error instanceof Error ? error.message : String(error)}`);
        showLspErrorMessage(error);
    }
}

function convertWindowsPathToWSL(windowsPath: string): string {
    // Convert Windows paths like d:\path\to\file to WSL paths like /mnt/d/path/to/file
    // This handles the case where VSCode is running in WSL but finds Windows paths
    if (windowsPath.match(/^[a-zA-Z]:\\/)) {
        // Windows absolute path - convert to WSL
        const drive = windowsPath.charAt(0).toLowerCase();
        const restOfPath = windowsPath.slice(3).replace(/\\/g, '/');
        return `/mnt/${drive}/${restOfPath}`;
    }
    // If it's already a Unix-style path or relative path, return as-is
    return windowsPath;
}

function findLspExecutable(): string | null {
    // Look for runa-lsp in several locations
    const possiblePaths = [
        // WSL/Linux paths (for development in WSL environment)
        '/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/lsp-server/target/release/runa-lsp',
        '/mnt/d/SybertneticsUmbrella/SybertneticsAISolutions/MonoRepo/runa/lsp-server/target/debug/runa-lsp',
        // Relative to extension (development) - convert Windows paths to WSL if needed
        convertWindowsPathToWSL(path.join(__dirname, '..', '..', '..', 'lsp-server', 'target', 'release', 'runa-lsp')),
        convertWindowsPathToWSL(path.join(__dirname, '..', '..', '..', 'lsp-server', 'target', 'debug', 'runa-lsp')),
        // Installed in system PATH
        'runa-lsp',
        // Common installation locations
        path.join(process.env.HOME || '', '.local', 'bin', 'runa-lsp'),
        '/usr/local/bin/runa-lsp',
        // Windows locations (for native Windows installations)
        path.join(process.env.USERPROFILE || '', '.local', 'bin', 'runa-lsp.exe'),
        path.join(process.env.PROGRAMFILES || '', 'Runa', 'bin', 'runa-lsp.exe')
    ];
    
    for (const lspPath of possiblePaths) {
        try {
            if (fs.existsSync(lspPath)) {
                // Check if it's executable by trying to get stats
                const stats = fs.statSync(lspPath);
                if (stats.isFile()) {
                    outputChannel.appendLine(`Found LSP candidate: ${lspPath}`);
                    return lspPath;
                }
            }
        } catch (error) {
            // Continue to next path
            outputChannel.appendLine(`Checked path ${lspPath}: not found or not accessible`);
        }
    }
    
    return null;
}

function showLspNotFoundMessage() {
    vscode.window.showWarningMessage(
        'Runa Language Server not found. Please install it or disable language server features.',
        'Install Instructions',
        'Disable Language Server',
        'Retry'
    ).then(selection => {
        if (selection === 'Install Instructions') {
            vscode.env.openExternal(vscode.Uri.parse('https://github.com/sybertneticsaisolutions/runa#installation'));
        } else if (selection === 'Disable Language Server') {
            const config = vscode.workspace.getConfiguration('runa');
            config.update('languageServer.enabled', false, vscode.ConfigurationTarget.Global);
        } else if (selection === 'Retry') {
            const config = vscode.workspace.getConfiguration('runa');
            if (config.get('languageServer.enabled', false)) {
                // Re-trigger initialization
                vscode.commands.executeCommand('runa.restartLanguageServer');
            }
        }
    });
}

function showLspErrorMessage(error: any) {
    const errorMsg = error instanceof Error ? error.message : String(error);
    vscode.window.showErrorMessage(
        `Failed to start Runa Language Server: ${errorMsg}`,
        'View Output',
        'Disable Language Server'
    ).then(selection => {
        if (selection === 'View Output') {
            outputChannel.show();
        } else if (selection === 'Disable Language Server') {
            const config = vscode.workspace.getConfiguration('runa');
            config.update('languageServer.enabled', false, vscode.ConfigurationTarget.Global);
        }
    });
}

function registerCommands(context: vscode.ExtensionContext) {
    const commands = [
        vscode.commands.registerCommand('runa.compileFile', compileFile),
        vscode.commands.registerCommand('runa.runFile', runFile),
        vscode.commands.registerCommand('runa.formatDocument', formatDocument),
        vscode.commands.registerCommand('runa.restartLanguageServer', restartLanguageServer),
        vscode.commands.registerCommand('runa.convertSymbolsToWords', convertSymbolsToWords),
        vscode.commands.registerCommand('runa.newRunaFile', newRunaFile)
    ];
    
    commands.forEach(command => context.subscriptions.push(command));
}

function registerLanguageProviders(context: vscode.ExtensionContext) {
    // Document formatter
    context.subscriptions.push(
        vscode.languages.registerDocumentFormattingEditProvider('runa', {
            provideDocumentFormattingEdits(document: vscode.TextDocument): vscode.TextEdit[] {
                return formatRunaDocument(document);
            }
        })
    );
    
    // Hover provider
    context.subscriptions.push(
        vscode.languages.registerHoverProvider('runa', {
            provideHover(document: vscode.TextDocument, position: vscode.Position): vscode.Hover | null {
                return provideRunaHover(document, position);
            }
        })
    );
    
    // Completion provider
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider('runa', {
            provideCompletionItems(document: vscode.TextDocument, position: vscode.Position): vscode.CompletionItem[] {
                return provideRunaCompletions(document, position);
            }
        }, '.', ' ', ':')
    );
    
    // Diagnostic provider for mathematical symbol enforcement
    context.subscriptions.push(
        vscode.languages.registerCodeActionsProvider('runa', {
            provideCodeActions(document: vscode.TextDocument, range: vscode.Range): vscode.CodeAction[] {
                return provideMathSymbolFixes(document, range);
            }
        })
    );
}

function createStatusBarItem(context: vscode.ExtensionContext) {
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
    statusBarItem.text = "$(rune) Runa";
    statusBarItem.tooltip = "Runa Language Support Active";
    statusBarItem.command = 'runa.compileFile';
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);
}

async function compileFile() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor || activeEditor.document.languageId !== 'runa') {
        vscode.window.showErrorMessage('No active Runa file to compile');
        return;
    }
    
    const filePath = activeEditor.document.fileName;
    const config = vscode.workspace.getConfiguration('runa');
    const compilerPath = config.get('compiler.path', 'runa');
    
    outputChannel.clear();
    outputChannel.show();
    outputChannel.appendLine(`Compiling: ${filePath}`);
    outputChannel.appendLine(`Using compiler: ${compilerPath}`);
    
    try {
        // Save the document first
        await activeEditor.document.save();
        
        const process = spawn(compilerPath, ['compile', filePath], {
            cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath
        });
        
        let stdout = '';
        let stderr = '';
        
        process.stdout.on('data', (data) => {
            const output = data.toString();
            stdout += output;
            outputChannel.append(output);
        });
        
        process.stderr.on('data', (data) => {
            const output = data.toString();
            stderr += output;
            outputChannel.append(output);
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                outputChannel.appendLine('\\n✓ Compilation successful!');
                vscode.window.showInformationMessage('Runa file compiled successfully');
            } else {
                outputChannel.appendLine(`\\n✗ Compilation failed with code ${code}`);
                vscode.window.showErrorMessage('Compilation failed. Check output for details.');
            }
        });
        
        process.on('error', (error) => {
            outputChannel.appendLine(`\\nError starting compiler: ${error.message}`);
            if (error.message.includes('ENOENT')) {
                vscode.window.showErrorMessage(
                    'Runa compiler not found. Please check the runa.compiler.path setting.',
                    'Open Settings'
                ).then(selection => {
                    if (selection === 'Open Settings') {
                        vscode.commands.executeCommand('workbench.action.openSettings', 'runa.compiler.path');
                    }
                });
            } else {
                vscode.window.showErrorMessage(`Compiler error: ${error.message}`);
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
    const config = vscode.workspace.getConfiguration('runa');
    const compilerPath = config.get('compiler.path', 'runa');
    
    outputChannel.clear();
    outputChannel.show();
    outputChannel.appendLine(`Running: ${filePath}`);
    
    try {
        // Save the document first
        await activeEditor.document.save();
        
        const process = spawn(compilerPath, ['run', filePath], {
            cwd: vscode.workspace.workspaceFolders?.[0]?.uri.fsPath
        });
        
        process.stdout.on('data', (data) => {
            outputChannel.append(data.toString());
        });
        
        process.stderr.on('data', (data) => {
            outputChannel.append(data.toString());
        });
        
        process.on('close', (code) => {
            outputChannel.appendLine(`\\n--- Process exited with code ${code} ---`);
        });
        
        process.on('error', (error) => {
            outputChannel.appendLine(`\\nError: ${error.message}`);
            vscode.window.showErrorMessage(`Runtime error: ${error.message}`);
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
        client = undefined;
    }
    
    const context = vscode.extensions.getExtension('sybertnetics.runa-language-support')?.exports;
    if (context) {
        initializeLanguageServer(context);
    }
    
    vscode.window.showInformationMessage('Language server restarted');
}

async function convertSymbolsToWords() {
    const activeEditor = vscode.window.activeTextEditor;
    if (!activeEditor || activeEditor.document.languageId !== 'runa') {
        vscode.window.showErrorMessage('No active Runa file');
        return;
    }
    
    const document = activeEditor.document;
    const edits: vscode.TextEdit[] = [];
    
    // Symbol to word mappings based on Runa specification
    const symbolMappings: { [key: string]: string } = {
        '+': ' plus ',
        '-': ' minus ',
        '*': ' multiplied by ',
        '/': ' divided by ',
        '%': ' modulo ',
        '==': ' equals ',
        '!=': ' does not equal ',
        '>': ' is greater than ',
        '<': ' is less than ',
        '>=': ' is greater than or equal to ',
        '<=': ' is less than or equal to '
    };
    
    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        let newText = line.text;
        
        // Only convert symbols in mathematical contexts (not in strings or comments)
        if (!line.text.trim().startsWith('Note:') && !isInString(line.text)) {
            for (const [symbol, word] of Object.entries(symbolMappings)) {
                const regex = new RegExp(`\\\\s*\\\\${symbol.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')}\\\\s*`, 'g');
                newText = newText.replace(regex, word);
            }
        }
        
        if (newText !== line.text) {
            edits.push(vscode.TextEdit.replace(line.range, newText));
        }
    }
    
    if (edits.length > 0) {
        const edit = new vscode.WorkspaceEdit();
        edit.set(document.uri, edits);
        await vscode.workspace.applyEdit(edit);
        vscode.window.showInformationMessage(`Converted ${edits.length} mathematical symbols to words`);
    } else {
        vscode.window.showInformationMessage('No mathematical symbols found to convert');
    }
}

async function newRunaFile() {
    const fileName = await vscode.window.showInputBox({
        prompt: 'Enter the name for the new Runa file',
        value: 'untitled.runa',
        validateInput: (value) => {
            if (!value.endsWith('.runa')) {
                return 'File name must end with .runa';
            }
            return null;
        }
    });
    
    if (fileName) {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (workspaceFolder) {
            const filePath = path.join(workspaceFolder.uri.fsPath, fileName);
            const templateContent = `Note: ${fileName.replace('.runa', '')} - Runa program
Note: Created on ${new Date().toISOString().split('T')[0]}

Display "Hello from Runa!"

Note: Add your code below
`;
            
            try {
                fs.writeFileSync(filePath, templateContent);
                const document = await vscode.workspace.openTextDocument(filePath);
                await vscode.window.showTextDocument(document);
            } catch (error) {
                vscode.window.showErrorMessage(`Failed to create file: ${error}`);
            }
        }
    }
}

function formatRunaDocument(document: vscode.TextDocument): vscode.TextEdit[] {
    const edits: vscode.TextEdit[] = [];
    let indentLevel = 0;
    const indentSize = 4;
    
    for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        const text = line.text;
        const trimmed = text.trim();
        
        if (trimmed.length === 0) {
            continue;
        }
        
        // Handle decrease indent patterns
        if (trimmed.match(/^(Otherwise|Catch|Finally)\\b/)) {
            indentLevel = Math.max(0, indentLevel - 1);
        }
        
        // Calculate expected indentation
        const expectedIndent = ' '.repeat(indentLevel * indentSize);
        const currentIndent = text.match(/^\\s*/)?.[0] || '';
        
        // Apply formatting if needed
        if (currentIndent !== expectedIndent) {
            const range = new vscode.Range(
                new vscode.Position(i, 0),
                new vscode.Position(i, currentIndent.length)
            );
            edits.push(vscode.TextEdit.replace(range, expectedIndent));
        }
        
        // Handle increase indent patterns
        if (trimmed.match(/^(If|Otherwise if|Unless|When|Match|For|While|Loop|Try|Catch|Finally|Process|Type)\\b.*:$/)) {
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
        'Process': 'Define a function/process that can be called with parameters',
        'Let': 'Declare a variable and assign a value using natural syntax: `Let variable be value`',
        'Define': 'Define a constant value: `Define constant as value`',
        'Set': 'Assign a new value to an existing variable: `Set variable to new_value`',
        'If': 'Execute code conditionally: `If condition:`',
        'Otherwise': 'Alternative branch in conditional statements',
        'Unless': 'Execute code unless condition is true: `Unless condition:`',
        'When': 'Pattern matching condition or event handler',
        'Match': 'Pattern matching statement for complex conditionals',
        'For': 'Loop through items: `For each item in collection:` or `For i from 1 to 10:`',
        'While': 'Loop while condition is true: `While condition:`',
        'Try': 'Handle potential errors in a code block',
        'Catch': 'Handle exceptions thrown in try block',
        'Finally': 'Code that always executes after try/catch',
        'Import': 'Import functionality from another module',
        'Export': 'Export functionality to other modules',
        'Display': 'Output text or values to the console',
        'Assert': 'Verify that a condition is true',
        'Return': 'Return a value from a function'
    };
    
    const operators: { [key: string]: string } = {
        'plus': 'Addition operator (natural language): `a plus b`',
        'minus': 'Subtraction operator (natural language): `a minus b`', 
        'multiplied': 'Multiplication operator (natural language): `a multiplied by b`',
        'divided': 'Division operator (natural language): `a divided by b`',
        'modulo': 'Modulo operator (natural language): `a modulo b`',
        'equals': 'Equality comparison (natural language): `a equals b`',
        'greater': 'Comparison operator: `a is greater than b`',
        'less': 'Comparison operator: `a is less than b`',
        'contains': 'Membership test: `collection contains item`'
    };
    
    const builtins: { [key: string]: string } = {
        'Display': 'Output values to console: `Display message`',
        'Input': 'Get input from user: `Input prompt`',
        'Length': 'Get length of collection or string: `Length of collection`',
        'Type': 'Get type of value: `Type of value`',
        'Convert': 'Convert value to different type: `Convert value to Type`'
    };
    
    if (keywords[word]) {
        return `**${word}** _(keyword)_\\n\\n${keywords[word]}`;
    }
    
    if (operators[word]) {
        return `**${word}** _(operator)_\\n\\n${operators[word]}`;
    }
    
    if (builtins[word]) {
        return `**${word}** _(built-in function)_\\n\\n${builtins[word]}`;
    }
    
    return null;
}

function provideRunaCompletions(document: vscode.TextDocument, position: vscode.Position): vscode.CompletionItem[] {
    const completions: vscode.CompletionItem[] = [];
    const config = vscode.workspace.getConfiguration('runa');
    
    if (!config.get('completion.enabled', true)) {
        return completions;
    }
    
    const line = document.lineAt(position).text;
    const linePrefix = line.substr(0, position.character);
    
    // Runa-specific intelligent completions
    
    // Type declaration
    if (linePrefix.match(/^\s*Typ?$/)) {
        const typeItem = new vscode.CompletionItem('Type called', vscode.CompletionItemKind.Snippet);
        typeItem.insertText = new vscode.SnippetString('Type called "${1:TypeName}":\n    ${2:field_name} as ${3:DataType}$0');
        typeItem.documentation = new vscode.MarkdownString('Create a new Runa type definition');
        typeItem.detail = 'Runa Type Declaration';
        completions.push(typeItem);
        return completions;
    }
    
    // Process declaration
    if (linePrefix.match(/^\s*Pro?c?e?s?s?$/)) {
        const processItem = new vscode.CompletionItem('Process called', vscode.CompletionItemKind.Snippet);
        processItem.insertText = new vscode.SnippetString('Process called "${1:process_name}" that takes ${2:parameter} as ${3:Type} returns ${4:ReturnType}:\n    ${5:// Implementation}\n    Return ${6:value}$0');
        processItem.documentation = new vscode.MarkdownString('Create a new Runa process (function)');
        processItem.detail = 'Runa Process Declaration';
        completions.push(processItem);
        return completions;
    }
    
    // Import statement
    if (linePrefix.match(/^\s*Imp?o?r?t?$/)) {
        const importItem = new vscode.CompletionItem('Import', vscode.CompletionItemKind.Snippet);
        importItem.insertText = new vscode.SnippetString('Import "${1:module_name}" as ${2:Alias}$0');
        importItem.documentation = new vscode.MarkdownString('Import a Runa module');
        importItem.detail = 'Runa Import Statement';
        completions.push(importItem);
        return completions;
    }
    
    // If statement with Otherwise
    if (linePrefix.match(/^\s*If?$/)) {
        const ifItem = new vscode.CompletionItem('If', vscode.CompletionItemKind.Snippet);
        ifItem.insertText = new vscode.SnippetString('If ${1:condition}:\n    ${2:// Then block}\nOtherwise:\n    ${3:// Else block}$0');
        ifItem.documentation = new vscode.MarkdownString('Create a Runa conditional statement');
        ifItem.detail = 'Runa If-Otherwise Statement';
        completions.push(ifItem);
        return completions;
    }
    
    // Let declaration
    if (linePrefix.match(/^\s*Le?t?$/)) {
        const letItem = new vscode.CompletionItem('Let', vscode.CompletionItemKind.Snippet);
        letItem.insertText = new vscode.SnippetString('Let ${1:variable} be ${2:value}$0');
        letItem.documentation = new vscode.MarkdownString('Declare a Runa variable');
        letItem.detail = 'Runa Variable Declaration';
        completions.push(letItem);
        return completions;
    }
    
    // General keywords
    const keywords = [
        { name: 'Return', snippet: 'Return ${1:value}$0', description: 'Return a value from a process' },
        { name: 'Otherwise', snippet: 'Otherwise:\n    ${1:// Else block}$0', description: 'Else clause for If statement' },
        { name: 'Note', snippet: 'Note: ${1:comment}$0', description: 'Add a comment' },
        { name: 'External', snippet: 'External "${1:function_name}" that takes ${2:params} returns ${3:Type}$0', description: 'Declare external function' },
        { name: 'Throw', snippet: 'Throw ${1:Error} with "${2:message}"$0', description: 'Throw an error' },
        { name: 'While', snippet: 'While ${1:condition}:\n    ${2:// Loop body}$0', description: 'While loop' },
        { name: 'For', snippet: 'For ${1:item} in ${2:collection}:\n    ${3:// Loop body}$0', description: 'For loop' }
    ];
    
    keywords.forEach(keyword => {
        const item = new vscode.CompletionItem(keyword.name, vscode.CompletionItemKind.Keyword);
        item.insertText = keyword.snippet ? new vscode.SnippetString(keyword.snippet) : keyword.name;
        item.documentation = new vscode.MarkdownString(keyword.description);
        item.detail = 'Runa Keyword';
        completions.push(item);
    });
    
    // Natural language operators
    const operators = [
        'plus', 'minus', 'multiplied by', 'divided by', 'modulo',
        'equals', 'does not equal', 'is greater than', 'is less than',
        'is greater than or equal to', 'is less than or equal to',
        'contains', 'is in', 'followed by', 'joined with'
    ];
    
    operators.forEach(op => {
        const item = new vscode.CompletionItem(op, vscode.CompletionItemKind.Operator);
        item.documentation = new vscode.MarkdownString(`Natural language operator: **${op}**`);
        completions.push(item);
    });
    
    // Built-in functions
    if (config.get('completion.includeBuiltins', true)) {
        const builtins = [
            'Display', 'Input', 'Length', 'Type', 'Convert', 'Parse', 'Format',
            'Range', 'Enumerate', 'Zip', 'Map', 'Filter', 'Reduce', 'Sort',
            'Reverse', 'Split', 'Join', 'Replace', 'Contains', 'Starts_with',
            'Ends_with', 'Uppercase', 'Lowercase', 'Trim'
        ];
        
        builtins.forEach(builtin => {
            const item = new vscode.CompletionItem(builtin, vscode.CompletionItemKind.Function);
            item.documentation = new vscode.MarkdownString(`Built-in function: **${builtin}**`);
            completions.push(item);
        });
    }
    
    // Types
    const types = [
        'Integer', 'Float', 'String', 'Boolean', 'List', 'Dictionary',
        'Function', 'Optional', 'Any', 'Void'
    ];
    
    types.forEach(type => {
        const item = new vscode.CompletionItem(type, vscode.CompletionItemKind.Class);
        item.documentation = new vscode.MarkdownString(`Runa type: **${type}**`);
        completions.push(item);
    });
    
    return completions;
}

function provideMathSymbolFixes(document: vscode.TextDocument, range: vscode.Range): vscode.CodeAction[] {
    const actions: vscode.CodeAction[] = [];
    const config = vscode.workspace.getConfiguration('runa');
    
    if (!config.get('diagnostics.mathSymbolEnforcement', true)) {
        return actions;
    }
    
    const text = document.getText(range);
    
    // Check for mathematical symbols in non-mathematical contexts
    const mathSymbols = /[+*/%<>=!-]+/g;
    const matches = text.match(mathSymbols);
    
    if (matches) {
        matches.forEach(symbol => {
            const action = new vscode.CodeAction(
                `Convert '${symbol}' to natural language`,
                vscode.CodeActionKind.QuickFix
            );
            action.command = {
                command: 'runa.convertSymbolsToWords',
                title: 'Convert symbols to words'
            };
            actions.push(action);
        });
    }
    
    return actions;
}

function isInString(text: string): boolean {
    // Simple check if we're inside a string literal
    const singleQuotes = (text.match(/'/g) || []).length;
    const doubleQuotes = (text.match(/"/g) || []).length;
    return (singleQuotes % 2 !== 0) || (doubleQuotes % 2 !== 0);
}

function handleConfigurationChange() {
    const config = vscode.workspace.getConfiguration('runa');
    
    // Language server is disabled by default - don't auto-start
    outputChannel.appendLine('Configuration changed - language server remains disabled for stability');
    
    // Only manually restart if explicitly enabled and user has configured it
    if (config.get('languageServer.enabled', false) && !client) {
        outputChannel.appendLine('Language server manually enabled - attempting connection');
        const context = vscode.extensions.getExtension('sybertnetics.runa-language-support')?.exports;
        if (context) {
            initializeLanguageServer(context);
        }
    } else if (!config.get('languageServer.enabled', false) && client) {
        outputChannel.appendLine('Stopping language server');
        client.stop();
        client = undefined;
    }
}

export function deactivate(): Thenable<void> | undefined {
    if (client) {
        return client.stop();
    }
    return undefined;
}
