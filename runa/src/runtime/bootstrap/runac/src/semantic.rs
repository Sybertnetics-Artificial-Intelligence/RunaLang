//! The Runa semantic analyzer, which walks the AST to find semantic errors.

use runa_common::ast::*;
use runa_common::token::{Token, TokenType};
use runa_common::types::RunaType;
use std::collections::HashMap;

pub struct SemanticAnalyzer {
    // A stack of scopes. Each scope is a HashMap of variable names to a tuple
    // indicating (is_initialized, type).
    scopes: Vec<HashMap<String, (bool, RunaType)>>,
    // Track whether we're currently inside a function
    in_function: bool,
}

// The visitor pattern now returns the inferred type for expressions.
trait AstVisitor {
    fn visit_stmt(&mut self, stmt: &Stmt) -> Result<(), String>;
    fn visit_expr(&mut self, expr: &Expr) -> Result<RunaType, String>;

    fn visit_let_stmt(&mut self, stmt: &LetStmt) -> Result<(), String>;
    fn visit_block_stmt(&mut self, stmt: &BlockStmt) -> Result<(), String>;
    fn visit_expr_stmt(&mut self, stmt: &ExprStmt) -> Result<(), String>;
    fn visit_if_stmt(&mut self, stmt: &IfStmt) -> Result<(), String>;
    fn visit_while_stmt(&mut self, stmt: &WhileStmt) -> Result<(), String>;
    fn visit_for_stmt(&mut self, stmt: &ForStmt) -> Result<(), String>;
    fn visit_return_stmt(&mut self, stmt: &ReturnStmt) -> Result<(), String>;
    fn visit_function_stmt(&mut self, stmt: &FunctionStmt) -> Result<(), String>;
    fn visit_print_stmt(&mut self, stmt: &PrintStmt) -> Result<(), String>;
    
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<RunaType, String>;
    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<RunaType, String>;
    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<RunaType, String>;
    fn visit_unary_expr(&mut self, expr: &UnaryExpr) -> Result<RunaType, String>;
    fn visit_grouping_expr(&mut self, expr: &GroupingExpr) -> Result<RunaType, String>;
    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<RunaType, String>;
    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<RunaType, String>;
    fn visit_index_expr(&mut self, expr: &IndexAccessExpr) -> Result<RunaType, String>;
}


impl SemanticAnalyzer {
    pub fn new() -> Self {
        SemanticAnalyzer {
            scopes: vec![HashMap::new()],
            in_function: false,
        }
    }

    pub fn analyze(&mut self, statements: &[Stmt]) -> Result<(), String> {
        for statement in statements {
            self.visit_stmt(statement)?;
        }
        Ok(())
    }

    fn begin_scope(&mut self) {
        self.scopes.push(HashMap::new());
    }

    fn end_scope(&mut self) {
        self.scopes.pop();
    }

    fn declare(&mut self, name: &Token) -> Result<(), String> {
        if self.scopes.is_empty() {
            return Ok(()); // Global scope is handled differently if we add it
        }
        let scope = self.scopes.last_mut().unwrap();
        if scope.contains_key(&name.lexeme) {
            return Err(format!("Variable '{}' already declared in this scope.", name.lexeme));
        }
        // Mark as declared but not yet initialized, with a temporary type.
        scope.insert(name.lexeme.clone(), (false, RunaType::Nil));
        Ok(())
    }

    fn define(&mut self, name: &Token, var_type: RunaType) {
        if let Some(scope) = self.scopes.last_mut() {
            // Mark as fully initialized and ready for use with its final type.
            scope.insert(name.lexeme.clone(), (true, var_type));
        }
    }

    fn resolve_local(&self, name: &Token) -> Result<RunaType, String> {
        for scope in self.scopes.iter().rev() {
            if let Some((is_initialized, var_type)) = scope.get(&name.lexeme) {
                if !is_initialized {
                     return Err(format!("Cannot read local variable '{}' in its own initializer.", name.lexeme));
                }
                return Ok(var_type.clone());
            }
        }
        Err(format!("Undeclared variable '{}'.", name.lexeme))
    }
}

impl AstVisitor for SemanticAnalyzer {
    fn visit_stmt(&mut self, stmt: &Stmt) -> Result<(), String> {
        match stmt {
            Stmt::Let(s) => self.visit_let_stmt(s),
            Stmt::Expression(s) => self.visit_expr_stmt(s),
            Stmt::If(s) => self.visit_if_stmt(s),
            Stmt::While(s) => self.visit_while_stmt(s),
            Stmt::For(s) => self.visit_for_stmt(s),
            Stmt::Block(s) => self.visit_block_stmt(s),
            Stmt::Return(s) => self.visit_return_stmt(s),
            Stmt::Function(s) => self.visit_function_stmt(s),
            Stmt::Print(s) => self.visit_print_stmt(s),
        }
    }
    
    fn visit_expr(&mut self, expr: &Expr) -> Result<RunaType, String> {
        match expr {
            Expr::Assign(e) => self.visit_assign_expr(e),
            Expr::Binary(e) => self.visit_binary_expr(e),
            Expr::Grouping(e) => self.visit_grouping_expr(e),
            Expr::Literal(e) => self.visit_literal_expr(e),
            Expr::Unary(e) => self.visit_unary_expr(e),
            Expr::Variable(e) => self.visit_variable_expr(e),
            Expr::Call(e) => self.visit_call_expr(e),
            Expr::Index(e) => self.visit_index_expr(e),
        }
    }

    fn visit_block_stmt(&mut self, stmt: &BlockStmt) -> Result<(), String> {
        self.begin_scope();
        for statement in &stmt.statements {
            self.visit_stmt(statement)?;
        }
        self.end_scope();
        Ok(())
    }

    fn visit_let_stmt(&mut self, stmt: &LetStmt) -> Result<(), String> {
        self.declare(&stmt.name)?;
        let initializer_type = if let Some(initializer) = &stmt.initializer {
            self.visit_expr(initializer)?
        } else {
            RunaType::Nil // No initializer, so it's Nil for now
        };
        self.define(&stmt.name, initializer_type);
        Ok(())
    }

    fn visit_expr_stmt(&mut self, stmt: &ExprStmt) -> Result<(), String> {
        self.visit_expr(&stmt.expr)?; // Evaluate for side-effects and errors, but discard type.
        Ok(())
    }

    fn visit_if_stmt(&mut self, stmt: &IfStmt) -> Result<(), String> {
        let condition_type = self.visit_expr(&stmt.condition)?;
        if condition_type != RunaType::Boolean {
            return Err("If condition must be a boolean.".to_string());
        }
        self.visit_block_stmt(&stmt.then_branch)?;
        if let Some(else_branch) = &stmt.else_branch {
            self.visit_stmt(else_branch)?;
        }
        Ok(())
    }
    
    fn visit_while_stmt(&mut self, stmt: &WhileStmt) -> Result<(), String> {
        let condition_type = self.visit_expr(&stmt.condition)?;
        if condition_type != RunaType::Boolean {
             return Err("While condition must be a boolean.".to_string());
        }
        self.visit_block_stmt(&stmt.body)
    }
    
    fn visit_for_stmt(&mut self, stmt: &ForStmt) -> Result<(), String> {
        let start_type = self.visit_expr(&stmt.start)?;
        if start_type != RunaType::Number {
            return Err("For loop start must be a number.".to_string());
        }
        let end_type = self.visit_expr(&stmt.end)?;
        if end_type != RunaType::Number {
            return Err("For loop end must be a number.".to_string());
        }
        if let Some(step) = &stmt.step {
            let step_type = self.visit_expr(step)?;
             if step_type != RunaType::Number {
                return Err("For loop step must be a number.".to_string());
            }
        }

        self.begin_scope();
        self.declare(&stmt.variable)?;
        self.define(&stmt.variable, RunaType::Number); // Loop variable is always a number.
        self.visit_block_stmt(&stmt.body)?;
        self.end_scope();

        Ok(())
    }
    
    fn visit_return_stmt(&mut self, stmt: &ReturnStmt) -> Result<(), String> {
        if !self.in_function {
            return Err("Return statement is only allowed inside functions.".to_string());
        }
        
        if let Some(expr) = &stmt.value {
            self.visit_expr(expr)?;
        }
        Ok(())
    }
    
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<RunaType, String> {
        self.resolve_local(&expr.name)
    }

    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<RunaType, String> {
        let var_type = self.resolve_local(&expr.name)?;
        let value_type = self.visit_expr(&expr.value)?;

        if var_type != value_type {
            return Err(format!("Mismatched types. Cannot assign {:?} to variable of type {:?}.", value_type, var_type));
        }

        Ok(value_type)
    }

    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<RunaType, String> {
        let left_type = self.visit_expr(&expr.left)?;
        let right_type = self.visit_expr(&expr.right)?;

        match expr.operator.token_type {
            TokenType::Plus => {
                if left_type == RunaType::Number && right_type == RunaType::Number {
                    Ok(RunaType::Number)
                } else if left_type == RunaType::String || right_type == RunaType::String {
                    Ok(RunaType::String)
                } else {
                    Err("Addition requires both operands to be numbers or at least one to be a string.".to_string())
                }
            }
            TokenType::Minus | TokenType::MultipliedBy | TokenType::DividedBy => {
                if left_type == RunaType::Number && right_type == RunaType::Number {
                    Ok(RunaType::Number)
                } else {
                    Err("Binary arithmetic operations require number operands.".to_string())
                }
            }
            TokenType::IsGreaterThan | TokenType::IsLessThan | TokenType::IsGreaterThanOrEqualTo | TokenType::IsLessThanOrEqualTo => {
                if left_type == RunaType::Number && right_type == RunaType::Number {
                    Ok(RunaType::Boolean)
                } else {
                    Err("Comparison operations require number operands.".to_string())
                }
            }
            TokenType::IsEqualTo | TokenType::IsNotEqualTo => {
                if left_type == right_type {
                    Ok(RunaType::Boolean)
                } else {
                    Err("Equality operations require operands of the same type.".to_string())
                }
            }
            _ => Err("Unsupported binary operator.".to_string()),
        }
    }

    fn visit_unary_expr(&mut self, expr: &UnaryExpr) -> Result<RunaType, String> {
        let right_type = self.visit_expr(&expr.right)?;

        match expr.operator.token_type {
            TokenType::Not => {
                if right_type == RunaType::Boolean {
                    Ok(RunaType::Boolean)
                } else {
                    Err("Logical 'not' operator requires a boolean operand.".to_string())
                }
            },
            TokenType::Minus => {
                if right_type == RunaType::Number {
                    Ok(RunaType::Number)
                } else {
                    Err("Unary minus operator requires a number operand.".to_string())
                }
            },
            _ => Err("Unsupported unary operator.".to_string()),
        }
    }

    fn visit_grouping_expr(&mut self, expr: &GroupingExpr) -> Result<RunaType, String> {
        self.visit_expr(&expr.expression)
    }

    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<RunaType, String> {
        match expr.value.token_type {
            TokenType::Integer | TokenType::Float => Ok(RunaType::Number),
            TokenType::String => Ok(RunaType::String),
            TokenType::Boolean => Ok(RunaType::Boolean),
            _ => Ok(RunaType::Nil), // Should not happen with valid syntax
        }
    }

    fn visit_function_stmt(&mut self, stmt: &FunctionStmt) -> Result<(), String> {
        // Declare the function name in the current scope
        self.declare(&stmt.name)?;
        
        // Define it as a function type (we'll use a simple approach for now)
        self.define(&stmt.name, RunaType::Function);
        
        // Analyze the function body in a new scope
        self.begin_scope();
        
        // Mark that we're entering a function
        let was_in_function = self.in_function;
        self.in_function = true;
        
        // Add parameters to the function scope
        for param in &stmt.params {
            self.declare(param)?;
            self.define(param, RunaType::Number); // Assume all params are numbers for now
        }
        
        // Analyze the function body
        for stmt in &stmt.body {
            self.visit_stmt(stmt)?;
        }
        
        // Restore the previous function context
        self.in_function = was_in_function;
        
        self.end_scope();
        Ok(())
    }

    fn visit_print_stmt(&mut self, stmt: &PrintStmt) -> Result<(), String> {
        // Analyze the expression to be printed
        self.visit_expr(&stmt.value)?;
        Ok(())
    }

    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<RunaType, String> {
        // Analyze the callee (should be a function)
        let callee_type = self.visit_expr(&expr.callee)?;
        
        if callee_type != RunaType::Function {
            return Err("Can only call functions.".to_string());
        }
        
        // Analyze all arguments
        for arg in &expr.arguments {
            self.visit_expr(arg)?;
        }
        
        // For now, assume all functions return Number
        // In a more sophisticated system, we'd track function signatures
        Ok(RunaType::Number)
    }

    fn visit_index_expr(&mut self, expr: &IndexAccessExpr) -> Result<RunaType, String> {
        let target_type = self.visit_expr(&expr.target)?;
        let index_type = self.visit_expr(&expr.index)?;
        match target_type {
            RunaType::List(boxed_elem_type) => {
                if index_type != RunaType::Number {
                    return Err("List indices must be numbers.".to_string());
                }
                Ok(*boxed_elem_type)
            }
            RunaType::Dictionary(_boxed_key_type, boxed_value_type) => {
                // For now, allow any key type (could be stricter)
                Ok(*boxed_value_type)
            }
            RunaType::String => {
                if index_type != RunaType::Number {
                    return Err("String indices must be numbers.".to_string());
                }
                Ok(RunaType::String)
            }
            _ => Err("Cannot index into this type.".to_string()),
        }
    }
} 