use anyhow::{Result, anyhow};
use crate::lexer::Token;
use crate::types::*;

pub fn parse(tokens: Vec<Token>) -> Result<Program> {
    let mut parser = Parser { tokens, pos: 0 };
    parser.parse_program()
}

struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    fn parse_program(&mut self) -> Result<Program> {
        let mut imports = Vec::new();
        let mut functions = Vec::new();
        let mut types = Vec::new();
        
        while !self.is_at_end() {
            match self.peek() {
                Token::Import => imports.push(self.parse_import()?),
                Token::Process => functions.push(self.parse_function()?),
                Token::Type => types.push(self.parse_type_definition()?),
                _ => return Err(anyhow!("Expected Import, Process or Type declaration")),
            }
        }
        
        Ok(Program { imports, functions, types })
    }
    
    fn parse_import(&mut self) -> Result<Import> {
        self.consume(Token::Import)?;
        
        let module_name = match self.advance() {
            Token::String(name) => name,
            _ => return Err(anyhow!("Expected module name as string")),
        };
        
        self.consume(Token::As)?;
        
        let alias = match self.advance() {
            Token::Identifier(alias) => alias,
            _ => return Err(anyhow!("Expected alias identifier")),
        };
        
        Ok(Import { module_name, alias })
    }
    
    fn parse_function(&mut self) -> Result<Function> {
        self.consume(Token::Process)?;
        self.consume(Token::Called)?;
        
        let name = match self.advance() {
            Token::String(name) => name,
            _ => return Err(anyhow!("Expected function name")),
        };
        
        let mut params = Vec::new();
        if self.check(&Token::That) {
            self.advance(); // consume "that"
            self.consume(Token::Takes)?;
            
            loop {
                let param_name = match self.advance() {
                    Token::Identifier(name) => name,
                    Token::Value => "value".to_string(), // Allow "value" as parameter name
                    token => return Err(anyhow!("Expected parameter name, found {:?}", token)),
                };
                
                self.consume(Token::As)?;
                
                let param_type = self.parse_type()?;
                
                params.push((param_name, param_type));
                
                if !self.check(&Token::Comma) { break; }
                self.advance(); // consume comma
            }
        }
        
        let return_type = if self.check(&Token::Returns) {
            self.advance(); // consume "returns"
            self.parse_type()?
        } else {
            Type::Void
        };
        
        self.consume(Token::Colon)?;
        
        let mut body = Vec::new();
        while !self.check(&Token::End) {
            body.push(self.parse_statement()?);
        }
        
        self.consume(Token::End)?;
        self.consume(Token::Process)?;
        
        Ok(Function { name, params, return_type, body })
    }
    
    fn parse_type_definition(&mut self) -> Result<TypeDefinition> {
        self.consume(Token::Type)?;
        self.consume(Token::Called)?;
        
        let name = match self.advance() {
            Token::String(name) => name,
            _ => return Err(anyhow!("Expected type name")),
        };
        
        self.consume(Token::Colon)?;
        
        let mut fields = Vec::new();
        while !self.check(&Token::End) {
            let field_name = match self.advance() {
                Token::Identifier(name) => name,
                _ => return Err(anyhow!("Expected field name")),
            };
            
            self.consume(Token::As)?;
            
            let field_type = self.parse_type()?;
            fields.push((field_name, field_type));
        }
        
        self.consume(Token::End)?;
        self.consume(Token::Type)?;
        
        Ok(TypeDefinition { name, fields })
    }
    
    fn parse_type(&mut self) -> Result<Type> {
        match self.advance() {
            Token::Identifier(type_name) => match type_name.as_str() {
                "Integer" => Ok(Type::Integer),
                "Float" => Ok(Type::Float),
                "String" => Ok(Type::String),
                "Boolean" => Ok(Type::Boolean),
                _ => Ok(Type::Named(type_name)),
            },
            _ => Err(anyhow!("Expected type name")),
        }
    }
    
    fn parse_statement(&mut self) -> Result<Statement> {
        match &self.peek() {
            Token::Let => {
                self.advance(); // consume "Let"
                let name = match self.advance() {
                    Token::Identifier(name) => name,
                    _ => return Err(anyhow!("Expected variable name")),
                };
                self.consume(Token::Be)?;
                let value = self.parse_expression()?;
                Ok(Statement::Let { name, value })
            }
            Token::Set => {
                self.advance(); // consume "Set"
                let name = match self.advance() {
                    Token::Identifier(name) => name,
                    _ => return Err(anyhow!("Expected variable name")),
                };
                self.consume(Token::To)?;
                let value = self.parse_expression()?;
                Ok(Statement::Set { name, value })
            }
            Token::Return => {
                self.advance(); // consume "Return"
                let value = if self.check(&Token::End) {
                    None
                } else {
                    Some(self.parse_expression()?)
                };
                Ok(Statement::Return { value })
            }
            Token::Print => {
                self.advance(); // consume "Print"
                let message = self.parse_expression()?;
                Ok(Statement::Print { message })
            }
            Token::ReadFile => {
                self.advance(); // consume "ReadFile"
                let filename = self.parse_expression()?;
                self.consume(Token::Into)?;
                let target = match self.advance() {
                    Token::Identifier(name) => name,
                    _ => return Err(anyhow!("Expected variable name after 'into'")),
                };
                Ok(Statement::ReadFile { filename, target })
            }
            Token::WriteFile => {
                self.advance(); // consume "WriteFile"
                let content = self.parse_expression()?;
                self.consume(Token::To)?;
                let filename = self.parse_expression()?;
                Ok(Statement::WriteFile { filename, content })
            }
            Token::If => self.parse_if_statement(),
            Token::While => self.parse_while_statement(),
            Token::For => self.parse_for_statement(),
            Token::Inline => self.parse_inline_assembly(),
            _ => {
                let expr = self.parse_expression()?;
                Ok(Statement::Expression(expr))
            }
        }
    }
    
    fn parse_expression(&mut self) -> Result<Expression> {
        self.parse_comparison()
    }
    
    fn parse_additive(&mut self) -> Result<Expression> {
        let mut expr = self.parse_multiplicative()?;
        
        while self.check(&Token::Plus) || self.check(&Token::Minus) {
            let op = if self.check(&Token::Plus) {
                self.advance();
                BinOp::Add
            } else {
                self.advance();
                BinOp::Sub
            };
            let right = self.parse_multiplicative()?;
            expr = Expression::Binary {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_multiplicative(&mut self) -> Result<Expression> {
        let mut expr = self.parse_postfix()?;
        
        while self.check(&Token::Multiply) || self.check(&Token::Divide) {
            let op = if self.check(&Token::Multiply) {
                self.advance();
                BinOp::Mul
            } else {
                self.advance();
                BinOp::Div
            };
            let right = self.parse_postfix()?;
            expr = Expression::Binary {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_postfix(&mut self) -> Result<Expression> {
        let mut expr = self.parse_primary()?;

        loop {
            if self.check(&Token::Dot) {
                self.advance(); // consume '.'
                let field_name = match self.advance() {
                    Token::Identifier(name) => name,
                    _ => return Err(anyhow!("Expected field name after '.'")),
                };
                expr = Expression::FieldAccess {
                    object: Box::new(expr),
                    field: field_name,
                };
            } else {
                break;
            }
        }

        Ok(expr)
    }
    
    fn parse_constructor_fields(&mut self) -> Result<Vec<(String, Expression)>> {
        let mut fields = Vec::new();
        
        loop {
            // Parse field name
            let field_name = match self.advance() {
                Token::Identifier(name) => name,
                _ => return Err(anyhow!("Expected field name in constructor")),
            };
            
            // Expect "as"
            self.consume(Token::As)?;
            
            // Parse field value expression
            let field_value = self.parse_expression()?;
            
            fields.push((field_name, field_value));
            
            // Check for more fields (comma-separated)
            if !self.check(&Token::Comma) {
                break;
            }
            self.advance(); // consume comma
        }
        
        Ok(fields)
    }
    
    fn parse_if_statement(&mut self) -> Result<Statement> {
        self.consume(Token::If)?;
        let condition = self.parse_comparison()?;
        self.consume(Token::Colon)?;
        
        let mut then_body = Vec::new();
        while !self.check(&Token::Otherwise) && !self.check(&Token::End) {
            then_body.push(self.parse_statement()?);
        }
        
        let mut else_ifs = Vec::new();
        let mut else_body = None;
        
        while self.check(&Token::Otherwise) {
            self.advance(); // consume "Otherwise"
            
            if self.check(&Token::If) {
                // Otherwise if
                self.advance(); // consume "if"
                let else_if_condition = self.parse_comparison()?;
                self.consume(Token::Colon)?;
                
                let mut else_if_body = Vec::new();
                while !self.check(&Token::Otherwise) && !self.check(&Token::End) {
                    else_if_body.push(self.parse_statement()?);
                }
                
                else_ifs.push((else_if_condition, else_if_body));
            } else {
                // Otherwise (else)
                self.consume(Token::Colon)?;
                let mut else_statements = Vec::new();
                while !self.check(&Token::End) {
                    else_statements.push(self.parse_statement()?);
                }
                else_body = Some(else_statements);
                break;
            }
        }
        
        self.consume(Token::End)?;
        self.consume(Token::If)?;
        
        Ok(Statement::If {
            condition,
            then_body,
            else_ifs,
            else_body,
        })
    }
    
    fn parse_while_statement(&mut self) -> Result<Statement> {
        self.consume(Token::While)?;
        let condition = self.parse_comparison()?;
        self.consume(Token::Colon)?;
        
        let mut body = Vec::new();
        while !self.check(&Token::End) {
            body.push(self.parse_statement()?);
        }
        
        self.consume(Token::End)?;
        self.consume(Token::While)?;
        
        Ok(Statement::While { condition, body })
    }
    
    fn parse_for_statement(&mut self) -> Result<Statement> {
        self.consume(Token::For)?;
        self.consume(Token::Each)?;
        
        let variable = match self.advance() {
            Token::Identifier(name) => name,
            _ => return Err(anyhow!("Expected variable name in for each")),
        };
        
        self.consume(Token::In)?;
        let collection = self.parse_expression()?;
        self.consume(Token::Colon)?;
        
        let mut body = Vec::new();
        while !self.check(&Token::End) {
            body.push(self.parse_statement()?);
        }
        
        self.consume(Token::End)?;
        self.consume(Token::For)?;
        
        Ok(Statement::ForEach { variable, collection, body })
    }
    
    fn parse_comparison(&mut self) -> Result<Expression> {
        self.parse_logical_or()
    }
    
    fn parse_logical_or(&mut self) -> Result<Expression> {
        let mut expr = self.parse_logical_and()?;
        
        while self.check(&Token::Or) {
            self.advance(); // consume "or"
            let right = self.parse_logical_and()?;
            expr = Expression::Binary {
                left: Box::new(expr),
                op: BinOp::Or,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_logical_and(&mut self) -> Result<Expression> {
        let mut expr = self.parse_relational()?;
        
        while self.check(&Token::And) {
            self.advance(); // consume "and"
            let right = self.parse_relational()?;
            expr = Expression::Binary {
                left: Box::new(expr),
                op: BinOp::And,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_relational(&mut self) -> Result<Expression> {
        let mut expr = self.parse_additive()?;
        
        // Handle "is equal to", "is greater than", etc.
        if self.check(&Token::Is) {
            self.advance(); // consume "is"
            
            let op = if self.check(&Token::Equal) {
                self.advance(); // consume "equal"
                self.consume(Token::To)?; // consume "to"
                BinOp::Equal
            } else if self.check(&Token::Not) {
                self.advance(); // consume "not"
                self.consume(Token::Equal)?; // consume "equal"
                self.consume(Token::To)?; // consume "to"
                BinOp::NotEqual
            } else if self.check(&Token::Greater) {
                self.advance(); // consume "greater"
                self.consume(Token::Than)?; // consume "than"
                
                if self.check(&Token::Or) {
                    self.advance(); // consume "or"
                    self.consume(Token::Equal)?; // consume "equal"
                    self.consume(Token::To)?; // consume "to"
                    BinOp::GreaterOrEqual
                } else {
                    BinOp::Greater
                }
            } else if self.check(&Token::Less) {
                self.advance(); // consume "less"
                self.consume(Token::Than)?; // consume "than"
                
                if self.check(&Token::Or) {
                    self.advance(); // consume "or"
                    self.consume(Token::Equal)?; // consume "equal"
                    self.consume(Token::To)?; // consume "to"
                    BinOp::LessOrEqual
                } else {
                    BinOp::Less
                }
            } else {
                return Err(anyhow!("Expected comparison operator after 'is'"));
            };
            
            let right = self.parse_additive()?;
            expr = Expression::Binary {
                left: Box::new(expr),
                op,
                right: Box::new(right),
            };
        }
        
        Ok(expr)
    }
    
    fn parse_inline_assembly(&mut self) -> Result<Statement> {
        self.consume(Token::Inline)?;
        self.consume(Token::Assembly)?;
        self.consume(Token::Colon)?;
        
        let mut instructions = Vec::new();
        let mut output_constraints = Vec::new();
        let mut input_constraints = Vec::new();
        let mut clobbers = Vec::new();
        
        // Parse assembly instructions
        while !self.check(&Token::Colon) && !self.check(&Token::End) {
            if let Token::String(instruction) = self.advance() {
                instructions.push(instruction);
            } else if self.check(&Token::Colon) {
                break; // Start of constraints
            } else {
                return Err(anyhow!("Expected assembly instruction string"));
            }
        }
        
        // Parse constraints if present
        if self.check(&Token::Colon) {
            self.advance(); // consume first ':'
            
            // Parse output constraints
            if !self.check(&Token::Colon) {
                output_constraints = self.parse_constraints()?;
            }
            
            if self.check(&Token::Colon) {
                self.advance(); // consume second ':'
                
                // Parse input constraints
                if !self.check(&Token::Colon) {
                    input_constraints = self.parse_constraints()?;
                }
                
                if self.check(&Token::Colon) {
                    self.advance(); // consume third ':'
                    
                    // Parse clobber list
                    while !self.check(&Token::End) {
                        if let Token::String(clobber) = self.advance() {
                            clobbers.push(clobber);
                            if self.check(&Token::Comma) {
                                self.advance(); // consume comma
                            }
                        } else {
                            break;
                        }
                    }
                }
            }
        }
        
        self.consume(Token::End)?;
        self.consume(Token::Assembly)?;
        
        Ok(Statement::InlineAssembly {
            instructions,
            output_constraints,
            input_constraints,
            clobbers,
        })
    }
    
    fn parse_constraints(&mut self) -> Result<Vec<(String, String)>> {
        let mut constraints = Vec::new();
        
        // Parse constraint format: "constraint"(variable), "constraint"(variable), ...
        while !self.check(&Token::Colon) && !self.check(&Token::End) {
            if let Token::String(constraint) = self.advance() {
                // Expect '(' immediately after constraint string
                self.consume(Token::LeftParen)?;
                
                // Parse variable name
                let var_name = match self.advance() {
                    Token::Identifier(name) => name,
                    Token::Value => "value".to_string(), // Allow "value" as variable name in constraints
                    _ => return Err(anyhow!("Expected variable name in constraint")),
                };
                
                self.consume(Token::RightParen)?;
                
                constraints.push((constraint, var_name));
                
                if self.check(&Token::Comma) {
                    self.advance(); // consume comma
                } else {
                    break;
                }
            } else {
                break;
            }
        }
        
        Ok(constraints)
    }
    
    fn parse_primary(&mut self) -> Result<Expression> {
        match self.advance() {
            Token::Integer(n) => Ok(Expression::Integer(n)),
            Token::Float(f) => Ok(Expression::Float(f)),
            Token::String(s) => Ok(Expression::String(s)),
            Token::Boolean(b) => Ok(Expression::Boolean(b)),
            Token::A => {
                // Parse "a value of type TypeName" (constructor syntax)
                self.consume(Token::Value)?;
                self.consume(Token::Of)?;
                self.consume(Token::Type)?;

                let type_name = match self.advance() {
                    Token::Identifier(name) => name,
                    _ => return Err(anyhow!("Expected type name in constructor")),
                };

                // Check for field initialization
                let fields = if self.check(&Token::With) {
                    self.advance(); // consume "with"
                    self.parse_constructor_fields()?
                } else {
                    Vec::new()
                };

                Ok(Expression::Constructor { type_name, fields })
            }
            Token::Identifier(name) => {
                if self.check(&Token::LeftParen) {
                    self.advance(); // consume '('
                    let mut args = Vec::new();
                    
                    if !self.check(&Token::RightParen) {
                        loop {
                            args.push(self.parse_expression()?);
                            if !self.check(&Token::Comma) { break; }
                            self.advance(); // consume comma
                        }
                    }
                    
                    self.consume(Token::RightParen)?;
                    Ok(Expression::Call { name, args })
                } else {
                    Ok(Expression::Variable(name))
                }
            }
            Token::LeftParen => {
                let expr = self.parse_expression()?;
                self.consume(Token::RightParen)?;
                Ok(expr)
            }
            _ => Err(anyhow!("Unexpected token in expression")),
        }
    }
    
    fn advance(&mut self) -> Token {
        if !self.is_at_end() {
            self.pos += 1;
        }
        self.previous()
    }
    
    fn peek(&self) -> &Token {
        &self.tokens[self.pos]
    }
    
    fn previous(&self) -> Token {
        self.tokens[self.pos - 1].clone()
    }
    
    fn check(&self, token_type: &Token) -> bool {
        if self.is_at_end() {
            false
        } else {
            std::mem::discriminant(self.peek()) == std::mem::discriminant(token_type)
        }
    }
    
    fn consume(&mut self, expected: Token) -> Result<()> {
        if self.check(&expected) {
            self.advance();
            Ok(())
        } else {
            Err(anyhow!("Expected {:?}, found {:?}", expected, self.peek()))
        }
    }
    
    fn is_at_end(&self) -> bool {
        matches!(self.peek(), Token::Eof)
    }
}