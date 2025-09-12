// Runa Language Server Protocol (LSP) Server Executable
//
// This is the main entry point for the Runa Language Server, providing
// real-time language intelligence for Runa code in IDEs and editors.
//
// Usage: runa-lsp [options]
//
// The server communicates via JSON-RPC over stdin/stdout according to
// the Language Server Protocol specification.

use std::env;
use std::process;
use std::io::{self, Write};

use runa_runtime::lsp_bridge::run_lsp_server_from_args;

fn main() {
    // Collect command line arguments
    let args: Vec<String> = env::args().collect();
    
    // Initialize logger for debug output (stderr only, to avoid interfering with LSP communication)
    env_logger::Builder::from_default_env()
        .target(env_logger::Target::Stderr)
        .filter_level(log::LevelFilter::Info)
        .init();
    
    // Print startup banner to stderr (not interfering with JSON-RPC)
    eprintln!("🎯 Runa Language Server v{}", env!("CARGO_PKG_VERSION"));
    eprintln!("Initializing language intelligence...");
    
    // Run the LSP server
    match run_lsp_server_from_args(args) {
        Ok(exit_code) => {
            if exit_code == 0 {
                eprintln!("✅ Runa Language Server shutdown complete");
            } else {
                eprintln!("⚠️  Runa Language Server exited with code {}", exit_code);
            }
            process::exit(exit_code);
        }
        Err(e) => {
            eprintln!("❌ Runa Language Server failed to start: {}", e);
            
            // Try to send error notification to client if possible
            let error_response = serde_json::json!({
                "jsonrpc": "2.0",
                "method": "window/showMessage",
                "params": {
                    "type": 1, // Error
                    "message": format!("Runa Language Server startup failed: {}", e)
                }
            });
            
            if let Ok(json_str) = serde_json::to_string(&error_response) {
                let content_length = json_str.len();
                let _ = write!(
                    io::stdout(),
                    "Content-Length: {}\\r\\n\\r\\n{}",
                    content_length,
                    json_str
                );
            }
            
            process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::process::Command;
    
    #[test]
    fn test_help_option() {
        let output = Command::new(env!("CARGO_BIN_EXE_runa-lsp"))
            .arg("--help")
            .output()
            .expect("Failed to execute runa-lsp");
        
        assert_eq!(output.status.code(), Some(0));
        
        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Runa Language Server"));
        assert!(stdout.contains("Usage:"));
    }
    
    #[test]
    fn test_version_information() {
        // Test that the version information is properly embedded
        let version = env!("CARGO_PKG_VERSION");
        assert!(!version.is_empty());
        assert!(version.chars().any(|c| c.is_ascii_digit()));
    }
    
    #[test] 
    fn test_invalid_option() {
        let output = Command::new(env!("CARGO_BIN_EXE_runa-lsp"))
            .arg("--invalid-option")
            .output()
            .expect("Failed to execute runa-lsp");
        
        assert_ne!(output.status.code(), Some(0));
        
        let stderr = String::from_utf8_lossy(&output.stderr);
        assert!(stderr.contains("Unknown option"));
    }
}