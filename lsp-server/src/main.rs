// Runa Language Server Protocol (LSP) Server
//
// This is a standalone LSP server implementation that provides language
// intelligence for Runa code without requiring full compiler integration.
//
// Usage: runa-lsp [options]

use std::env;
use std::process;
use std::io::{self, BufRead, Write};
use serde_json::{Value, json};

fn main() {
    // Parse command line arguments
    let args: Vec<String> = env::args().collect();
    
    // Handle help and version options
    if args.len() > 1 {
        match args[1].as_str() {
            "--help" | "-h" => {
                println!("Runa Language Server v{}", env!("CARGO_PKG_VERSION"));
                println!("Usage: {} [options]", args[0]);
                println!("");
                println!("Options:");
                println!("  --help, -h           Show this help message");
                println!("  --version, -v        Show version information");
                println!("  --debug             Enable debug logging");
                println!("  --max-errors <n>    Maximum errors to report (default: 100)");
                println!("  --max-warnings <n>  Maximum warnings to report (default: 200)");
                println!("  --enable-incremental Enable incremental analysis");
                println!("  --disable-incremental Disable incremental analysis");
                println!("  --cache-size <n>    Analysis cache size (default: 1000)");
                println!("  --performance-tracking Enable performance tracking");
                println!("  --no-performance-tracking Disable performance tracking");
                println!("");
                println!("The LSP server communicates via JSON-RPC over stdin/stdout.");
                println!("It provides intelligent IDE support for Runa programming language.");
                process::exit(0);
            }
            "--version" | "-v" => {
                println!("Runa Language Server v{}", env!("CARGO_PKG_VERSION"));
                println!("Built for Runa programming language");
                process::exit(0);
            }
            opt if opt.starts_with("--") => {
                eprintln!("Error: Unknown option '{}'", opt);
                eprintln!("Use --help for usage information.");
                process::exit(1);
            }
            _ => {}
        }
    }
    
    // Initialize logger for debug output (stderr only)
    if args.contains(&"--debug".to_string()) {
        env_logger::Builder::from_default_env()
            .target(env_logger::Target::Stderr)
            .filter_level(log::LevelFilter::Debug)
            .init();
        
        log::info!("Debug mode enabled");
    }
    
    // Print startup banner to stderr
    eprintln!("🎯 Runa Language Server v{}", env!("CARGO_PKG_VERSION"));
    eprintln!("Providing intelligent language support for Runa...");
    
    // Run the LSP server
    match run_lsp_server() {
        Ok(()) => {
            eprintln!("✅ Runa Language Server shutdown complete");
        }
        Err(e) => {
            eprintln!("❌ Runa Language Server error: {}", e);
            process::exit(1);
        }
    }
}

fn run_lsp_server() -> io::Result<()> {
    let stdin = io::stdin();
    let mut stdout = io::stdout();
    let mut initialized = false;
    let mut content_length = 0usize;
    let mut reading_headers = true;
    
    eprintln!("📡 LSP server listening for JSON-RPC messages...");
    
    for line in stdin.lock().lines() {
        let line = line?;
        
        if reading_headers {
            if line.is_empty() {
                reading_headers = false;
                continue;
            }
            
            if line.starts_with("Content-Length:") {
                content_length = line
                    .split(':')
                    .nth(1)
                    .unwrap_or("0")
                    .trim()
                    .parse()
                    .unwrap_or(0);
            }
            continue;
        }
        
        // We have the message content
        if !line.is_empty() && content_length > 0 {
            match serde_json::from_str::<Value>(&line) {
                Ok(message) => {
                    if let Some(response) = handle_lsp_message(&message, &mut initialized)? {
                        send_lsp_response(&mut stdout, &response)?;
                    }
                }
                Err(e) => {
                    log::warn!("Failed to parse JSON-RPC message: {}", e);
                }
            }
        }
        
        // Reset for next message
        reading_headers = true;
        content_length = 0;
    }
    
    Ok(())
}

fn handle_lsp_message(message: &Value, initialized: &mut bool) -> io::Result<Option<Value>> {
    let method = message.get("method").and_then(|m| m.as_str());
    let id = message.get("id");
    
    log::debug!("Received LSP message: method={:?}, id={:?}", method, id);
    
    match method {
        Some("initialize") => {
            *initialized = true;
            log::info!("LSP client initializing...");
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "capabilities": {
                        "textDocumentSync": {
                            "openClose": true,
                            "change": 1,
                            "save": {
                                "includeText": true
                            }
                        },
                        "hoverProvider": true,
                        "completionProvider": {
                            "triggerCharacters": ["."],
                            "resolveProvider": false
                        },
                        "documentSymbolProvider": true,
                        "workspaceSymbolProvider": true,
                        "definitionProvider": true,
                        "referencesProvider": true,
                        "documentHighlightProvider": true,
                        "semanticTokensProvider": {
                            "legend": {
                                "tokenTypes": ["keyword", "type", "function", "variable", "string", "comment"],
                                "tokenModifiers": []
                            },
                            "full": true
                        }
                    },
                    "serverInfo": {
                        "name": "Runa Language Server",
                        "version": env!("CARGO_PKG_VERSION")
                    }
                }
            })))
        }
        Some("initialized") => {
            eprintln!("📋 LSP client initialized successfully");
            log::info!("LSP server fully initialized");
            Ok(None)
        }
        Some("shutdown") => {
            log::info!("LSP shutdown requested");
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": null
            })))
        }
        Some("exit") => {
            eprintln!("🚪 Received exit request, shutting down...");
            log::info!("LSP server exiting");
            process::exit(0);
        }
        Some("textDocument/hover") => {
            if !*initialized {
                return Ok(None);
            }
            
            let hover_content = get_hover_content(message);
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": hover_content
                    }
                }
            })))
        }
        Some("textDocument/completion") => {
            if !*initialized {
                return Ok(None);
            }
            
            let completions = get_completions(message);
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "isIncomplete": false,
                    "items": completions
                }
            })))
        }
        Some("textDocument/documentSymbol") => {
            if !*initialized {
                return Ok(None);
            }
            
            let symbols = get_document_symbols(message);
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": symbols
            })))
        }
        Some("workspace/symbol") => {
            if !*initialized {
                return Ok(None);
            }
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": []
            })))
        }
        Some("textDocument/definition") => {
            if !*initialized {
                return Ok(None);
            }
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": null
            })))
        }
        Some("textDocument/references") => {
            if !*initialized {
                return Ok(None);
            }
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": []
            })))
        }
        Some("textDocument/semanticTokens/full") => {
            if !*initialized {
                return Ok(None);
            }
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "data": []
                }
            })))
        }
        Some("textDocument/didOpen") |
        Some("textDocument/didChange") |
        Some("textDocument/didSave") |
        Some("textDocument/didClose") => {
            // Handle document events but don't send responses for notifications
            log::debug!("Document event: {}", method.unwrap_or("unknown"));
            Ok(None)
        }
        _ => {
            // Unknown method
            if id.is_some() {
                log::warn!("Unknown LSP method: {}", method.unwrap_or("none"));
                Ok(Some(json!({
                    "jsonrpc": "2.0",
                    "id": id,
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    }
                })))
            } else {
                Ok(None)
            }
        }
    }
}

fn get_hover_content(message: &Value) -> String {
    // Try to extract position and context for intelligent hover
    if let Some(params) = message.get("params") {
        if let Some(text_document) = params.get("textDocument") {
            if let Some(uri) = text_document.get("uri").and_then(|u| u.as_str()) {
                if let Some(position) = params.get("position") {
                    if let (Some(line), Some(character)) = (
                        position.get("line").and_then(|l| l.as_u64()),
                        position.get("character").and_then(|c| c.as_u64())
                    ) {
                        // Try to get context-specific hover information
                        return get_context_aware_hover(uri, line as usize, character as usize);
                    }
                }
            }
        }
    }
    
    get_runa_language_hover()
}

fn get_context_aware_hover(uri: &str, line: usize, character: usize) -> String {
    // Extract file path from URI and try to read the document
    let file_path = if uri.starts_with("file://") {
        uri.strip_prefix("file://").unwrap_or(uri)
    } else {
        uri
    };
    
    // Try to read the file content
    if let Ok(content) = std::fs::read_to_string(file_path) {
        let lines: Vec<&str> = content.lines().collect();
        if line < lines.len() {
            let current_line = lines[line];
            
            // Get the word or phrase at the current position
            if let Some(hover_text) = extract_hover_text(current_line, character) {
                return get_specific_hover_info(&hover_text);
            }
        }
    }
    
    // Fallback to general information
    get_runa_language_hover()
}

fn extract_hover_text(line: &str, character: usize) -> Option<String> {
    if character >= line.len() {
        return None;
    }
    
    // Simple approach: Check for multi-word patterns by looking for exact substrings
    // around the cursor position
    
    // Define compound patterns with their exact text
    let compound_patterns = [
        ("Process called", 14),
        ("Type called", 11),
        ("Let", 3), // We'll handle "Let ... be" specially
        ("that takes", 10),
        ("returns", 7),
        ("is equal to", 11),
        ("is not equal to", 15),
        ("is greater than", 15),
        ("is less than", 12),
        ("is greater than or equal to", 27),
        ("is less than or equal to", 24),
        ("multiplied by", 13),
        ("divided by", 10),
        ("to the power of", 15),
        ("followed by", 11),
        ("joined with", 11),
        ("Set", 3), // For assignment
    ];
    
    // Convert line to lowercase once
    let line_lower = line.to_lowercase();
    
    // Check each pattern to see if cursor is within any occurrence
    for (pattern, _pattern_len) in &compound_patterns {
        let pattern_lower = pattern.to_lowercase();
        
        // Find ALL occurrences of this pattern in the line
        let mut start_idx = 0;
        while let Some(relative_start) = line_lower[start_idx..].find(&pattern_lower) {
            let start_pos = start_idx + relative_start;
            let end_pos = start_pos + pattern_lower.len();
            
            // Check if cursor is within this occurrence
            if character >= start_pos && character <= end_pos {
                // Special case for "Let ... be" pattern
                if pattern_lower == "let" {
                    // Look ahead to see if this is "Let ... be" construct
                    if line_lower[start_pos..].contains(" be ") {
                        return Some("Let ... be".to_string());
                    }
                }
                return Some(pattern.to_string());
            }
            
            // Move to search for next occurrence
            start_idx = start_pos + 1;
        }
    }
    
    // Fallback to single word extraction
    let chars: Vec<char> = line.chars().collect();
    let mut start = character;
    let mut end = character;
    
    // Find word boundaries
    while start > 0 && (chars[start - 1].is_alphanumeric() || chars[start - 1] == '_') {
        start -= 1;
    }
    while end < chars.len() && (chars[end].is_alphanumeric() || chars[end] == '_') {
        end += 1;
    }
    
    if start < end {
        Some(chars[start..end].iter().collect())
    } else {
        None
    }
}

fn get_specific_hover_info(text: &str) -> String {
    match text {
        "Process called" => {
            "**Process called** 🔧\n\n*Function/Procedure Definition*\n\n```runa\nProcess called \"function_name\" that takes param as Type returns ReturnType:\n    Let result be computation\n    Return result\n```\n\n**Usage:**\n- Define reusable code blocks\n- Can take multiple parameters\n- Must specify parameter types\n- Must specify return type\n- Use `that takes` for parameters\n- Use `returns` for return type".to_string()
        }
        "Type called" => {
            "**Type called** 📦\n\n*Structured Type Definition*\n\n```runa\nType called \"PersonData\":\n    name as String\n    age as Integer\n    email as String\n```\n\n**Usage:**\n- Define custom data structures\n- Group related fields together\n- Fields have explicit types\n- Used for organizing complex data".to_string()
        }
        "Let" | "Let ... be" => {
            "**Let ... be** 📝\n\n*Variable Declaration*\n\n```runa\nLet variable_name be value\nLet count be 42\nLet message be \"Hello, World!\"\nLet numbers be [1, 2, 3, 4, 5]\n```\n\n**Usage:**\n- Declare new variables\n- Assign initial values\n- Type is inferred from value\n- Variables are immutable by default".to_string()
        }
        "Set" => {
            "**Set** 🔄\n\n*Assignment or Collection Type (context-dependent)*\n\n**Assignment Usage:**\n```runa\nSet variable_name to new_value\nSet count to 42\nSet message to \"Updated text\"\n```\n\n**Collection Type Usage:**\n```runa\nLet unique_items be Set[String]\nLet numbers be {1, 2, 3, 4, 5}  // Set literal\n```\n\n**Set Operations:**\n- Unique elements only\n- Add: `Add(set, item)`\n- Contains: `Contains(set, item)`\n- Union, intersection, difference".to_string()
        }
        "that takes" => {
            "**that takes** ⚙️\n\n*Parameter Declaration*\n\n```runa\nProcess called \"example\" that takes param1 as String and param2 as Integer:\n```\n\n**Usage:**\n- Specify function parameters\n- Each parameter needs a type\n- Use `and` to separate multiple parameters\n- Parameters are available inside the process".to_string()
        }
        "returns" => {
            "**returns** ↩️\n\n*Return Type Declaration*\n\n```runa\nProcess called \"calculate\" that takes x as Integer returns Integer:\n    Return x * 2\n```\n\n**Usage:**\n- Specify what type the process returns\n- Must match the actual returned value\n- Use `Return` statement to return values".to_string()
        }
        "String" => {
            "**String** 📝\n\n*Text Data Type*\n\n```runa\nLet message be \"Hello, World!\"\nLet name be \"Runa\"\n```\n\n**Operations:**\n- Concatenation: `\"Hello\" + \" World\"` (math context)\n- Joining: `\"Hello\" followed by \" World\"`\n- Length: `Length(text)`\n- Comparison: `text1 equals text2`".to_string()
        }
        "Integer" => {
            "**Integer** 🔢\n\n*Whole Number Type*\n\n```runa\nLet count be 42\nLet age be 25\n```\n\n**Operations:**\n- Arithmetic: `+`, `-`, `*`, `/`, `%` (math context only)\n- Natural: `plus`, `minus`, `multiplied by`, `divided by`\n- Comparison: `equals`, `is greater than`, etc.\n- Range: `Range(1, 10)`".to_string()
        }
        "Float" => {
            "**Float** 🔢.🔢\n\n*Decimal Number Type*\n\n```runa\nLet price be 19.99\nLet pi be 3.14159\n```\n\n**Operations:**\n- Arithmetic: `+`, `-`, `*`, `/` (math context only)\n- Natural: `plus`, `minus`, `multiplied by`, `divided by`\n- Comparison: `equals`, `is greater than`, etc.\n- Scientific notation supported".to_string()
        }
        "Boolean" => {
            "**Boolean** ✓/✗\n\n*True/False Type*\n\n```runa\nLet is_valid be true\nLet is_complete be false\n```\n\n**Operations:**\n- Logical: `and`, `or`, `not`\n- Comparison results are Boolean\n- Used in conditional statements".to_string()
        }
        "List" => {
            "**List** 📋\n\n*Ordered Collection*\n\n```runa\nLet numbers be [1, 2, 3, 4, 5]\nLet names be [\"Alice\", \"Bob\", \"Charlie\"]\nLet items be List[String]\n```\n\n**Operations:**\n- Access: `items[0]`\n- Length: `Length(items)`\n- Add: `Append(items, new_item)`\n- Allows duplicates, maintains order".to_string()
        }
        "Dictionary" => {
            "**Dictionary** 🗂️\n\n*Key-Value Collection*\n\n```runa\nLet scores be {\"Alice\": 95, \"Bob\": 87}\nLet config be Dictionary[String, Integer]\n```\n\n**Operations:**\n- Access: `scores[\"Alice\"]`\n- Keys: `Keys(dictionary)`\n- Values: `Values(dictionary)`\n- Unique keys, fast lookup".to_string()
        }
        "multiplied by" => {
            "**multiplied by** ✖️\n\n*Mathematical Multiplication*\n\n```runa\nLet area be width multiplied by height\nLet result be 5 * 3  // Math context only\n```\n\n**Usage:**\n- Natural language multiplication operator\n- Mathematical symbol `*` allowed in math contexts only\n- Works with Integer, Float types".to_string()
        }
        "divided by" => {
            "**divided by** ➗\n\n*Mathematical Division*\n\n```runa\nLet average be total divided by count\nLet result be 10 / 2  // Math context only\n```\n\n**Usage:**\n- Natural language division operator\n- Mathematical symbol `/` allowed in math contexts only\n- Works with Integer, Float types".to_string()
        }
        "is greater than" => {
            "**is greater than** >\n\n*Mathematical Comparison*\n\n```runa\nIf age is greater than 18:\nIf score > 90:  // Math context only\n```\n\n**Usage:**\n- Natural language comparison operator\n- Mathematical symbol `>` allowed in math contexts only\n- Returns Boolean result".to_string()
        }
        "is less than" => {
            "**is less than** <\n\n*Mathematical Comparison*\n\n```runa\nIf temperature is less than 32:\nIf value < threshold:  // Math context only\n```\n\n**Usage:**\n- Natural language comparison operator\n- Mathematical symbol `<` allowed in math contexts only\n- Returns Boolean result".to_string()
        }
        "joined with" => {
            "**joined with** 🔗\n\n*String Concatenation*\n\n```runa\nLet full_name be first_name joined with \" \" joined with last_name\nLet greeting be \"Hello, \" joined with name\n```\n\n**Usage:**\n- Natural language string concatenation\n- Combines two strings into one\n- Always use for string joining (not `+` symbol)\n- Can chain multiple joins together".to_string()
        }
        "followed by" => {
            "**followed by** ➡️\n\n*String Concatenation (Alternative)*\n\n```runa\nLet message be \"Hello\" followed by \" World\"\nLet path be directory followed by \"/\" followed by filename\n```\n\n**Usage:**\n- Alternative natural language for string concatenation\n- Same as 'joined with' but different phrasing\n- Use for readability in specific contexts\n- Preferred for path/sequence construction".to_string()
        }
        _ => get_runa_language_hover()
    }
}

fn get_runa_language_hover() -> String {
    "**Runa Language** 🎯\n\n*AI-First Programming Language*\n\n---\n\n### 🔧 **Core Constructs:**\n\n**`Process called \"name\"`** - Define functions/procedures\n```runa\nProcess called \"greet\" that takes name as String returns String:\n    Let message be \"Hello, \" + name\n    Return message\n```\n\n**`Type called \"Name\"`** - Define structured types  \n```runa\nType called \"Person\":\n    name as String\n    age as Integer\n```\n\n**`Let variable be value`** - Variable declarations\n```runa\nLet count be 42\nLet message be \"Hello, World!\"\n```\n\n### 🎯 **Built-in Types:**\n- `String` - Text data\n- `Integer` - Whole numbers  \n- `Float` - Decimal numbers\n- `Boolean` - True/false values\n- `List[Type]` - Ordered collections\n- `Dictionary[Key, Value]` - Key-value maps\n\n### 🔄 **Control Flow:**\n- `If condition: ... Otherwise:` - Conditional logic\n- `While condition:` - Loops\n- `For item in collection:` - Iteration\n\n*Hover over specific constructs for detailed information.*".to_string()
}

fn get_completions(_message: &Value) -> Vec<Value> {
    vec![
        json!({
            "label": "Type called",
            "kind": 7, // Class
            "detail": "Runa Type Definition",
            "documentation": "Define a new type in Runa",
            "insertText": "Type called \"${1:TypeName}\":\n    ${2:field_name} as ${3:DataType}",
            "insertTextFormat": 2 // Snippet
        }),
        json!({
            "label": "Process called",
            "kind": 3, // Function
            "detail": "Runa Process Definition",
            "documentation": "Define a new process (function) in Runa",
            "insertText": "Process called \"${1:process_name}\" that takes ${2:parameter} as ${3:Type} returns ${4:ReturnType}:\n    ${5:// Implementation}",
            "insertTextFormat": 2 // Snippet
        }),
        json!({
            "label": "Import",
            "kind": 9, // Module
            "detail": "Import Statement",
            "documentation": "Import a module or library",
            "insertText": "Import \"${1:module_name}\" as ${2:Alias}",
            "insertTextFormat": 2 // Snippet
        }),
        json!({
            "label": "Let",
            "kind": 14, // Keyword
            "detail": "Variable Declaration",
            "documentation": "Declare a variable with Let",
            "insertText": "Let ${1:variable} be ${2:value}",
            "insertTextFormat": 2 // Snippet
        }),
        json!({
            "label": "Return",
            "kind": 14, // Keyword
            "detail": "Return Statement",
            "documentation": "Return a value from a process"
        }),
        json!({
            "label": "If",
            "kind": 14, // Keyword
            "detail": "Conditional Statement",
            "documentation": "Conditional execution",
            "insertText": "If ${1:condition}:\n    ${2:// Then block}",
            "insertTextFormat": 2 // Snippet
        }),
        json!({
            "label": "Note",
            "kind": 17, // Text
            "detail": "Comment",
            "documentation": "Add a comment to your code",
            "insertText": "Note: ${1:comment}",
            "insertTextFormat": 2 // Snippet
        })
    ]
}

fn get_document_symbols(_message: &Value) -> Vec<Value> {
    // For now, return empty array. In a full implementation, this would
    // parse the document and extract symbols (types, processes, etc.)
    vec![]
}

fn send_lsp_response(stdout: &mut io::Stdout, response: &Value) -> io::Result<()> {
    let response_str = serde_json::to_string(response)?;
    let content_length = response_str.len();
    
    // LSP requires CRLF line endings in headers
    write!(stdout, "Content-Length: {}\r\n\r\n{}", content_length, response_str)?;
    stdout.flush()?;
    
    log::debug!("Sent LSP response: {} bytes", content_length);
    
    Ok(())
}