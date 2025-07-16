//! The Runa code generator, which walks the AST and emits bytecode.

use runa_common::ast::*;
use runa_common::bytecode::{Chunk, OpCode, Value};
use runa_common::token::{Token, TokenType};

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
    
    // ... Expressions ...
    fn visit_expr(&mut self, expr: &Expr) -> Result<(), String>;
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<(), String>;
    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<(), String>;
    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<(), String>;
    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<(), String>;
    fn visit_grouping_expr(&mut self, expr: &GroupingExpr) -> Result<(), String>;
    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<(), String>;
}

impl<'a> CodeGenerator<'a> {
    pub fn compile(statements: &[Stmt]) -> Result<Chunk, String> {
        let mut chunk = Chunk::new();
        let mut codegen = CodeGenerator {
            compiler: Compiler::new(),
            chunk: &mut chunk,
        };

        for statement in statements {
            codegen.visit_stmt(statement)?;
        }

        codegen.chunk.write(OpCode::Return as u8);
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
        self.chunk.write(byte);
        println!("[DEBUG] EMIT: Chunk code now: {:?}", self.chunk.code);
    }

    fn emit_bytes(&mut self, byte1: u8, byte2: u8) {
        println!("[DEBUG] EMIT_BYTES: Writing bytes {} {} (0x{:02x} 0x{:02x}) to chunk at {:p}", byte1, byte2, byte1, byte2, self.chunk as *const _);
        self.emit_byte(byte1);
        self.emit_byte(byte2);
    }
    
    fn emit_jump(&mut self, instruction: OpCode) -> usize {
        self.emit_byte(instruction as u8);
        // Emit placeholder bytes for the jump offset.
        // We use a 16-bit offset, allowing jumps of up to 65,535 bytes.
        self.emit_byte(0xff);
        self.emit_byte(0xff);
        self.chunk.code.len() - 2
    }
    
    fn patch_jump(&mut self, offset: usize) {
        // -2 to adjust for the bytecode for the jump itself.
        let jump = self.chunk.code.len() - offset - 2;

        if jump > u16::MAX as usize {
            // This would be a real error in a production compiler.
            panic!("Jump too large.");
        }
        
        self.chunk.code[offset] = ((jump >> 8) & 0xff) as u8;
        self.chunk.code[offset + 1] = (jump & 0xff) as u8;
    }

    fn emit_loop(&mut self, loop_start: usize) {
        self.emit_byte(OpCode::Loop as u8);

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
        }
    }
    
    fn visit_expr(&mut self, expr: &Expr) -> Result<(), String> {
        match expr {
            Expr::Literal(e) => self.visit_literal_expr(e),
            Expr::Binary(e) => self.visit_binary_expr(e),
            Expr::Grouping(e) => self.visit_grouping_expr(e),
            Expr::Variable(e) => self.visit_variable_expr(e),
            Expr::Assign(e) => self.visit_assign_expr(e),
            Expr::Call(e) => self.visit_call_expr(e),
            // Unary will be added later
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
            self.patch_jump(then_jump);

            // Compile the 'else' branch
            self.visit_stmt(else_branch)?;
            
            // Backpatch the second jump to point to the instruction right after the 'else' branch.
            self.patch_jump(else_jump);
        } else {
            // If there's no 'else' branch, just patch the first jump.
            self.patch_jump(then_jump);
        }

        Ok(())
    }

    fn visit_while_stmt(&mut self, stmt: &WhileStmt) -> Result<(), String> {
        let loop_start = self.chunk.code.len();
        self.visit_expr(&stmt.condition)?;

        let exit_jump = self.emit_jump(OpCode::JumpIfFalse);
        self.visit_stmt(&Stmt::Block(stmt.body.clone()))?;
        self.emit_loop(loop_start);

        self.patch_jump(exit_jump);
        Ok(())
    }

    fn visit_for_stmt(&mut self, stmt: &ForStmt) -> Result<(), String> {
        self.begin_scope();

        // Initializer
        self.visit_expr(&stmt.start)?;
        self.add_local(stmt.variable.clone());

        let loop_start = self.chunk.code.len();

        // Condition
        self.visit_expr(&stmt.end)?;
        let var_slot = self.resolve_local(&stmt.variable)?;
        self.emit_bytes(OpCode::GetLocal as u8, var_slot);
        self.emit_byte(OpCode::Less as u8); // For now, we only support 'to' which is exclusive upper bound.

        let exit_jump = self.emit_jump(OpCode::JumpIfFalse);

        // Body
        self.visit_stmt(&Stmt::Block(stmt.body.clone()))?;

        // Increment
        let var_slot = self.resolve_local(&stmt.variable)?;
        self.emit_bytes(OpCode::GetLocal as u8, var_slot);
        let const_index = self.chunk.add_constant(Value::Number(1.0));
        self.emit_bytes(OpCode::Constant as u8, const_index);
        self.emit_byte(OpCode::Add as u8);
        self.emit_bytes(OpCode::SetLocal as u8, var_slot);
        self.emit_byte(OpCode::Pop as u8); // Pop the result of the increment expression.

        self.emit_loop(loop_start);

        self.patch_jump(exit_jump);
        
        self.end_scope();

        Ok(())
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
        self.emit_byte(OpCode::Print as u8);
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
            function_codegen.chunk.write(OpCode::Return as u8);
        }
        
        // Create function object
        let function = runa_common::bytecode::Function {
            name: stmt.name.lexeme.clone(),
            chunk: function_chunk,
            arity: stmt.params.len(),
        };
        
        // Add function to constants and emit DefineFunction
        let name_constant = self.chunk.add_constant(Value::Number(0.0)); // TODO: Use proper string constant
        let function_constant = self.chunk.add_constant(Value::Function(Box::new(function)));
        
        self.emit_byte(OpCode::Constant as u8);
        self.emit_byte(function_constant);
        self.emit_byte(OpCode::DefineFunction as u8);
        self.emit_byte(name_constant);
        self.emit_byte(stmt.params.len() as u8);
        
        // Add the function name to the current scope so it can be called
        self.add_local(stmt.name.clone());
        
        // Store the function in the local variable
        let slot = self.resolve_local(&stmt.name)?;
        self.emit_bytes(OpCode::SetLocal as u8, slot);
        
        println!("[DEBUG] FUNCTION: Function compilation complete. Main chunk now: {:?}", self.chunk.code);
        
        Ok(())
    }
    
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<(), String> {
        let arg = self.resolve_local(&expr.name)?;
        self.emit_bytes(OpCode::GetLocal as u8, arg);
        Ok(())
    }
    
    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<(), String> {
        self.visit_expr(&expr.value)?;
        let arg = self.resolve_local(&expr.name)?;
        self.emit_bytes(OpCode::SetLocal as u8, arg);
        Ok(())
    }

    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<(), String> {
        match expr.value.token_type {
            TokenType::Integer | TokenType::Float => {
                let value = expr.value.lexeme.parse::<f64>().unwrap();
                let const_index = self.chunk.add_constant(Value::Number(value));
                self.emit_bytes(OpCode::Constant as u8, const_index);
            }
            TokenType::String => {
                // Remove quotes from the string literal
                let value = expr.value.lexeme.trim_matches('"').to_string();
                let const_index = self.chunk.add_constant(Value::String(value));
                self.emit_bytes(OpCode::Constant as u8, const_index);
            }
            TokenType::Boolean => {
                let value = expr.value.lexeme.parse::<bool>().unwrap();
                let const_index = self.chunk.add_constant(Value::Boolean(value));
                self.emit_bytes(OpCode::Constant as u8, const_index);
            }
            _ => return Err("This literal type is not yet supported.".to_string()),
        };
        Ok(())
    }

    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<(), String> {
        println!("[DEBUG] BINARY: Visiting binary expression with chunk at {:p}", self.chunk as *const _);
        
        self.visit_expr(&expr.left)?;
        self.visit_expr(&expr.right)?;

        match expr.operator.token_type {
            TokenType::Plus => {
                // At runtime, if either operand is a string, use Concat; else Add
                // (Semantic analysis guarantees this is valid)
                self.emit_byte(OpCode::Concat as u8);
            },
            TokenType::Minus => {
                println!("[DEBUG] BINARY: Emitting Subtract opcode to chunk at {:p}", self.chunk as *const _);
                self.emit_byte(OpCode::Subtract as u8);
            },
            TokenType::MultipliedBy => self.emit_byte(OpCode::Multiply as u8),
            TokenType::DividedBy => self.emit_byte(OpCode::Divide as u8),
            TokenType::IsEqualTo => self.emit_byte(OpCode::Equal as u8),
            TokenType::IsNotEqualTo => self.emit_byte(OpCode::NotEqual as u8),
            TokenType::IsGreaterThan => self.emit_byte(OpCode::Greater as u8),
            TokenType::IsGreaterThanOrEqualTo => self.emit_byte(OpCode::GreaterEqual as u8),
            TokenType::IsLessThan => self.emit_byte(OpCode::Less as u8),
            TokenType::IsLessThanOrEqualTo => self.emit_byte(OpCode::LessEqual as u8),
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
} 