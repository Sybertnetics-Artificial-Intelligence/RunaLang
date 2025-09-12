use anyhow::Result;
use crate::utils::diagnostics::DiagnosticEngine;
use crate::compiler::frontend::lexer::{Token, TokenType};
use crate::compiler::frontend::ast::*;
use std::collections::HashMap;

pub struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            position: 0,
        }
    }
    
    pub fn parse(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Program> {
        let mut imports = Vec::new();
        let mut type_definitions = Vec::new();
        let mut functions = Vec::new();
        let mut constants = HashMap::new();
        
        while !self.is_at_end() {
            // Skip newlines at top level
            if matches!(self.peek().token_type, TokenType::Newline) {
                self.advance();
                continue;
            }
            
            match &self.peek().token_type {
                TokenType::Import => {
                    imports.push(self.parse_import(diagnostic_engine)?);
                }
                TokenType::Type => {
                    type_definitions.push(self.parse_type_definition(diagnostic_engine)?);
                }
                TokenType::Process => {
                    functions.push(self.parse_function(diagnostic_engine)?);
                }
                TokenType::Eof => break,
                _ => {
                    diagnostic_engine.error(
                        format!("Unexpected token: {:?}", self.peek().token_type),
                        None
                    );
                    self.advance(); // Skip unexpected token
                }
            }
        }
        
        Ok(Program {
            imports,
            type_definitions,
            functions,
            constants,
        })
    }
    
    fn parse_import(&mut self, _diagnostic_engine: &mut DiagnosticEngine) -> Result<Import> {
        self.consume_token(TokenType::Import)?;
        
        let module = if let TokenType::Identifier(name) = &self.peek().token_type {
            let module_name = name.clone();
            self.advance();
            module_name
        } else {
            return Err(anyhow::anyhow!("Expected module name after 'Import'"));
        };
        
        let items = Vec::new(); // Simplified for now
        
        Ok(Import { module, items })
    }
    
    fn parse_type_definition(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<TypeDefinition> {
        self.consume_token(TokenType::Type)?;
        self.consume_token(TokenType::Called)?;
        
        let name = if let TokenType::String(type_name) = &self.peek().token_type {
            let name = type_name.clone();
            self.advance();
            name
        } else {
            diagnostic_engine.error("Expected type name".to_string(), None);
            return Err(anyhow::anyhow!("Expected type name"));
        };
        
        self.consume_token(TokenType::Colon)?;
        
        let mut fields = Vec::new();
        
        // Parse fields until "End Type"
        while !self.is_at_end() && !self.check(&TokenType::End) {
            if matches!(self.peek().token_type, TokenType::Newline) {
                self.advance();
                continue;
            }
            
            if let TokenType::Identifier(field_name) = &self.peek().token_type {
                let field_name = field_name.clone();
                self.advance();
                
                self.consume_token(TokenType::As)?;
                
                let field_type = self.parse_type(diagnostic_engine)?;
                
                fields.push(Field {
                    name: field_name,
                    field_type,
                });
            } else {
                break;
            }
        }
        
        self.consume_token(TokenType::End)?;
        self.consume_token(TokenType::Type)?;
        
        Ok(TypeDefinition::Struct { name, fields })
    }
    
    fn parse_function(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Function> {
        self.consume_token(TokenType::Process)?;
        self.consume_token(TokenType::Called)?;
        
        let name = if let TokenType::String(func_name) = &self.peek().token_type {
            let name = func_name.clone();
            self.advance();
            name
        } else {
            diagnostic_engine.error("Expected function name".to_string(), None);
            return Err(anyhow::anyhow!("Expected function name"));
        };
        
        // Parse parameters
        let mut parameters = Vec::new();
        if self.check(&TokenType::That) {
            self.advance(); // consume "that"
            self.consume_token(TokenType::Takes)?;
            
            // Parse parameter list
            if let TokenType::Identifier(param_name) = &self.peek().token_type {
                let param_name = param_name.clone();
                self.advance();
                
                self.consume_token(TokenType::As)?;
                let param_type = self.parse_type(diagnostic_engine)?;
                
                parameters.push(Parameter {
                    name: param_name,
                    param_type,
                });
            }
        }
        
        // Parse return type
        let return_type = if self.check(&TokenType::Returns) {
            self.advance(); // consume "returns"
            self.parse_type(diagnostic_engine)?
        } else {
            Type::Void
        };
        
        self.consume_token(TokenType::Colon)?;
        
        // Parse function body
        let mut body = Vec::new();
        while !self.is_at_end() && !self.check(&TokenType::End) {
            if matches!(self.peek().token_type, TokenType::Newline) {
                self.advance();
                continue;
            }
            
            body.push(self.parse_statement(diagnostic_engine)?);
        }
        
        self.consume_token(TokenType::End)?;
        self.consume_token(TokenType::Process)?;
        
        Ok(Function {
            name,
            parameters,
            return_type,
            body,
        })
    }
    
    fn parse_statement(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Statement> {
        match &self.peek().token_type {
            TokenType::Let => {
                self.advance();
                
                let name = if let TokenType::Identifier(var_name) = &self.peek().token_type {
                    let name = var_name.clone();
                    self.advance();
                    name
                } else {
                    diagnostic_engine.error("Expected variable name".to_string(), None);
                    return Err(anyhow::anyhow!("Expected variable name"));
                };
                
                self.consume_token(TokenType::Be)?;
                
                let initializer = self.parse_expression(diagnostic_engine)?;
                
                Ok(Statement::VariableDeclaration {
                    name,
                    var_type: None,
                    initializer,
                })
            }
            TokenType::Set => {
                self.advance();
                
                let target = if let TokenType::Identifier(var_name) = &self.peek().token_type {
                    let name = var_name.clone();
                    self.advance();
                    name
                } else {
                    diagnostic_engine.error("Expected variable name".to_string(), None);
                    return Err(anyhow::anyhow!("Expected variable name"));
                };
                
                self.consume_token(TokenType::To)?;
                
                let value = self.parse_expression(diagnostic_engine)?;
                
                Ok(Statement::Assignment { target, value })
            }
            TokenType::Return => {
                self.advance();
                
                let value = if !matches!(self.peek().token_type, TokenType::Newline | TokenType::End) {
                    Some(self.parse_expression(diagnostic_engine)?)
                } else {
                    None
                };
                
                Ok(Statement::Return { value })
            }
            _ => {
                // Expression statement
                let expr = self.parse_expression(diagnostic_engine)?;
                Ok(Statement::Expression(expr))
            }
        }
    }
    
    fn parse_expression(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        self.parse_logical_or(diagnostic_engine)
    }
    
    fn parse_logical_or(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        let mut expr = self.parse_logical_and(diagnostic_engine)?;
        
        while self.check(&TokenType::Or) {
            self.advance();
            let right = self.parse_logical_and(diagnostic_engine)?;
            expr = Expression::BinaryOperation {
                left: Box::new(expr),
                operator: BinaryOperator::Or,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_logical_and(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        let mut expr = self.parse_equality(diagnostic_engine)?;
        
        while self.check(&TokenType::And) {
            self.advance();
            let right = self.parse_equality(diagnostic_engine)?;
            expr = Expression::BinaryOperation {
                left: Box::new(expr),
                operator: BinaryOperator::And,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_equality(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        let mut expr = self.parse_comparison(diagnostic_engine)?;
        
        while matches!(self.peek().token_type, TokenType::Equal | TokenType::NotEqual) {
            let operator = match self.peek().token_type {
                TokenType::Equal => BinaryOperator::Equal,
                TokenType::NotEqual => BinaryOperator::NotEqual,
                _ => unreachable!(),
            };
            self.advance();
            
            let right = self.parse_comparison(diagnostic_engine)?;
            expr = Expression::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_comparison(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        let mut expr = self.parse_term(diagnostic_engine)?;
        
        while matches!(self.peek().token_type, 
            TokenType::LessThan | TokenType::LessThanEqual | 
            TokenType::GreaterThan | TokenType::GreaterThanEqual) {
            
            let operator = match self.peek().token_type {
                TokenType::LessThan => BinaryOperator::LessThan,
                TokenType::LessThanEqual => BinaryOperator::LessThanEqual,
                TokenType::GreaterThan => BinaryOperator::GreaterThan,
                TokenType::GreaterThanEqual => BinaryOperator::GreaterThanEqual,
                _ => unreachable!(),
            };
            self.advance();
            
            let right = self.parse_term(diagnostic_engine)?;
            expr = Expression::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_term(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        let mut expr = self.parse_factor(diagnostic_engine)?;
        
        while matches!(self.peek().token_type, TokenType::Plus | TokenType::Minus) {
            let operator = match self.peek().token_type {
                TokenType::Plus => BinaryOperator::Add,
                TokenType::Minus => BinaryOperator::Subtract,
                _ => unreachable!(),
            };
            self.advance();
            
            let right = self.parse_factor(diagnostic_engine)?;
            expr = Expression::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_factor(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        let mut expr = self.parse_unary(diagnostic_engine)?;
        
        while matches!(self.peek().token_type, TokenType::Multiply | TokenType::Divide | TokenType::Modulo) {
            let operator = match self.peek().token_type {
                TokenType::Multiply => BinaryOperator::Multiply,
                TokenType::Divide => BinaryOperator::Divide,
                TokenType::Modulo => BinaryOperator::Modulo,
                _ => unreachable!(),
            };
            self.advance();
            
            let right = self.parse_unary(diagnostic_engine)?;
            expr = Expression::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_unary(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        if matches!(self.peek().token_type, TokenType::Not | TokenType::Minus) {
            let operator = match self.peek().token_type {
                TokenType::Not => UnaryOperator::Not,
                TokenType::Minus => UnaryOperator::Negate,
                _ => unreachable!(),
            };
            self.advance();
            
            let operand = self.parse_unary(diagnostic_engine)?;
            return Ok(Expression::UnaryOperation {
                operator,
                operand: Box::new(operand),
            });
        }
        
        self.parse_primary(diagnostic_engine)
    }
    
    fn parse_primary(&mut self, _diagnostic_engine: &mut DiagnosticEngine) -> Result<Expression> {
        match &self.peek().token_type {
            TokenType::Integer(value) => {
                let value = *value;
                self.advance();
                Ok(Expression::Literal {
                    value: LiteralValue::Integer(value),
                })
            }
            TokenType::Float(value) => {
                let value = *value;
                self.advance();
                Ok(Expression::Literal {
                    value: LiteralValue::Float(value),
                })
            }
            TokenType::String(value) => {
                let value = value.clone();
                self.advance();
                Ok(Expression::Literal {
                    value: LiteralValue::String(value),
                })
            }
            TokenType::Boolean(value) => {
                let value = *value;
                self.advance();
                Ok(Expression::Literal {
                    value: LiteralValue::Boolean(value),
                })
            }
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();
                
                // Check for function call
                if self.check(&TokenType::LeftParen) {
                    self.advance(); // consume '('
                    
                    let mut args = Vec::new();
                    if !self.check(&TokenType::RightParen) {
                        loop {
                            args.push(self.parse_expression(_diagnostic_engine)?);
                            if !self.check(&TokenType::Comma) {
                                break;
                            }
                            self.advance(); // consume ','
                        }
                    }
                    
                    self.consume_token(TokenType::RightParen)?;
                    
                    Ok(Expression::FunctionCall { name, args })
                } else {
                    Ok(Expression::Variable { name })
                }
            }
            TokenType::LeftParen => {
                self.advance(); // consume '('
                let expr = self.parse_expression(_diagnostic_engine)?;
                self.consume_token(TokenType::RightParen)?;
                Ok(expr)
            }
            _ => Err(anyhow::anyhow!("Unexpected token in expression: {:?}", self.peek().token_type)),
        }
    }
    
    fn parse_type(&mut self, _diagnostic_engine: &mut DiagnosticEngine) -> Result<Type> {
        match &self.peek().token_type {
            TokenType::Identifier(type_name) => {
                match type_name.as_str() {
                    "Integer" => {
                        self.advance();
                        Ok(Type::Integer)
                    }
                    "Float" => {
                        self.advance();
                        Ok(Type::Float)
                    }
                    "String" => {
                        self.advance();
                        Ok(Type::String)
                    }
                    "Boolean" => {
                        self.advance();
                        Ok(Type::Boolean)
                    }
                    _ => {
                        let name = type_name.clone();
                        self.advance();
                        Ok(Type::Named(name))
                    }
                }
            }
            _ => Err(anyhow::anyhow!("Expected type name")),
        }
    }
    
    // Helper methods
    fn is_at_end(&self) -> bool {
        matches!(self.peek().token_type, TokenType::Eof)
    }
    
    fn peek(&self) -> &Token {
        &self.tokens[self.position]
    }
    
    fn advance(&mut self) -> &Token {
        if !self.is_at_end() {
            self.position += 1;
        }
        &self.tokens[self.position - 1]
    }
    
    fn check(&self, token_type: &TokenType) -> bool {
        if self.is_at_end() {
            false
        } else {
            std::mem::discriminant(&self.peek().token_type) == std::mem::discriminant(token_type)
        }
    }
    
    fn consume_token(&mut self, expected: TokenType) -> Result<()> {
        if self.check(&expected) {
            self.advance();
            Ok(())
        } else {
            Err(anyhow::anyhow!("Expected {:?}, found {:?}", expected, self.peek().token_type))
        }
    }
}