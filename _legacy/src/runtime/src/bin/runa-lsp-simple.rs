// Simplified Runa Language Server Protocol (LSP) Server
//
// This is a minimal LSP server implementation that provides basic language
// intelligence for Runa code without requiring full compiler integration.
//
// Usage: runa-lsp-simple [options]

use std::env;
use std::process;
use std::io::{self, BufRead, Write};
use std::collections::HashMap;
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
                println!("");
                println!("The LSP server communicates via JSON-RPC over stdin/stdout.");
                process::exit(0);
            }
            "--version" | "-v" => {
                println!("Runa Language Server v{}", env!("CARGO_PKG_VERSION"));
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
    eprintln!("Providing basic language intelligence for Runa...");
    
    // Run the simplified LSP server
    match run_simple_lsp_server() {
        Ok(()) => {
            eprintln!("✅ Runa Language Server shutdown complete");
        }
        Err(e) => {
            eprintln!("❌ Runa Language Server error: {}", e);
            process::exit(1);
        }
    }
}

fn run_simple_lsp_server() -> io::Result<()> {
    let stdin = io::stdin();
    let mut stdout = io::stdout();
    let mut initialized = false;
    
    eprintln!("📡 LSP server listening for JSON-RPC messages...");
    
    for line in stdin.lock().lines() {
        let line = line?;
        
        // Skip empty lines and Content-Length headers
        if line.is_empty() || line.starts_with("Content-Length:") {
            continue;
        }
        
        // Try to parse JSON-RPC message
        match serde_json::from_str::<Value>(&line) {
            Ok(message) => {
                if let Some(response) = handle_lsp_message(&message, &mut initialized)? {
                    send_lsp_response(&mut stdout, &response)?;
                }
            }
            Err(_) => {
                // Skip malformed JSON
                continue;
            }
        }
    }
    
    Ok(())
}

fn handle_lsp_message(message: &Value, initialized: &mut bool) -> io::Result<Option<Value>> {
    let method = message.get("method").and_then(|m| m.as_str());
    let id = message.get("id");
    
    match method {
        Some("initialize") => {
            *initialized = true;
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "capabilities": {
                        "textDocumentSync": 1,
                        "hoverProvider": true,
                        "completionProvider": {
                            "triggerCharacters": ["."]
                        },
                        "documentSymbolProvider": true,
                        "workspaceSymbolProvider": true
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
            Ok(None)
        }
        Some("shutdown") => {
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": null
            })))
        }
        Some("exit") => {
            eprintln!("🚪 Received exit request, shutting down...");
            process::exit(0);
        }
        Some("textDocument/hover") => {
            if !*initialized {
                return Ok(None);
            }
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": "**Runa Language** - Basic hover information available.\n\nThis is a simplified LSP server providing basic language intelligence."
                    }
                }
            })))
        }
        Some("textDocument/completion") => {
            if !*initialized {
                return Ok(None);
            }
            
            let completions = vec![
                json!({
                    "label": "Type",
                    "kind": 7, // Class
                    "detail": "Runa Type Definition",
                    "documentation": "Define a new type in Runa"
                }),
                json!({
                    "label": "Process",
                    "kind": 3, // Function
                    "detail": "Runa Process Definition",
                    "documentation": "Define a new process (function) in Runa"
                }),
                json!({
                    "label": "Import",
                    "kind": 9, // Module
                    "detail": "Import Statement",
                    "documentation": "Import a module or library"
                }),
                json!({
                    "label": "Let",
                    "kind": 14, // Keyword
                    "detail": "Variable Declaration",
                    "documentation": "Declare a variable with Let"
                }),
                json!({
                    "label": "Return",
                    "kind": 14, // Keyword
                    "detail": "Return Statement",
                    "documentation": "Return a value from a process"
                })
            ];
            
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
            
            Ok(Some(json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": []
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
        Some("textDocument/didOpen") |
        Some("textDocument/didChange") |
        Some("textDocument/didSave") |
        Some("textDocument/didClose") => {
            // Handle document events but don't send responses
            Ok(None)
        }
        _ => {
            // Unknown method - send method not found error
            if id.is_some() {
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

fn send_lsp_response(stdout: &mut io::Stdout, response: &Value) -> io::Result<()> {
    let response_str = serde_json::to_string(response)?;
    let content_length = response_str.len();
    
    writeln!(stdout, "Content-Length: {}\r", content_length)?;
    writeln!(stdout, "\r")?;
    writeln!(stdout, "{}", response_str)?;
    stdout.flush()?;
    
    Ok(())
}