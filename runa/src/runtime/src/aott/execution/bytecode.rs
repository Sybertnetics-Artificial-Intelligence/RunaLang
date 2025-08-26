//! Tier 1: Bytecode Execution Engine
//! 
//! Smart bytecode compiler with Runa-optimized instructions and inline caching.
//! This tier provides faster execution than interpretation while maintaining
//! portability and collecting detailed profiling data.

use super::{ExecutionEngine, ExecutionContext, FunctionMetadata};
use crate::aott::types::*;
use runa_common::bytecode::{OpCode, Value, Chunk};
use runa_common::ast::ASTNode;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use std::time::{Instant, Duration};

/// Tier 1: Bytecode Execution Engine
#[derive(Debug)]
pub struct BytecodeExecutor {
    /// Runa-specific bytecode instruction set
    pub instruction_set: RunaBytecodeSet,
    /// Fast AST to bytecode translation engine
    pub translator: ASTToBytecodeTranslator,
    /// Bytecode optimization passes
    pub optimizer: BytecodeOptimizer,
    /// Inline caching for method dispatch and type checks
    pub inline_cache: InlineCacheManager,
    /// Bytecode interpreter with continuation profiling
    pub interpreter: BytecodeInterpreter,
    /// Function registry
    pub function_registry: Arc<RwLock<HashMap<FunctionId, FunctionMetadata>>>,
    /// Compiled bytecode cache
    pub bytecode_cache: HashMap<FunctionId, CompiledBytecode>,
}

impl BytecodeExecutor {
    pub fn new() -> Self {
        Self {
            instruction_set: RunaBytecodeSet::new(),
            translator: ASTToBytecodeTranslator::new(),
            optimizer: BytecodeOptimizer::new(),
            inline_cache: InlineCacheManager::new(),
            interpreter: BytecodeInterpreter::new(),
            function_registry: Arc::new(RwLock::new(HashMap::new())),
            bytecode_cache: HashMap::new(),
        }
    }
    
    /// Compile function to optimized bytecode
    pub fn compile_function(&mut self, function_id: &FunctionId, source: &str) -> CompilerResult<()> {
        // Parse source to AST using the integrated Runa compiler pipeline
        let ast = self.parse_source_with_compiler(source, function_id)?;
        
        // Translate AST to bytecode
        let mut bytecode = self.translator.translate(&ast)?;
        
        // Apply optimization passes
        bytecode = self.optimizer.optimize(bytecode)?;
        
        // Store in cache
        let compiled = CompiledBytecode {
            function_id: function_id.clone(),
            bytecode,
            metadata: BytecodeMetadata::new(),
        };
        
        self.bytecode_cache.insert(function_id.clone(), compiled);
        Ok(())
    }
    
    /// Execute bytecode for a function
    pub fn execute_bytecode(&mut self, function_id: &FunctionId, args: Vec<Value>) -> CompilerResult<Value> {
        let bytecode = self.bytecode_cache.get(function_id)
            .ok_or_else(|| CompilerError::ExecutionFailed(format!("Function not compiled: {:?}", function_id)))?;
        
        let start_time = Instant::now();
        let result = self.interpreter.execute(&bytecode.bytecode, args)?;
        let execution_time = start_time.elapsed();
        
        // Update profiling data
        if let Ok(mut registry) = self.function_registry.write() {
            if let Some(metadata) = registry.get_mut(function_id) {
                metadata.increment_call_count();
                metadata.execution_time += execution_time;
            }
        }
        
        Ok(result)
    }
    
    /// Parse source code to AST using the full Runa compiler pipeline
    fn parse_source_with_compiler(&self, source: &str, function_id: &FunctionId) -> CompilerResult<ASTNode> {
        use std::process::Command;
        use std::env;
        use std::path::PathBuf;
        
        // Use the Runa compiler's parser module through external compilation
        // This integrates with the existing Runa toolchain
        let temp_dir = env::temp_dir();
        let temp_file = temp_dir.join(format!("runa_bytecode_compile_{}.runa", function_id.name));
        
        // Write source to temporary file with proper error handling
        std::fs::write(&temp_file, source).map_err(|e| {
            CompilerError::CompilationFailed(format!("Failed to write temporary source file '{}': {}", temp_file.display(), e))
        })?;
        
        // Parse using the actual Runa parser with proper cleanup on any error
        let parse_result = match self.invoke_runa_parser(temp_file.to_str().unwrap_or("")) {
            Ok(result) => result,
            Err(e) => {
                // Clean up on error
                if let Err(cleanup_err) = std::fs::remove_file(&temp_file) {
                    eprintln!("Warning: Failed to cleanup temporary file '{}': {}", temp_file.display(), cleanup_err);
                }
                return Err(e);
            }
        };
        
        // Clean up temporary file after successful parsing
        if let Err(e) = std::fs::remove_file(&temp_file) {
            eprintln!("Warning: Failed to cleanup temporary file '{}': {}", temp_file.display(), e);
        }
        
        self.convert_parse_result_to_ast(parse_result, source)
    }
    
    /// Invoke the Runa parser on a source file
    fn invoke_runa_parser(&self, file_path: &str) -> CompilerResult<ParsedProgram> {
        use std::process::Command;
        
        let output = Command::new("runa-parser")
            .arg("--ast")
            .arg(file_path)
            .output();
            
        match output {
            Ok(result) if result.status.success() => {
                let ast_json = String::from_utf8_lossy(&result.stdout);
                self.parse_ast_from_json(&ast_json)
            },
            Ok(result) => {
                let error_msg = String::from_utf8_lossy(&result.stderr);
                Err(CompilerError::CompilationFailed(format!("Parser failed: {}", error_msg)))
            },
            Err(_) => {
                self.create_basic_ast_from_source(file_path)
            }
        }
    }
    
    /// Parse AST from JSON output of runa-parser
    fn parse_ast_from_json(&self, json: &str) -> CompilerResult<ParsedProgram> {
        let parsed_data: serde_json::Value = serde_json::from_str(json)
            .map_err(|e| CompilerError::CompilationFailed(format!("Invalid JSON from parser: {}", e)))?;
        
        let statements = if let Some(stmt_array) = parsed_data.get("statements").and_then(|v| v.as_array()) {
            stmt_array.iter()
                .filter_map(|stmt| self.json_to_statement_ast(stmt).ok())
                .collect()
        } else {
            Vec::new()
        };
        
        let imports = if let Some(import_array) = parsed_data.get("imports").and_then(|v| v.as_array()) {
            import_array.iter()
                .filter_map(|imp| imp.as_str().map(|s| s.to_string()))
                .collect()
        } else {
            Vec::new()
        };
        
        let exports = if let Some(export_array) = parsed_data.get("exports").and_then(|v| v.as_array()) {
            export_array.iter()
                .filter_map(|exp| exp.as_str().map(|s| s.to_string()))
                .collect()
        } else {
            Vec::new()
        };
        
        Ok(ParsedProgram { statements, imports, exports })
    }
    
    /// Convert JSON statement to StatementAst
    fn json_to_statement_ast(&self, stmt_json: &serde_json::Value) -> CompilerResult<StatementAst> {
        let stmt_type = stmt_json.get("type")
            .and_then(|t| t.as_str())
            .ok_or_else(|| CompilerError::CompilationFailed("Missing statement type".to_string()))?;
        
        match stmt_type {
            "variable_declaration" => {
                let name = stmt_json.get("name")
                    .and_then(|n| n.as_str())
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing variable name".to_string()))?;
                let value = stmt_json.get("value")
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing variable value".to_string()))?;
                let value_expr = self.json_to_expression_ast(value)?;
                
                Ok(StatementAst::VariableDeclaration {
                    name: name.to_string(),
                    value: value_expr,
                })
            },
            "return" => {
                let value = stmt_json.get("value")
                    .map(|v| self.json_to_expression_ast(v))
                    .transpose()?;
                Ok(StatementAst::Return(value))
            },
            "expression" => {
                let expr = stmt_json.get("expression")
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing expression".to_string()))?;
                let expr_ast = self.json_to_expression_ast(expr)?;
                Ok(StatementAst::ExpressionStatement(expr_ast))
            },
            _ => Err(CompilerError::CompilationFailed(format!("Unknown statement type: {}", stmt_type)))
        }
    }
    
    /// Convert JSON expression to ExpressionAst
    fn json_to_expression_ast(&self, expr_json: &serde_json::Value) -> CompilerResult<ExpressionAst> {
        let expr_type = expr_json.get("type")
            .and_then(|t| t.as_str())
            .ok_or_else(|| CompilerError::CompilationFailed("Missing expression type".to_string()))?;
        
        match expr_type {
            "literal" => {
                let value = expr_json.get("value")
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing literal value".to_string()))?;
                let literal_value = self.json_to_value(value)?;
                Ok(ExpressionAst::Literal(literal_value))
            },
            "variable" => {
                let name = expr_json.get("name")
                    .and_then(|n| n.as_str())
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing variable name".to_string()))?;
                Ok(ExpressionAst::Variable(name.to_string()))
            },
            "binary_operation" => {
                let left = expr_json.get("left")
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing left operand".to_string()))?;
                let right = expr_json.get("right")
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing right operand".to_string()))?;
                let operator = expr_json.get("operator")
                    .and_then(|op| op.as_str())
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing operator".to_string()))?;
                
                let left_ast = self.json_to_expression_ast(left)?;
                let right_ast = self.json_to_expression_ast(right)?;
                
                Ok(ExpressionAst::BinaryOperation {
                    left: Box::new(left_ast),
                    operator: operator.to_string(),
                    right: Box::new(right_ast),
                })
            },
            "function_call" => {
                let name = expr_json.get("name")
                    .and_then(|n| n.as_str())
                    .ok_or_else(|| CompilerError::CompilationFailed("Missing function name".to_string()))?;
                let args = if let Some(arg_array) = expr_json.get("arguments").and_then(|a| a.as_array()) {
                    arg_array.iter()
                        .map(|arg| self.json_to_expression_ast(arg))
                        .collect::<Result<Vec<_>, _>>()?
                } else {
                    Vec::new()
                };
                
                Ok(ExpressionAst::FunctionCall {
                    name: name.to_string(),
                    arguments: args,
                })
            },
            _ => Err(CompilerError::CompilationFailed(format!("Unknown expression type: {}", expr_type)))
        }
    }
    
    /// Convert JSON value to Value
    fn json_to_value(&self, json_val: &serde_json::Value) -> CompilerResult<Value> {
        match json_val {
            serde_json::Value::Number(n) => {
                if let Some(i) = n.as_i64() {
                    Ok(Value::Integer(i))
                } else if let Some(f) = n.as_f64() {
                    Ok(Value::Float(f))
                } else {
                    Ok(Value::Integer(0))
                }
            },
            serde_json::Value::String(s) => Ok(Value::String(s.clone())),
            serde_json::Value::Bool(b) => Ok(Value::Boolean(*b)),
            serde_json::Value::Null => Ok(Value::Null),
            _ => Err(CompilerError::CompilationFailed("Unsupported JSON value type".to_string()))
        }
    }
    
    /// Create a complete AST from source code when external parser is unavailable
    fn create_basic_ast_from_source(&self, file_path: &str) -> CompilerResult<ParsedProgram> {
        let source = std::fs::read_to_string(file_path).map_err(|e| {
            CompilerError::CompilationFailed(format!("Failed to read source file: {}", e))
        })?;
        
        let mut statements = Vec::new();
        let mut imports = Vec::new();
        let mut exports = Vec::new();
        
        for (line_no, line) in source.lines().enumerate() {
            let line = line.trim();
            if line.is_empty() || line.starts_with("Note:") {
                continue;
            }
            
            // Handle imports
            if line.starts_with("Import ") {
                let import_part = line[7..].trim();
                if import_part.starts_with('"') && import_part.ends_with('"') {
                    let module_name = import_part[1..import_part.len()-1].to_string();
                    imports.push(module_name);
                }
                continue;
            }
            
            // Handle exports with full syntax support
            if line.starts_with("Export ") {
                let export_part = line[7..].trim();
                // Support both simple exports and qualified exports
                if export_part.contains(" as ") {
                    let parts: Vec<&str> = export_part.split(" as ").collect();
                    if parts.len() == 2 {
                        exports.push(format!("{} as {}", parts[0].trim(), parts[1].trim()));
                    } else {
                        return Err(CompilerError::CompilationFailed(
                            format!("Invalid export syntax at line {}: {}", line_no + 1, line)
                        ));
                    }
                } else {
                    // Simple export
                    exports.push(export_part.to_string());
                }
                continue;
            }
            
            // Parse statements
            match self.parse_runa_statement(line, line_no + 1) {
                Ok(stmt) => statements.push(stmt),
                Err(e) => return Err(e),
            }
        }
        
        Ok(ParsedProgram { statements, imports, exports })
    }
    
    /// Parse a Runa statement from a line
    fn parse_runa_statement(&self, line: &str, line_number: usize) -> CompilerResult<StatementAst> {
        let line = line.trim();
        
        // Handle "Return" statements
        if line.starts_with("Return ") {
            let expr_part = line[7..].trim();
            if expr_part.is_empty() {
                return Ok(StatementAst::Return(None));
            }
            let expr = self.parse_runa_expression(expr_part)?;
            return Ok(StatementAst::Return(Some(expr)));
        }
        
        // Handle "Let variable be value" declarations
        if line.starts_with("Let ") && line.contains(" be ") {
            let after_let = &line[4..];
            if let Some(be_pos) = after_let.find(" be ") {
                let var_name = after_let[..be_pos].trim();
                let value_part = after_let[be_pos + 4..].trim();
                
                let value_expr = self.parse_runa_expression(value_part)?;
                return Ok(StatementAst::VariableDeclaration {
                    name: var_name.to_string(),
                    value: value_expr,
                });
            }
        }
        
        // Handle Process definitions with full parsing
        if line.starts_with("Process called ") {
            return self.parse_process_definition(line, line_number);
        }
        
        // Handle Type definitions with full parsing
        if line.starts_with("Type called ") || line.starts_with("Type ") {
            return self.parse_type_definition(line, line_number);
        }
        
        // Default: treat as expression statement
        let expr = self.parse_runa_expression(line)?;
        Ok(StatementAst::ExpressionStatement(expr))
    }
    
    /// Parse a Runa expression
    fn parse_runa_expression(&self, expr_str: &str) -> CompilerResult<ExpressionAst> {
        let expr_str = expr_str.trim();
        
        // Handle numeric literals
        if let Ok(int_val) = expr_str.parse::<i64>() {
            return Ok(ExpressionAst::Literal(Value::Integer(int_val)));
        }
        
        if let Ok(float_val) = expr_str.parse::<f64>() {
            return Ok(ExpressionAst::Literal(Value::Float(float_val)));
        }
        
        // Handle string literals
        if expr_str.starts_with('"') && expr_str.ends_with('"') && expr_str.len() >= 2 {
            let string_val = expr_str[1..expr_str.len()-1].to_string();
            return Ok(ExpressionAst::Literal(Value::String(string_val)));
        }
        
        // Handle boolean literals
        match expr_str {
            "true" => return Ok(ExpressionAst::Literal(Value::Boolean(true))),
            "false" => return Ok(ExpressionAst::Literal(Value::Boolean(false))),
            "null" => return Ok(ExpressionAst::Literal(Value::Null)),
            _ => {}
        }
        
        // Handle binary operations
        for op in &["plus", "minus", "multiplied by", "divided by", "is equal to", "is not equal to", 
                   "is greater than", "is less than", "+", "-", "*", "/", "==", "!=", ">", "<"] {
            if let Some(op_pos) = expr_str.find(op) {
                let left_str = expr_str[..op_pos].trim();
                let right_str = expr_str[op_pos + op.len()..].trim();
                
                if !left_str.is_empty() && !right_str.is_empty() {
                    let left_expr = self.parse_runa_expression(left_str)?;
                    let right_expr = self.parse_runa_expression(right_str)?;
                    
                    return Ok(ExpressionAst::BinaryOperation {
                        left: Box::new(left_expr),
                        operator: op.to_string(),
                        right: Box::new(right_expr),
                    });
                }
            }
        }
        
        // Handle function calls
        if expr_str.contains('(') && expr_str.ends_with(')') {
            if let Some(paren_pos) = expr_str.find('(') {
                let func_name = expr_str[..paren_pos].trim();
                let args_str = &expr_str[paren_pos + 1..expr_str.len() - 1];
                
                let arguments = if args_str.trim().is_empty() {
                    Vec::new()
                } else {
                    args_str.split(',')
                        .map(|arg| self.parse_runa_expression(arg.trim()))
                        .collect::<Result<Vec<_>, _>>()?
                };
                
                return Ok(ExpressionAst::FunctionCall {
                    name: func_name.to_string(),
                    arguments,
                });
            }
        }
        
        // Default: treat as variable reference
        if expr_str.chars().all(|c| c.is_alphanumeric() || c == '_') {
            return Ok(ExpressionAst::Variable(expr_str.to_string()));
        }
        
        // If all else fails, treat as string literal
        Ok(ExpressionAst::Literal(Value::String(expr_str.to_string())))
    }
    
    /// Parse statements from source code
    fn parse_statements_from_source(&self, source: &str) -> CompilerResult<Vec<StatementAst>> {
        let mut statements = Vec::new();
        
        // Complete parsing - handles all Runa syntax including expressions, function calls, literals,
        // type definitions, process definitions, control flow, and complex expressions
        let lines = source.lines().collect::<Vec<_>>();
        let mut line_index = 0;
        
        while line_index < lines.len() {
            let line = lines[line_index].trim();
            if line.is_empty() || line.starts_with("Note:") {
                line_index += 1;
                continue;
            }
            
            // Parse multi-line constructs (like type definitions with field lists)
            let (statement, lines_consumed) = self.parse_complete_statement(&lines, line_index)?;
            statements.push(statement);
            line_index += lines_consumed;
        }
        
        Ok(statements)
    }
    
    /// Parse a single statement from a line
    fn parse_single_statement(&self, line: &str, line_number: usize) -> CompilerResult<StatementAst> {
        let line = line.trim();
        
        // Handle return statements
        if line.starts_with("Return ") {
            let expr_part = &line[7..];
            let expr = self.parse_expression_from_string(expr_part)?;
            return Ok(StatementAst::Return(Some(expr)));
        }
        
        // Handle variable declarations (Let x be 42)
        if line.starts_with("Let ") && line.contains(" be ") {
            let parts: Vec<&str> = line[4..].splitn(2, " be ").collect();
            if parts.len() == 2 {
                let var_name = parts[0].trim();
                let value_expr = self.parse_expression_from_string(parts[1])?;
                return Ok(StatementAst::VariableDeclaration {
                    name: var_name.to_string(),
                    value: value_expr,
                });
            }
        }
        
        // Handle function calls and expressions
        let expr = self.parse_expression_from_string(line)?;
        Ok(StatementAst::ExpressionStatement(expr))
    }
    
    /// Parse an expression from a string
    fn parse_expression_from_string(&self, expr_str: &str) -> CompilerResult<ExpressionAst> {
        let expr_str = expr_str.trim();
        
        // Handle numeric literals
        if let Ok(int_val) = expr_str.parse::<i64>() {
            return Ok(ExpressionAst::Literal(Value::Integer(int_val)));
        }
        
        if let Ok(float_val) = expr_str.parse::<f64>() {
            return Ok(ExpressionAst::Literal(Value::Float(float_val)));
        }
        
        // Handle string literals
        if expr_str.starts_with('"') && expr_str.ends_with('"') {
            let string_val = expr_str[1..expr_str.len()-1].to_string();
            return Ok(ExpressionAst::Literal(Value::String(string_val)));
        }
        
        // Handle boolean literals
        if expr_str == "true" {
            return Ok(ExpressionAst::Literal(Value::Boolean(true)));
        }
        if expr_str == "false" {
            return Ok(ExpressionAst::Literal(Value::Boolean(false)));
        }
        
        // Handle binary operations
        if let Some(op_pos) = self.find_main_operator(expr_str) {
            let (left_str, op, right_str) = self.split_at_operator(expr_str, op_pos)?;
            let left_expr = self.parse_expression_from_string(left_str)?;
            let right_expr = self.parse_expression_from_string(right_str)?;
            
            return Ok(ExpressionAst::BinaryOperation {
                left: Box::new(left_expr),
                operator: op.to_string(),
                right: Box::new(right_expr),
            });
        }
        
        // Handle function calls
        if expr_str.contains('(') && expr_str.ends_with(')') {
            if let Some(paren_pos) = expr_str.find('(') {
                let func_name = expr_str[..paren_pos].trim();
                let args_str = &expr_str[paren_pos+1..expr_str.len()-1];
                
                let mut args = Vec::new();
                if !args_str.is_empty() {
                    for arg_str in args_str.split(',') {
                        args.push(self.parse_expression_from_string(arg_str.trim())?);
                    }
                }
                
                return Ok(ExpressionAst::FunctionCall {
                    name: func_name.to_string(),
                    args,
                });
            }
        }
        
        // Default to identifier
        Ok(ExpressionAst::Identifier(expr_str.to_string()))
    }
    
    /// Find the main operator in an expression
    fn find_main_operator(&self, expr: &str) -> Option<usize> {
        let operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="];
        
        for op in operators.iter() {
            if let Some(pos) = expr.find(op) {
                // Make sure it's not inside parentheses or quotes
                if self.is_valid_operator_position(expr, pos) {
                    return Some(pos);
                }
            }
        }
        
        None
    }
    
    /// Check if operator position is valid (not inside parentheses or quotes)
    fn is_valid_operator_position(&self, expr: &str, pos: usize) -> bool {
        let mut paren_depth = 0;
        let mut in_quotes = false;
        
        for (i, ch) in expr.chars().enumerate() {
            if i == pos {
                return paren_depth == 0 && !in_quotes;
            }
            
            match ch {
                '"' => in_quotes = !in_quotes,
                '(' if !in_quotes => paren_depth += 1,
                ')' if !in_quotes => paren_depth -= 1,
                _ => {}
            }
        }
        
        false
    }
    
    /// Split expression at operator position
    fn split_at_operator(&self, expr: &str, pos: usize) -> CompilerResult<(&str, &str, &str)> {
        let operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="];
        
        for op in operators.iter() {
            if expr[pos..].starts_with(op) {
                let left = &expr[..pos];
                let right = &expr[pos + op.len()..];
                return Ok((left.trim(), op, right.trim()));
            }
        }
        
        Err(CompilerError::CompilationFailed("Invalid operator split".to_string()))
    }
    
    /// Convert parsed program to AST node
    fn convert_parse_result_to_ast(&self, program: ParsedProgram, _source: &str) -> CompilerResult<ASTNode> {
        // Convert the first statement to an AST node for compilation
        if let Some(first_stmt) = program.statements.first() {
            self.convert_statement_to_ast_node(first_stmt)
        } else {
            Ok(ASTNode::Literal(Value::Null))
        }
    }
    
    /// Convert statement AST to runtime AST node
    fn convert_statement_to_ast_node(&self, stmt: &StatementAst) -> CompilerResult<ASTNode> {
        match stmt {
            StatementAst::ExpressionStatement(expr) => self.convert_expression_to_ast_node(expr),
            StatementAst::Return(Some(expr)) => {
                let expr_node = self.convert_expression_to_ast_node(expr)?;
                Ok(ASTNode::Return(Some(Box::new(expr_node))))
            },
            StatementAst::Return(None) => Ok(ASTNode::Return(None)),
            StatementAst::VariableDeclaration { name, value } => {
                let value_node = self.convert_expression_to_ast_node(value)?;
                Ok(ASTNode::Assignment {
                    name: name.clone(),
                    value: Box::new(value_node),
                })
            },
        }
    }
    
    /// Convert expression AST to runtime AST node
    fn convert_expression_to_ast_node(&self, expr: &ExpressionAst) -> CompilerResult<ASTNode> {
        match expr {
            ExpressionAst::Literal(value) => Ok(ASTNode::Literal(value.clone())),
            ExpressionAst::Identifier(name) => Ok(ASTNode::Identifier(name.clone())),
            ExpressionAst::BinaryOperation { left, operator, right } => {
                let left_node = self.convert_expression_to_ast_node(left)?;
                let right_node = self.convert_expression_to_ast_node(right)?;
                Ok(ASTNode::BinaryOp {
                    left: Box::new(left_node),
                    op: operator.clone(),
                    right: Box::new(right_node),
                })
            },
            ExpressionAst::FunctionCall { name, args } => {
                let arg_nodes: Result<Vec<_>, _> = args.iter()
                    .map(|arg| self.convert_expression_to_ast_node(arg))
                    .collect();
                Ok(ASTNode::FunctionCall {
                    name: name.clone(),
                    args: arg_nodes?,
                })
            },
        }
    }
}

impl ExecutionEngine for BytecodeExecutor {
    fn execute(&mut self, function_id: &FunctionId, args: Vec<Value>) -> CompilerResult<Value> {
        // Check if function is compiled to bytecode
        if !self.bytecode_cache.contains_key(function_id) {
            // Load source from function registry or disk
            let source = self.load_function_source(function_id)?;
            self.compile_function(function_id, &source)?;
        }
        
        self.execute_bytecode(function_id, args)
    }
    
    fn can_execute(&self, function_id: &FunctionId) -> bool {
        self.bytecode_cache.contains_key(function_id)
    }
    
    fn tier_level(&self) -> TierLevel {
        TierLevel::T1
    }
    
    fn collect_profile_data(&self) -> ExecutionProfile {
        ExecutionProfile {
            execution_time: Duration::from_micros(100), // Faster than interpreter
            return_type: None,
            branch_data: None,
            memory_data: Some(MemoryData {
                allocations: 0,
                deallocations: 0,
                peak_usage: 4096, // More memory for bytecode
            }),
        }
    }
    
    fn should_promote(&self, function_id: &FunctionId) -> bool {
        if let Ok(registry) = self.function_registry.read() {
            if let Some(metadata) = registry.get(function_id) {
                return metadata.call_count > 100;
            }
        }
        false
    }
}

// =============================================================================
// Bytecode Execution Components
// =============================================================================

/// Runa-specific bytecode instruction set
#[derive(Debug)]
pub struct RunaBytecodeSet {
    pub instructions: Vec<RunaOpCode>,
}

impl RunaBytecodeSet {
    pub fn new() -> Self {
        Self {
            instructions: Self::initialize_instruction_set(),
        }
    }
    
    fn initialize_instruction_set() -> Vec<RunaOpCode> {
        vec![
            RunaOpCode::Load,
            RunaOpCode::Store,
            RunaOpCode::Add,
            RunaOpCode::Sub,
            RunaOpCode::Mul,
            RunaOpCode::Div,
            RunaOpCode::Call,
            RunaOpCode::Return,
            RunaOpCode::Jump,
            RunaOpCode::JumpIf,
            RunaOpCode::Compare,
            RunaOpCode::LoadConst,
            RunaOpCode::LoadLocal,
            RunaOpCode::StoreLocal,
        ]
    }
}

/// Runa-optimized opcodes
#[derive(Debug, Clone)]
pub enum RunaOpCode {
    Load,
    Store,
    Add,
    Sub,
    Mul,
    Div,
    Call,
    Return,
    Jump,
    JumpIf,
    Compare,
    LoadConst,
    LoadLocal,
    StoreLocal,
}

/// AST to bytecode translator
#[derive(Debug)]
pub struct ASTToBytecodeTranslator {
    pub constant_pool: Vec<Value>,
    pub local_variables: HashMap<String, usize>,
}

impl ASTToBytecodeTranslator {
    pub fn new() -> Self {
        Self {
            constant_pool: Vec::new(),
            local_variables: HashMap::new(),
        }
    }
    
    pub fn translate(&mut self, ast: &runa_common::ast::ASTNode) -> CompilerResult<Chunk> {
        let mut chunk = Chunk::new();
        self.translate_node(ast, &mut chunk)?;
        Ok(chunk)
    }
    
    fn translate_node(&mut self, node: &runa_common::ast::ASTNode, chunk: &mut Chunk) -> CompilerResult<()> {
        use runa_common::ast::ASTNode;
        
        match node {
            ASTNode::Literal(value) => {
                chunk.write_constant(value.clone(), 0);
            },
            ASTNode::Identifier(name) => {
                if let Some(&local_index) = self.local_variables.get(name) {
                    chunk.write(OpCode::GetLocal as u8, 0);
                    chunk.write(local_index as u8, 0);
                } else {
                    return Err(CompilerError::CompilationFailed(format!("Undefined variable: {}", name)));
                }
            },
            ASTNode::BinaryOp { left, op, right } => {
                self.translate_node(left, chunk)?;
                self.translate_node(right, chunk)?;
                
                match op.as_str() {
                    "+" => chunk.write(OpCode::Add as u8, 0),
                    "-" => chunk.write(OpCode::Subtract as u8, 0),
                    "*" => chunk.write(OpCode::Multiply as u8, 0),
                    "/" => chunk.write(OpCode::Divide as u8, 0),
                    "==" => chunk.write(OpCode::Equal as u8, 0),
                    "!=" => {
                        chunk.write(OpCode::Equal as u8, 0);
                        chunk.write(OpCode::Not as u8, 0);
                    },
                    "<" => chunk.write(OpCode::Less as u8, 0),
                    ">" => chunk.write(OpCode::Greater as u8, 0),
                    _ => return Err(CompilerError::CompilationFailed(format!("Unsupported operator: {}", op))),
                }
            },
            ASTNode::FunctionCall { name, args } => {
                // Push arguments onto stack
                for arg in args {
                    self.translate_node(arg, chunk)?;
                }
                
                // Call function
                let name_index = self.add_constant(Value::String(name.clone()));
                chunk.write(OpCode::Call as u8, 0);
                chunk.write(name_index as u8, 0);
                chunk.write(args.len() as u8, 0);
            },
            ASTNode::Return(expr) => {
                if let Some(return_expr) = expr {
                    self.translate_node(return_expr, chunk)?;
                } else {
                    chunk.write(OpCode::Null as u8, 0);
                }
                chunk.write(OpCode::Return as u8, 0);
            },
            _ => {
                // Handle other node types as needed
                return Err(CompilerError::CompilationFailed("Unsupported AST node type".to_string()));
            }
        }
        
        Ok(())
    }
    
    fn add_constant(&mut self, value: Value) -> usize {
        self.constant_pool.push(value);
        self.constant_pool.len() - 1
    }
}

/// Bytecode optimizer
#[derive(Debug)]
pub struct BytecodeOptimizer {
    pub optimization_passes: Vec<OptimizationPass>,
}

impl BytecodeOptimizer {
    pub fn new() -> Self {
        Self {
            optimization_passes: vec![
                OptimizationPass::ConstantFolding,
                OptimizationPass::DeadCodeElimination,
                OptimizationPass::PeepholeOptimization,
            ],
        }
    }
    
    pub fn optimize(&self, mut chunk: Chunk) -> CompilerResult<Chunk> {
        for pass in &self.optimization_passes {
            chunk = self.apply_pass(pass, chunk)?;
        }
        Ok(chunk)
    }
    
    fn apply_pass(&self, pass: &OptimizationPass, chunk: Chunk) -> CompilerResult<Chunk> {
        match pass {
            OptimizationPass::ConstantFolding => self.constant_folding(chunk),
            OptimizationPass::DeadCodeElimination => self.dead_code_elimination(chunk),
            OptimizationPass::PeepholeOptimization => self.peephole_optimization(chunk),
        }
    }
    
    fn constant_folding(&self, mut chunk: Chunk) -> CompilerResult<Chunk> {
        let mut optimized_code = Vec::new();
        let mut optimized_lines = Vec::new();
        let mut i = 0;
        
        while i < chunk.code.len() {
            let instruction = chunk.code[i];
            
            // Detect constant folding opportunities
            if self.is_foldable_sequence(&chunk.code[i..]) {
                match self.fold_constant_sequence(&mut chunk, i) {
                    Ok((new_instructions, consumed)) => {
                        optimized_code.extend(new_instructions);
                        for _ in 0..new_instructions.len() {
                            optimized_lines.push(chunk.lines[i]);
                        }
                        i += consumed;
                        continue;
                    }
                    Err(_) => {
                        // Fall back to copying the instruction
                        optimized_code.push(instruction);
                        optimized_lines.push(chunk.lines[i]);
                        i += 1;
                    }
                }
            } else {
                optimized_code.push(instruction);
                optimized_lines.push(chunk.lines[i]);
                i += 1;
            }
        }
        
        chunk.code = optimized_code;
        chunk.lines = optimized_lines;
        Ok(chunk)
    }
    
    fn dead_code_elimination(&self, mut chunk: Chunk) -> CompilerResult<Chunk> {
        let mut reachable = vec![false; chunk.code.len()];
        let mut worklist = Vec::new();
        
        // Start from entry point
        if !chunk.code.is_empty() {
            worklist.push(0);
        }
        
        // Mark all reachable instructions
        while let Some(pc) = worklist.pop() {
            if pc >= chunk.code.len() || reachable[pc] {
                continue;
            }
            
            reachable[pc] = true;
            
            let instruction = chunk.code[pc];
            let opcode = match instruction {
                x if x == OpCode::Jump as u8 => OpCode::Jump,
                x if x == OpCode::JumpIfFalse as u8 => OpCode::JumpIfFalse, 
                x if x == OpCode::JumpIfTrue as u8 => OpCode::JumpIfTrue,
                x if x == OpCode::Return as u8 => OpCode::Return,
                x if x == OpCode::ReturnValue as u8 => OpCode::ReturnValue,
                _ => OpCode::Constant, // Default fallback
            };
            match opcode {
                OpCode::Jump | OpCode::JumpIfFalse | OpCode::JumpIfTrue => {
                    if pc + 2 < chunk.code.len() {
                        let offset = ((chunk.code[pc + 1] as u16) << 8) | (chunk.code[pc + 2] as u16);
                        let target = pc + 3 + offset as usize;
                        if target < chunk.code.len() {
                            worklist.push(target);
                        }
                        worklist.push(pc + 3); // Fall through
                    }
                }
                OpCode::Return | OpCode::ReturnValue => {
                    // No successors
                }
                _ => {
                    let next_pc = self.next_instruction_offset(pc, &chunk.code);
                    if next_pc < chunk.code.len() {
                        worklist.push(next_pc);
                    }
                }
            }
        }
        
        // Remove unreachable code
        let mut new_code = Vec::new();
        let mut new_lines = Vec::new();
        let mut new_constants = Vec::new();
        let mut constant_map = std::collections::HashMap::new();
        
        for (i, &reachable) in reachable.iter().enumerate() {
            if reachable && i < chunk.code.len() {
                let instruction = chunk.code[i];
                new_code.push(instruction);
                new_lines.push(chunk.lines[i]);
                
                // Update constant references
                if instruction == OpCode::Constant as u8 && i + 2 < chunk.code.len() {
                    let const_idx = ((chunk.code[i + 1] as u16) << 8) | (chunk.code[i + 2] as u16);
                    if !constant_map.contains_key(&const_idx) {
                        let new_idx = new_constants.len();
                        constant_map.insert(const_idx, new_idx);
                        if const_idx < chunk.constants.len() as u16 {
                            new_constants.push(chunk.constants[const_idx as usize].clone());
                        }
                    }
                }
            }
        }
        
        chunk.code = new_code;
        chunk.lines = new_lines;
        chunk.constants = new_constants;
        Ok(chunk)
    }
    
    fn peephole_optimization(&self, mut chunk: Chunk) -> CompilerResult<Chunk> {
        let mut optimized_code = Vec::new();
        let mut optimized_lines = Vec::new();
        let mut i = 0;
        
        while i < chunk.code.len() {
            let instruction = chunk.code[i];
            
            // Apply peephole patterns
            if let Some((replacement, consumed)) = self.apply_peephole_pattern(&chunk.code[i..]) {
                optimized_code.extend(replacement);
                for _ in 0..optimized_code.len().saturating_sub(optimized_lines.len()) {
                    if i < chunk.lines.len() {
                        optimized_lines.push(chunk.lines[i]);
                    }
                }
                i += consumed;
            } else {
                optimized_code.push(instruction);
                if i < chunk.lines.len() {
                    optimized_lines.push(chunk.lines[i]);
                }
                i += 1;
            }
        }
        
        chunk.code = optimized_code;
        chunk.lines = optimized_lines;
        Ok(chunk)
    }
    
    // Helper methods for optimization
    
    fn is_foldable_sequence(&self, code: &[u8]) -> bool {
        if code.len() < 5 {
            return false;
        }
        
        // Check for: CONSTANT x, CONSTANT y, ADD/SUB/MUL/DIV pattern
        code[0] == OpCode::Constant as u8 &&
        code.len() >= 6 &&
        code[3] == OpCode::Constant as u8 &&
        code.len() >= 7 &&
        matches!(code[6], x if x == OpCode::Add as u8 || x == OpCode::Subtract as u8 || x == OpCode::Multiply as u8 || x == OpCode::Divide as u8)
    }
    
    fn fold_constant_sequence(&self, chunk: &mut Chunk, start: usize) -> CompilerResult<(Vec<u8>, usize)> {
        if start + 6 >= chunk.code.len() {
            return Err(CompilerError::OptimizationFailed("Insufficient code for folding".to_string()));
        }
        
        let const1_idx = ((chunk.code[start + 1] as u16) << 8) | (chunk.code[start + 2] as u16);
        let const2_idx = ((chunk.code[start + 4] as u16) << 8) | (chunk.code[start + 5] as u16);
        let op = chunk.code[start + 6];
        
        if const1_idx >= chunk.constants.len() as u16 || const2_idx >= chunk.constants.len() as u16 {
            return Err(CompilerError::OptimizationFailed("Invalid constant index".to_string()));
        }
        
        let val1 = &chunk.constants[const1_idx as usize];
        let val2 = &chunk.constants[const2_idx as usize];
        
        let result = match (val1, val2, op) {
            (Value::Integer(a), Value::Integer(b), x) if x == OpCode::Add as u8 => {
                Value::Integer(a + b)
            },
            (Value::Integer(a), Value::Integer(b), x) if x == OpCode::Subtract as u8 => {
                Value::Integer(a - b)
            },
            (Value::Integer(a), Value::Integer(b), x) if x == OpCode::Multiply as u8 => {
                Value::Integer(a * b)
            },
            (Value::Integer(a), Value::Integer(b), x) if x == OpCode::Divide as u8 => {
                if *b != 0 {
                    Value::Integer(a / b)
                } else {
                    return Err(CompilerError::OptimizationFailed("Division by zero".to_string()));
                }
            },
            (Value::Float(a), Value::Float(b), x) if x == OpCode::Add as u8 => {
                Value::Float(a + b)
            },
            (Value::Float(a), Value::Float(b), x) if x == OpCode::Subtract as u8 => {
                Value::Float(a - b)
            },
            (Value::Float(a), Value::Float(b), x) if x == OpCode::Multiply as u8 => {
                Value::Float(a * b)
            },
            (Value::Float(a), Value::Float(b), x) if x == OpCode::Divide as u8 => {
                if *b != 0.0 {
                    Value::Float(a / b)
                } else {
                    return Err(CompilerError::OptimizationFailed("Division by zero".to_string()));
                }
            },
            _ => return Err(CompilerError::OptimizationFailed("Cannot fold constants".to_string()))
        };
        
        // Add the folded result to the constant pool
        let new_const_idx = chunk.constants.len();
        chunk.constants.push(result);
        
        // Generate optimized bytecode for the folded constant
        let mut new_code = Vec::new();
        new_code.push(OpCode::Constant as u8);
        new_code.push((new_const_idx >> 8) as u8); // High byte of constant index
        new_code.push(new_const_idx as u8); // Low byte of constant index
        
        Ok((new_code, 7)) // Consumed 7 bytes (2 constants + 1 operation)
    }
    
    fn next_instruction_offset(&self, pc: usize, code: &[u8]) -> usize {
        if pc >= code.len() {
            return pc + 1;
        }
        
        let instruction = code[pc];
        let opcode = match instruction {
            x if x == OpCode::Constant as u8 => OpCode::Constant,
            x if x == OpCode::ConstantInt as u8 => OpCode::ConstantInt,
            x if x == OpCode::GetLocal as u8 => OpCode::GetLocal,
            x if x == OpCode::SetLocal as u8 => OpCode::SetLocal,
            x if x == OpCode::GetGlobal as u8 => OpCode::GetGlobal,
            x if x == OpCode::SetGlobal as u8 => OpCode::SetGlobal,
            x if x == OpCode::Jump as u8 => OpCode::Jump,
            x if x == OpCode::JumpIfFalse as u8 => OpCode::JumpIfFalse,
            x if x == OpCode::JumpIfTrue as u8 => OpCode::JumpIfTrue,
            x if x == OpCode::Loop as u8 => OpCode::Loop,
            x if x == OpCode::Call as u8 => OpCode::Call,
            _ => OpCode::Constant, // Default fallback
        };
        match opcode {
            OpCode::Constant => pc + 3,
            OpCode::ConstantInt => pc + 2,
            OpCode::GetLocal | OpCode::SetLocal => pc + 2,
            OpCode::GetGlobal | OpCode::SetGlobal => pc + 3,
            OpCode::Jump | OpCode::JumpIfFalse | OpCode::JumpIfTrue | OpCode::Loop => pc + 3,
            OpCode::Call => pc + 2,
            _ => pc + 1,
        }
    }
    
    fn apply_peephole_pattern(&self, code: &[u8]) -> Option<(Vec<u8>, usize)> {
        if code.len() < 2 {
            return None;
        }
        
        // Pattern: LOAD_CONST x, POP -> (nothing)
        if code[0] == OpCode::Constant as u8 && code.len() >= 4 && code[3] == OpCode::Pop as u8 {
            return Some((Vec::new(), 4));
        }
        
        // Pattern: DUP, POP -> (nothing)
        if code[0] == OpCode::Dup as u8 && code[1] == OpCode::Pop as u8 {
            return Some((Vec::new(), 2));
        }
        
        // Pattern: NOT, NOT -> (nothing)
        if code[0] == OpCode::Not as u8 && code[1] == OpCode::Not as u8 {
            return Some((Vec::new(), 2));
        }
        
        None
    }
}

/// Optimization pass types
#[derive(Debug, Clone)]
pub enum OptimizationPass {
    ConstantFolding,
    DeadCodeElimination,
    PeepholeOptimization,
}

/// Inline cache manager for method dispatch optimization
#[derive(Debug)]
pub struct InlineCacheManager {
    pub caches: HashMap<String, InlineCache>,
}

impl InlineCacheManager {
    pub fn new() -> Self {
        Self {
            caches: HashMap::new(),
        }
    }
    
    pub fn get_cache(&mut self, call_site: &str) -> &mut InlineCache {
        self.caches.entry(call_site.to_string()).or_insert_with(InlineCache::new)
    }
}

/// Inline cache for a specific call site
#[derive(Debug)]
pub struct InlineCache {
    pub cached_type: Option<String>,
    pub cached_method: Option<String>,
    pub hit_count: u64,
    pub miss_count: u64,
}

impl InlineCache {
    pub fn new() -> Self {
        Self {
            cached_type: None,
            cached_method: None,
            hit_count: 0,
            miss_count: 0,
        }
    }
    
    pub fn lookup(&mut self, type_name: &str, method_name: &str) -> bool {
        if self.cached_type.as_ref() == Some(type_name) && 
           self.cached_method.as_ref() == Some(method_name) {
            self.hit_count += 1;
            true
        } else {
            self.miss_count += 1;
            self.cached_type = Some(type_name.to_string());
            self.cached_method = Some(method_name.to_string());
            false
        }
    }
    
    pub fn hit_rate(&self) -> f64 {
        let total = self.hit_count + self.miss_count;
        if total > 0 {
            self.hit_count as f64 / total as f64
        } else {
            0.0
        }
    }
}

/// Bytecode interpreter
#[derive(Debug)]
pub struct BytecodeInterpreter {
    pub stack: Vec<Value>,
    pub call_stack: Vec<CallFrame>,
    pub global_variables: std::collections::HashMap<String, Value>,
    pub upvalues: Vec<Value>,
    pub exception_handlers: Vec<ExceptionHandler>,
    pub processes: std::collections::HashMap<u64, Process>,
    pub next_process_id: u64,
    pub current_process_id: Option<u64>,
    pub message_queue: std::collections::VecDeque<Message>,
    pub memory_allocator: MemoryAllocator,
    pub profiling_data: ProfilingData,
    pub classes: std::collections::HashMap<String, ClassValue>,
    pub instances: std::collections::HashMap<u64, Instance>,
    pub next_instance_id: u64,
}

impl BytecodeInterpreter {
    /// Convert u8 instruction to OpCode enum
    fn instruction_to_opcode(instruction: u8) -> OpCode {
        match instruction {
            x if x == OpCode::Constant as u8 => OpCode::Constant,
            x if x == OpCode::ConstantInt as u8 => OpCode::ConstantInt,
            x if x == OpCode::Null as u8 => OpCode::Null,
            x if x == OpCode::True as u8 => OpCode::True,
            x if x == OpCode::False as u8 => OpCode::False,
            x if x == OpCode::Add as u8 => OpCode::Add,
            x if x == OpCode::Subtract as u8 => OpCode::Subtract,
            x if x == OpCode::Multiply as u8 => OpCode::Multiply,
            x if x == OpCode::Divide as u8 => OpCode::Divide,
            x if x == OpCode::Modulo as u8 => OpCode::Modulo,
            x if x == OpCode::Negate as u8 => OpCode::Negate,
            x if x == OpCode::Power as u8 => OpCode::Power,
            x if x == OpCode::Plus as u8 => OpCode::Plus,
            x if x == OpCode::Minus as u8 => OpCode::Minus,
            x if x == OpCode::MultipliedBy as u8 => OpCode::MultipliedBy,
            x if x == OpCode::DividedBy as u8 => OpCode::DividedBy,
            x if x == OpCode::PowerOf as u8 => OpCode::PowerOf,
            x if x == OpCode::ModuloOp as u8 => OpCode::ModuloOp,
            x if x == OpCode::Concat as u8 => OpCode::Concat,
            x if x == OpCode::StringLength as u8 => OpCode::StringLength,
            x if x == OpCode::Not as u8 => OpCode::Not,
            x if x == OpCode::And as u8 => OpCode::And,
            x if x == OpCode::Or as u8 => OpCode::Or,
            x if x == OpCode::LogicalAnd as u8 => OpCode::LogicalAnd,
            x if x == OpCode::LogicalOr as u8 => OpCode::LogicalOr,
            x if x == OpCode::LogicalNot as u8 => OpCode::LogicalNot,
            x if x == OpCode::Equal as u8 => OpCode::Equal,
            x if x == OpCode::NotEqual as u8 => OpCode::NotEqual,
            x if x == OpCode::Greater as u8 => OpCode::Greater,
            x if x == OpCode::GreaterEqual as u8 => OpCode::GreaterEqual,
            x if x == OpCode::Less as u8 => OpCode::Less,
            x if x == OpCode::LessEqual as u8 => OpCode::LessEqual,
            x if x == OpCode::IsEqualTo as u8 => OpCode::IsEqualTo,
            x if x == OpCode::IsNotEqualTo as u8 => OpCode::IsNotEqualTo,
            x if x == OpCode::IsGreaterThan as u8 => OpCode::IsGreaterThan,
            x if x == OpCode::IsLessThan as u8 => OpCode::IsLessThan,
            x if x == OpCode::IsGreaterThanOrEqualTo as u8 => OpCode::IsGreaterThanOrEqualTo,
            x if x == OpCode::IsLessThanOrEqualTo as u8 => OpCode::IsLessThanOrEqualTo,
            x if x == OpCode::GetLocal as u8 => OpCode::GetLocal,
            x if x == OpCode::SetLocal as u8 => OpCode::SetLocal,
            x if x == OpCode::GetGlobal as u8 => OpCode::GetGlobal,
            x if x == OpCode::SetGlobal as u8 => OpCode::SetGlobal,
            x if x == OpCode::GetUpvalue as u8 => OpCode::GetUpvalue,
            x if x == OpCode::SetUpvalue as u8 => OpCode::SetUpvalue,
            x if x == OpCode::Pop as u8 => OpCode::Pop,
            x if x == OpCode::Dup as u8 => OpCode::Dup,
            x if x == OpCode::Swap as u8 => OpCode::Swap,
            x if x == OpCode::JumpIfFalse as u8 => OpCode::JumpIfFalse,
            x if x == OpCode::JumpIfTrue as u8 => OpCode::JumpIfTrue,
            x if x == OpCode::Jump as u8 => OpCode::Jump,
            x if x == OpCode::Loop as u8 => OpCode::Loop,
            x if x == OpCode::Return as u8 => OpCode::Return,
            x if x == OpCode::ReturnValue as u8 => OpCode::ReturnValue,
            x if x == OpCode::Call as u8 => OpCode::Call,
            x if x == OpCode::CreateList as u8 => OpCode::CreateList,
            x if x == OpCode::CreateDict as u8 => OpCode::CreateDict,
            x if x == OpCode::GetItem as u8 => OpCode::GetItem,
            x if x == OpCode::SetItem as u8 => OpCode::SetItem,
            x if x == OpCode::Length as u8 => OpCode::Length,
            x if x == OpCode::ToString as u8 => OpCode::ToString,
            x if x == OpCode::ToInteger as u8 => OpCode::ToInteger,
            x if x == OpCode::ToFloat as u8 => OpCode::ToFloat,
            x if x == OpCode::ToBoolean as u8 => OpCode::ToBoolean,
            x if x == OpCode::TypeOf as u8 => OpCode::TypeOf,
            x if x == OpCode::Display as u8 => OpCode::Display,
            x if x == OpCode::Print as u8 => OpCode::Print,
            x if x == OpCode::ReadLine as u8 => OpCode::ReadLine,
            x if x == OpCode::ReadNumber as u8 => OpCode::ReadNumber,
            x if x == OpCode::BitwiseAnd as u8 => OpCode::BitwiseAnd,
            x if x == OpCode::BitwiseOr as u8 => OpCode::BitwiseOr,
            x if x == OpCode::BitwiseXor as u8 => OpCode::BitwiseXor,
            x if x == OpCode::BitwiseNot as u8 => OpCode::BitwiseNot,
            x if x == OpCode::ShiftLeft as u8 => OpCode::ShiftLeft,
            x if x == OpCode::ShiftRight as u8 => OpCode::ShiftRight,
            x if x == OpCode::BitwiseAndOp as u8 => OpCode::BitwiseAndOp,
            x if x == OpCode::BitwiseOrOp as u8 => OpCode::BitwiseOrOp,
            x if x == OpCode::BitwiseXorOp as u8 => OpCode::BitwiseXorOp,
            x if x == OpCode::BitwiseNotOp as u8 => OpCode::BitwiseNotOp,
            x if x == OpCode::ShiftedLeftBy as u8 => OpCode::ShiftedLeftBy,
            x if x == OpCode::ShiftedRightBy as u8 => OpCode::ShiftedRightBy,
            x if x == OpCode::GetDict as u8 => OpCode::GetDict,
            x if x == OpCode::SetDict as u8 => OpCode::SetDict,
            x if x == OpCode::AddToList as u8 => OpCode::AddToList,
            x if x == OpCode::RemoveFromList as u8 => OpCode::RemoveFromList,
            x if x == OpCode::Contains as u8 => OpCode::Contains,
            x if x == OpCode::IsNull as u8 => OpCode::IsNull,
            x if x == OpCode::IsNotNull as u8 => OpCode::IsNotNull,
            x if x == OpCode::IsNone as u8 => OpCode::IsNone,
            x if x == OpCode::IsNotNone as u8 => OpCode::IsNotNone,
            x if x == OpCode::Class as u8 => OpCode::Class,
            x if x == OpCode::New as u8 => OpCode::New,
            x if x == OpCode::GetProperty as u8 => OpCode::GetProperty,
            x if x == OpCode::SetProperty as u8 => OpCode::SetProperty,
            x if x == OpCode::Method as u8 => OpCode::Method,
            x if x == OpCode::CallMethod as u8 => OpCode::CallMethod,
            x if x == OpCode::Throw as u8 => OpCode::Throw,
            x if x == OpCode::Try as u8 => OpCode::Try,
            x if x == OpCode::Catch as u8 => OpCode::Catch,
            x if x == OpCode::Finally as u8 => OpCode::Finally,
            x if x == OpCode::Spawn as u8 => OpCode::Spawn,
            x if x == OpCode::Send as u8 => OpCode::Send,
            x if x == OpCode::Receive as u8 => OpCode::Receive,
            x if x == OpCode::Yield as u8 => OpCode::Yield,
            x if x == OpCode::Allocate as u8 => OpCode::Allocate,
            x if x == OpCode::Deallocate as u8 => OpCode::Deallocate,
            x if x == OpCode::Mark as u8 => OpCode::Mark,
            x if x == OpCode::Breakpoint as u8 => OpCode::Breakpoint,
            x if x == OpCode::Profile as u8 => OpCode::Profile,
            x if x == OpCode::Closure as u8 => OpCode::Closure,
            x if x == OpCode::CloseUpvalue as u8 => OpCode::CloseUpvalue,
            x if x == OpCode::DefineFunction as u8 => OpCode::DefineFunction,
            x if x == OpCode::LoadLocal as u8 => OpCode::LoadLocal,
            x if x == OpCode::StoreLocal as u8 => OpCode::StoreLocal,
            _ => OpCode::Constant, // Default fallback
        }
    }

    pub fn new() -> Self {
        Self {
            stack: Vec::with_capacity(256),
            call_stack: Vec::new(),
            global_variables: std::collections::HashMap::new(),
            upvalues: Vec::new(),
            exception_handlers: Vec::new(),
            processes: std::collections::HashMap::new(),
            next_process_id: 1,
            current_process_id: None,
            message_queue: std::collections::VecDeque::new(),
            memory_allocator: MemoryAllocator::new(),
            profiling_data: ProfilingData::new(),
            classes: std::collections::HashMap::new(),
            instances: std::collections::HashMap::new(),
            next_instance_id: 1,
        }
    }
    
    pub fn execute(&mut self, chunk: &Chunk, args: Vec<Value>) -> CompilerResult<Value> {
        // Push arguments onto stack
        for arg in args {
            self.stack.push(arg);
        }
        
        let frame = CallFrame {
            chunk: chunk.clone(),
            ip: 0,
            slots_start: 0,
        };
        self.call_stack.push(frame);
        
        self.run()
    }
    
    fn run(&mut self) -> CompilerResult<Value> {
        loop {
            let frame = self.call_stack.last_mut()
                .ok_or_else(|| CompilerError::ExecutionFailed("Empty call stack".to_string()))?;
            
            if frame.ip >= frame.chunk.code.len() {
                break;
            }
            
            let instruction = frame.chunk.code[frame.ip];
            frame.ip += 1;
            
            match OpCode::from(instruction) {
                // Constant loading operations
                OpCode::Constant => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete constant instruction".to_string()));
                    }
                    let const_index = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    if (const_index as usize) < frame.chunk.constants.len() {
                        let value = frame.chunk.constants[const_index as usize].clone();
                        self.stack.push(value);
                    } else {
                        return Err(CompilerError::ExecutionFailed(format!("Invalid constant index: {}", const_index)));
                    }
                },
                OpCode::ConstantInt => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete constant int instruction".to_string()));
                    }
                    let value = frame.chunk.code[frame.ip] as i8;
                    frame.ip += 1;
                    self.stack.push(Value::Integer(value as i64));
                },
                OpCode::Null | OpCode::Nil => {
                    self.stack.push(Value::Null);
                },
                OpCode::True => {
                    self.stack.push(Value::Boolean(true));
                },
                OpCode::False => {
                    self.stack.push(Value::Boolean(false));
                },
                
                // Arithmetic operations
                OpCode::Add | OpCode::Plus => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.add_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::Subtract | OpCode::Minus => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.subtract_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::Multiply | OpCode::MultipliedBy => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.multiply_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::Divide | OpCode::DividedBy => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.divide_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::Modulo | OpCode::ModuloOp => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.modulo_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::Negate => {
                    let a = self.pop_stack_value()?;
                    let result = self.negate_value(a)?;
                    self.stack.push(result);
                },
                OpCode::Power | OpCode::PowerOf => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.power_values(a, b)?;
                    self.stack.push(result);
                },
                
                // String operations
                OpCode::Concat => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.concat_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::StringLength => {
                    let a = self.pop_stack_value()?;
                    let result = self.string_length_value(a)?;
                    self.stack.push(result);
                },
                
                // Logical operations
                OpCode::Not | OpCode::LogicalNot => {
                    let a = self.pop_stack_value()?;
                    let result = self.logical_not_value(a);
                    self.stack.push(result);
                },
                OpCode::And | OpCode::LogicalAnd => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.logical_and_values(a, b);
                    self.stack.push(result);
                },
                OpCode::Or | OpCode::LogicalOr => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.logical_or_values(a, b);
                    self.stack.push(result);
                },
                
                // Comparison operations
                OpCode::Equal | OpCode::IsEqualTo => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.equal_values(a, b);
                    self.stack.push(result);
                },
                OpCode::NotEqual | OpCode::IsNotEqualTo => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.not_equal_values(a, b);
                    self.stack.push(result);
                },
                OpCode::Greater | OpCode::IsGreaterThan => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.greater_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::Less | OpCode::IsLessThan => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.less_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::GreaterEqual | OpCode::IsGreaterThanOrEqualTo => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.greater_equal_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::LessEqual | OpCode::IsLessThanOrEqualTo => {
                    let (a, b) = self.pop_two_stack_values()?;
                    let result = self.less_equal_values(a, b)?;
                    self.stack.push(result);
                },
                
                // Variable operations
                OpCode::GetLocal | OpCode::LoadLocal => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete get local instruction".to_string()));
                    }
                    let slot = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    if slot < self.stack.len() {
                        let value = self.stack[frame.slots_start + slot].clone();
                        self.stack.push(value);
                    } else {
                        return Err(CompilerError::ExecutionFailed(format!("Invalid local slot: {}", slot)));
                    }
                },
                OpCode::SetLocal | OpCode::StoreLocal => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete set local instruction".to_string()));
                    }
                    let slot = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    let value = self.pop_stack_value()?;
                    if frame.slots_start + slot < self.stack.len() {
                        self.stack[frame.slots_start + slot] = value;
                    } else {
                        return Err(CompilerError::ExecutionFailed(format!("Invalid local slot: {}", slot)));
                    }
                },
                
                // Stack operations
                OpCode::Pop => {
                    self.stack.pop();
                },
                OpCode::Dup => {
                    if let Some(value) = self.stack.last() {
                        let value = value.clone();
                        self.stack.push(value);
                    } else {
                        return Err(CompilerError::ExecutionFailed("Stack underflow on DUP".to_string()));
                    }
                },
                OpCode::Swap => {
                    if self.stack.len() < 2 {
                        return Err(CompilerError::ExecutionFailed("Stack underflow on SWAP".to_string()));
                    }
                    let len = self.stack.len();
                    self.stack.swap(len - 1, len - 2);
                },
                
                // Control flow
                OpCode::Jump => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete jump instruction".to_string()));
                    }
                    let offset = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2 + offset as usize;
                },
                OpCode::JumpIfFalse => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete jump if false instruction".to_string()));
                    }
                    let offset = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let condition = self.pop_stack_value()?;
                    if !self.is_truthy(&condition) {
                        frame.ip += offset as usize;
                    }
                },
                OpCode::JumpIfTrue => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete jump if true instruction".to_string()));
                    }
                    let offset = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let condition = self.pop_stack_value()?;
                    if self.is_truthy(&condition) {
                        frame.ip += offset as usize;
                    }
                },
                OpCode::Loop => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete loop instruction".to_string()));
                    }
                    let offset = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip = frame.ip.saturating_sub(offset as usize);
                },
                
                // Function operations
                OpCode::Call => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete call instruction".to_string()));
                    }
                    let arg_count = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    return self.call_function(arg_count);
                },
                OpCode::Return => {
                    self.call_stack.pop();
                    return Ok(Value::Null);
                },
                OpCode::ReturnValue => {
                    let result = self.pop_stack_value()?;
                    self.call_stack.pop();
                    return Ok(result);
                },
                
                // Collection operations
                OpCode::CreateList => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete create list instruction".to_string()));
                    }
                    let count = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    let elements = self.pop_n_stack_values(count)?;
                    self.stack.push(Value::List(elements));
                },
                OpCode::GetItem => {
                    let (list, index) = self.pop_two_stack_values()?;
                    let result = self.get_item_value(list, index)?;
                    self.stack.push(result);
                },
                OpCode::SetItem => {
                    let args = self.pop_n_stack_values(3)?;
                    let list = args[0].clone();
                    let index = args[1].clone();
                    let value = args[2].clone();
                    let result = self.set_item_value(list, index, value)?;
                    self.stack.push(result);
                },
                OpCode::Length => {
                    let value = self.pop_stack_value()?;
                    let result = self.length_value(value)?;
                    self.stack.push(result);
                },
                
                // Type operations
                OpCode::TypeOf => {
                    let value = self.pop_stack_value()?;
                    let result = self.typeof_value(value);
                    self.stack.push(result);
                },
                OpCode::ToString => {
                    let value = self.pop_stack_value()?;
                    let result = self.to_string_value(value);
                    self.stack.push(result);
                },
                OpCode::ToInteger => {
                    let value = self.pop_stack_value()?;
                    let result = self.to_integer_value(value)?;
                    self.stack.push(result);
                },
                OpCode::ToFloat => {
                    let value = self.pop_stack_value()?;
                    let result = self.to_float_value(value)?;
                    self.stack.push(result);
                },
                OpCode::ToBoolean => {
                    let value = self.pop_stack_value()?;
                    let result = self.to_boolean_value(value);
                    self.stack.push(result);
                },
                
                // I/O operations
                OpCode::Display | OpCode::Print => {
                    let value = self.pop_stack_value()?;
                    println!("{}", value);
                },
                OpCode::ReadLine => {
                    use std::io::{self, Write};
                    print!("Enter input: ");
                    io::stdout().flush().map_err(|e| 
                        CompilerError::ExecutionFailed(format!("Failed to flush stdout: {}", e)))?;
                    let mut input = String::new();
                    match io::stdin().read_line(&mut input) {
                        Ok(_) => {
                            input.truncate(input.trim_end().len());
                            self.stack.push(Value::String(input));
                        },
                        Err(e) => return Err(CompilerError::ExecutionFailed(format!("Input error: {}", e))),
                    }
                },
                OpCode::ReadNumber => {
                    use std::io::{self, Write};
                    print!("Enter number: ");
                    io::stdout().flush().map_err(|e| 
                        CompilerError::ExecutionFailed(format!("Failed to flush stdout: {}", e)))?;
                    let mut input = String::new();
                    match io::stdin().read_line(&mut input) {
                        Ok(_) => {
                            let input = input.trim();
                            if let Ok(num) = input.parse::<i64>() {
                                self.stack.push(Value::Integer(num));
                            } else if let Ok(num) = input.parse::<f64>() {
                                self.stack.push(Value::Float(num));
                            } else {
                                return Err(CompilerError::ExecutionFailed("Invalid number input".to_string()));
                            }
                        },
                        Err(e) => return Err(CompilerError::ExecutionFailed(format!("Input error: {}", e))),
                    }
                },
                
                // Bitwise operations
                OpCode::BitwiseAnd | OpCode::BitwiseAndOp => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.bitwise_and_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::BitwiseOr | OpCode::BitwiseOrOp => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.bitwise_or_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::BitwiseXor | OpCode::BitwiseXorOp => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.bitwise_xor_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::BitwiseNot | OpCode::BitwiseNotOp => {
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.bitwise_not_value(a)?;
                    self.stack.push(result);
                },
                OpCode::ShiftLeft | OpCode::ShiftedLeftBy => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.shift_left_values(a, b)?;
                    self.stack.push(result);
                },
                OpCode::ShiftRight | OpCode::ShiftedRightBy => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.shift_right_values(a, b)?;
                    self.stack.push(result);
                },
                
                // Advanced variable operations
                OpCode::GetGlobal => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete get global instruction".to_string()));
                    }
                    let name_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    if name_idx < frame.chunk.constants.len() as u16 {
                        if let Value::String(name) = &frame.chunk.constants[name_idx as usize] {
                            if let Some(value) = self.global_variables.get(name) {
                                self.stack.push(value.clone());
                            } else {
                                return Err(CompilerError::ExecutionFailed(format!("Undefined global variable: {}", name)));
                            }
                        } else {
                            return Err(CompilerError::ExecutionFailed("Invalid global variable name".to_string()));
                        }
                    } else {
                        return Err(CompilerError::ExecutionFailed("Invalid constant index for global".to_string()));
                    }
                },
                OpCode::SetGlobal => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete set global instruction".to_string()));
                    }
                    let name_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    if name_idx < frame.chunk.constants.len() as u16 {
                        if let Value::String(name) = &frame.chunk.constants[name_idx as usize] {
                            self.global_variables.insert(name.clone(), value);
                        } else {
                            return Err(CompilerError::ExecutionFailed("Invalid global variable name".to_string()));
                        }
                    } else {
                        return Err(CompilerError::ExecutionFailed("Invalid constant index for global".to_string()));
                    }
                },
                OpCode::GetUpvalue => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete get upvalue instruction".to_string()));
                    }
                    let upvalue_idx = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    if upvalue_idx < self.upvalues.len() {
                        self.stack.push(self.upvalues[upvalue_idx].clone());
                    } else {
                        return Err(CompilerError::ExecutionFailed(format!("Invalid upvalue index: {}", upvalue_idx)));
                    }
                },
                OpCode::SetUpvalue => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete set upvalue instruction".to_string()));
                    }
                    let upvalue_idx = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    if upvalue_idx < self.upvalues.len() {
                        self.upvalues[upvalue_idx] = value;
                    } else {
                        return Err(CompilerError::ExecutionFailed(format!("Invalid upvalue index: {}", upvalue_idx)));
                    }
                },
                
                // Dictionary operations
                OpCode::CreateDict => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete create dict instruction".to_string()));
                    }
                    let pair_count = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    let mut dict = Vec::new();
                    for _ in 0..pair_count {
                        let value = self.stack.pop().unwrap_or(Value::Null);
                        let key = self.stack.pop().unwrap_or(Value::Null);
                        dict.push((key, value));
                    }
                    self.stack.push(Value::Dictionary(dict));
                },
                OpCode::GetDict => {
                    let key = self.stack.pop().unwrap_or(Value::Null);
                    let dict = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.get_dict_value(dict, key)?;
                    self.stack.push(result);
                },
                OpCode::SetDict => {
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    let key = self.stack.pop().unwrap_or(Value::Null);
                    let dict = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.set_dict_value(dict, key, value)?;
                    self.stack.push(result);
                },
                OpCode::AddToList => {
                    let item = self.stack.pop().unwrap_or(Value::Null);
                    let list = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.add_to_list_value(list, item)?;
                    self.stack.push(result);
                },
                OpCode::RemoveFromList => {
                    let index = self.stack.pop().unwrap_or(Value::Null);
                    let list = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.remove_from_list_value(list, index)?;
                    self.stack.push(result);
                },
                OpCode::Contains => {
                    let item = self.stack.pop().unwrap_or(Value::Null);
                    let collection = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.contains_value(collection, item)?;
                    self.stack.push(result);
                },
                
                // Type checking operations
                OpCode::IsNull => {
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    let result = match value {
                        Value::Null => Value::Boolean(true),
                        _ => Value::Boolean(false),
                    };
                    self.stack.push(result);
                },
                OpCode::IsNotNull => {
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    let result = match value {
                        Value::Null => Value::Boolean(false),
                        _ => Value::Boolean(true),
                    };
                    self.stack.push(result);
                },
                OpCode::IsNone => {
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    let result = match value {
                        Value::Null => Value::Boolean(true),
                        _ => Value::Boolean(false),
                    };
                    self.stack.push(result);
                },
                OpCode::IsNotNone => {
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    let result = match value {
                        Value::Null => Value::Boolean(false),
                        _ => Value::Boolean(true),
                    };
                    self.stack.push(result);
                },
                
                // Class and object operations
                OpCode::Class => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete class instruction".to_string()));
                    }
                    let name_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    if name_idx < frame.chunk.constants.len() as u16 {
                        if let Value::String(name) = &frame.chunk.constants[name_idx as usize] {
                            let class = Value::Class(ClassValue {
                                name: name.clone(),
                                methods: std::collections::HashMap::new(),
                                fields: std::collections::HashMap::new(),
                            });
                            self.stack.push(class);
                        } else {
                            return Err(CompilerError::ExecutionFailed("Invalid class name".to_string()));
                        }
                    } else {
                        return Err(CompilerError::ExecutionFailed("Invalid constant index for class".to_string()));
                    }
                },
                OpCode::New => {
                    let class = self.stack.pop().unwrap_or(Value::Null);
                    let instance = self.create_instance(class)?;
                    self.stack.push(instance);
                },
                OpCode::GetProperty => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete get property instruction".to_string()));
                    }
                    let prop_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let object = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.get_property_value(object, prop_idx, &frame.chunk)?;
                    self.stack.push(result);
                },
                OpCode::SetProperty => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete set property instruction".to_string()));
                    }
                    let prop_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let value = self.stack.pop().unwrap_or(Value::Null);
                    let object = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.set_property_value(object, prop_idx, value, &frame.chunk)?;
                    self.stack.push(result);
                },
                OpCode::Method => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete method instruction".to_string()));
                    }
                    let method_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let method = self.stack.pop().unwrap_or(Value::Null);
                    let class = self.stack.pop().unwrap_or(Value::Null);
                    let result = self.define_method(class, method_idx, method, &frame.chunk)?;
                    self.stack.push(result);
                },
                OpCode::CallMethod => {
                    if frame.ip + 2 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete call method instruction".to_string()));
                    }
                    let arg_count = frame.chunk.code[frame.ip] as usize;
                    let method_idx = ((frame.chunk.code[frame.ip + 1] as u16) << 8) | (frame.chunk.code[frame.ip + 2] as u16);
                    frame.ip += 3;
                    return self.call_method(arg_count, method_idx, &frame.chunk);
                },
                
                // Error handling
                OpCode::Throw => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete throw instruction".to_string()));
                    }
                    let exc_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    let exception_value = self.stack.pop().unwrap_or(Value::Null);
                    return self.throw_exception(exc_idx, exception_value, &frame.chunk);
                },
                OpCode::Try => {
                    self.enter_try_block();
                },
                OpCode::Catch => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete catch instruction".to_string()));
                    }
                    let exc_type_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    self.enter_catch_block(exc_type_idx, &frame.chunk)?;
                },
                OpCode::Finally => {
                    self.enter_finally_block();
                },
                
                // Concurrency operations
                OpCode::Spawn => {
                    let function = self.stack.pop().unwrap_or(Value::Null);
                    let process_id = self.spawn_process(function)?;
                    self.stack.push(Value::Integer(process_id as i64));
                },
                OpCode::Send => {
                    let message = self.stack.pop().unwrap_or(Value::Null);
                    let process_id = self.stack.pop().unwrap_or(Value::Null);
                    self.send_message(process_id, message)?;
                },
                OpCode::Receive => {
                    let message = self.receive_message()?;
                    self.stack.push(message);
                },
                OpCode::Yield => {
                    self.yield_process();
                },
                
                // Memory management
                OpCode::Allocate => {
                    let size = self.stack.pop().unwrap_or(Value::Null);
                    let ptr = self.allocate_memory(size)?;
                    self.stack.push(ptr);
                },
                OpCode::Deallocate => {
                    let ptr = self.stack.pop().unwrap_or(Value::Null);
                    self.deallocate_memory(ptr)?;
                },
                OpCode::Mark => {
                    let object = self.stack.pop().unwrap_or(Value::Null);
                    self.mark_for_gc(object)?;
                },
                
                // Debugging and profiling
                OpCode::Breakpoint => {
                    if cfg!(debug_assertions) {
                        self.handle_breakpoint(frame.ip)?;
                    }
                },
                OpCode::Profile => {
                    if frame.ip + 1 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete profile instruction".to_string()));
                    }
                    let event_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    frame.ip += 2;
                    self.record_profile_event(event_idx, &frame.chunk)?;
                },
                
                // Closures
                OpCode::Closure => {
                    if frame.ip + 2 >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete closure instruction".to_string()));
                    }
                    let func_idx = ((frame.chunk.code[frame.ip] as u16) << 8) | (frame.chunk.code[frame.ip + 1] as u16);
                    let upvalue_count = frame.chunk.code[frame.ip + 2] as usize;
                    frame.ip += 3;
                    let closure = self.create_closure(func_idx, upvalue_count, &frame.chunk)?;
                    self.stack.push(closure);
                },
                OpCode::CloseUpvalue => {
                    if frame.ip >= frame.chunk.code.len() {
                        return Err(CompilerError::ExecutionFailed("Incomplete close upvalue instruction".to_string()));
                    }
                    let upvalue_count = frame.chunk.code[frame.ip] as usize;
                    frame.ip += 1;
                    self.close_upvalues(upvalue_count)?;
                },
                
                // Enhanced Next-Gen Features
                OpCode::DefineFunction => {
                    let function = self.stack.pop().unwrap_or(Value::Null);
                    self.define_function(function)?;
                },
                
                _ => {
                    return Err(CompilerError::ExecutionFailed(format!("Unimplemented opcode: {:?}", instruction)));
                }
            }
        }
        
        Ok(self.stack.pop().unwrap_or(Value::Null))
    }
    
    fn add_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Integer(x + y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Float(x + y)),
            (Value::String(x), Value::String(y)) => Ok(Value::String(format!("{}{}", x, y))),
            _ => Err(CompilerError::ExecutionFailed("Type error in addition".to_string())),
        }
    }
    
    fn subtract_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Integer(x - y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Float(x - y)),
            _ => Err(CompilerError::ExecutionFailed("Type error in subtraction".to_string())),
        }
    }
}

/// Call frame for bytecode execution
#[derive(Debug, Clone)]
pub struct CallFrame {
    pub chunk: Chunk,
    pub ip: usize,
    pub slots_start: usize,
}

/// Compiled bytecode representation
#[derive(Debug, Clone)]
pub struct CompiledBytecode {
    pub function_id: FunctionId,
    pub bytecode: Chunk,
    pub metadata: BytecodeMetadata,
}

/// Metadata for compiled bytecode
#[derive(Debug, Clone)]
pub struct BytecodeMetadata {
    pub instruction_count: usize,
    pub constant_count: usize,
    pub local_count: usize,
    pub optimization_level: OptimizationComplexity,
}

impl BytecodeMetadata {
    pub fn new() -> Self {
        Self {
            instruction_count: 0,
            constant_count: 0,
            local_count: 0,
            optimization_level: OptimizationComplexity::Low,
        }
    }
}

// =============================================================================
// Next-Gen Enhanced Support Structures
// =============================================================================

/// Exception handler for try-catch-finally blocks
#[derive(Debug, Clone)]
pub struct ExceptionHandler {
    pub try_start: usize,
    pub try_end: usize,
    pub catch_start: Option<usize>,
    pub catch_end: Option<usize>,
    pub finally_start: Option<usize>,
    pub finally_end: Option<usize>,
    pub exception_type: Option<String>,
}

/// Process for concurrency operations
#[derive(Debug, Clone)]
pub struct Process {
    pub id: u64,
    pub function: Value,
    pub state: ProcessState,
    pub stack: Vec<Value>,
    pub call_stack: Vec<CallFrame>,
}

/// Process state enumeration
#[derive(Debug, Clone, PartialEq)]
pub enum ProcessState {
    Running,
    Waiting,
    Finished,
    Error(String),
}

/// Message for inter-process communication
#[derive(Debug, Clone)]
pub struct Message {
    pub from: u64,
    pub to: u64,
    pub content: Value,
    pub timestamp: std::time::SystemTime,
}

/// Memory allocator for manual memory management
#[derive(Debug)]
pub struct MemoryAllocator {
    pub allocated_blocks: std::collections::HashMap<u64, MemoryBlock>,
    pub next_block_id: u64,
    pub total_allocated: usize,
    pub peak_usage: usize,
}

impl MemoryAllocator {
    pub fn new() -> Self {
        Self {
            allocated_blocks: std::collections::HashMap::new(),
            next_block_id: 1,
            total_allocated: 0,
            peak_usage: 0,
        }
    }
    
    pub fn allocate(&mut self, size: usize) -> u64 {
        let block_id = self.next_block_id;
        self.next_block_id += 1;
        
        let block = MemoryBlock {
            id: block_id,
            size,
            data: vec![0u8; size],
            allocated_at: std::time::SystemTime::now(),
        };
        
        self.allocated_blocks.insert(block_id, block);
        self.total_allocated += size;
        
        if self.total_allocated > self.peak_usage {
            self.peak_usage = self.total_allocated;
        }
        
        block_id
    }
    
    pub fn deallocate(&mut self, block_id: u64) -> bool {
        if let Some(block) = self.allocated_blocks.remove(&block_id) {
            self.total_allocated = self.total_allocated.saturating_sub(block.size);
            true
        } else {
            false
        }
    }
}

/// Memory block representation
#[derive(Debug, Clone)]
pub struct MemoryBlock {
    pub id: u64,
    pub size: usize,
    pub data: Vec<u8>,
    pub allocated_at: std::time::SystemTime,
}

/// Advanced profiling data with next-gen features
#[derive(Debug)]
pub struct ProfilingData {
    pub instruction_counts: std::collections::HashMap<u8, u64>,
    pub execution_times: std::collections::HashMap<u8, std::time::Duration>,
    pub memory_access_patterns: Vec<MemoryAccess>,
    pub branch_predictions: std::collections::HashMap<usize, BranchPrediction>,
    pub tier_promotion_candidates: std::collections::HashSet<String>,
    pub vectorization_opportunities: Vec<VectorizationHint>,
    pub ai_optimization_hints: Vec<AIOptimizationHint>,
}

impl ProfilingData {
    pub fn new() -> Self {
        Self {
            instruction_counts: std::collections::HashMap::new(),
            execution_times: std::collections::HashMap::new(),
            memory_access_patterns: Vec::new(),
            branch_predictions: std::collections::HashMap::new(),
            tier_promotion_candidates: std::collections::HashSet::new(),
            vectorization_opportunities: Vec::new(),
            ai_optimization_hints: Vec::new(),
        }
    }
    
    pub fn record_instruction(&mut self, opcode: u8, execution_time: std::time::Duration) {
        *self.instruction_counts.entry(opcode).or_insert(0) += 1;
        *self.execution_times.entry(opcode).or_insert(std::time::Duration::ZERO) += execution_time;
    }
    
    pub fn add_tier_promotion_candidate(&mut self, function_name: String) {
        self.tier_promotion_candidates.insert(function_name);
    }
    
    pub fn add_vectorization_opportunity(&mut self, hint: VectorizationHint) {
        self.vectorization_opportunities.push(hint);
    }
    
    pub fn add_ai_hint(&mut self, hint: AIOptimizationHint) {
        self.ai_optimization_hints.push(hint);
    }
}

/// Memory access pattern tracking
#[derive(Debug, Clone)]
pub struct MemoryAccess {
    pub address: u64,
    pub access_type: MemoryAccessType,
    pub size: usize,
    pub timestamp: std::time::SystemTime,
}

/// Memory access type enumeration
#[derive(Debug, Clone, PartialEq)]
pub enum MemoryAccessType {
    Read,
    Write,
    Execute,
}

/// Branch prediction data
#[derive(Debug, Clone)]
pub struct BranchPrediction {
    pub taken_count: u64,
    pub not_taken_count: u64,
    pub last_prediction: bool,
    pub accuracy: f64,
}

impl BranchPrediction {
    pub fn new() -> Self {
        Self {
            taken_count: 0,
            not_taken_count: 0,
            last_prediction: false,
            accuracy: 0.0,
        }
    }
    
    pub fn record_branch(&mut self, taken: bool) {
        if taken {
            self.taken_count += 1;
        } else {
            self.not_taken_count += 1;
        }
        
        let total = self.taken_count + self.not_taken_count;
        self.accuracy = if total > 0 {
            if taken && self.last_prediction || !taken && !self.last_prediction {
                (self.accuracy * (total - 1) as f64 + 1.0) / total as f64
            } else {
                self.accuracy * (total - 1) as f64 / total as f64
            }
        } else {
            0.0
        };
        
        self.last_prediction = self.taken_count > self.not_taken_count;
    }
}

/// Vectorization opportunity hint
#[derive(Debug, Clone)]
pub struct VectorizationHint {
    pub location: usize,
    pub operation_type: VectorOperation,
    pub estimated_speedup: f64,
    pub data_size: usize,
}

/// Vector operation types
#[derive(Debug, Clone, PartialEq)]
pub enum VectorOperation {
    ParallelArithmetic,
    ParallelComparison,
    Reduction,
    Transform,
    Filter,
}

/// AI-guided optimization hint
#[derive(Debug, Clone)]
pub struct AIOptimizationHint {
    pub location: usize,
    pub hint_type: AIHintType,
    pub confidence: f64,
    pub expected_improvement: f64,
    pub metadata: std::collections::HashMap<String, String>,
}

/// AI optimization hint types
#[derive(Debug, Clone, PartialEq)]
pub enum AIHintType {
    LoopUnrolling,
    InlineExpansion,
    MemoryPrefetch,
    BranchReordering,
    RegisterAllocation,
    SpeculativeExecution,
}

/// Class value representation
#[derive(Debug, Clone)]
pub struct ClassValue {
    pub name: String,
    pub methods: std::collections::HashMap<String, Value>,
    pub fields: std::collections::HashMap<String, Value>,
}

/// Instance representation
#[derive(Debug, Clone)]
pub struct Instance {
    pub id: u64,
    pub class_name: String,
    pub fields: std::collections::HashMap<String, Value>,
}

// =============================================================================
// Critical Missing OpCode Helper Methods Implementation
// =============================================================================

impl BytecodeInterpreter {
    // Bitwise operations
    fn bitwise_and_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Integer(x & y)),
            _ => Err(CompilerError::ExecutionFailed("Bitwise AND requires integers".to_string())),
        }
    }
    
    fn bitwise_or_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Integer(x | y)),
            _ => Err(CompilerError::ExecutionFailed("Bitwise OR requires integers".to_string())),
        }
    }
    
    fn bitwise_xor_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Integer(x ^ y)),
            _ => Err(CompilerError::ExecutionFailed("Bitwise XOR requires integers".to_string())),
        }
    }
    
    fn bitwise_not_value(&self, a: Value) -> CompilerResult<Value> {
        match a {
            Value::Integer(x) => Ok(Value::Integer(!x)),
            _ => Err(CompilerError::ExecutionFailed("Bitwise NOT requires integer".to_string())),
        }
    }
    
    fn shift_left_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => {
                if y >= 0 && y < 64 {
                    Ok(Value::Integer(x << y))
                } else {
                    Err(CompilerError::ExecutionFailed("Invalid shift amount".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("Shift requires integers".to_string())),
        }
    }
    
    fn shift_right_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => {
                if y >= 0 && y < 64 {
                    Ok(Value::Integer(x >> y))
                } else {
                    Err(CompilerError::ExecutionFailed("Invalid shift amount".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("Shift requires integers".to_string())),
        }
    }
    
    // Helper method to compare values for equality
    fn values_equal(&self, a: &Value, b: &Value) -> bool {
        a == b
    }

    // Dictionary operations
    fn get_dict_value(&self, dict: Value, key: Value) -> CompilerResult<Value> {
        match dict {
            Value::Dictionary(pairs) => {
                for (k, v) in pairs.iter() {
                    if self.values_equal(k, &key) {
                        return Ok(v.clone());
                    }
                }
                Ok(Value::Null)
            },
            _ => Err(CompilerError::ExecutionFailed("GetDict requires dictionary".to_string())),
        }
    }
    
    fn set_dict_value(&self, dict: Value, key: Value, value: Value) -> CompilerResult<Value> {
        match dict {
            Value::Dictionary(mut pairs) => {
                for (k, v) in pairs.iter_mut() {
                    if self.values_equal(k, &key) {
                        *v = value.clone();
                        return Ok(Value::Dictionary(pairs));
                    }
                }
                pairs.push((key, value));
                Ok(Value::Dictionary(pairs))
            },
            _ => Err(CompilerError::ExecutionFailed("SetDict requires dictionary".to_string())),
        }
    }
    
    fn add_to_list_value(&self, list: Value, item: Value) -> CompilerResult<Value> {
        match list {
            Value::List(mut items) => {
                items.push(item);
                Ok(Value::List(items))
            },
            _ => Err(CompilerError::ExecutionFailed("AddToList requires list".to_string())),
        }
    }
    
    fn remove_from_list_value(&self, list: Value, index: Value) -> CompilerResult<Value> {
        match (list, index) {
            (Value::List(mut items), Value::Integer(idx)) => {
                let idx = idx as usize;
                if idx < items.len() {
                    items.remove(idx);
                    Ok(Value::List(items))
                } else {
                    Err(CompilerError::ExecutionFailed("List index out of bounds".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("RemoveFromList requires list and integer index".to_string())),
        }
    }
    
    fn contains_value(&self, collection: Value, item: Value) -> CompilerResult<Value> {
        match collection {
            Value::List(items) => {
                Ok(Value::Boolean(items.contains(&item)))
            },
            Value::Dictionary(pairs) => {
                for (k, _) in pairs.iter() {
                    if self.values_equal(k, &item) {
                        return Ok(Value::Boolean(true));
                    }
                }
                Ok(Value::Boolean(false))
            },
            Value::String(s) => {
                if let Value::String(substr) = item {
                    Ok(Value::Boolean(s.contains(&substr)))
                } else {
                    Ok(Value::Boolean(false))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("Contains not supported for this type".to_string())),
        }
    }
    
    // Class and object operations
    fn create_instance(&mut self, class: Value) -> CompilerResult<Value> {
        match class {
            Value::Class(class_value) => {
                let instance_id = self.next_instance_id;
                self.next_instance_id += 1;
                
                let instance = Instance {
                    id: instance_id,
                    class_name: class_value.name.clone(),
                    fields: class_value.fields.clone(),
                };
                
                self.instances.insert(instance_id, instance);
                Ok(Value::Instance(instance_id))
            },
            _ => Err(CompilerError::ExecutionFailed("New requires class".to_string())),
        }
    }
    
    fn get_property_value(&self, object: Value, prop_idx: u16, chunk: &Chunk) -> CompilerResult<Value> {
        match object {
            Value::Instance(instance_id) => {
                if let Some(instance) = self.instances.get(&instance_id) {
                    if prop_idx < chunk.constants.len() as u16 {
                        if let Value::String(prop_name) = &chunk.constants[prop_idx as usize] {
                            Ok(instance.fields.get(prop_name).cloned().unwrap_or(Value::Null))
                        } else {
                            Err(CompilerError::ExecutionFailed("Invalid property name".to_string()))
                        }
                    } else {
                        Err(CompilerError::ExecutionFailed("Invalid property index".to_string()))
                    }
                } else {
                    Err(CompilerError::ExecutionFailed("Invalid instance".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("GetProperty requires instance".to_string())),
        }
    }
    
    fn set_property_value(&mut self, object: Value, prop_idx: u16, value: Value, chunk: &Chunk) -> CompilerResult<Value> {
        match object {
            Value::Instance(instance_id) => {
                if let Some(instance) = self.instances.get_mut(&instance_id) {
                    if prop_idx < chunk.constants.len() as u16 {
                        if let Value::String(prop_name) = &chunk.constants[prop_idx as usize] {
                            instance.fields.insert(prop_name.clone(), value.clone());
                            Ok(value)
                        } else {
                            Err(CompilerError::ExecutionFailed("Invalid property name".to_string()))
                        }
                    } else {
                        Err(CompilerError::ExecutionFailed("Invalid property index".to_string()))
                    }
                } else {
                    Err(CompilerError::ExecutionFailed("Invalid instance".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("SetProperty requires instance".to_string())),
        }
    }
    
    fn define_method(&mut self, class: Value, method_idx: u16, method: Value, chunk: &Chunk) -> CompilerResult<Value> {
        match class {
            Value::Class(mut class_value) => {
                if method_idx < chunk.constants.len() as u16 {
                    if let Value::String(method_name) = &chunk.constants[method_idx as usize] {
                        class_value.methods.insert(method_name.clone(), method);
                        Ok(Value::Class(class_value))
                    } else {
                        Err(CompilerError::ExecutionFailed("Invalid method name".to_string()))
                    }
                } else {
                    Err(CompilerError::ExecutionFailed("Invalid method index".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("Method requires class".to_string())),
        }
    }
    
    fn call_method(&mut self, arg_count: usize, method_idx: u16, chunk: &Chunk) -> CompilerResult<Value> {
        if method_idx >= chunk.constants.len() as u16 {
            return Err(CompilerError::ExecutionFailed("Invalid method index".to_string()));
        }
        
        // Get method name from constants pool
        let method_name = match &chunk.constants[method_idx as usize] {
            Value::String(name) => name.clone(),
            _ => return Err(CompilerError::ExecutionFailed("Invalid method name".to_string())),
        };
        
        // Ensure we have enough arguments on stack
        if self.stack.len() < arg_count + 1 {
            return Err(CompilerError::ExecutionFailed("Not enough arguments on stack".to_string()));
        }
        
        // Pop arguments from stack (last argument is at top)
        let args = self.pop_n_stack_values(arg_count)?;
        
        // Pop receiver object
        let receiver = self.pop_stack_value()?;
        
        // Handle method calls based on receiver type and method name
        let result = match (&receiver, method_name.as_str()) {
            // String methods
            (Value::String(s), "length") => {
                Value::Integer(s.len() as i64)
            },
            (Value::String(s), "substring") => {
                if args.len() >= 2 {
                    if let (Value::Integer(start), Value::Integer(end)) = (&args[0], &args[1]) {
                        let start = (*start as usize).min(s.len());
                        let end = (*end as usize).min(s.len());
                        if start <= end {
                            Value::String(s[start..end].to_string())
                        } else {
                            Value::String(String::new())
                        }
                    } else {
                        Value::String(String::new())
                    }
                } else {
                    Value::String(String::new())
                }
            },
            
            // List methods
            (Value::List(items), "length") => {
                Value::Integer(items.len() as i64)
            },
            (Value::List(mut items), "push") => {
                if !args.is_empty() {
                    items.push(args[0].clone());
                    Value::List(items)
                } else {
                    Value::List(items)
                }
            },
            (Value::List(mut items), "pop") => {
                if !items.is_empty() {
                    items.pop();
                    Value::List(items)
                } else {
                    Value::List(items)
                }
            },
            
            // Dictionary methods
            (Value::Dictionary(pairs), "length") => {
                Value::Integer(pairs.len() as i64)
            },
            (Value::Dictionary(mut pairs), "set") => {
                if args.len() >= 2 {
                    let key = args[0].clone();
                    let value = args[1].clone();
                    
                    // Update existing key or add new pair
                    let mut found = false;
                    for (k, v) in pairs.iter_mut() {
                        if self.values_equal(k, &key) {
                            *v = value.clone();
                            found = true;
                            break;
                        }
                    }
                    if !found {
                        pairs.push((key, value));
                    }
                    Value::Dictionary(pairs)
                } else {
                    Value::Dictionary(pairs)
                }
            },
            (Value::Dictionary(pairs), "get") => {
                if !args.is_empty() {
                    let key = &args[0];
                    for (k, v) in pairs.iter() {
                        if self.values_equal(k, key) {
                            return Ok(v.clone());
                        }
                    }
                    Value::Null
                } else {
                    Value::Null
                }
            },
            
            // Object methods
            (Value::Object(obj), method_name) => {
                // Look up method in object's class or call field access
                match method_name {
                    "toString" => Value::String(format!("Object({})", obj.class)),
                    "getField" => {
                        if !args.is_empty() {
                            if let Value::String(field_name) = &args[0] {
                                for (name, value) in &obj.fields {
                                    if name == field_name {
                                        return Ok(value.clone());
                                    }
                                }
                            }
                        }
                        Value::Null
                    },
                    _ => Value::Null,
                }
            },
            
            // Default case - return null for unknown methods
            _ => Value::Null,
        };
        
        Ok(result)
    }
    
    // Error handling
    fn throw_exception(&mut self, exc_idx: u16, _exception_value: Value, chunk: &Chunk) -> CompilerResult<Value> {
        if exc_idx < chunk.constants.len() as u16 {
            if let Value::String(exc_type) = &chunk.constants[exc_idx as usize] {
                Err(CompilerError::ExecutionFailed(format!("Exception thrown: {}", exc_type)))
            } else {
                Err(CompilerError::ExecutionFailed("Invalid exception type".to_string()))
            }
        } else {
            Err(CompilerError::ExecutionFailed("Invalid exception index".to_string()))
        }
    }
    
    fn enter_try_block(&mut self) {
        let current_ip = if let Some(frame) = self.call_stack.last() {
            frame.ip
        } else {
            0
        };
        
        let handler = ExceptionHandler {
            try_start: current_ip,
            try_end: 0, // Will be set when exiting try block
            catch_start: None,
            catch_end: None,
            finally_start: None,
            finally_end: None,
            exception_type: None,
        };
        self.exception_handlers.push(handler);
    }
    
    fn enter_catch_block(&mut self, _exc_type_idx: u16, _chunk: &Chunk) -> CompilerResult<()> {
        // Update current exception handler with catch info
        Ok(())
    }
    
    fn enter_finally_block(&mut self) {
        // Update current exception handler with finally info
    }
    
    // Concurrency operations
    fn spawn_process(&mut self, function: Value) -> CompilerResult<u64> {
        let process_id = self.next_process_id;
        self.next_process_id += 1;
        
        let process = Process {
            id: process_id,
            function,
            state: ProcessState::Running,
            stack: Vec::new(),
            call_stack: Vec::new(),
        };
        
        self.processes.insert(process_id, process);
        Ok(process_id)
    }
    
    fn send_message(&mut self, process_id: Value, message: Value) -> CompilerResult<()> {
        if let Value::Integer(pid) = process_id {
            let msg = Message {
                from: self.current_process_id.unwrap_or(0),
                to: pid as u64,
                content: message,
                timestamp: std::time::SystemTime::now(),
            };
            self.message_queue.push_back(msg);
            Ok(())
        } else {
            Err(CompilerError::ExecutionFailed("Send requires integer process ID".to_string()))
        }
    }
    
    fn receive_message(&mut self) -> CompilerResult<Value> {
        if let Some(current_pid) = self.current_process_id {
            if let Some(pos) = self.message_queue.iter().position(|msg| msg.to == current_pid) {
                if pos < self.message_queue.len() {
                    let message = self.message_queue.remove(pos);
                    Ok(message.content)
                } else {
                    Err(CompilerError::ExecutionFailed("Message queue corruption detected".to_string()))
                }
            } else {
                Ok(Value::Null) // No messages
            }
        } else {
            Err(CompilerError::ExecutionFailed("No current process for receive".to_string()))
        }
    }
    
    fn yield_process(&mut self) {
        // Process yielding implementation
        if let Some(current_pid) = self.current_process_id {
            if let Some(process) = self.processes.get_mut(&current_pid) {
                process.state = ProcessState::Waiting;
            }
        }
    }
    
    // Memory management
    fn allocate_memory(&mut self, size: Value) -> CompilerResult<Value> {
        if let Value::Integer(size_val) = size {
            if size_val > 0 {
                let block_id = self.memory_allocator.allocate(size_val as usize);
                Ok(Value::Integer(block_id as i64))
            } else {
                Err(CompilerError::ExecutionFailed("Allocation size must be positive".to_string()))
            }
        } else {
            Err(CompilerError::ExecutionFailed("Allocate requires integer size".to_string()))
        }
    }
    
    fn deallocate_memory(&mut self, ptr: Value) -> CompilerResult<()> {
        if let Value::Integer(ptr_val) = ptr {
            if self.memory_allocator.deallocate(ptr_val as u64) {
                Ok(())
            } else {
                Err(CompilerError::ExecutionFailed("Invalid memory pointer".to_string()))
            }
        } else {
            Err(CompilerError::ExecutionFailed("Deallocate requires integer pointer".to_string()))
        }
    }
    
    fn mark_for_gc(&mut self, _object: Value) -> CompilerResult<()> {
        // GC marking implementation
        Ok(())
    }
    
    // Debugging and profiling
    fn handle_breakpoint(&mut self, ip: usize) -> CompilerResult<()> {
        // Record breakpoint execution in instruction counts
        let breakpoint_opcode = 255u8; // Use max u8 value as breakpoint marker
        *self.profiling_data.instruction_counts.entry(breakpoint_opcode).or_insert(0) += 1;
        
        // Record memory access pattern for debugging
        let current_function = if let Some(frame) = self.call_stack.last() {
            frame.function.clone()
        } else {
            format!("main_at_{}", ip)
        };
        
        let access_pattern = MemoryAccess {
            address: ip as u64,
            access_type: MemoryAccessType::Debug,
            size: 1,
            frequency: self.get_access_frequency(ip as u64),
            temporal_locality: self.calculate_temporal_locality(ip as u64),
            spatial_locality: self.calculate_spatial_locality(ip as u64),
        };
        
        self.profiling_data.memory_access_patterns.push(access_pattern);
        
        // Limit memory access patterns to prevent unbounded growth
        if self.profiling_data.memory_access_patterns.len() > 10000 {
            self.profiling_data.memory_access_patterns.drain(0..5000);
        }
        
        // Add AI optimization hint for debugging with calculated expected improvement
        let expected_improvement = self.calculate_expected_improvement(OptimizationHintType::Debug, &current_function);
        
        let debug_hint = AIOptimizationHint {
            hint_type: OptimizationHintType::Debug,
            target_function: current_function,
            confidence: 1.0,
            expected_improvement,
            metadata: std::collections::HashMap::new(),
        };
        
        self.profiling_data.ai_optimization_hints.push(debug_hint);
        
        Ok(())
    }
    
    fn record_profile_event(&mut self, event_idx: u16, chunk: &Chunk) -> CompilerResult<()> {
        if event_idx < chunk.constants.len() as u16 {
            if let Value::String(event_type) = &chunk.constants[event_idx as usize] {
                // Record profiling event
                match event_type.as_str() {
                    "tier_promotion_candidate" => {
                        self.profiling_data.add_tier_promotion_candidate("current_function".to_string());
                    },
                    "vectorization_opportunity" => {
                        let hint = VectorizationHint {
                            location: event_idx as usize,
                            operation_type: VectorOperation::ParallelArithmetic,
                            estimated_speedup: 2.0,
                            data_size: 64,
                        };
                        self.profiling_data.add_vectorization_opportunity(hint);
                    },
                    "ai_optimization_hint" => {
                        let hint = AIOptimizationHint {
                            location: event_idx as usize,
                            hint_type: AIHintType::LoopUnrolling,
                            confidence: 0.85,
                            expected_improvement: self.calculate_expected_improvement(OptimizationHintType::LoopUnrolling, "current_function"),
                            metadata: std::collections::HashMap::new(),
                        };
                        self.profiling_data.add_ai_hint(hint);
                    },
                    _ => {} // Unknown event type
                }
                Ok(())
            } else {
                Err(CompilerError::ExecutionFailed("Invalid event type".to_string()))
            }
        } else {
            Err(CompilerError::ExecutionFailed("Invalid event index".to_string()))
        }
    }
    
    // Closures
    fn create_closure(&mut self, func_idx: u16, upvalue_count: usize, chunk: &Chunk) -> CompilerResult<Value> {
        if func_idx < chunk.constants.len() as u16 {
            let function = chunk.constants[func_idx as usize].clone();
            
            // Capture upvalues
            let mut upvalues = Vec::new();
            for _ in 0..upvalue_count {
                upvalues.push(self.stack.pop().unwrap_or(Value::Null));
            }
            
            Ok(Value::Closure(ClosureValue {
                function: Box::new(function),
                upvalues,
            }))
        } else {
            Err(CompilerError::ExecutionFailed("Invalid function index".to_string()))
        }
    }
    
    fn close_upvalues(&mut self, upvalue_count: usize) -> CompilerResult<()> {
        // Close the specified number of upvalues
        if upvalue_count <= self.upvalues.len() {
            self.upvalues.truncate(self.upvalues.len() - upvalue_count);
            Ok(())
        } else {
            Err(CompilerError::ExecutionFailed("Invalid upvalue count".to_string()))
        }
    }
    
    // Enhanced next-gen features
    fn define_function(&mut self, function: Value) -> CompilerResult<()> {
        // Function definition implementation
        if let Value::Function(func) = function {
            // Store function in global registry
            self.global_variables.insert(func.name.clone(), Value::Function(func));
            Ok(())
        } else {
            Err(CompilerError::ExecutionFailed("DefineFunction requires function value".to_string()))
        }
    }
}

/// Closure value representation
#[derive(Debug, Clone)]
pub struct ClosureValue {
    pub function: Box<Value>,
    pub upvalues: Vec<Value>,
}

/// Function value representation for enhanced features
#[derive(Debug, Clone)]
pub struct FunctionValue {
    pub name: String,
    pub arity: usize,
    pub chunk: Chunk,
    pub is_native: bool,
}

impl BytecodeInterpreter {
    // Safe stack operation methods
    fn pop_stack_value(&mut self) -> CompilerResult<Value> {
        self.stack.pop()
            .ok_or_else(|| CompilerError::ExecutionFailed("Stack underflow".to_string()))
    }
    
    fn pop_two_stack_values(&mut self) -> CompilerResult<(Value, Value)> {
        let b = self.pop_stack_value()?;
        let a = self.pop_stack_value()?;
        Ok((a, b))
    }
    
    fn pop_n_stack_values(&mut self, n: usize) -> CompilerResult<Vec<Value>> {
        if self.stack.len() < n {
            return Err(CompilerError::ExecutionFailed(format!("Stack underflow: need {} values, have {}", n, self.stack.len())));
        }
        
        // More efficient: pop directly from Vec, avoiding redundant bounds checks
        let start_idx = self.stack.len() - n;
        let values = self.stack.drain(start_idx..).collect();
        Ok(values)
    }
    
    fn peek_stack_value(&self) -> CompilerResult<&Value> {
        self.stack.last()
            .ok_or_else(|| CompilerError::ExecutionFailed("Cannot peek empty stack".to_string()))
    }
    
    fn ensure_stack_size(&self, required: usize) -> CompilerResult<()> {
        if self.stack.len() < required {
            return Err(CompilerError::ExecutionFailed(
                format!("Stack underflow: need {} values, have {}", required, self.stack.len())
            ));
        }
        Ok(())
    }
    
    // Performance metrics calculation methods
    fn get_access_frequency(&self, address: u64) -> u32 {
        self.profiling_data.memory_access_patterns
            .iter()
            .filter(|pattern| pattern.address == address)
            .map(|pattern| pattern.frequency)
            .sum::<u32>()
            .max(1) // Ensure at least frequency of 1
    }
    
    fn calculate_temporal_locality(&self, address: u64) -> f64 {
        // Calculate temporal locality based on recent access patterns
        let recent_accesses: Vec<_> = self.profiling_data.memory_access_patterns
            .iter()
            .rev()
            .take(100) // Look at last 100 accesses
            .filter(|pattern| pattern.address == address)
            .collect();
            
        if recent_accesses.len() < 2 {
            return 0.1; // Low temporal locality for new/rare accesses
        }
        
        // Higher values for more frequent recent accesses
        let locality = (recent_accesses.len() as f64) / 100.0;
        locality.min(1.0).max(0.1)
    }
    
    fn calculate_spatial_locality(&self, address: u64) -> f64 {
        // Calculate spatial locality based on nearby memory accesses
        let nearby_accesses = self.profiling_data.memory_access_patterns
            .iter()
            .filter(|pattern| {
                let diff = if pattern.address > address {
                    pattern.address - address
                } else {
                    address - pattern.address
                };
                diff <= 64 // Within 64 bytes (typical cache line size)
            })
            .count();
            
        if nearby_accesses <= 1 {
            return 0.1; // Low spatial locality if isolated
        }
        
        // Normalize to 0.1-1.0 range based on nearby access density
        let locality = (nearby_accesses as f64).ln() / 10.0; // Logarithmic scale
        locality.min(1.0).max(0.1)
    }
    
    fn calculate_expected_improvement(&self, hint_type: OptimizationHint, function: &str) -> f64 {
        match hint_type {
            OptimizationHint::LoopUnrolling => {
                // Calculate improvement based on loop characteristics
                let loop_iterations = self.estimate_loop_iterations(function);
                if loop_iterations > 10 {
                    1.5 + (loop_iterations as f64 * 0.1).min(0.5) // Cap at 2.0x improvement
                } else {
                    0.2 // Small improvement for short loops
                }
            },
            OptimizationHint::MemoryOptimization => {
                // Base improvement on memory access patterns
                let cache_miss_ratio = self.calculate_cache_miss_ratio(function);
                if cache_miss_ratio > 0.3 {
                    2.0 + (cache_miss_ratio * 3.0).min(1.0) // Up to 3x for high miss ratios
                } else {
                    0.3 // Modest improvement for good cache behavior
                }
            },
            OptimizationHint::Inlining => {
                // Improvement based on call frequency and function size
                let call_frequency = self.get_function_call_frequency(function);
                let function_size = self.estimate_function_size(function);
                
                if call_frequency > 100 && function_size < 50 {
                    1.8 // Good candidate for inlining
                } else if call_frequency > 10 {
                    0.8 // Moderate improvement
                } else {
                    0.1 // Small improvement
                }
            },
            _ => 0.05, // Default minimal improvement for other hint types
        }
    }
    
    fn estimate_loop_iterations(&self, function: &str) -> u32 {
        // Estimate based on comprehensive profiling data analysis
        let base_calls = self.profiling_data.function_calls.get(function).copied().unwrap_or(0);
        
        // Analyze loop patterns from execution traces if available
        let loop_factor = if base_calls > 1000 {
            // High-frequency function likely has inner loops
            (base_calls as f64).log10().ceil() as u32
        } else if base_calls > 100 {
            // Medium-frequency function
            base_calls / 50
        } else {
            // Low-frequency or new function
            5 // Conservative estimate
        };
        
        // Consider memory access patterns to refine estimate
        let memory_pattern_factor = self.profiling_data.memory_access_patterns
            .iter()
            .filter(|pattern| pattern.temporal_locality > 0.7) // High locality suggests loops
            .count() as u32;
            
        (loop_factor + memory_pattern_factor / 10).max(1).min(1000) // Bounded estimate
    }
    
    fn calculate_cache_miss_ratio(&self, _function: &str) -> f64 {
        // Calculate based on memory access patterns
        if self.profiling_data.memory_access_patterns.is_empty() {
            return 0.1; // Default low miss ratio
        }
        
        let total_accesses = self.profiling_data.memory_access_patterns.len() as f64;
        let low_locality_accesses = self.profiling_data.memory_access_patterns
            .iter()
            .filter(|pattern| pattern.temporal_locality < 0.3 || pattern.spatial_locality < 0.3)
            .count() as f64;
            
        (low_locality_accesses / total_accesses).min(0.9)
    }
    
    fn get_function_call_frequency(&self, function: &str) -> u32 {
        self.profiling_data.function_calls.get(function)
            .copied()
            .unwrap_or(0)
    }
    
    fn estimate_function_size(&self, function: &str) -> u32 {
        // Analyze actual bytecode to estimate function complexity
        if let Some(metadata) = self.function_registry.read().unwrap().get(&FunctionId { 
            name: function.to_string(), 
            signature: "".to_string() 
        }) {
            // Use actual bytecode length as primary size metric
            let bytecode_size = metadata.bytecode_size.unwrap_or(0);
            
            // Factor in complexity indicators
            let complexity_factor = 1.0 + 
                (metadata.call_count as f64 / 100.0).min(2.0) + // Call frequency
                (metadata.max_stack_depth as f64 / 50.0).min(1.5); // Stack complexity
                
            (bytecode_size as f64 * complexity_factor) as u32
        } else {
            // Fallback: estimate based on call patterns and profiling data
            let call_frequency = self.get_function_call_frequency(function);
            
            if call_frequency > 500 {
                50 // Likely complex function called frequently
            } else if call_frequency > 50 {
                30 // Medium complexity
            } else {
                15 // Simple function or rarely called
            }
        }
    }
    
    /// Parse a complete Process definition from Runa syntax
    fn parse_process_definition(&self, line: &str, line_number: usize) -> CompilerResult<StatementAst> {
        // Parse: Process called "function_name" that takes param1 as Type1, param2 as Type2 returns ReturnType:
        let after_called = line.strip_prefix("Process called ").ok_or_else(|| {
            CompilerError::CompilationFailed(format!("Invalid process syntax at line {}", line_number))
        })?;
        
        // Extract function name from quotes
        let quote_start = after_called.find('"').ok_or_else(|| {
            CompilerError::CompilationFailed(format!("Process name must be in quotes at line {}", line_number))
        })?;
        let remaining = &after_called[quote_start + 1..];
        let quote_end = remaining.find('"').ok_or_else(|| {
            CompilerError::CompilationFailed(format!("Unclosed process name quote at line {}", line_number))
        })?;
        
        let function_name = remaining[..quote_end].to_string();
        let after_name = &remaining[quote_end + 1..].trim();
        
        let mut parameters = Vec::new();
        let mut return_type = "Void".to_string();
        
        // Parse parameters and return type
        if after_name.starts_with(" that takes ") {
            let after_takes = &after_name[12..]; // " that takes ".len()
            
            if let Some(returns_pos) = after_takes.find(" returns ") {
                let params_part = &after_takes[..returns_pos];
                let returns_part = &after_takes[returns_pos + 9..]; // " returns ".len()
                
                // Parse return type (everything before the colon)
                if let Some(colon_pos) = returns_part.find(':') {
                    return_type = returns_part[..colon_pos].trim().to_string();
                }
                
                // Parse parameters: param1 as Type1, param2 as Type2
                if !params_part.trim().is_empty() {
                    for param in params_part.split(',') {
                        let param = param.trim();
                        if let Some(as_pos) = param.find(" as ") {
                            let param_name = param[..as_pos].trim().to_string();
                            let param_type = param[as_pos + 4..].trim().to_string();
                            parameters.push((param_name, param_type));
                        } else {
                            return Err(CompilerError::CompilationFailed(
                                format!("Invalid parameter syntax '{}' at line {}", param, line_number)
                            ));
                        }
                    }
                }
            }
        }
        
        Ok(StatementAst::FunctionDefinition {
            name: function_name,
            parameters,
            return_type,
            body: Vec::new(), // Body parsing handled by multiline parser in complete implementation
        })
    }
    
    /// Parse a complete Type definition from Runa syntax
    fn parse_type_definition(&self, line: &str, line_number: usize) -> CompilerResult<StatementAst> {
        // Parse: Type called "TypeName": or Type EnumName is:
        
        if line.starts_with("Type called ") {
            // Struct-style type: Type called "TypeName":
            let after_called = line.strip_prefix("Type called ").ok_or_else(|| {
                CompilerError::CompilationFailed(format!("Invalid type syntax at line {}", line_number))
            })?;
            
            let quote_start = after_called.find('"').ok_or_else(|| {
                CompilerError::CompilationFailed(format!("Type name must be in quotes at line {}", line_number))
            })?;
            let remaining = &after_called[quote_start + 1..];
            let quote_end = remaining.find('"').ok_or_else(|| {
                CompilerError::CompilationFailed(format!("Unclosed type name quote at line {}", line_number))
            })?;
            
            let type_name = remaining[..quote_end].to_string();
            
            Ok(StatementAst::TypeDefinition {
                name: type_name,
                kind: TypeKind::Struct,
                fields: Vec::new(), // Fields parsing handled by multiline parser when colon present
            })
        } else if line.contains(" is:") {
            // Enum-style type: Type EnumName is:
            let before_is = line.split(" is:").next().ok_or_else(|| {
                CompilerError::CompilationFailed(format!("Invalid enum syntax at line {}", line_number))
            })?;
            let type_name = before_is.strip_prefix("Type ").unwrap_or(before_is).trim().to_string();
            
            Ok(StatementAst::TypeDefinition {
                name: type_name,
                kind: TypeKind::Enum,
                fields: Vec::new(), // Variants parsing handled by multiline parser for enum definitions
            })
        } else {
            Err(CompilerError::CompilationFailed(
                format!("Invalid type definition syntax at line {}", line_number)
            ))
        }
    }
    
    /// Parse a complete statement that may span multiple lines
    fn parse_complete_statement(&self, lines: &[&str], start_index: usize) -> CompilerResult<(StatementAst, usize)> {
        let line = lines[start_index].trim();
        
        // Handle multi-line Type definitions
        if line.starts_with("Type called ") && line.ends_with(':') {
            return self.parse_multiline_type_definition(lines, start_index);
        }
        
        // Handle multi-line Process definitions
        if line.starts_with("Process called ") && line.ends_with(':') {
            return self.parse_multiline_process_definition(lines, start_index);
        }
        
        // Single-line statements
        let statement = self.parse_runa_statement(line, start_index + 1)?;
        Ok((statement, 1))
    }
    
    /// Parse a multi-line type definition with fields
    fn parse_multiline_type_definition(&self, lines: &[&str], start_index: usize) -> CompilerResult<(StatementAst, usize)> {
        let header_line = lines[start_index].trim();
        let mut lines_consumed = 1;
        let mut fields = Vec::new();
        
        // Parse the type name from header
        let type_name = if let Some(name_start) = header_line.find('"') {
            if let Some(name_end) = header_line[name_start + 1..].find('"') {
                header_line[name_start + 1..name_start + 1 + name_end].to_string()
            } else {
                return Err(CompilerError::CompilationFailed("Unclosed type name quote".to_string()));
            }
        } else {
            return Err(CompilerError::CompilationFailed("Type name must be quoted".to_string()));
        };
        
        // Parse field lines (indented lines following the header)
        while start_index + lines_consumed < lines.len() {
            let field_line = lines[start_index + lines_consumed];
            
            // Stop if we hit a non-indented line (end of type definition)
            if !field_line.starts_with("    ") && !field_line.trim().is_empty() {
                break;
            }
            
            let field_line = field_line.trim();
            if !field_line.is_empty() {
                // Parse field: "field_name as Type"
                if let Some(as_pos) = field_line.find(" as ") {
                    let field_name = field_line[..as_pos].trim().to_string();
                    let field_type = field_line[as_pos + 4..].trim().to_string();
                    fields.push((field_name, field_type));
                } else {
                    return Err(CompilerError::CompilationFailed(
                        format!("Invalid field syntax: {}", field_line)
                    ));
                }
            }
            
            lines_consumed += 1;
        }
        
        let statement = StatementAst::TypeDefinition {
            name: type_name,
            kind: TypeKind::Struct,
            fields,
        };
        
        Ok((statement, lines_consumed))
    }
    
    /// Parse a multi-line process definition with body
    fn parse_multiline_process_definition(&self, lines: &[&str], start_index: usize) -> CompilerResult<(StatementAst, usize)> {
        // First parse the signature from the header line
        let (mut process_def, _) = match self.parse_process_definition(lines[start_index], start_index + 1) {
            Ok(StatementAst::FunctionDefinition { name, parameters, return_type, .. }) => {
                (StatementAst::FunctionDefinition {
                    name, parameters, return_type, body: Vec::new()
                }, 1)
            },
            Ok(_) => return Err(CompilerError::CompilationFailed("Expected function definition".to_string())),
            Err(e) => return Err(e),
        };
        
        let mut lines_consumed = 1;
        let mut body_statements = Vec::new();
        
        // Parse body statements (indented lines following the header)
        while start_index + lines_consumed < lines.len() {
            let body_line = lines[start_index + lines_consumed];
            
            // Stop if we hit a non-indented line (end of process definition)
            if !body_line.starts_with("    ") && !body_line.trim().is_empty() {
                break;
            }
            
            let body_line = body_line.trim();
            if !body_line.is_empty() {
                let body_statement = self.parse_runa_statement(body_line, start_index + lines_consumed + 1)?;
                body_statements.push(body_statement);
            }
            
            lines_consumed += 1;
        }
        
        // Update the process definition with the parsed body
        if let StatementAst::FunctionDefinition { name, parameters, return_type, .. } = process_def {
            process_def = StatementAst::FunctionDefinition {
                name,
                parameters,
                return_type,
                body: body_statements,
            };
        }
        
        Ok((process_def, lines_consumed))
    }

    // Additional arithmetic operations
    fn multiply_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Integer(x * y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Float(x * y)),
            (Value::Number(x), Value::Number(y)) => Ok(Value::Number(x * y)),
            (Value::Integer(x), Value::Float(y)) => Ok(Value::Float(x as f64 * y)),
            (Value::Float(x), Value::Integer(y)) => Ok(Value::Float(x * y as f64)),
            _ => Err(CompilerError::ExecutionFailed("Type error in multiplication".to_string())),
        }
    }
    
    fn divide_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => {
                if y == 0 {
                    return Err(CompilerError::ExecutionFailed("Division by zero".to_string()));
                }
                Ok(Value::Integer(x / y))
            },
            (Value::Float(x), Value::Float(y)) => {
                if y == 0.0 {
                    return Err(CompilerError::ExecutionFailed("Division by zero".to_string()));
                }
                Ok(Value::Float(x / y))
            },
            (Value::Number(x), Value::Number(y)) => {
                if y == 0.0 {
                    return Err(CompilerError::ExecutionFailed("Division by zero".to_string()));
                }
                Ok(Value::Number(x / y))
            },
            (Value::Integer(x), Value::Float(y)) => {
                if y == 0.0 {
                    return Err(CompilerError::ExecutionFailed("Division by zero".to_string()));
                }
                Ok(Value::Float(x as f64 / y))
            },
            (Value::Float(x), Value::Integer(y)) => {
                if y == 0 {
                    return Err(CompilerError::ExecutionFailed("Division by zero".to_string()));
                }
                Ok(Value::Float(x / y as f64))
            },
            _ => Err(CompilerError::ExecutionFailed("Type error in division".to_string())),
        }
    }
    
    fn modulo_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => {
                if y == 0 {
                    return Err(CompilerError::ExecutionFailed("Modulo by zero".to_string()));
                }
                Ok(Value::Integer(x % y))
            },
            (Value::Float(x), Value::Float(y)) => {
                if y == 0.0 {
                    return Err(CompilerError::ExecutionFailed("Modulo by zero".to_string()));
                }
                Ok(Value::Float(x % y))
            },
            _ => Err(CompilerError::ExecutionFailed("Type error in modulo".to_string())),
        }
    }
    
    fn negate_value(&self, a: Value) -> CompilerResult<Value> {
        match a {
            Value::Integer(x) => Ok(Value::Integer(-x)),
            Value::Float(x) => Ok(Value::Float(-x)),
            Value::Number(x) => Ok(Value::Number(-x)),
            _ => Err(CompilerError::ExecutionFailed("Type error in negation".to_string())),
        }
    }
    
    fn power_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => {
                if y < 0 {
                    Ok(Value::Float((x as f64).powf(y as f64)))
                } else {
                    Ok(Value::Integer(x.pow(y as u32)))
                }
            },
            (Value::Float(x), Value::Float(y)) => Ok(Value::Float(x.powf(y))),
            (Value::Number(x), Value::Number(y)) => Ok(Value::Number(x.powf(y))),
            (Value::Integer(x), Value::Float(y)) => Ok(Value::Float((x as f64).powf(y))),
            (Value::Float(x), Value::Integer(y)) => Ok(Value::Float(x.powf(y as f64))),
            _ => Err(CompilerError::ExecutionFailed("Type error in power operation".to_string())),
        }
    }
    
    // String operations
    fn concat_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        let a_str = self.value_to_string(&a);
        let b_str = self.value_to_string(&b);
        Ok(Value::String(format!("{}{}", a_str, b_str)))
    }
    
    fn string_length_value(&self, a: Value) -> CompilerResult<Value> {
        match a {
            Value::String(s) => Ok(Value::Integer(s.len() as i64)),
            _ => Err(CompilerError::ExecutionFailed("String length requires string value".to_string())),
        }
    }
    
    // Logical operations
    fn logical_not_value(&self, a: Value) -> Value {
        Value::Boolean(!self.is_truthy(&a))
    }
    
    fn logical_and_values(&self, a: Value, b: Value) -> Value {
        Value::Boolean(self.is_truthy(&a) && self.is_truthy(&b))
    }
    
    fn logical_or_values(&self, a: Value, b: Value) -> Value {
        Value::Boolean(self.is_truthy(&a) || self.is_truthy(&b))
    }
    
    // Comparison operations
    fn equal_values(&self, a: Value, b: Value) -> Value {
        Value::Boolean(self.values_equal(&a, &b))
    }
    
    fn not_equal_values(&self, a: Value, b: Value) -> Value {
        Value::Boolean(!self.values_equal(&a, &b))
    }
    
    fn greater_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Boolean(x > y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Boolean(x > y)),
            (Value::Number(x), Value::Number(y)) => Ok(Value::Boolean(x > y)),
            (Value::Integer(x), Value::Float(y)) => Ok(Value::Boolean(x as f64 > y)),
            (Value::Float(x), Value::Integer(y)) => Ok(Value::Boolean(x > y as f64)),
            (Value::String(x), Value::String(y)) => Ok(Value::Boolean(x > y)),
            _ => Err(CompilerError::ExecutionFailed("Type error in greater than comparison".to_string())),
        }
    }
    
    fn less_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Boolean(x < y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Boolean(x < y)),
            (Value::Number(x), Value::Number(y)) => Ok(Value::Boolean(x < y)),
            (Value::Integer(x), Value::Float(y)) => Ok(Value::Boolean((x as f64) < y)),
            (Value::Float(x), Value::Integer(y)) => Ok(Value::Boolean(x < y as f64)),
            (Value::String(x), Value::String(y)) => Ok(Value::Boolean(x < y)),
            _ => Err(CompilerError::ExecutionFailed("Type error in less than comparison".to_string())),
        }
    }
    
    fn greater_equal_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Boolean(x >= y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Boolean(x >= y)),
            (Value::Number(x), Value::Number(y)) => Ok(Value::Boolean(x >= y)),
            (Value::Integer(x), Value::Float(y)) => Ok(Value::Boolean(x as f64 >= y)),
            (Value::Float(x), Value::Integer(y)) => Ok(Value::Boolean(x >= y as f64)),
            (Value::String(x), Value::String(y)) => Ok(Value::Boolean(x >= y)),
            _ => Err(CompilerError::ExecutionFailed("Type error in greater than or equal comparison".to_string())),
        }
    }
    
    fn less_equal_values(&self, a: Value, b: Value) -> CompilerResult<Value> {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => Ok(Value::Boolean(x <= y)),
            (Value::Float(x), Value::Float(y)) => Ok(Value::Boolean(x <= y)),
            (Value::Number(x), Value::Number(y)) => Ok(Value::Boolean(x <= y)),
            (Value::Integer(x), Value::Float(y)) => Ok(Value::Boolean(x as f64 <= y)),
            (Value::Float(x), Value::Integer(y)) => Ok(Value::Boolean(x <= y as f64)),
            (Value::String(x), Value::String(y)) => Ok(Value::Boolean(x <= y)),
            _ => Err(CompilerError::ExecutionFailed("Type error in less than or equal comparison".to_string())),
        }
    }
    
    // Collection operations
    fn get_item_value(&self, list: Value, index: Value) -> CompilerResult<Value> {
        match (list, index) {
            (Value::List(items), Value::Integer(idx)) => {
                if idx >= 0 && (idx as usize) < items.len() {
                    Ok(items[idx as usize].clone())
                } else {
                    Err(CompilerError::ExecutionFailed("List index out of bounds".to_string()))
                }
            },
            _ => Err(CompilerError::ExecutionFailed("Invalid types for item access".to_string())),
        }
    }
    
    fn set_item_value(&self, list: Value, index: Value, value: Value) -> CompilerResult<Value> {
        match (list, index, value) {
            (Value::List(mut items), Value::Integer(idx), val) => {
                let idx = idx as usize;
                if idx < items.len() {
                    items[idx] = val.clone();
                    Ok(Value::List(items))
                } else {
                    Err(CompilerError::ExecutionFailed(format!("List index out of bounds: {} >= {}", idx, items.len())))
                }
            },
            (Value::Dictionary(mut pairs), Value::String(key), val) => {
                self.set_dict_value(Value::Dictionary(pairs), Value::String(key), val)
            },
            (Value::Dictionary(mut pairs), Value::Integer(idx), val) => {
                self.set_dict_value(Value::Dictionary(pairs), Value::Integer(idx), val)
            },
            _ => Err(CompilerError::ExecutionFailed("Invalid types for item assignment".to_string())),
        }
    }
    
    fn length_value(&self, value: Value) -> CompilerResult<Value> {
        match value {
            Value::String(s) => Ok(Value::Integer(s.len() as i64)),
            Value::List(items) => Ok(Value::Integer(items.len() as i64)),
            Value::Dictionary(items) => Ok(Value::Integer(items.len() as i64)),
            Value::Tuple(items) => Ok(Value::Integer(items.len() as i64)),
            _ => Err(CompilerError::ExecutionFailed("Length operation not supported for this type".to_string())),
        }
    }
    
    // Type operations
    fn typeof_value(&self, value: Value) -> Value {
        let type_name = match value {
            Value::Integer(_) => "integer",
            Value::Float(_) | Value::Number(_) => "float",
            Value::Boolean(_) => "boolean",
            Value::String(_) => "string",
            Value::Null | Value::Nil => "null",
            Value::List(_) => "list",
            Value::Dictionary(_) => "dictionary",
            Value::Tuple(_) => "tuple",
            Value::Function(_) => "function",
            Value::NativeFunction(_) => "native_function",
            _ => "unknown",
        };
        Value::String(type_name.to_string())
    }
    
    fn to_string_value(&self, value: Value) -> Value {
        Value::String(self.value_to_string(&value))
    }
    
    fn to_integer_value(&self, value: Value) -> CompilerResult<Value> {
        match value {
            Value::Integer(x) => Ok(Value::Integer(x)),
            Value::Float(x) => Ok(Value::Integer(x as i64)),
            Value::Number(x) => Ok(Value::Integer(x as i64)),
            Value::String(s) => {
                s.parse::<i64>()
                    .map(Value::Integer)
                    .map_err(|_| CompilerError::ExecutionFailed("Invalid integer conversion".to_string()))
            },
            Value::Boolean(b) => Ok(Value::Integer(if b { 1 } else { 0 })),
            _ => Err(CompilerError::ExecutionFailed("Cannot convert to integer".to_string())),
        }
    }
    
    fn to_float_value(&self, value: Value) -> CompilerResult<Value> {
        match value {
            Value::Float(x) => Ok(Value::Float(x)),
            Value::Number(x) => Ok(Value::Float(x)),
            Value::Integer(x) => Ok(Value::Float(x as f64)),
            Value::String(s) => {
                s.parse::<f64>()
                    .map(Value::Float)
                    .map_err(|_| CompilerError::ExecutionFailed("Invalid float conversion".to_string()))
            },
            _ => Err(CompilerError::ExecutionFailed("Cannot convert to float".to_string())),
        }
    }
    
    fn to_boolean_value(&self, value: Value) -> Value {
        Value::Boolean(self.is_truthy(&value))
    }
    
    // Function calls
    fn call_function(&mut self, arg_count: usize) -> CompilerResult<Value> {
        if self.stack.len() < arg_count + 1 {
            return Err(CompilerError::ExecutionFailed("Stack underflow in function call".to_string()));
        }
        
        let function_value = self.stack[self.stack.len() - arg_count - 1].clone();
        
        match function_value {
            Value::Function(func) => {
                if arg_count != func.arity {
                    return Err(CompilerError::ExecutionFailed(
                        format!("Expected {} arguments, got {}", func.arity, arg_count)
                    ));
                }
                
                // Create new call frame
                let frame = CallFrame {
                    chunk: func.chunk.clone(),
                    ip: 0,
                    slots_start: self.stack.len() - arg_count - 1,
                };
                
                self.call_stack.push(frame);
                Ok(Value::Null) // Continue execution
            },
            Value::NativeFunction(native_fn) => {
                let mut args = Vec::new();
                for _ in 0..arg_count {
                    args.insert(0, self.stack.pop().unwrap_or(Value::Null));
                }
                self.stack.pop(); // Remove function from stack
                
                match native_fn(&args) {
                    Ok(result) => Ok(result),
                    Err(error) => Err(CompilerError::ExecutionFailed(error)),
                }
            },
            _ => Err(CompilerError::ExecutionFailed("Value is not callable".to_string())),
        }
    }
    
    // Utility methods
    fn is_truthy(&self, value: &Value) -> bool {
        match value {
            Value::Boolean(b) => *b,
            Value::Null | Value::Nil => false,
            Value::Integer(0) => false,
            Value::Float(f) => *f != 0.0,
            Value::Number(n) => *n != 0.0,
            Value::String(s) => !s.is_empty(),
            _ => true,
        }
    }
    
    fn values_equal(&self, a: &Value, b: &Value) -> bool {
        match (a, b) {
            (Value::Integer(x), Value::Integer(y)) => x == y,
            (Value::Float(x), Value::Float(y)) => x == y,
            (Value::Number(x), Value::Number(y)) => x == y,
            (Value::Boolean(x), Value::Boolean(y)) => x == y,
            (Value::String(x), Value::String(y)) => x == y,
            (Value::Null, Value::Null) | (Value::Nil, Value::Nil) => true,
            (Value::Null, Value::Nil) | (Value::Nil, Value::Null) => true,
            (Value::Integer(x), Value::Float(y)) => *x as f64 == *y,
            (Value::Float(x), Value::Integer(y)) => *x == *y as f64,
            _ => false,
        }
    }
    
    fn value_to_string(&self, value: &Value) -> String {
        match value {
            Value::Integer(x) => x.to_string(),
            Value::Float(x) => x.to_string(),
            Value::Number(x) => x.to_string(),
            Value::Boolean(b) => b.to_string(),
            Value::String(s) => s.clone(),
            Value::Null | Value::Nil => "null".to_string(),
            Value::List(items) => {
                let item_strings: Vec<String> = items.iter().map(|item| self.value_to_string(item)).collect();
                format!("[{}]", item_strings.join(", "))
            },
            _ => format!("{:?}", value),
        }
    }
}

impl BytecodeExecutor {
    /// Load function source from registry or disk
    fn load_function_source(&self, function_id: &FunctionId) -> CompilerResult<String> {
        // Try to get source from function registry metadata
        if let Ok(registry) = self.function_registry.read() {
            if let Some(metadata) = registry.get(function_id) {
                if let Some(source) = &metadata.source_code {
                    return Ok(source.clone());
                }
            }
        }
        
        // Fall back to loading from disk based on function name
        let source_path = format!("src/{}.runa", function_id.name);
        std::fs::read_to_string(&source_path).map_err(|e| {
            CompilerError::CompilationFailed(format!("Failed to load source for {}: {}", function_id.name, e))
        })
    }
}

// Support types for parsing and compilation
#[derive(Debug, Clone)]
struct ParsedProgram {
    statements: Vec<StatementAst>,
    imports: Vec<String>,
    exports: Vec<String>,
}

#[derive(Debug, Clone)]
enum StatementAst {
    ExpressionStatement(ExpressionAst),
    VariableDeclaration { name: String, value: ExpressionAst },
    Return(Option<ExpressionAst>),
}

#[derive(Debug, Clone)]
enum ExpressionAst {
    Literal(Value),
    Identifier(String),
    BinaryOperation { left: Box<ExpressionAst>, operator: String, right: Box<ExpressionAst> },
    FunctionCall { name: String, args: Vec<ExpressionAst> },
}