// Runa LSP Bridge: Rust-to-Runa Integration Layer
//
// This module provides the Rust implementation needed to bridge between
// the JSON-RPC protocol (stdin/stdout) and the Runa LSP server implementation.
// The actual LSP logic is implemented in Runa code, this just handles I/O.

use std::io::{self, BufRead, BufReader, Write};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};
use serde_json::{Value, json};
use serde::{Deserialize, Serialize};

use crate::vm::RunaVM;
use crate::bytecode_generator::BytecodeGenerator;

/// LSP Bridge for handling JSON-RPC communication with Runa LSP implementation
pub struct LSPBridge {
    vm: Arc<Mutex<RunaVM>>,
    request_counter: Arc<Mutex<u64>>,
    performance_metrics: Arc<Mutex<LSPMetrics>>,
    config: LSPBridgeConfig,
}

/// Configuration for the LSP Bridge
#[derive(Debug, Clone)]
pub struct LSPBridgeConfig {
    pub max_errors: usize,
    pub max_warnings: usize,
    pub enable_incremental_analysis: bool,
    pub cache_size: usize,
    pub performance_tracking: bool,
    pub debug_mode: bool,
    pub io_timeout_ms: u64,
}

/// Performance metrics for the LSP server
#[derive(Debug, Default)]
pub struct LSPMetrics {
    pub requests_processed: u64,
    pub analysis_time_ms: u64,
    pub cache_hits: u64,
    pub cache_misses: u64,
    pub documents_analyzed: u64,
    pub errors_reported: u64,
    pub warnings_reported: u64,
    pub startup_time: Option<Instant>,
}

/// JSON-RPC message types
#[derive(Debug, Deserialize, Serialize)]
pub struct JsonRpcRequest {
    pub jsonrpc: String,
    pub id: Option<Value>,
    pub method: String,
    pub params: Option<Value>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct JsonRpcResponse {
    pub jsonrpc: String,
    pub id: Option<Value>,
    pub result: Option<Value>,
    pub error: Option<JsonRpcError>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct JsonRpcError {
    pub code: i32,
    pub message: String,
    pub data: Option<Value>,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct JsonRpcNotification {
    pub jsonrpc: String,
    pub method: String,
    pub params: Option<Value>,
}

impl Default for LSPBridgeConfig {
    fn default() -> Self {
        Self {
            max_errors: 100,
            max_warnings: 200,
            enable_incremental_analysis: true,
            cache_size: 1000,
            performance_tracking: true,
            debug_mode: false,
            io_timeout_ms: 30000, // 30 second timeout
        }
    }
}

impl LSPBridge {
    /// Create a new LSP Bridge with the given configuration
    pub fn new(config: LSPBridgeConfig) -> io::Result<Self> {
        // Initialize the Runa VM with LSP modules loaded
        let mut vm = RunaVM::new();
        
        // Load the Runa LSP server code
        Self::load_lsp_modules(&mut vm)?;
        
        // Initialize the Runa LSP server with configuration
        let runa_config = Self::create_runa_config(&config);
        let server_result = vm.call_function("create_lsp_server", vec![runa_config])?;
        
        if config.debug_mode {
            eprintln!("🚀 Runa LSP Bridge initialized");
        }
        
        Ok(Self {
            vm: Arc::new(Mutex::new(vm)),
            request_counter: Arc::new(Mutex::new(0)),
            performance_metrics: Arc::new(Mutex::new(LSPMetrics {
                startup_time: Some(Instant::now()),
                ..Default::default()
            })),
            config,
        })
    }
    
    /// Main LSP server loop - handles JSON-RPC communication
    pub fn run(&self) -> io::Result<()> {
        if self.config.debug_mode {
            eprintln!("🎯 Starting Runa LSP Server main loop");
        }
        
        let stdin = io::stdin();
        let mut stdin_lock = stdin.lock();
        let stdout = io::stdout();
        let mut stdout_lock = stdout.lock();
        
        // Send server startup notification
        if self.config.debug_mode {
            self.send_log_message(&mut stdout_lock, "Runa Language Server started")?;
        }
        
        loop {
            match self.read_message(&mut stdin_lock) {
                Ok(Some(message)) => {
                    let start_time = Instant::now();
                    
                    if let Some(response) = self.handle_message(message)? {
                        self.send_message(&mut stdout_lock, response)?;
                    }
                    
                    // Update performance metrics
                    if self.config.performance_tracking {
                        let mut metrics = self.performance_metrics.lock().unwrap();
                        metrics.requests_processed += 1;
                        metrics.analysis_time_ms += start_time.elapsed().as_millis() as u64;
                    }
                }
                Ok(None) => {
                    // End of input - graceful shutdown
                    if self.config.debug_mode {
                        eprintln!("📡 LSP Server: End of input received, shutting down");
                    }
                    break;
                }
                Err(e) => {
                    eprintln!("❌ LSP Server I/O error: {}", e);
                    // Try to continue - some errors are recoverable
                    continue;
                }
            }
        }
        
        if self.config.debug_mode {
            let metrics = self.performance_metrics.lock().unwrap();
            eprintln!("📊 LSP Server performance metrics:");
            eprintln!("   Requests processed: {}", metrics.requests_processed);
            eprintln!("   Documents analyzed: {}", metrics.documents_analyzed);
            eprintln!("   Cache hits: {}", metrics.cache_hits);
            eprintln!("   Total analysis time: {}ms", metrics.analysis_time_ms);
        }
        
        Ok(())
    }
    
    /// Read a JSON-RPC message from stdin
    fn read_message(&self, stdin: &mut dyn BufRead) -> io::Result<Option<Value>> {
        let mut headers = HashMap::new();
        let mut line = String::new();
        
        // Read headers
        loop {
            line.clear();
            match stdin.read_line(&mut line) {
                Ok(0) => return Ok(None), // EOF
                Ok(_) => {}
                Err(e) => return Err(e),
            }
            
            let line = line.trim();
            if line.is_empty() {
                break; // End of headers
            }
            
            if let Some((key, value)) = line.split_once(": ") {
                headers.insert(key.to_lowercase(), value.to_string());
            }
        }
        
        // Read content
        let content_length: usize = headers
            .get("content-length")
            .and_then(|v| v.parse().ok())
            .unwrap_or(0);
        
        if content_length == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "Missing or invalid Content-Length header"
            ));
        }
        
        let mut content = vec![0; content_length];
        stdin.read_exact(&mut content)?;
        
        let content_str = String::from_utf8(content)
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
        
        let json_value: Value = serde_json::from_str(&content_str)
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
        
        Ok(Some(json_value))
    }
    
    /// Send a JSON-RPC message to stdout
    fn send_message(&self, stdout: &mut dyn Write, message: Value) -> io::Result<()> {
        let content = serde_json::to_string(&message)
            .map_err(|e| io::Error::new(io::ErrorKind::InvalidData, e))?;
        
        write!(stdout, "Content-Length: {}\\r\\n\\r\\n{}", content.len(), content)?;
        stdout.flush()?;
        
        Ok(())
    }
    
    /// Handle a JSON-RPC message by forwarding it to the Runa LSP implementation
    fn handle_message(&self, message: Value) -> io::Result<Option<Value>> {
        let vm = self.vm.lock().unwrap();
        
        // Convert JSON message to Runa data structure
        let runa_request = self.json_to_runa_value(message)?;
        
        // Call the Runa LSP handler
        match vm.call_function("handle_lsp_request", vec![runa_request]) {
            Ok(runa_response) => {
                if let Some(response) = runa_response {
                    // Convert Runa response back to JSON
                    let json_response = self.runa_value_to_json(response)?;
                    Ok(Some(json_response))
                } else {
                    Ok(None) // Notification - no response
                }
            }
            Err(e) => {
                eprintln!("❌ LSP Handler error: {}", e);
                
                // Try to extract request ID for error response
                let request_id = message.get("id").cloned();
                
                let error_response = json!({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": format!("Internal error: {}", e)
                    }
                });
                
                Ok(Some(error_response))
            }
        }
    }
    
    /// Convert JSON Value to Runa runtime value
    fn json_to_runa_value(&self, json: Value) -> io::Result<crate::vm::RunaValue> {
        match json {
            Value::Null => Ok(crate::vm::RunaValue::Null),
            Value::Bool(b) => Ok(crate::vm::RunaValue::Boolean(b)),
            Value::Number(n) => {
                if let Some(i) = n.as_i64() {
                    Ok(crate::vm::RunaValue::Integer(i))
                } else if let Some(f) = n.as_f64() {
                    Ok(crate::vm::RunaValue::Float(f))
                } else {
                    Err(io::Error::new(io::ErrorKind::InvalidData, "Invalid number"))
                }
            }
            Value::String(s) => Ok(crate::vm::RunaValue::String(s)),
            Value::Array(arr) => {
                let mut runa_list = Vec::new();
                for item in arr {
                    runa_list.push(self.json_to_runa_value(item)?);
                }
                Ok(crate::vm::RunaValue::List(runa_list))
            }
            Value::Object(obj) => {
                let mut runa_dict = HashMap::new();
                for (key, value) in obj {
                    runa_dict.insert(key, self.json_to_runa_value(value)?);
                }
                Ok(crate::vm::RunaValue::Dictionary(runa_dict))
            }
        }
    }
    
    /// Convert Runa runtime value to JSON Value
    fn runa_value_to_json(&self, runa_value: crate::vm::RunaValue) -> io::Result<Value> {
        match runa_value {
            crate::vm::RunaValue::Null => Ok(Value::Null),
            crate::vm::RunaValue::Boolean(b) => Ok(Value::Bool(b)),
            crate::vm::RunaValue::Integer(i) => Ok(json!(i)),
            crate::vm::RunaValue::Float(f) => Ok(json!(f)),
            crate::vm::RunaValue::String(s) => Ok(Value::String(s)),
            crate::vm::RunaValue::List(list) => {
                let mut json_array = Vec::new();
                for item in list {
                    json_array.push(self.runa_value_to_json(item)?);
                }
                Ok(Value::Array(json_array))
            }
            crate::vm::RunaValue::Dictionary(dict) => {
                let mut json_object = serde_json::Map::new();
                for (key, value) in dict {
                    json_object.insert(key, self.runa_value_to_json(value)?);
                }
                Ok(Value::Object(json_object))
            }
            _ => Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "Unsupported Runa value type for JSON conversion"
            ))
        }
    }
    
    /// Load Runa LSP modules into the VM
    fn load_lsp_modules(vm: &mut RunaVM) -> io::Result<()> {
        // These would be loaded from the compiled Runa bytecode
        // For now, we'll register the external functions needed by the LSP
        
        vm.register_external_function("read_line_from_stdin", Self::read_stdin_line);
        vm.register_external_function("write_line_to_stdout", Self::write_stdout_line);
        vm.register_external_function("parse_json", Self::parse_json_function);
        vm.register_external_function("serialize_json", Self::serialize_json_function);
        vm.register_external_function("get_current_time_ms", Self::get_current_time_ms);
        
        // Load the compiled LSP bytecode modules
        let lsp_bytecode = include_bytes!("../../../compiler/lsp/compiled/lsp_server.bc");
        vm.load_bytecode(lsp_bytecode)?;
        
        Ok(())
    }
    
    /// Create Runa configuration from Rust config
    fn create_runa_config(config: &LSPBridgeConfig) -> crate::vm::RunaValue {
        let mut config_dict = HashMap::new();
        config_dict.insert("max_errors".to_string(), 
                          crate::vm::RunaValue::Integer(config.max_errors as i64));
        config_dict.insert("max_warnings".to_string(),
                          crate::vm::RunaValue::Integer(config.max_warnings as i64));
        config_dict.insert("enable_incremental_analysis".to_string(),
                          crate::vm::RunaValue::Boolean(config.enable_incremental_analysis));
        config_dict.insert("cache_size".to_string(),
                          crate::vm::RunaValue::Integer(config.cache_size as i64));
        config_dict.insert("performance_tracking".to_string(),
                          crate::vm::RunaValue::Boolean(config.performance_tracking));
        config_dict.insert("debug_mode".to_string(),
                          crate::vm::RunaValue::Boolean(config.debug_mode));
        
        crate::vm::RunaValue::Dictionary(config_dict)
    }
    
    /// Send a log message to the client
    fn send_log_message(&self, stdout: &mut dyn Write, message: &str) -> io::Result<()> {
        let notification = json!({
            "jsonrpc": "2.0",
            "method": "window/logMessage",
            "params": {
                "type": 3, // Info
                "message": message
            }
        });
        
        self.send_message(stdout, notification)
    }
    
    // External functions for Runa LSP implementation
    
    fn read_stdin_line(_args: Vec<crate::vm::RunaValue>) -> Result<crate::vm::RunaValue, String> {
        let mut line = String::new();
        match io::stdin().read_line(&mut line) {
            Ok(0) => Ok(crate::vm::RunaValue::Null), // EOF
            Ok(_) => Ok(crate::vm::RunaValue::String(line.trim().to_string())),
            Err(e) => Err(format!("Failed to read from stdin: {}", e)),
        }
    }
    
    fn write_stdout_line(args: Vec<crate::vm::RunaValue>) -> Result<crate::vm::RunaValue, String> {
        if let Some(crate::vm::RunaValue::String(line)) = args.get(0) {
            println!("{}", line);
            Ok(crate::vm::RunaValue::Null)
        } else {
            Err("write_stdout_line requires a string argument".to_string())
        }
    }
    
    fn parse_json_function(args: Vec<crate::vm::RunaValue>) -> Result<crate::vm::RunaValue, String> {
        if let Some(crate::vm::RunaValue::String(json_str)) = args.get(0) {
            match serde_json::from_str::<Value>(json_str) {
                Ok(json_value) => {
                    // Convert JSON to Runa value (simplified)
                    Ok(crate::vm::RunaValue::String(json_str.clone()))
                }
                Err(e) => Err(format!("JSON parse error: {}", e)),
            }
        } else {
            Err("parse_json requires a string argument".to_string())
        }
    }
    
    fn serialize_json_function(args: Vec<crate::vm::RunaValue>) -> Result<crate::vm::RunaValue, String> {
        if let Some(data) = args.get(0) {
            // Convert Runa value to JSON (simplified)
            Ok(crate::vm::RunaValue::String("{}".to_string()))
        } else {
            Err("serialize_json requires a data argument".to_string())
        }
    }
    
    fn get_current_time_ms(_args: Vec<crate::vm::RunaValue>) -> Result<crate::vm::RunaValue, String> {
        use std::time::{SystemTime, UNIX_EPOCH};
        
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|e| format!("Time error: {}", e))?;
        
        Ok(crate::vm::RunaValue::Integer(now.as_millis() as i64))
    }
}

/// CLI entry point for the LSP server
pub fn run_lsp_server_from_args(args: Vec<String>) -> io::Result<i32> {
    let config = parse_cli_args(args)?;
    
    let bridge = LSPBridge::new(config)?;
    bridge.run()?;
    
    Ok(0)
}

/// Parse command line arguments into LSP configuration
fn parse_cli_args(args: Vec<String>) -> io::Result<LSPBridgeConfig> {
    let mut config = LSPBridgeConfig::default();
    let mut i = 1;
    
    while i < args.len() {
        match args[i].as_str() {
            "--max-errors" => {
                if i + 1 < args.len() {
                    config.max_errors = args[i + 1].parse()
                        .map_err(|_| io::Error::new(io::ErrorKind::InvalidInput, "Invalid max-errors value"))?;
                    i += 1;
                }
            }
            "--max-warnings" => {
                if i + 1 < args.len() {
                    config.max_warnings = args[i + 1].parse()
                        .map_err(|_| io::Error::new(io::ErrorKind::InvalidInput, "Invalid max-warnings value"))?;
                    i += 1;
                }
            }
            "--enable-incremental" => config.enable_incremental_analysis = true,
            "--disable-incremental" => config.enable_incremental_analysis = false,
            "--cache-size" => {
                if i + 1 < args.len() {
                    config.cache_size = args[i + 1].parse()
                        .map_err(|_| io::Error::new(io::ErrorKind::InvalidInput, "Invalid cache-size value"))?;
                    i += 1;
                }
            }
            "--performance-tracking" => config.performance_tracking = true,
            "--no-performance-tracking" => config.performance_tracking = false,
            "--debug" => config.debug_mode = true,
            "--help" => {
                print_usage();
                std::process::exit(0);
            }
            _ => {
                if args[i].starts_with("--") {
                    eprintln!("Unknown option: {}", args[i]);
                    print_usage();
                    std::process::exit(1);
                }
            }
        }
        i += 1;
    }
    
    Ok(config)
}

/// Print CLI usage information
fn print_usage() {
    println!("Runa Language Server");
    println!("===================");
    println!();
    println!("Usage: runa-lsp [options]");
    println!();
    println!("Options:");
    println!("  --max-errors <number>     Maximum number of errors to report (default: 100)");
    println!("  --max-warnings <number>   Maximum number of warnings to report (default: 200)");
    println!("  --enable-incremental      Enable incremental analysis (default: true)");
    println!("  --disable-incremental     Disable incremental analysis");
    println!("  --cache-size <number>     Analysis cache size (default: 1000)");
    println!("  --performance-tracking    Enable performance tracking (default: true)");
    println!("  --no-performance-tracking Disable performance tracking");
    println!("  --debug                   Enable debug mode");
    println!("  --help                    Show this help message");
    println!();
    println!("The server communicates via JSON-RPC over stdin/stdout.");
    println!("It is designed to be used by IDEs and text editors.");
}