use anyhow::Result;
use crate::utils::diagnostics::DiagnosticEngine;
use crate::compiler::frontend::ast::*;

pub struct TypeChecker {
    // Future: Add more sophisticated type checking state
}

impl TypeChecker {
    pub fn new() -> Self {
        Self {}
    }
    
    pub fn check_types(&mut self, program: Program, diagnostic_engine: &mut DiagnosticEngine) -> Result<Program> {
        let mut checked_functions = Vec::new();
        
        for function in program.functions {
            checked_functions.push(self.check_function(function, diagnostic_engine)?);
        }
        
        Ok(Program {
            imports: program.imports,
            type_definitions: program.type_definitions,
            functions: checked_functions,
            constants: program.constants,
        })
    }
    
    fn check_function(&mut self, function: Function, diagnostic_engine: &mut DiagnosticEngine) -> Result<Function> {
        // Check function body statements
        let mut checked_body = Vec::new();
        for statement in function.body {
            checked_body.push(self.check_statement(statement, &function.return_type, diagnostic_engine)?);
        }
        
        Ok(Function {
            name: function.name,
            parameters: function.parameters,
            return_type: function.return_type,
            body: checked_body,
        })
    }
    
    fn check_statement(&mut self, statement: Statement, expected_return_type: &Type, diagnostic_engine: &mut DiagnosticEngine) -> Result<Statement> {
        match statement {
            Statement::VariableDeclaration { name, var_type, initializer } => {
                let checked_initializer = self.check_expression(initializer, diagnostic_engine)?;
                let initializer_type = self.infer_expression_type(&checked_initializer, diagnostic_engine)?;
                
                // Check type compatibility if type is explicitly specified
                if let Some(declared_type) = &var_type {
                    if !self.types_compatible(declared_type, &initializer_type) {
                        diagnostic_engine.error(
                            format!(
                                "Type mismatch in variable '{}': expected {:?}, found {:?}",
                                name, declared_type, initializer_type
                            ),
                            None
                        );
                    }
                }
                
                Ok(Statement::VariableDeclaration {
                    name,
                    var_type: var_type.or(Some(initializer_type)),
                    initializer: checked_initializer,
                })
            }
            Statement::Assignment { target, value } => {
                let checked_value = self.check_expression(value, diagnostic_engine)?;
                // TODO: Check type compatibility with target variable
                
                Ok(Statement::Assignment {
                    target,
                    value: checked_value,
                })
            }
            Statement::FunctionCall { name, args } => {
                let mut checked_args = Vec::new();
                for arg in args {
                    checked_args.push(self.check_expression(arg, diagnostic_engine)?);
                }
                
                Ok(Statement::FunctionCall {
                    name,
                    args: checked_args,
                })
            }
            Statement::Return { value } => {
                if let Some(return_expr) = value {
                    let checked_expr = self.check_expression(return_expr, diagnostic_engine)?;
                    let return_type = self.infer_expression_type(&checked_expr, diagnostic_engine)?;
                    
                    if !self.types_compatible(expected_return_type, &return_type) {
                        diagnostic_engine.error(
                            format!(
                                "Return type mismatch: expected {:?}, found {:?}",
                                expected_return_type, return_type
                            ),
                            None
                        );
                    }
                    
                    Ok(Statement::Return {
                        value: Some(checked_expr),
                    })
                } else {
                    // Void return
                    if !matches!(expected_return_type, Type::Void) {
                        diagnostic_engine.error(
                            format!("Expected return value of type {:?}", expected_return_type),
                            None
                        );
                    }
                    
                    Ok(Statement::Return { value: None })
                }
            }
            Statement::If { condition, then_branch, else_branch } => {
                let checked_condition = self.check_expression(condition, diagnostic_engine)?;
                let condition_type = self.infer_expression_type(&checked_condition, diagnostic_engine)?;
                
                // Condition must be boolean
                if !matches!(condition_type, Type::Boolean) {
                    diagnostic_engine.error(
                        format!("If condition must be Boolean, found {:?}", condition_type),
                        None
                    );
                }
                
                let mut checked_then = Vec::new();
                for stmt in then_branch {
                    checked_then.push(self.check_statement(stmt, expected_return_type, diagnostic_engine)?);
                }
                
                let checked_else = if let Some(else_stmts) = else_branch {
                    let mut checked_else_stmts = Vec::new();
                    for stmt in else_stmts {
                        checked_else_stmts.push(self.check_statement(stmt, expected_return_type, diagnostic_engine)?);
                    }
                    Some(checked_else_stmts)
                } else {
                    None
                };
                
                Ok(Statement::If {
                    condition: checked_condition,
                    then_branch: checked_then,
                    else_branch: checked_else,
                })
            }
            Statement::While { condition, body } => {
                let checked_condition = self.check_expression(condition, diagnostic_engine)?;
                let condition_type = self.infer_expression_type(&checked_condition, diagnostic_engine)?;
                
                // Condition must be boolean
                if !matches!(condition_type, Type::Boolean) {
                    diagnostic_engine.error(
                        format!("While condition must be Boolean, found {:?}", condition_type),
                        None
                    );
                }
                
                let mut checked_body = Vec::new();
                for stmt in body {
                    checked_body.push(self.check_statement(stmt, expected_return_type, diagnostic_engine)?);
                }
                
                Ok(Statement::While {
                    condition: checked_condition,
                    body: checked_body,
                })
            }
            Statement::For { variable, iterable, body } => {
                let checked_iterable = self.check_expression(iterable, diagnostic_engine)?;
                // TODO: Proper type checking for iterable types
                
                let mut checked_body = Vec::new();
                for stmt in body {
                    checked_body.push(self.check_statement(stmt, expected_return_type, diagnostic_engine)?);
                }
                
                Ok(Statement::For {
                    variable,
                    iterable: checked_iterable,
                    body: checked_body,
                })
            }
            Statement::Expression(expr) => {
                let checked_expr = self.check_expression(expr, diagnostic_engine)?;
                Ok(Statement::Expression(checked_expr))
            }
            Statement::FieldAssignment { object, field, value } => {
                let checked_value = self.check_expression(value, diagnostic_engine)?;
                // TODO: Check field exists and type compatibility
                
                Ok(Statement::FieldAssignment {
                    object,
                    field,
                    value: checked_value,
                })
            }
        }
    }
    
    fn check_expression(&mut self, expression: Expression, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        match expression {
            Expression::BinaryOperation { left, operator, right } => {
                let checked_left = self.check_expression(*left, diagnostic_engine)?;
                let checked_right = self.check_expression(*right, diagnostic_engine)?;
                
                let left_type = self.infer_expression_type(&checked_left, diagnostic_engine)?;
                let right_type = self.infer_expression_type(&checked_right, diagnostic_engine)?;
                
                // Check operator compatibility
                self.check_binary_operator_compatibility(&operator, &left_type, &right_type, diagnostic_engine)?;
                
                Ok(Expression::BinaryOperation {
                    left: Box::new(checked_left),
                    operator,
                    right: Box::new(checked_right),
                })
            }
            Expression::UnaryOperation { operator, operand } => {
                let checked_operand = self.check_expression(*operand, diagnostic_engine)?;
                let operand_type = self.infer_expression_type(&checked_operand, diagnostic_engine)?;
                
                // Check unary operator compatibility
                self.check_unary_operator_compatibility(&operator, &operand_type, diagnostic_engine)?;
                
                Ok(Expression::UnaryOperation {
                    operator,
                    operand: Box::new(checked_operand),
                })
            }
            Expression::FunctionCall { name, args } => {
                let mut checked_args = Vec::new();
                for arg in args {
                    checked_args.push(self.check_expression(arg, diagnostic_engine)?);
                }
                
                Ok(Expression::FunctionCall {
                    name,
                    args: checked_args,
                })
            }
            Expression::FieldAccess { object, field } => {
                let checked_object = self.check_expression(*object, diagnostic_engine)?;
                // TODO: Check field exists in object type
                
                Ok(Expression::FieldAccess {
                    object: Box::new(checked_object),
                    field,
                })
            }
            Expression::Constructor { type_name, fields } => {
                let mut checked_fields = std::collections::HashMap::new();
                for (field_name, field_expr) in fields {
                    checked_fields.insert(
                        field_name,
                        self.check_expression(field_expr, diagnostic_engine)?
                    );
                }
                
                Ok(Expression::Constructor {
                    type_name,
                    fields: checked_fields,
                })
            }
            // These don't need type checking
            Expression::Literal { .. } => Ok(expression),
            Expression::Variable { .. } => Ok(expression),
        }
    }
    
    fn infer_expression_type(&self, expression: &Expression, _diagnostic_engine: &mut DiagnosticEngine) -> Result<Type> {
        match expression {
            Expression::Literal { value } => {
                Ok(match value {
                    LiteralValue::Integer(_) => Type::Integer,
                    LiteralValue::Float(_) => Type::Float,
                    LiteralValue::String(_) => Type::String,
                    LiteralValue::Boolean(_) => Type::Boolean,
                })
            }
            Expression::Variable { name: _ } => {
                // TODO: Look up variable type in symbol table
                Ok(Type::Integer) // Placeholder
            }
            Expression::BinaryOperation { left, operator, right: _ } => {
                match operator {
                    BinaryOperator::Equal | BinaryOperator::NotEqual
                    | BinaryOperator::LessThan | BinaryOperator::LessThanEqual
                    | BinaryOperator::GreaterThan | BinaryOperator::GreaterThanEqual
                    | BinaryOperator::And | BinaryOperator::Or => Ok(Type::Boolean),
                    _ => self.infer_expression_type(left, _diagnostic_engine),
                }
            }
            Expression::UnaryOperation { operator, operand } => {
                match operator {
                    UnaryOperator::Not => Ok(Type::Boolean),
                    UnaryOperator::Negate => self.infer_expression_type(operand, _diagnostic_engine),
                }
            }
            Expression::FunctionCall { name: _, args: _ } => {
                // TODO: Look up function return type
                Ok(Type::Integer) // Placeholder
            }
            Expression::FieldAccess { object: _, field: _ } => {
                // TODO: Look up field type
                Ok(Type::Integer) // Placeholder
            }
            Expression::Constructor { type_name, fields: _ } => {
                Ok(Type::Named(type_name.clone()))
            }
        }
    }
    
    fn types_compatible(&self, expected: &Type, actual: &Type) -> bool {
        match (expected, actual) {
            (Type::Integer, Type::Integer) => true,
            (Type::Float, Type::Float) => true,
            (Type::String, Type::String) => true,
            (Type::Boolean, Type::Boolean) => true,
            (Type::Named(a), Type::Named(b)) => a == b,
            (Type::Void, Type::Void) => true,
            // Numeric coercion
            (Type::Float, Type::Integer) => true,
            _ => false,
        }
    }
    
    fn check_binary_operator_compatibility(
        &self,
        operator: &BinaryOperator,
        left_type: &Type,
        right_type: &Type,
        diagnostic_engine: &mut DiagnosticEngine,
    ) -> Result<()> {
        match operator {
            BinaryOperator::Add | BinaryOperator::Subtract 
            | BinaryOperator::Multiply | BinaryOperator::Divide 
            | BinaryOperator::Modulo => {
                if !left_type.is_numeric() || !right_type.is_numeric() {
                    diagnostic_engine.error(
                        format!(
                            "Arithmetic operator {:?} requires numeric operands, found {:?} and {:?}",
                            operator, left_type, right_type
                        ),
                        None
                    );
                }
            }
            BinaryOperator::Equal | BinaryOperator::NotEqual => {
                if !self.types_compatible(left_type, right_type) {
                    diagnostic_engine.error(
                        format!(
                            "Comparison operator {:?} requires compatible types, found {:?} and {:?}",
                            operator, left_type, right_type
                        ),
                        None
                    );
                }
            }
            BinaryOperator::LessThan | BinaryOperator::LessThanEqual
            | BinaryOperator::GreaterThan | BinaryOperator::GreaterThanEqual => {
                if !left_type.is_numeric() || !right_type.is_numeric() {
                    diagnostic_engine.error(
                        format!(
                            "Relational operator {:?} requires numeric operands, found {:?} and {:?}",
                            operator, left_type, right_type
                        ),
                        None
                    );
                }
            }
            BinaryOperator::And | BinaryOperator::Or => {
                if !matches!(left_type, Type::Boolean) || !matches!(right_type, Type::Boolean) {
                    diagnostic_engine.error(
                        format!(
                            "Logical operator {:?} requires Boolean operands, found {:?} and {:?}",
                            operator, left_type, right_type
                        ),
                        None
                    );
                }
            }
        }
        Ok(())
    }
    
    fn check_unary_operator_compatibility(
        &self,
        operator: &UnaryOperator,
        operand_type: &Type,
        diagnostic_engine: &mut DiagnosticEngine,
    ) -> Result<()> {
        match operator {
            UnaryOperator::Negate => {
                if !operand_type.is_numeric() {
                    diagnostic_engine.error(
                        format!(
                            "Negation operator requires numeric operand, found {:?}",
                            operand_type
                        ),
                        None
                    );
                }
            }
            UnaryOperator::Not => {
                if !matches!(operand_type, Type::Boolean) {
                    diagnostic_engine.error(
                        format!(
                            "Logical NOT operator requires Boolean operand, found {:?}",
                            operand_type
                        ),
                        None
                    );
                }
            }
        }
        Ok(())
    }
}