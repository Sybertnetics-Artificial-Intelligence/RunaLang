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
    fn visit_annotation_stmt(&mut self, stmt: &AnnotationStmt) -> Result<(), String>;
    
    fn visit_variable_expr(&mut self, expr: &VariableExpr) -> Result<RunaType, String>;
    fn visit_assign_expr(&mut self, expr: &AssignExpr) -> Result<RunaType, String>;
    fn visit_binary_expr(&mut self, expr: &BinaryExpr) -> Result<RunaType, String>;
    fn visit_unary_expr(&mut self, expr: &UnaryExpr) -> Result<RunaType, String>;
    fn visit_grouping_expr(&mut self, expr: &GroupingExpr) -> Result<RunaType, String>;
    fn visit_literal_expr(&mut self, expr: &LiteralExpr) -> Result<RunaType, String>;
    fn visit_list_expr(&mut self, expr: &ListExpr) -> Result<RunaType, String>;
    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<RunaType, String>;
    fn visit_index_expr(&mut self, expr: &IndexAccessExpr) -> Result<RunaType, String>;
    fn visit_interpolated_string_expr(&mut self, expr: &InterpolatedStringExpr) -> Result<RunaType, String>;
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
        scope.insert(name.lexeme.clone(), (false, RunaType::Null));
        Ok(())
    }

    fn define(&mut self, name: &Token, var_type: RunaType) {
        if let Some(scope) = self.scopes.last_mut() {
            // Mark as fully initialized and ready for use with its final type.
            scope.insert(name.lexeme.clone(), (true, var_type));
        }
    }

    fn resolve_local(&self, name: &Token) -> Result<RunaType, String> {
        // First, try to find as a variable
        for scope in self.scopes.iter().rev() {
            if let Some((is_initialized, var_type)) = scope.get(&name.lexeme) {
                if !is_initialized {
                     return Err(format!("Cannot read local variable '{}' in its own initializer.", name.lexeme));
                }
                return Ok(var_type.clone());
            }
        }
        
        // If not found as variable, try to find as a function call
        // Convert "Greet" to "greet", "Add Numbers" to "add numbers", etc.
        let function_name = self.convert_call_to_function_name(&name.lexeme);
        let quoted_function_name = format!("\"{}\"", function_name);
        for scope in self.scopes.iter().rev() {
            if let Some((is_initialized, var_type)) = scope.get(&quoted_function_name) {
                if !is_initialized {
                     return Err(format!("Cannot call function '{}' in its own definition.", function_name));
                }
                return Ok(var_type.clone());
            }
        }
        
        Err(format!("Undeclared variable or function '{}'.", name.lexeme))
    }
    
    fn convert_call_to_function_name(&self, call_name: &str) -> String {
        // Convert "Greet" to "greet"
        // Convert "Add Numbers" to "add numbers"
        // Split on capital letters, lowercase each word, join with spaces
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

    fn analyze_expression(&mut self, expr: &Expr) -> Result<RunaType, String> {
        self.visit_expr(expr)
    }

    fn infer_type_from_context(&mut self, name: &str) -> Result<RunaType, String> {
        // Analyze variable name patterns and usage context for type inference
        if name.starts_with("is_") || name.starts_with("has_") || name.ends_with("_flag") {
            return Ok(RunaType::Boolean);
        }
        if name.ends_with("_count") || name.ends_with("_index") || name.ends_with("_size") {
            return Ok(RunaType::Integer);
        }
        if name.ends_with("_name") || name.ends_with("_text") || name.ends_with("_message") {
            return Ok(RunaType::String);
        }
        if name.ends_with("_list") || name.ends_with("_array") || name.ends_with("_items") {
            return Ok(RunaType::List(Box::new(RunaType::Any)));
        }
        if name.ends_with("_map") || name.ends_with("_dict") || name.ends_with("_table") {
            return Ok(RunaType::Dictionary {
                key: Box::new(RunaType::String),
                value: Box::new(RunaType::Any),
            });
        }
        Ok(RunaType::Any)
    }

    fn find_common_type(&mut self, types: &[RunaType]) -> Result<RunaType, String> {
        if types.is_empty() {
            return Ok(RunaType::Null);
        }
        
        if types.len() == 1 {
            return Ok(types[0].clone());
        }
        
        // Find the least common supertype
        let mut common_type = types[0].clone();
        
        for type_info in &types[1..] {
            common_type = self.compute_least_common_supertype(&common_type, type_info)?;
        }
        
        Ok(common_type)
    }
    
    fn compute_least_common_supertype(&self, t1: &RunaType, t2: &RunaType) -> Result<RunaType, String> {
        match (t1, t2) {
            (RunaType::Integer, RunaType::Integer) => Ok(RunaType::Integer),
            (RunaType::Float, RunaType::Float) => Ok(RunaType::Float),
            (RunaType::Integer, RunaType::Float) | (RunaType::Float, RunaType::Integer) => Ok(RunaType::Float),
            (RunaType::String, RunaType::String) => Ok(RunaType::String),
            (RunaType::Boolean, RunaType::Boolean) => Ok(RunaType::Boolean),
            (RunaType::Null, t) | (t, RunaType::Null) => Ok(t.clone()),
            (RunaType::Any, _) | (_, RunaType::Any) => Ok(RunaType::Any),
            (RunaType::List(elem1), RunaType::List(elem2)) => {
                let common_elem = self.compute_least_common_supertype(elem1, elem2)?;
                Ok(RunaType::List(Box::new(common_elem)))
            }
            (RunaType::Dictionary { key: k1, value: v1 }, RunaType::Dictionary { key: k2, value: v2 }) => {
                let common_key = self.compute_least_common_supertype(k1, k2)?;
                let common_value = self.compute_least_common_supertype(v1, v2)?;
                Ok(RunaType::Dictionary {
                    key: Box::new(common_key),
                    value: Box::new(common_value),
                })
            }
            _ => Ok(RunaType::Any)
        }
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
            Stmt::Annotation(s) => self.visit_annotation_stmt(s),
        }
    }
    
    fn visit_expr(&mut self, expr: &Expr) -> Result<RunaType, String> {
        match expr {
            Expr::Assign(e) => self.visit_assign_expr(e),
            Expr::Binary(e) => self.visit_binary_expr(e),
            Expr::Grouping(e) => self.visit_grouping_expr(e),
            Expr::Literal(e) => self.visit_literal_expr(e),
            Expr::List(e) => self.visit_list_expr(e),
            Expr::Unary(e) => self.visit_unary_expr(e),
            Expr::Variable(e) => self.visit_variable_expr(e),
            Expr::Call(e) => self.visit_call_expr(e),
            Expr::Index(e) => self.visit_index_expr(e),
            Expr::InterpolatedString(e) => self.visit_interpolated_string_expr(e),
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
        if let Some(initializer) = &stmt.initializer {
            let init_type = self.analyze_expression(initializer)?;
            self.define(&stmt.name, init_type);
        } else {
            let inferred_type = self.infer_type_from_context(&stmt.name.lexeme)?;
            self.define(&stmt.name, inferred_type);
        }
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
        
        // Check if this is a for-each loop over a collection
        match &start_type {
            RunaType::List(element_type) => {
                // For-each loop over a list
                self.begin_scope();
                self.declare(&stmt.variable)?;
                self.define(&stmt.variable, *element_type.clone()); // Loop variable has the element type
                self.visit_block_stmt(&stmt.body)?;
                self.end_scope();
            }
            RunaType::Dictionary { key: _, value } => {
                // For-each loop over a dictionary (iterates over values)
                self.begin_scope();
                self.declare(&stmt.variable)?;
                self.define(&stmt.variable, *value.clone()); // Loop variable has the value type
                self.visit_block_stmt(&stmt.body)?;
                self.end_scope();
            }
            RunaType::String => {
                // For-each loop over a string (iterates over characters)
                self.begin_scope();
                self.declare(&stmt.variable)?;
                self.define(&stmt.variable, RunaType::String); // Loop variable is a character (string)
                self.visit_block_stmt(&stmt.body)?;
                self.end_scope();
            }
            RunaType::Integer | RunaType::Float => {
                // Traditional numeric for loop (For i from start to end)
                let end_type = self.visit_expr(&stmt.end)?;
                if end_type != RunaType::Integer && end_type != RunaType::Float {
                    return Err("For loop end must be a number (integer or float).".to_string());
                }
                if let Some(step) = &stmt.step {
                    let step_type = self.visit_expr(step)?;
                     if step_type != RunaType::Integer && step_type != RunaType::Float {
                        return Err("For loop step must be a number (integer or float).".to_string());
                    }
                }

                self.begin_scope();
                self.declare(&stmt.variable)?;
                self.define(&stmt.variable, RunaType::Integer); // Loop variable is always an integer for indexing
                self.visit_block_stmt(&stmt.body)?;
                self.end_scope();
            }
            _ => {
                return Err("For loop must iterate over a collection (list, dictionary, string) or use numeric range.".to_string());
            }
        }

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
                // Enforce math-only: '+' is only for numbers. Suggest 'joined with' for strings.
                let left_is_num = left_type == RunaType::Integer || left_type == RunaType::Float;
                let right_is_num = right_type == RunaType::Integer || right_type == RunaType::Float;

                if left_is_num && right_is_num {
                    if left_type == RunaType::Integer && right_type == RunaType::Integer {
                        Ok(RunaType::Integer)
                    } else {
                        Ok(RunaType::Float)
                    }
                } else if left_type == RunaType::String || right_type == RunaType::String {
                    Err("Use 'joined with' for string concatenation instead of '+'.".to_string())
                } else {
                    Err("'+' requires numeric operands (integer/float).".to_string())
                }
            }
            TokenType::Minus | TokenType::MultipliedBy | TokenType::DividedBy | TokenType::Modulo => {
                if (left_type == RunaType::Integer || left_type == RunaType::Float) && 
                   (right_type == RunaType::Integer || right_type == RunaType::Float) {
                    // Integer op Integer = Integer, otherwise Float
                    if left_type == RunaType::Integer && right_type == RunaType::Integer {
                        Ok(RunaType::Integer)
                    } else {
                        Ok(RunaType::Float)
                    }
                } else {
                    Err("Binary arithmetic operations require number operands (integer/float).".to_string())
                }
            }
            TokenType::IsGreaterThan | TokenType::IsLessThan | TokenType::IsGreaterThanOrEqualTo | TokenType::IsLessThanOrEqualTo => {
                if (left_type == RunaType::Integer || left_type == RunaType::Float) && 
                   (right_type == RunaType::Integer || right_type == RunaType::Float) {
                    Ok(RunaType::Boolean)
                } else {
                    Err("Comparison operations require number operands (integer/float).".to_string())
                }
            }
            TokenType::IsEqualTo | TokenType::IsNotEqualTo => {
                if left_type == right_type {
                    Ok(RunaType::Boolean)
                } else {
                    Err("Equality operations require operands of the same type.".to_string())
                }
            }
            TokenType::FollowedBy => {
                // String concatenation - canonical in natural syntax ('joined with' / 'concatenated with' aliases)
                if left_type == RunaType::String {
                    Ok(RunaType::String)
                } else {
                    Err("String concatenation requires the left operand to be a string. Use 'joined with'.".to_string())
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
                if right_type == RunaType::Integer || right_type == RunaType::Float {
                    Ok(right_type) // Preserve the type (Integer -> Integer, Float -> Float)
                } else {
                    Err("Unary minus operator requires a number operand (integer/float).".to_string())
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
            TokenType::Integer => Ok(RunaType::Integer),
            TokenType::Float => Ok(RunaType::Float),
            TokenType::String => Ok(RunaType::String),
            TokenType::Boolean => Ok(RunaType::Boolean),
            _ => Ok(RunaType::Null), // Should not happen with valid syntax
        }
    }

    fn visit_list_expr(&mut self, expr: &ListExpr) -> Result<RunaType, String> {
        if expr.elements.is_empty() {
            // Empty list - use generic Any type
            return Ok(RunaType::List(Box::new(RunaType::Any)));
        }
        
        // Analyze all elements to determine the most specific common type
        let mut element_types = Vec::new();
        for element in &expr.elements {
            let element_type = self.visit_expr(element)?;
            element_types.push(element_type);
        }
        
        // Find the common type for all elements
        let common_element_type = self.find_common_type(&element_types)?;
        
        Ok(RunaType::List(Box::new(common_element_type)))
    }

    fn visit_function_stmt(&mut self, stmt: &FunctionStmt) -> Result<(), String> {
        // Declare the function name in the current scope
        self.declare(&stmt.name)?;
        
        // Analyze the function body in a new scope
        self.begin_scope();
        
        // Mark that we're entering a function
        let was_in_function = self.in_function;
        self.in_function = true;
        
        // Add parameters to the function scope
        for param in &stmt.params {
            self.declare(param)?;
            self.define(param, RunaType::Any); // Parameters are dynamically typed for now
        }
        
        // Analyze the function body and collect return types
        let mut return_types = Vec::new();
        for statement in &stmt.body {
            self.visit_stmt(statement)?;
            
            // If this statement is a return, analyze its type
            if let Stmt::Return(return_stmt) = statement {
                if let Some(return_expr) = &return_stmt.value {
                    let return_type = self.analyze_expression(return_expr)?;
                    return_types.push(return_type);
                } else {
                    return_types.push(RunaType::Null);
                }
            }
        }
        
        // Restore the previous function context
        self.in_function = was_in_function;
        
        self.end_scope();
        
        // Determine the most specific return type
        let function_type = if return_types.is_empty() {
            RunaType::Null // No return statements
        } else if return_types.len() == 1 {
            return_types[0].clone() // Single return type
        } else {
            // Multiple return types - find the most specific common type
            self.find_common_type(&return_types)?
        };
        
        // Define function with proper type
        self.define(&stmt.name, function_type);
        
        Ok(())
    }

    fn visit_print_stmt(&mut self, stmt: &PrintStmt) -> Result<(), String> {
        // Analyze the expression to be printed
        self.visit_expr(&stmt.value)?;
        Ok(())
    }

    fn visit_annotation_stmt(&mut self, stmt: &AnnotationStmt) -> Result<(), String> {
        // Annotations don't affect the type system directly
        // They provide metadata for AI systems and documentation
        // We could store them in a separate annotation context for later use
        
        // For now, just validate that the annotation is well-formed
        if stmt.content.is_empty() {
            return Err("Annotation content cannot be empty".to_string());
        }
        
        Ok(())
    }

    fn visit_call_expr(&mut self, expr: &CallExpr) -> Result<RunaType, String> {
        // Analyze the callee (should be a function)
        let callee_type = self.visit_expr(&expr.callee)?;
        
        // Check if callee is a function type
        match callee_type {
            RunaType::Function { .. } => {
                // Function type check passed
            }
            _ => {
                return Err("Can only call functions.".to_string());
            }
        }
        
        // Analyze all arguments
        for arg in &expr.arguments {
            self.visit_expr(arg)?;
        }
        
        // For now, assume all functions return Any
        // In a more sophisticated system, we'd track function signatures
        Ok(RunaType::Any)
    }

    fn visit_index_expr(&mut self, expr: &IndexAccessExpr) -> Result<RunaType, String> {
        let target_type = self.visit_expr(&expr.target)?;
        let index_type = self.visit_expr(&expr.index)?;
        match target_type {
            RunaType::List(boxed_elem_type) => {
                if index_type != RunaType::Integer && index_type != RunaType::Float {
                    return Err("List indices must be numbers (integer or float).".to_string());
                }
                Ok(*boxed_elem_type)
            }
            RunaType::Dictionary { key: _boxed_key_type, value: boxed_value_type } => {
                // For now, allow any key type (could be stricter)
                Ok(*boxed_value_type)
            }
            RunaType::String => {
                if index_type != RunaType::Integer && index_type != RunaType::Float {
                    return Err("String indices must be numbers (integer or float).".to_string());
                }
                Ok(RunaType::String)
            }
            _ => Err("Cannot index into this type.".to_string()),
        }
    }

    fn visit_interpolated_string_expr(&mut self, expr: &InterpolatedStringExpr) -> Result<RunaType, String> {
        // Analyze all expressions within the interpolated string
        for part in &expr.parts {
            match part {
                InterpolatedStringPart::String(_) => {
                    // Static strings are always valid
                }
                InterpolatedStringPart::Expression(expr) => {
                    // Analyze the expression and ensure it can be converted to string
                    let expr_type = self.visit_expr(expr)?;
                    // For now, allow any type to be interpolated (they'll be converted to strings at runtime)
                    // In a stricter implementation, we could require string conversion methods
                    let _ = expr_type; // Just to use the variable
                }
            }
        }
        
        // Interpolated strings always result in String type
        Ok(RunaType::String)
    }
} 