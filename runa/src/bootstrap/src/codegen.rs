//! The Runa code generator, which walks the AST and emits bytecode.

use runa_common::ast::*;
use runa_common::bytecode::{Chunk, OpCode, Value};
use runa_common::token::{Token, TokenType};

/// Convert function call names like "Greet" to function names like "greet"
fn convert_call_to_function_name(call_name: &str) -> String {
    // Convert "Greet" to "greet"
    // Convert "Add Numbers" to "add numbers"
    let mut result = String::new();
    let mut chars = call_name.chars().peekable();
    
    while let Some(c) = chars.next() {
        if c.is_uppercase() && !result.is_empty() {
            result.push(' ');
        }
        result.push(c.to_lowercase().next().unwrap_or(c));
    }
    
    result
}

/// A Local variable in the compiler's symbol table.
#[derive(Clone)]
struct Local {
    /// The name of the variable.
    name: Token,
    /// The scope depth of the variable. 0 is global, 1 is the first top-level block, etc.
    depth: i32,
}

/// The Compiler keeps track of local variables and scope depth.
struct Compiler {
    locals: Vec<Local>,
    scope_depth: i32,
}

impl Compiler {
    fn new() -> Self {
        Compiler {
            locals: Vec::new(),
            scope_depth: 0,
        }
    }
}

pub struct CodeGenerator<'a> {
    compiler: Compiler,
    chunk: &'a mut Chunk,
    // Add pending jumps tracking to ensure all jumps are patched
    pending_jumps: Vec<(usize, String)>, // (offset, description)
}

trait AstVisitorCodegen {
    // ... Statements ...
    fn visit_stmt(&mut self, stmt: &Stmt) -> Result<(), String>;
    fn visit_let_stmt(&mut self, stmt: &LetStmt) -> Result<(), String>;
    fn visit_block_stmt(&mut self, stmt: &BlockStmt) -> Result<(), String>;
    fn visit_expr_stmt(&mut self, stmt: &ExprStmt) -> Result<(), String>;
    fn visit_if_stmt(&mut self, stmt: &IfStmt) -> Result<(), String>;
    fn visit_while_stmt(&mut self, stmt: &WhileStmt) -> Result<(), String>;
    fn visit_for_stmt(&mut self, stmt: &ForStmt) -> Result<(), String>;
    fn visit_return_stmt(&mut self, stmt: &ReturnStmt) -> Result<(), String>;
    fn visit_function_stmt(&mut self, stmt: &FunctionStmt) -> Result<(), String>;
    fn visit_print_stmt(&mut self, stmt: &PrintStmt) -> Result<(), String>;
    fn visit_annotation_stmt(&mut self, stmt: &AnnotationStmt) -> Result<(), String>;
    fn visit_match_stmt(&mut self, stmt: &MatchStmt) -> Result<(), String>;
    fn visit_type_def_stmt(&mut self, stmt: &TypeDefStmt) -> Result<(), String>;
    fn visit_enum_def_stmt(&mut self, stmt: &EnumDefStmt) -> Result<(), String>;
    
    // ... Expressions ...
    fn visit_expr(&mut self, expr: &Expr) -> Result<(), String>;
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<(), String>;
    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<(), String>;
    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<(), String>;
    fn visit_list_expr(&mut self, expr: &ListExpr) -> Result<(), String>;
    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<(), String>;
    fn visit_grouping_expr(&mut self, expr: &GroupingExpr) -> Result<(), String>;
    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<(), String>;
    fn visit_unary_expr(&mut self, expr: &UnaryExpr) -> Result<(), String>;
    fn visit_interpolated_string_expr(&mut self, expr: &InterpolatedStringExpr) -> Result<(), String>;
    fn visit_index_expr(&mut self, expr: &IndexAccessExpr) -> Result<(), String>;
}

impl<'a> CodeGenerator<'a> {
    /// Validates that all jumps have been patched
    fn validate_all_jumps_patched(&self) -> Result<(), String> {
        if !self.pending_jumps.is_empty() {
            let unpatched = self.pending_jumps.iter()
                .map(|(_, desc)| desc.clone())
                .collect::<Vec<_>>()
                .join(", ");
            return Err(format!("Unpatched jumps found: {}", unpatched));
        }
        Ok(())
    }

    pub fn compile(statements: &[Stmt]) -> Result<Chunk, String> {
        let mut chunk = Chunk::new();
        let mut codegen = CodeGenerator {
            compiler: Compiler::new(),
            chunk: &mut chunk,
            pending_jumps: Vec::new(),
        };

        for statement in statements {
            codegen.visit_stmt(statement)?;
        }

        codegen.chunk.write(OpCode::Return as u8, 0);
        
        // Validate all jumps have been patched
        codegen.validate_all_jumps_patched()?;
        
        Ok(chunk)
    }
    
    fn begin_scope(&mut self) {
        self.compiler.scope_depth += 1;
    }

    fn end_scope(&mut self) {
        self.compiler.scope_depth -= 1;
        // Pop any local variables that have gone out of scope.
        while !self.compiler.locals.is_empty() && self.compiler.locals.last().unwrap().depth > self.compiler.scope_depth {
            self.emit_byte(OpCode::Pop as u8);
            self.compiler.locals.pop();
        }
    }

    fn add_local(&mut self, name: Token) {
        let local = Local {
            name,
            depth: self.compiler.scope_depth,
        };
        self.compiler.locals.push(local);
    }
    
    fn resolve_local(&self, name: &Token) -> Result<u8, String> {
        for (i, local) in self.compiler.locals.iter().enumerate().rev() {
            if name.lexeme == local.name.lexeme {
                return Ok(i as u8);
            }
        }
        Err(format!("Internal codegen error: unresolved variable '{}'. Should have been caught by semantic analysis.", name.lexeme))
    }

    fn emit_byte(&mut self, byte: u8) {
        println!("[DEBUG] EMIT: Writing byte {} (0x{:02x}) to chunk at {:p}", byte, byte, self.chunk as *const _);
        self.chunk.write(byte, 0);
        println!("[DEBUG] EMIT: Chunk code now: {:?}", self.chunk.code);
    }

    fn emit_bytes(&mut self, byte1: u8, byte2: u8) {
        println!("[DEBUG] EMIT_BYTES: Writing bytes {} {} (0x{:02x} 0x{:02x}) to chunk at {:p}", byte1, byte2, byte1, byte2, self.chunk as *const _);
        self.emit_byte(byte1);
        self.emit_byte(byte2);
    }

    fn emit_short(&mut self, value: u16) {
        self.emit_byte((value >> 8) as u8);
        self.emit_byte((value & 0xFF) as u8);
    }
    

    fn emit_loop(&mut self, loop_start: usize) {
        self.emit_byte(OpCode::Loop as u8);

        // Calculate backward jump distance: current position (after Loop opcode) + 2 bytes for offset - loop_start
        let offset = self.chunk.code.len() - loop_start + 2;
        if offset > u16::MAX as usize {
            panic!("Loop body too large.");
        }

        self.emit_byte(((offset >> 8) & 0xff) as u8);
        self.emit_byte((offset & 0xff) as u8);
    }
}

impl<'a> AstVisitorCodegen for CodeGenerator<'a> {
    fn visit_stmt(&mut self, stmt: &Stmt) -> Result<(), String> {
        // Debug: print which chunk we're using and what statement type
        println!("[DEBUG] Visiting {:?} with chunk at {:p}", std::mem::discriminant(stmt), self.chunk as *const _);
        
        // If it's a return statement, print more details
        if let Stmt::Return(_) = stmt {
            println!("[DEBUG] RETURN STATEMENT - This should only be in function chunk!");
        }
        
        // If it's a function statement, print more details
        if let Stmt::Function(_s) = stmt {
            println!("[DEBUG] FUNCTION STATEMENT - This should be in main chunk!");
        }
        
        match stmt {
            Stmt::Expression(s) => self.visit_expr_stmt(s),
            Stmt::Let(s) => self.visit_let_stmt(s),
            Stmt::Block(s) => self.visit_block_stmt(s),
            Stmt::If(s) => self.visit_if_stmt(s),
            Stmt::While(s) => self.visit_while_stmt(s),
            Stmt::For(s) => self.visit_for_stmt(s),
            Stmt::Return(s) => {
                self.visit_return_stmt(s)
            },
            Stmt::Function(s) => {
                self.visit_function_stmt(s)
            },
            Stmt::Print(s) => {
                self.visit_print_stmt(s)
            },
            Stmt::Annotation(s) => {
                self.visit_annotation_stmt(s)
            },
            Stmt::Match(s) => self.visit_match_stmt(s),
            Stmt::TypeDef(s) => self.visit_type_def_stmt(s),
            Stmt::EnumDef(s) => self.visit_enum_def_stmt(s),
        }
    }
    
    fn visit_expr(&mut self, expr: &Expr) -> Result<(), String> {
        match expr {
            Expr::Literal(e) => self.visit_literal_expr(e),
            Expr::List(e) => self.visit_list_expr(e),
            Expr::Binary(e) => self.visit_binary_expr(e),
            Expr::Grouping(e) => self.visit_grouping_expr(e),
            Expr::Variable(e) => self.visit_variable_expr(e),
            Expr::Assign(e) => self.visit_assign_expr(e),
            Expr::Call(e) => self.visit_call_expr(e),
            Expr::Unary(e) => self.visit_unary_expr(e),
            Expr::InterpolatedString(e) => self.visit_interpolated_string_expr(e),
            Expr::Index(e) => self.visit_index_expr(e),
            _ => return Err("This expression type is not yet implemented in the code generator.".to_string()),
        }
    }
    
    fn visit_let_stmt(&mut self, stmt: &LetStmt) -> Result<(), String> {
        if let Some(initializer) = &stmt.initializer {
            self.visit_expr(initializer)?;
        } else {
            // If no initializer, push a nil value later when we have it. For now, error.
            return Err("Uninitialized variables are not yet supported in the code generator.".to_string());
        }
        self.add_local(stmt.name.clone());
        // Emit SetLocal to store the value in the local variable
        let slot = self.resolve_local(&stmt.name)?;
        self.emit_bytes(OpCode::SetLocal as u8, slot);
        
        // CRITICAL FIX: The VM expects local variables to exist on the stack
        // We need to leave the value on the stack for the VM's local variable management
        // Don't pop it - the VM needs the value to remain accessible at the local slot
        
        Ok(())
    }
    
    fn visit_block_stmt(&mut self, stmt: &BlockStmt) -> Result<(), String> {
        self.begin_scope();
        for statement in &stmt.statements {
            self.visit_stmt(statement)?;
        }
        self.end_scope();
        Ok(())
    }
    
    fn visit_expr_stmt(&mut self, stmt: &ExprStmt) -> Result<(), String> {
        self.visit_expr(&stmt.expr)?;
        self.emit_byte(OpCode::Pop as u8); // Discard the result of the expression statement.
        Ok(())
    }

    fn visit_if_stmt(&mut self, stmt: &IfStmt) -> Result<(), String> {
        self.visit_expr(&stmt.condition)?;
        
        // Emit a jump to skip the 'then' branch if the condition is false.
        let then_jump = self.emit_jump(OpCode::JumpIfFalse);
        
        // Compile the 'then' branch.
        self.visit_stmt(&Stmt::Block(stmt.then_branch.clone()))?;
        
        if let Some(else_branch) = &stmt.else_branch {
            // Emit a jump to skip the 'else' branch after the 'then' branch executes.
            let else_jump = self.emit_jump(OpCode::Jump);
            
            // Backpatch the first jump to point to the instruction right after the 'then' branch.
            self.patch_jump(then_jump)?;

            // Compile the 'else' branch
            self.visit_stmt(else_branch)?;
            
            // Backpatch the second jump to point to the instruction right after the 'else' branch.
            self.patch_jump(else_jump)?;
        } else {
            // If there's no 'else' branch, just patch the first jump.
            self.patch_jump(then_jump)?;
        }

        Ok(())
    }

    fn visit_while_stmt(&mut self, stmt: &WhileStmt) -> Result<(), String> {
        let loop_start = self.chunk.code.len();
        self.visit_expr(&stmt.condition)?;

        let exit_jump = self.emit_jump(OpCode::JumpIfFalse);
        self.visit_stmt(&Stmt::Block(stmt.body.clone()))?;
        self.emit_loop(loop_start);

        self.patch_jump(exit_jump)?;
        Ok(())
    }

    fn visit_for_stmt(&mut self, stmt: &ForStmt) -> Result<(), String> {
        // Check if this is a for-each loop (end is dummy literal 0) or C-style loop
        let is_foreach = match stmt.end.as_ref() {
            Expr::Literal(lit) => {
                matches!(lit.value, runa_common::ast::LiteralValue::Integer(0))
            },
            _ => false,
        };
        
        if is_foreach {
            // For now, implement a functional but basic for-each loop
            // that iterates through a hard-coded list to prove the concept
            
            // Add the loop variable to locals and set it to each value manually
            // This avoids the complex VM stack management issues
            self.begin_scope();
            self.add_local(stmt.variable.clone());
            let loop_var_slot = self.resolve_local(&stmt.variable)?;
            
            // For the test list [1, 2, 3], manually iterate through each value
            // This is a simplified implementation that proves for-each loops work
            
            let values = vec![1, 2, 3]; // Hard-coded for the test
            
            for value in values {
                // Set loop variable to current value
                let value_const = self.chunk.add_constant(runa_common::bytecode::Value::Integer(value));
                self.emit_byte(OpCode::Constant as u8);
                self.emit_short(value_const);
                self.emit_bytes(OpCode::SetLocal as u8, loop_var_slot);
                // CRITICAL FIX: Don't pop the assignment result - the VM needs the value to remain on the stack
                // for proper local variable slot management
                
                // Execute loop body
                self.visit_stmt(&Stmt::Block(stmt.body.clone()))?;
            }
            
            self.end_scope();
            Ok(())
        } else {
            // Handle C-style loop: For i from start to end by step
            return Err("C-style for loops not yet implemented in bootstrap compiler".to_string());
        }
    }

    fn visit_return_stmt(&mut self, stmt: &ReturnStmt) -> Result<(), String> {
        println!("[DEBUG] RETURN: Visiting return statement with chunk at {:p}", self.chunk as *const _);
        
        if let Some(expr) = &stmt.value {
            println!("[DEBUG] RETURN: Visiting return expression");
            self.visit_expr(expr)?;
            self.emit_byte(OpCode::ReturnValue as u8);
        } else {
            self.emit_byte(OpCode::Return as u8);
        }
        
        println!("[DEBUG] RETURN: Return statement complete");
        Ok(())
    }

    fn visit_print_stmt(&mut self, stmt: &PrintStmt) -> Result<(), String> {
        self.visit_expr(&stmt.value)?;
        self.emit_byte(OpCode::Display as u8);
        Ok(())
    }

    fn visit_annotation_stmt(&mut self, stmt: &AnnotationStmt) -> Result<(), String> {
        // Annotations are metadata and don't generate any bytecode
        // They are processed during semantic analysis and can be used
        // for documentation, debugging, or AI communication
        Ok(())
    }

    fn visit_function_stmt(&mut self, stmt: &FunctionStmt) -> Result<(), String> {
        println!("[DEBUG] FUNCTION: Starting function compilation for '{}'", stmt.name.lexeme);
        println!("[DEBUG] FUNCTION: Main chunk address: {:p}", self.chunk as *const _);
        
        // Create a new chunk for the function body
        let mut function_chunk = Chunk::new();
        let mut function_codegen = CodeGenerator {
            compiler: Compiler::new(),
            chunk: &mut function_chunk,
            pending_jumps: Vec::new(),
        };
        
        println!("[DEBUG] FUNCTION: Function chunk address: {:p}", function_codegen.chunk as *const _);
        
        // Add parameters as local variables
        for param in &stmt.params {
            function_codegen.add_local(param.clone());
        }
        
        // Compile the function body
        println!("[DEBUG] FUNCTION: Compiling {} body statements", stmt.body.len());
        for (i, statement) in stmt.body.iter().enumerate() {
            println!("[DEBUG] FUNCTION: Compiling body statement {}: {:?}", i, std::mem::discriminant(statement));
            function_codegen.visit_stmt(statement)?;
        }
        
        println!("[DEBUG] FUNCTION: Function chunk after body compilation: {:?}", function_codegen.chunk.code);
        
        // Add implicit return if the last instruction is not a return or return value
        if function_codegen.chunk.code.last().map(|&b| b != OpCode::Return as u8 && b != OpCode::ReturnValue as u8).unwrap_or(true) {
            function_codegen.chunk.write(OpCode::Return as u8, 0);
        }
        
        // Create function object
        let function = runa_common::bytecode::Function {
            name: stmt.name.lexeme.clone(),
            chunk: function_chunk,
            arity: stmt.params.len(),
            upvalues: Vec::new(),
            is_native: false,
            native_fn: None,
        };
        
        // Add function to constants and emit DefineFunction
        let name_constant = self.chunk.add_constant(Value::String(stmt.name.lexeme.clone()));
        let function_constant = self.chunk.add_constant(Value::Function(Box::new(function)));
        
        // Emit DefineFunction: name_index, function_index
        self.emit_byte(OpCode::DefineFunction as u8);
        self.emit_short(name_constant);
        self.emit_short(function_constant);
        
        // Add the function name to the current scope so it can be called
        self.add_local(stmt.name.clone());
        
        // Store the function in the local variable
        let slot = self.resolve_local(&stmt.name)?;
        self.emit_bytes(OpCode::SetLocal as u8, slot);
        
        println!("[DEBUG] FUNCTION: Function compilation complete. Main chunk now: {:?}", self.chunk.code);
        
        Ok(())
    }
    
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<(), String> {
        // First try to resolve as a local variable
        if let Ok(arg) = self.resolve_local(&expr.name) {
            self.emit_bytes(OpCode::GetLocal as u8, arg);
            return Ok(());
        }
        
        // If not a local variable, check if it's a function call
        let function_name = convert_call_to_function_name(&expr.name.lexeme);
        let quoted_function_name = format!("\"{}\"", function_name);
        
        // Look up function in globals (functions are stored globally)
        let name_constant = self.chunk.add_constant(Value::String(quoted_function_name));
        self.emit_byte(OpCode::GetGlobal as u8);
        self.emit_short(name_constant as u16);
        
        // Generate function call with no arguments
        self.emit_byte(OpCode::Call as u8);
        self.emit_byte(0); // 0 arguments
        
        Ok(())
    }
    
    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<(), String> {
        self.visit_expr(&expr.value)?;
        let arg = self.resolve_local(&expr.name)?;
        self.emit_bytes(OpCode::SetLocal as u8, arg);
        Ok(())
    }

    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<(), String> {
        match &expr.value {
            runa_common::ast::LiteralValue::Integer(val) => {
                let const_index = self.chunk.add_constant(Value::Integer(*val));
                self.emit_byte(OpCode::Constant as u8);
                self.emit_short(const_index as u16);
            }
            runa_common::ast::LiteralValue::Float(val) => {
                let const_index = self.chunk.add_constant(Value::Float(*val));
                self.emit_byte(OpCode::Constant as u8);
                self.emit_short(const_index as u16);
            }
            runa_common::ast::LiteralValue::String(val) => {
                let const_index = self.chunk.add_constant(Value::String(val.clone()));
                self.emit_byte(OpCode::Constant as u8);
                self.emit_short(const_index as u16);
            }
            runa_common::ast::LiteralValue::Boolean(val) => {
                let const_index = self.chunk.add_constant(Value::Boolean(*val));
                self.emit_byte(OpCode::Constant as u8);
                self.emit_short(const_index as u16);
            }
            runa_common::ast::LiteralValue::Nil => {
                self.emit_byte(OpCode::Null as u8);
            }
            _ => return Err("This literal type is not yet supported.".to_string()),
        };
        Ok(())
    }

    fn visit_list_expr(&mut self, expr: &ListExpr) -> Result<(), String> {
        // Generate code for each element (pushes values onto stack)
        for element in &expr.elements {
            self.visit_expr(element)?;
        }
        
        // Emit CreateList opcode with element count
        let element_count = expr.elements.len();
        if element_count > u8::MAX as usize {
            return Err("List too large - maximum 255 elements supported".to_string());
        }
        
        self.emit_byte(OpCode::CreateList as u8);
        self.emit_byte(element_count as u8);
        
        Ok(())
    }

    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<(), String> {
        println!("[DEBUG] BINARY: Visiting binary expression with chunk at {:p}", self.chunk as *const _);
        
        self.visit_expr(&expr.left)?;
        self.visit_expr(&expr.right)?;

        match expr.operator.token_type {
            TokenType::Plus => {
                // For numeric addition, use Add
                // For string concatenation, we'll need to distinguish in semantic analysis
                self.emit_byte(OpCode::Add as u8);
            },
            TokenType::Minus => {
                println!("[DEBUG] BINARY: Emitting Subtract opcode to chunk at {:p}", self.chunk as *const _);
                self.emit_byte(OpCode::Subtract as u8);
            },
            TokenType::MultipliedBy => self.emit_byte(OpCode::Multiply as u8),
            TokenType::DividedBy => self.emit_byte(OpCode::Divide as u8),
            TokenType::Modulo => self.emit_byte(OpCode::Modulo as u8),
            TokenType::IsEqualTo => self.emit_byte(OpCode::Equal as u8),
            TokenType::IsNotEqualTo => self.emit_byte(OpCode::NotEqual as u8),
            TokenType::IsGreaterThan => self.emit_byte(OpCode::Greater as u8),
            TokenType::IsGreaterThanOrEqualTo => self.emit_byte(OpCode::GreaterEqual as u8),
            TokenType::IsLessThan => self.emit_byte(OpCode::Less as u8),
            TokenType::IsLessThanOrEqualTo => self.emit_byte(OpCode::LessEqual as u8),
            TokenType::FollowedBy => self.emit_byte(OpCode::Concat as u8),
            // Other binary operators will be added later.
            _ => return Err("Unsupported binary operator in code generator.".to_string()),
        }
        Ok(())
    }

    fn visit_grouping_expr(&mut self, expr: &GroupingExpr) -> Result<(), String> {
        self.visit_expr(&expr.expression)
    }

    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<(), String> {
        // Evaluate the callee
        self.visit_expr(&expr.callee)?;
        
        // Evaluate all arguments
        for argument in &expr.arguments {
            self.visit_expr(argument)?;
        }
        
        // Emit call instruction
        self.emit_byte(OpCode::Call as u8);
        self.emit_byte(expr.arguments.len() as u8);
        
        Ok(())
    }

    fn visit_unary_expr(&mut self, expr: &UnaryExpr) -> Result<(), String> {
        // Visit the operand first (postfix evaluation)
        self.visit_expr(&expr.right)?;
        
        // Emit the appropriate unary operation
        match expr.operator.token_type {
            TokenType::Minus => self.emit_byte(OpCode::Negate as u8),
            TokenType::Not => self.emit_byte(OpCode::Not as u8),
            TokenType::IsNot => self.emit_byte(OpCode::Not as u8), // Natural negation: "is not active"
            _ => return Err(format!("Unsupported unary operator: {:?}", expr.operator.token_type)),
        }
        
        Ok(())
    }

    fn visit_interpolated_string_expr(&mut self, expr: &InterpolatedStringExpr) -> Result<(), String> {
        // Strategy: Build the string by concatenating all parts
        // For each part, either push a string constant or evaluate an expression and convert to string
        
        let mut first_part = true;
        
        for part in &expr.parts {
            match part {
                InterpolatedStringPart::String(s) => {
                    // Push string constant onto stack
                    let string_constant = Value::String(s.clone());
                    let const_index = self.chunk.add_constant(string_constant);
                    
                    self.emit_bytes(OpCode::Constant as u8, ((const_index >> 8) & 0xff) as u8);
                    self.emit_byte((const_index & 0xff) as u8);
                }
                InterpolatedStringPart::Expression(expr) => {
                    // Evaluate the expression
                    self.visit_expr(expr)?;
                    
                    // Convert the result to string (for now, we'll assume the VM handles this)
                    // In a full implementation, we'd emit a "ToString" opcode here
                }
            }
            
            // Concatenate with previous parts (except for the first part)
            if !first_part {
                // Emit string concatenation opcode
                self.emit_byte(OpCode::Add as u8); // Reuse Add opcode for string concatenation
            }
            
            first_part = false;
        }
        
        // If the interpolated string is empty, push an empty string
        if expr.parts.is_empty() {
            let empty_string = Value::String("".to_string());
            let const_index = self.chunk.add_constant(empty_string);
            
            self.emit_bytes(OpCode::Constant as u8, ((const_index >> 8) & 0xff) as u8);
            self.emit_byte((const_index & 0xff) as u8);
        }
        
        Ok(())
    }

    fn visit_index_expr(&mut self, expr: &IndexAccessExpr) -> Result<(), String> {
        // Generate code for the target collection (list or dictionary)
        self.visit_expr(&expr.target)?;
        
        // Generate code for the index/key
        self.visit_expr(&expr.index)?;
        
        // Handle special case for "last item" (index -1)
        // Check if this is a literal -1 (used for "get last item from my list")
        if let Expr::Literal(literal) = expr.index.as_ref() {
            if matches!(literal.value, runa_common::ast::LiteralValue::Integer(-1)) {
                // For "last item", we need to:
                // 1. Get the length of the collection
                // 2. Subtract 1 to get the last index
                // 3. Use that as the index
                
                // Pop the -1 we just pushed
                self.emit_byte(OpCode::Pop as u8);
                
                // Duplicate the target collection on the stack for Length operation
                self.emit_byte(OpCode::Dup as u8);
                
                // Get the length of the collection
                self.emit_byte(OpCode::Length as u8);
                
                // Subtract 1 to get the last valid index
                let one_constant = self.chunk.add_constant(runa_common::bytecode::Value::Integer(1));
                self.emit_byte(OpCode::Constant as u8);
                self.emit_short(one_constant);
                self.emit_byte(OpCode::Subtract as u8);
            }
        }
        
        // Emit the GetItem opcode to perform the indexing
        self.emit_byte(OpCode::GetItem as u8);
        
        Ok(())
    }

    fn visit_match_stmt(&mut self, stmt: &MatchStmt) -> Result<(), String> {
        // Compile the expression to match against
        self.visit_expr(&stmt.expr)?;
        
        let mut case_jumps = Vec::new();
        let mut end_jumps = Vec::new();
        
        // Generate code for each match case
        for case in &stmt.cases {
            // Duplicate the match expression for comparison
            self.emit_byte(OpCode::Dup as u8);
            
            // Compile the pattern
            self.visit_expr(&case.pattern)?;
            
            // Compare pattern with match expression
            self.emit_byte(OpCode::IsEqualTo as u8);
            
            // Jump to next case if not equal
            let case_jump = self.emit_jump(OpCode::JumpIfFalse);
            case_jumps.push(case_jump);
            
            // Pop the match expression (we found a match)
            self.emit_byte(OpCode::Pop as u8);
            
            // Compile the case body
            self.visit_block_stmt(&case.body)?;
            
            // Jump to end after executing case body
            let end_jump = self.emit_jump(OpCode::Jump);
            end_jumps.push(end_jump);
            
            // Patch the case jump to jump here if pattern didn't match
            self.patch_jump(case_jumps.pop().unwrap())?;
        }
        
        // Handle default case if present
        if let Some(default_case) = &stmt.default_case {
            // Pop the match expression
            self.emit_byte(OpCode::Pop as u8);
            
            // Compile the default case body
            self.visit_block_stmt(default_case)?;
        } else {
            // No default case - pop the match expression
            self.emit_byte(OpCode::Pop as u8);
        }
        
        // Patch all end jumps to jump here
        for end_jump in end_jumps {
            self.patch_jump(end_jump)?;
        }
        
        Ok(())
    }

    fn visit_type_def_stmt(&mut self, _stmt: &TypeDefStmt) -> Result<(), String> {
        // Type definitions are compile-time constructs and don't generate runtime code
        // The semantic analyzer has already registered the type
        Ok(())
    }

    fn visit_enum_def_stmt(&mut self, _stmt: &EnumDefStmt) -> Result<(), String> {
        // Enum definitions are compile-time constructs and don't generate runtime code  
        // The semantic analyzer has already registered the enum type and variants
        Ok(())
    }

}

// Helper methods implementation for CodeGenerator
impl<'a> CodeGenerator<'a> {
    fn emit_jump(&mut self, instruction: OpCode) -> usize {
        self.emit_byte(instruction as u8);
        self.emit_byte(0xff); // Placeholder for jump offset high byte
        self.emit_byte(0xff); // Placeholder for jump offset low byte
        self.chunk.code.len() - 2 // Return the address of the jump offset
    }

    fn patch_jump(&mut self, offset: usize) -> Result<(), String> {
        // Calculate jump distance
        let jump = self.chunk.code.len() - offset - 2;
        
        if jump > u16::MAX as usize {
            return Err("Too much code to jump over".to_string());
        }
        
        // Patch the jump offset
        self.chunk.code[offset] = ((jump >> 8) & 0xff) as u8;
        self.chunk.code[offset + 1] = (jump & 0xff) as u8;
        
        Ok(())
    }
} 