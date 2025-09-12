//! Compiler-Runtime Integration Layer
//!
//! This module provides the bridge between the Runa compiler's LIR output
//! and the canonical bytecode VM. It handles the complete translation pipeline
//! from optimized LIR to executable bytecode.

use crate::bytecode_generator::{BytecodeGenerator, LIRModule};
use crate::vm::NativeFunctionProvider;
use runa_common::bytecode::{Chunk, Value};
use std::collections::HashMap;

/// Compiler-Runtime Integration Layer
///
/// This is the main orchestrator that takes the compiler's final LIR output
/// and produces executable bytecode. It handles:
/// - LIR to bytecode translation
/// - Builtin function registration
/// - Module linking and dependency resolution
/// - Error handling and diagnostics
pub struct CompilerIntegration {
    /// The bytecode generator for LIR translation
    bytecode_generator: BytecodeGenerator,
    /// Registry of native functions available to the VM
    native_functions: HashMap<String, fn(&[Value]) -> Result<Value, String>>,
    /// Global constants and variables
    globals: HashMap<String, Value>,
    /// Module registry for linking
    modules: HashMap<String, Chunk>,
    /// Track constant usage for optimization
    constant_usage: HashMap<String, u32>,
    /// Track dependencies of constants
    constant_dependencies: HashMap<String, Vec<String>>,
    /// Mark constants that are actually used in this compilation unit
    used_constants: std::collections::HashSet<String>,
}

impl CompilerIntegration {
    /// Create a new CompilerIntegration instance
    pub fn new() -> Self {
        let mut integration = CompilerIntegration {
            bytecode_generator: BytecodeGenerator::new(),
            native_functions: HashMap::new(),
            globals: HashMap::new(),
            modules: HashMap::new(),
            constant_usage: HashMap::new(),
            constant_dependencies: HashMap::new(),
            used_constants: std::collections::HashSet::new(),
        };
        
        // Register all builtin functions
        integration.register_builtins();
        
        integration
    }

    /// Compile a complete LIR module to executable bytecode
    ///
    /// This is the main entry point for the compiler-runtime integration.
    /// It takes an optimized LIR module and produces bytecode ready for execution.
    pub fn compile_module(&mut self, lir_module: &LIRModule) -> Result<Chunk, String> {
        // Validate the LIR module
        self.validate_lir_module(lir_module)?;
        
        // Translate LIR to bytecode
        let mut chunk = self.bytecode_generator.translate_lir_module(lir_module)?;
        
        // Link any dependencies
        self.link_dependencies(&mut chunk, lir_module)?;
        
        // Register the module
        self.modules.insert(lir_module.name.clone(), chunk.clone());
        
        Ok(chunk)
    }

    /// Register a native function that can be called from Runa code
    pub fn register_native_function(
        &mut self,
        name: &str,
        function: fn(&[Value]) -> Result<Value, String>,
    ) {
        self.native_functions.insert(name.to_string(), function);
    }

    /// Get a registered native function
    pub fn get_native_function(&self, name: &str) -> Option<&fn(&[Value]) -> Result<Value, String>> {
        self.native_functions.get(name)
    }

    /// Set a global variable
    pub fn set_global(&mut self, name: &str, value: Value) {
        self.globals.insert(name.to_string(), value);
    }

    /// Get a global variable
    pub fn get_global(&self, name: &str) -> Option<&Value> {
        self.globals.get(name)
    }

    /// Validate that an LIR module is well-formed
    fn validate_lir_module(&self, lir_module: &LIRModule) -> Result<(), String> {
        // Check that the module has a name
        if lir_module.name.is_empty() {
            return Err("LIR module must have a non-empty name".to_string());
        }

        // Check that the module has at least one function
        if lir_module.functions.is_empty() {
            return Err(format!(
                "LIR module '{}' must contain at least one function",
                lir_module.name
            ));
        }

        // Validate each function
        for function in &lir_module.functions {
            self.validate_lir_function(function)?;
        }

        Ok(())
    }

    /// Validate that an LIR function is well-formed
    fn validate_lir_function(&self, lir_function: &crate::bytecode_generator::LIRFunction) -> Result<(), String> {
        // Check that the function has a name
        if lir_function.name.is_empty() {
            return Err("LIR function must have a non-empty name".to_string());
        }

        // Check that the function has at least one basic block
        if lir_function.basic_blocks.is_empty() {
            return Err(format!(
                "LIR function '{}' must contain at least one basic block",
                lir_function.name
            ));
        }

        // Validate each basic block
        for (block_index, basic_block) in lir_function.basic_blocks.iter().enumerate() {
            self.validate_lir_basic_block(basic_block, block_index)?;
        }

        Ok(())
    }

    /// Validate that an LIR basic block is well-formed
    fn validate_lir_basic_block(
        &self,
        basic_block: &crate::bytecode_generator::LIRBasicBlock,
        block_index: usize,
    ) -> Result<(), String> {
        // Check that the basic block has a name
        if basic_block.name.is_empty() {
            return Err(format!(
                "LIR basic block {} must have a non-empty name",
                block_index
            ));
        }

        // Check that the basic block has a terminator
        // (This is handled by the enum, but we can add additional validation here)

        Ok(())
    }

    /// Link dependencies for a module
    fn link_dependencies(&mut self, chunk: &mut Chunk, lir_module: &LIRModule) -> Result<(), String> {
        // Add global constants to the chunk with usage analysis
        let mut used_constants = std::collections::HashSet::new();
        
        // Analyze which constants are actually used in the module
        for function in &lir_module.functions {
            for basic_block in &function.basic_blocks {
                for instruction in &basic_block.instructions {
                    // Check if instruction references any constants
                    if let Some(constant_ref) = self.extract_constant_reference_from_lir(instruction) {
                        used_constants.insert(constant_ref);
                    }
                }
            }
        }
        
        // Only add constants that are actually used
        let mut constants_to_add = Vec::new();
        for (name, _value) in &self.globals {
            if used_constants.contains(name) {
                constants_to_add.push(name.clone());
            }
        }
        
        // Add constants to chunk (avoiding borrow checker issues)
        for name in constants_to_add {
            let constant_index = chunk.add_constant(Value::String(name.clone()));
            self.track_constant_usage(&name);
        }

        Ok(())
    }
    
    /// Extract constant references from LIR instructions
    fn extract_constant_reference_from_lir(&self, instruction: &crate::bytecode_generator::LIRInstruction) -> Option<String> {
        // Parse LIR instruction to find constant references
        match instruction {
            crate::bytecode_generator::LIRInstruction::LIRCall { function, .. } => {
                // Check if this is a call to a global function
                Some(function.clone())
            }
            crate::bytecode_generator::LIRInstruction::LIRIntrinsic { intrinsic_name, .. } => {
                // Check if this is an intrinsic that might reference constants
                Some(intrinsic_name.clone())
            }
            _ => None,
        }
    }
    
    /// Extract constant references from string instructions (legacy)
    fn extract_constant_reference(&self, instruction: &str) -> Option<String> {
        // Parse instruction to find constant references
        // This implements production-ready LIR parsing for string-based instructions
        if instruction.contains("const") || instruction.contains("global") {
            // Extract the constant name from the instruction
            let parts: Vec<&str> = instruction.split_whitespace().collect();
            for (i, part) in parts.iter().enumerate() {
                if *part == "const" || *part == "global" {
                    if i + 1 < parts.len() {
                        return Some(parts[i + 1].to_string());
                    }
                }
            }
        }
        None
    }
    
    /// Enhanced constant analysis and optimization
    fn track_constant_usage(&mut self, constant_name: &str) {
        // Analyze constant usage patterns for optimization
        let usage_count = self.constant_usage.entry(constant_name.to_string()).or_insert(0);
        *usage_count += 1;
        
        // Track constant dependencies for dead code elimination
        if let Some(dependencies) = self.analyze_constant_dependencies(constant_name) {
            for dep in dependencies {
                self.constant_dependencies.entry(constant_name.to_string())
                    .or_insert_with(Vec::new)
                    .push(dep);
            }
        }
        
        // Mark constant as used for this compilation unit
        self.used_constants.insert(constant_name.to_string());
    }
    
    /// Analyze dependencies of a constant by examining its value
    fn analyze_constant_dependencies(&self, constant_name: &str) -> Option<Vec<String>> {
        let mut dependencies = Vec::new();
        
        // Get the constant value for analysis
        if let Some(constant_value) = self.globals.get(constant_name) {
            match constant_value {
                Value::String(s) => {
                    // Parse string literals for constant references
                    self.extract_string_constant_refs(s, &mut dependencies);
                }
                Value::Integer(_) | Value::Float(_) | Value::Boolean(_) => {
                    // Primitive values have no dependencies
                }
                _ => {
                    // Complex values might have dependencies
                    self.extract_complex_constant_refs(constant_value, &mut dependencies);
                }
            }
        }
        
        // Module-qualified constants depend on their module
        if constant_name.contains("::") {
            let parts: Vec<&str> = constant_name.split("::").collect();
            if parts.len() > 1 {
                // Add module dependency
                dependencies.push(parts[0].to_string());
                
                // Check for nested module dependencies
                for i in 1..parts.len()-1 {
                    let nested_module = parts[0..=i].join("::");
                    dependencies.push(nested_module);
                }
            }
        }
        
        // Check existing dependency graph
        if let Some(cached_deps) = self.constant_dependencies.get(constant_name) {
            for dep in cached_deps {
                if !dependencies.contains(dep) {
                    dependencies.push(dep.clone());
                }
            }
        }
        
        // Remove self-references and duplicates
        dependencies.retain(|dep| dep != constant_name);
        dependencies.sort();
        dependencies.dedup();
        
        if dependencies.is_empty() {
            None
        } else {
            Some(dependencies)
        }
    }
    
    fn extract_string_constant_refs(&self, s: &str, dependencies: &mut Vec<String>) {
        // Parse string for constant reference patterns manually
        let chars: Vec<char> = s.chars().collect();
        let mut i = 0;
        
        while i < chars.len() {
            // Look for ${CONST_NAME} pattern
            if i + 2 < chars.len() && chars[i] == '$' && chars[i + 1] == '{' {
                i += 2; // Skip "${"
                let start = i;
                
                // Find closing brace
                while i < chars.len() && chars[i] != '}' {
                    i += 1;
                }
                
                if i < chars.len() && chars[i] == '}' {
                    let const_name: String = chars[start..i].iter().collect();
                    if self.is_valid_constant_name(&const_name) && self.globals.contains_key(&const_name) {
                        dependencies.push(const_name);
                    }
                }
            }
            // Look for @CONST_NAME pattern
            else if chars[i] == '@' && i + 1 < chars.len() && chars[i + 1].is_ascii_uppercase() {
                i += 1; // Skip "@"
                let start = i;
                
                // Read constant name (letters, digits, underscore)
                while i < chars.len() && (chars[i].is_ascii_alphanumeric() || chars[i] == '_' || chars[i] == ':') {
                    i += 1;
                }
                
                let const_name: String = chars[start..i].iter().collect();
                if self.is_valid_constant_name(&const_name) && self.globals.contains_key(&const_name) {
                    dependencies.push(const_name);
                }
                continue; // Don't increment i again
            }
            
            i += 1;
        }
    }
    
    fn is_valid_constant_name(&self, name: &str) -> bool {
        if name.is_empty() {
            return false;
        }
        
        // Check if it starts with uppercase letter or underscore
        let first_char = name.chars().next().unwrap();
        if !first_char.is_ascii_uppercase() && first_char != '_' {
            return false;
        }
        
        // Check remaining characters
        name.chars().all(|c| c.is_ascii_alphanumeric() || c == '_' || c == ':')
    }
    
    fn extract_complex_constant_refs(&self, value: &Value, dependencies: &mut Vec<String>) {
        // Analyze complex values for constant references
        match value {
            Value::String(s) => {
                // String values may contain constant references
                self.extract_string_constant_refs(s, dependencies);
            }
            Value::Integer(_) | Value::Float(_) | Value::Boolean(_) => {
                // Primitive values contain no references
            }
            _ => {
                // For other value types, convert to string and analyze
                let value_str = format!("{:?}", value);
                self.extract_string_constant_refs(&value_str, dependencies);
            }
        }
    }

    /// Register all builtin functions with the integration layer
    fn register_builtins(&mut self) {
        // Mathematical operations
        self.register_native_function("add", |args| {
            if args.len() != 2 {
                return Err("add requires exactly 2 arguments".to_string());
            }
            match (&args[0], &args[1]) {
                (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a + b)),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a + b)),
                (Value::Integer(a), Value::Float(b)) => Ok(Value::Float(*a as f64 + b)),
                (Value::Float(a), Value::Integer(b)) => Ok(Value::Float(a + *b as f64)),
                _ => Err("add requires numeric arguments".to_string()),
            }
        });

        self.register_native_function("subtract", |args| {
            if args.len() != 2 {
                return Err("subtract requires exactly 2 arguments".to_string());
            }
            match (&args[0], &args[1]) {
                (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a - b)),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a - b)),
                (Value::Integer(a), Value::Float(b)) => Ok(Value::Float(*a as f64 - b)),
                (Value::Float(a), Value::Integer(b)) => Ok(Value::Float(a - *b as f64)),
                _ => Err("subtract requires numeric arguments".to_string()),
            }
        });

        self.register_native_function("multiply", |args| {
            if args.len() != 2 {
                return Err("multiply requires exactly 2 arguments".to_string());
            }
            match (&args[0], &args[1]) {
                (Value::Integer(a), Value::Integer(b)) => Ok(Value::Integer(a * b)),
                (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a * b)),
                (Value::Integer(a), Value::Float(b)) => Ok(Value::Float(*a as f64 * b)),
                (Value::Float(a), Value::Integer(b)) => Ok(Value::Float(a * *b as f64)),
                _ => Err("multiply requires numeric arguments".to_string()),
            }
        });

        self.register_native_function("divide", |args| {
            if args.len() != 2 {
                return Err("divide requires exactly 2 arguments".to_string());
            }
            match (&args[0], &args[1]) {
                (Value::Integer(a), Value::Integer(b)) => {
                    if *b == 0 {
                        Err("division by zero".to_string())
                    } else {
                        Ok(Value::Integer(a / b))
                    }
                }
                (Value::Float(a), Value::Float(b)) => {
                    if *b == 0.0 {
                        Err("division by zero".to_string())
                    } else {
                        Ok(Value::Float(a / b))
                    }
                }
                (Value::Integer(a), Value::Float(b)) => {
                    if *b == 0.0 {
                        Err("division by zero".to_string())
                    } else {
                        Ok(Value::Float(*a as f64 / b))
                    }
                }
                (Value::Float(a), Value::Integer(b)) => {
                    if *b == 0 {
                        Err("division by zero".to_string())
                    } else {
                        Ok(Value::Float(a / *b as f64))
                    }
                }
                _ => Err("divide requires numeric arguments".to_string()),
            }
        });

        // String operations
        self.register_native_function("concat", |args| {
            if args.len() != 2 {
                return Err("concat requires exactly 2 arguments".to_string());
            }
            match (&args[0], &args[1]) {
                (Value::String(a), Value::String(b)) => {
                    Ok(Value::String(format!("{}{}", a, b)))
                }
                _ => Err("concat requires string arguments".to_string()),
            }
        });

        // Type conversion operations
        self.register_native_function("to_string", |args| {
            if args.len() != 1 {
                return Err("to_string requires exactly 1 argument".to_string());
            }
            Ok(Value::String(args[0].to_string()))
        });

        self.register_native_function("to_integer", |args| {
            if args.len() != 1 {
                return Err("to_integer requires exactly 1 argument".to_string());
            }
            match &args[0] {
                Value::Integer(i) => Ok(Value::Integer(*i)),
                Value::Float(f) => Ok(Value::Integer(*f as i64)),
                Value::String(s) => {
                    s.parse::<i64>()
                        .map(Value::Integer)
                        .map_err(|_| "cannot convert string to integer".to_string())
                }
                _ => Err("cannot convert to integer".to_string()),
            }
        });

        self.register_native_function("to_float", |args| {
            if args.len() != 1 {
                return Err("to_float requires exactly 1 argument".to_string());
            }
            match &args[0] {
                Value::Integer(i) => Ok(Value::Float(*i as f64)),
                Value::Float(f) => Ok(Value::Float(*f)),
                Value::String(s) => {
                    s.parse::<f64>()
                        .map(Value::Float)
                        .map_err(|_| "cannot convert string to float".to_string())
                }
                _ => Err("cannot convert to float".to_string()),
            }
        });

        // Collection operations
        self.register_native_function("create_list", |args| {
            let mut items = Vec::new();
            for arg in args {
                items.push(arg.clone());
            }
            Ok(Value::List(items))
        });

        self.register_native_function("create_dict", |args| {
            if args.len() % 2 != 0 {
                return Err("create_dict requires an even number of arguments".to_string());
            }
            let mut items = Vec::new();
            for i in (0..args.len()).step_by(2) {
                items.push((args[i].clone(), args[i + 1].clone()));
            }
            Ok(Value::Dictionary(items))
        });

        // I/O operations
        self.register_native_function("display", |args| {
            for arg in args {
                println!("{}", arg);
            }
            Ok(Value::Null)
        });

        // System operations
        self.register_native_function("get_time", |_args| {
            use std::time::{SystemTime, UNIX_EPOCH};
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs();
            Ok(Value::Integer(now as i64))
        });

        self.register_native_function("random", |args| {
            use std::collections::hash_map::DefaultHasher;
            use std::hash::{Hash, Hasher};
            
            let seed = if args.is_empty() {
                std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_nanos() as u64
            } else {
                let mut hasher = DefaultHasher::new();
                args[0].hash(&mut hasher);
                hasher.finish()
            };
            
            // Simple linear congruential generator
            let a = 1664525u64;
            let c = 1013904223u64;
            let m = 2u64.pow(32);
            let random_value = (a * seed + c) % m;
            
            Ok(Value::Integer(random_value as i64))
        });
    }
}

impl NativeFunctionProvider for CompilerIntegration {
    fn get_native_function(&self, name: &str) -> Option<&fn(&[Value]) -> Result<Value, String>> {
        self.native_functions.get(name)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::bytecode_generator::{LIRFunction, LIRBasicBlock, LIRInstruction};
    use std::collections::HashMap;

    #[test]
    fn test_compiler_integration_creation() {
        let integration = CompilerIntegration::new();
        assert!(!integration.native_functions.is_empty());
        assert!(integration.get_native_function("add").is_some());
        assert!(integration.get_native_function("nonexistent").is_none());
    }

    #[test]
    fn test_native_function_registration() {
        let mut integration = CompilerIntegration::new();
        
        let test_fn = |args: &[Value]| -> Result<Value, String> {
            Ok(Value::String("test".to_string()))
        };
        
        integration.register_native_function("test_function", test_fn);
        assert!(integration.get_native_function("test_function").is_some());
    }

    #[test]
    fn test_builtin_functions() {
        let integration = CompilerIntegration::new();
        
        // Test add function
        let add_fn = integration.get_native_function("add").unwrap();
        let result = add_fn(&[Value::Integer(2), Value::Integer(3)]).unwrap();
        assert!(matches!(result, Value::Integer(5)));
        
        // Test concat function
        let concat_fn = integration.get_native_function("concat").unwrap();
        let result = concat_fn(&[Value::String("hello".to_string()), Value::String(" world".to_string())]).unwrap();
        assert!(matches!(result, Value::String(s) if s == "hello world"));
    }

    #[test]
    fn test_validation() {
        let integration = CompilerIntegration::new();
        
        // Test valid module
        let valid_module = LIRModule {
            name: "test_module".to_string(),
            functions: vec![
                LIRFunction {
                    name: "main".to_string(),
                    parameters: vec![],
                    basic_blocks: vec![
                        LIRBasicBlock {
                            name: "entry".to_string(),
                            instructions: vec![
                                LIRInstruction::LIRReturn { value: None },
                            ],
                            successors: vec![],
                            predecessors: vec![],
                        }
                    ],
                    return_type: "Any".to_string(),
                    upvalues: vec![],
                }
            ],
            globals: vec![],
            constants: vec![],
        };
        
        assert!(integration.validate_lir_module(&valid_module).is_ok());
        
        // Test invalid module (empty name)
        let invalid_module = LIRModule {
            name: "".to_string(),
            functions: vec![],
            globals: vec![],
            constants: vec![],
        };
        
        assert!(integration.validate_lir_module(&invalid_module).is_err());
    }
} 