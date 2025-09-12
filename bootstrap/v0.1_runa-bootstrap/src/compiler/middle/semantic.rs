use anyhow::Result;
use crate::utils::diagnostics::DiagnosticEngine;
use crate::compiler::frontend::ast::*;
use crate::compiler::middle::symbol_table::SymbolTable;

pub struct SemanticAnalyzer {
    symbol_table: SymbolTable,
}

impl SemanticAnalyzer {
    pub fn new() -> Self {
        Self {
            symbol_table: SymbolTable::new(),
        }
    }
    
    pub fn analyze(&mut self, program: Program, diagnostic_engine: &mut DiagnosticEngine) -> Result<Program> {
        // First pass: Register all type definitions and functions
        for type_def in &program.type_definitions {
            self.register_type(type_def, diagnostic_engine)?;
        }
        
        for function in &program.functions {
            self.register_function(function, diagnostic_engine)?;
        }
        
        // Second pass: Analyze function bodies
        let mut analyzed_functions = Vec::new();
        for function in program.functions {
            analyzed_functions.push(self.analyze_function(function, diagnostic_engine)?);
        }
        
        Ok(Program {
            imports: program.imports,
            type_definitions: program.type_definitions,
            functions: analyzed_functions,
            constants: program.constants,
        })
    }
    
    fn register_type(&mut self, type_def: &TypeDefinition, _diagnostic_engine: &mut DiagnosticEngine) -> Result<()> {
        match type_def {
            TypeDefinition::Struct { name, fields: _ } => {
                self.symbol_table.define_type(name.clone(), type_def.clone());
            }
            TypeDefinition::Enum { name, variants: _ } => {
                self.symbol_table.define_type(name.clone(), type_def.clone());
            }
        }
        Ok(())
    }
    
    fn register_function(&mut self, function: &Function, _diagnostic_engine: &mut DiagnosticEngine) -> Result<()> {
        self.symbol_table.define_function(
            function.name.clone(),
            function.parameters.clone(),
            function.return_type.clone(),
        );
        Ok(())
    }
    
    fn analyze_function(&mut self, function: Function, diagnostic_engine: &mut DiagnosticEngine) -> Result<Function> {
        // Create new scope for function
        self.symbol_table.push_scope();
        
        // Register parameters in scope
        for param in &function.parameters {
            self.symbol_table.define_variable(param.name.clone(), param.param_type.clone());
        }
        
        // Analyze function body
        let mut analyzed_body = Vec::new();
        for statement in function.body {
            analyzed_body.push(self.analyze_statement(statement, diagnostic_engine)?);
        }
        
        // Pop function scope
        self.symbol_table.pop_scope();
        
        Ok(Function {
            name: function.name,
            parameters: function.parameters,
            return_type: function.return_type,
            body: analyzed_body,
        })
    }
    
    fn analyze_statement(&mut self, statement: Statement, diagnostic_engine: &mut DiagnosticEngine) -> Result<Statement> {
        match statement {
            Statement::VariableDeclaration { name, var_type, initializer } => {
                let analyzed_initializer = self.analyze_expression(initializer, diagnostic_engine)?;
                
                // Infer type if not specified
                let inferred_type = var_type.or_else(|| analyzed_initializer.get_type_hint());
                
                if let Some(var_type) = &inferred_type {
                    self.symbol_table.define_variable(name.clone(), var_type.clone());
                } else {
                    diagnostic_engine.error(
                        format!("Cannot infer type for variable '{}'", name),
                        None
                    );
                }
                
                Ok(Statement::VariableDeclaration {
                    name,
                    var_type: inferred_type,
                    initializer: analyzed_initializer,
                })
            }
            Statement::Assignment { target, value } => {
                // Check if variable exists
                if !self.symbol_table.lookup_variable(&target) {
                    diagnostic_engine.error(
                        format!("Undefined variable '{}'", target),
                        None
                    );
                }
                
                let analyzed_value = self.analyze_expression(value, diagnostic_engine)?;
                
                Ok(Statement::Assignment {
                    target,
                    value: analyzed_value,
                })
            }
            Statement::FunctionCall { name, args } => {
                // Check if function exists
                if !self.symbol_table.lookup_function(&name) {
                    diagnostic_engine.error(
                        format!("Undefined function '{}'", name),
                        None
                    );
                }
                
                let mut analyzed_args = Vec::new();
                for arg in args {
                    analyzed_args.push(self.analyze_expression(arg, diagnostic_engine)?);
                }
                
                Ok(Statement::FunctionCall {
                    name,
                    args: analyzed_args,
                })
            }
            Statement::Return { value } => {
                let analyzed_value = if let Some(expr) = value {
                    Some(self.analyze_expression(expr, diagnostic_engine)?)
                } else {
                    None
                };
                
                Ok(Statement::Return {
                    value: analyzed_value,
                })
            }
            Statement::If { condition, then_branch, else_branch } => {
                let analyzed_condition = self.analyze_expression(condition, diagnostic_engine)?;
                
                let mut analyzed_then = Vec::new();
                for stmt in then_branch {
                    analyzed_then.push(self.analyze_statement(stmt, diagnostic_engine)?);
                }
                
                let analyzed_else = if let Some(else_stmts) = else_branch {
                    let mut analyzed_else_stmts = Vec::new();
                    for stmt in else_stmts {
                        analyzed_else_stmts.push(self.analyze_statement(stmt, diagnostic_engine)?);
                    }
                    Some(analyzed_else_stmts)
                } else {
                    None
                };
                
                Ok(Statement::If {
                    condition: analyzed_condition,
                    then_branch: analyzed_then,
                    else_branch: analyzed_else,
                })
            }
            Statement::While { condition, body } => {
                let analyzed_condition = self.analyze_expression(condition, diagnostic_engine)?;
                
                let mut analyzed_body = Vec::new();
                for stmt in body {
                    analyzed_body.push(self.analyze_statement(stmt, diagnostic_engine)?);
                }
                
                Ok(Statement::While {
                    condition: analyzed_condition,
                    body: analyzed_body,
                })
            }
            Statement::For { variable, iterable, body } => {
                let analyzed_iterable = self.analyze_expression(iterable, diagnostic_engine)?;
                
                // Create new scope for loop variable
                self.symbol_table.push_scope();
                // TODO: Infer loop variable type from iterable
                self.symbol_table.define_variable(variable.clone(), Type::Integer); // Placeholder
                
                let mut analyzed_body = Vec::new();
                for stmt in body {
                    analyzed_body.push(self.analyze_statement(stmt, diagnostic_engine)?);
                }
                
                self.symbol_table.pop_scope();
                
                Ok(Statement::For {
                    variable,
                    iterable: analyzed_iterable,
                    body: analyzed_body,
                })
            }
            Statement::Expression(expr) => {
                let analyzed_expr = self.analyze_expression(expr, diagnostic_engine)?;
                Ok(Statement::Expression(analyzed_expr))
            }
            Statement::FieldAssignment { object, field, value } => {
                // Check if variable exists
                if !self.symbol_table.lookup_variable(&object) {
                    diagnostic_engine.error(
                        format!("Undefined variable '{}'", object),
                        None
                    );
                }
                
                let analyzed_value = self.analyze_expression(value, diagnostic_engine)?;
                
                Ok(Statement::FieldAssignment {
                    object,
                    field,
                    value: analyzed_value,
                })
            }
        }
    }
    
    fn analyze_expression(&mut self, expression: Expression, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        match expression {
            Expression::Variable { name } => {
                if !self.symbol_table.lookup_variable(&name) {
                    diagnostic_engine.error(
                        format!("Undefined variable '{}'", name),
                        None
                    );
                }
                Ok(Expression::Variable { name })
            }
            Expression::FunctionCall { name, args } => {
                if !self.symbol_table.lookup_function(&name) {
                    diagnostic_engine.error(
                        format!("Undefined function '{}'", name),
                        None
                    );
                }
                
                let mut analyzed_args = Vec::new();
                for arg in args {
                    analyzed_args.push(self.analyze_expression(arg, diagnostic_engine)?);
                }
                
                Ok(Expression::FunctionCall {
                    name,
                    args: analyzed_args,
                })
            }
            Expression::BinaryOperation { left, operator, right } => {
                let analyzed_left = self.analyze_expression(*left, diagnostic_engine)?;
                let analyzed_right = self.analyze_expression(*right, diagnostic_engine)?;
                
                Ok(Expression::BinaryOperation {
                    left: Box::new(analyzed_left),
                    operator,
                    right: Box::new(analyzed_right),
                })
            }
            Expression::UnaryOperation { operator, operand } => {
                let analyzed_operand = self.analyze_expression(*operand, diagnostic_engine)?;
                
                Ok(Expression::UnaryOperation {
                    operator,
                    operand: Box::new(analyzed_operand),
                })
            }
            Expression::FieldAccess { object, field } => {
                let analyzed_object = self.analyze_expression(*object, diagnostic_engine)?;
                
                Ok(Expression::FieldAccess {
                    object: Box::new(analyzed_object),
                    field,
                })
            }
            Expression::Constructor { type_name, fields } => {
                // Check if type exists
                if !self.symbol_table.lookup_type(&type_name) {
                    diagnostic_engine.error(
                        format!("Undefined type '{}'", type_name),
                        None
                    );
                }
                
                let mut analyzed_fields = std::collections::HashMap::new();
                for (field_name, field_expr) in fields {
                    analyzed_fields.insert(
                        field_name,
                        self.analyze_expression(field_expr, diagnostic_engine)?
                    );
                }
                
                Ok(Expression::Constructor {
                    type_name,
                    fields: analyzed_fields,
                })
            }
            // Literals don't need analysis
            Expression::Literal { value } => Ok(Expression::Literal { value }),
        }
    }
}