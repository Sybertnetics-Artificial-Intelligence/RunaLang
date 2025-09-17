use crate::lexer::{Token, TokenType};

#[derive(Debug, Clone)]
pub enum AstNode {
    Program(Vec<AstNode>),
    LetStatement {
        variable: String,
        value: Box<AstNode>,
    },
    SetStatement {
        variable: String,
        value: Box<AstNode>,
    },
    DisplayStatement {
        value: Box<AstNode>,
    },
    NoteStatement {
        content: String,
    },
    ReturnStatement {
        value: Option<Box<AstNode>>,
    },
    IfStatement {
        condition: Box<AstNode>,
        then_block: Vec<AstNode>,
        else_block: Option<Vec<AstNode>>,
    },
    WhileStatement {
        condition: Box<AstNode>,
        body: Vec<AstNode>,
    },
    ProcessDefinition {
        name: String,
        parameters: Vec<Parameter>,
        return_type: Option<String>,
        body: Vec<AstNode>,
    },
    TypeDefinition {
        name: String,
        fields: Vec<Field>,
    },
    StructCreation {
        type_name: String,
        field_values: Vec<(String, AstNode)>,
    },
    FieldAccess {
        object: Box<AstNode>,
        field: String,
    },
    IndexAccess {
        object: Box<AstNode>,
        index: Box<AstNode>,
    },
    BinaryExpression {
        left: Box<AstNode>,
        operator: BinaryOperator,
        right: Box<AstNode>,
    },
    FunctionCall {
        name: String,
        arguments: Vec<AstNode>,
    },
    ListLiteral {
        elements: Vec<AstNode>,
    },
    IntegerLiteral(i64),
    StringLiteral(String),
    Identifier(String),
}

#[derive(Debug, Clone)]
pub struct Parameter {
    pub name: String,
    pub param_type: String,
}

#[derive(Debug, Clone)]
pub struct Field {
    pub name: String,
    pub field_type: String,
}

#[derive(Debug, Clone)]
pub enum BinaryOperator {
    Add,
    Subtract,
    Equal,
    NotEqual,
    LessThan,
    GreaterThan,
    LogicalOr,
    LogicalAnd,
}

pub struct Parser {
    tokens: Vec<Token>,
    current: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            current: 0,
        }
    }

    pub fn parse(&mut self) -> Result<AstNode, String> {
        let mut statements = Vec::new();

        while !self.is_at_end() {
            let stmt = self.parse_statement()?;
            statements.push(stmt);
        }

        Ok(AstNode::Program(statements))
    }

    fn parse_statement(&mut self) -> Result<AstNode, String> {
        match &self.current_token().token_type {
            TokenType::Let => self.parse_let_statement(),
            TokenType::Set => self.parse_set_statement(),
            TokenType::Display => self.parse_display_statement(),
            TokenType::Note => self.parse_note_statement(),
            TokenType::Return => self.parse_return_statement(),
            TokenType::If => self.parse_if_statement(),
            TokenType::While => self.parse_while_statement(),
            TokenType::Process => self.parse_process_definition(),
            TokenType::Type => self.parse_type_definition(),
            TokenType::Identifier(_) => {
                // Could be a function call statement
                let expr = self.parse_expression()?;
                Ok(expr)
            }
            TokenType::Eof => Err("Unexpected end of file".to_string()),
            _ => Err(format!("Unexpected token: {:?}", self.current_token().token_type)),
        }
    }

    fn parse_let_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'Let'
        self.expect_token(TokenType::Let)?;

        // Get variable name
        let variable = match &self.current_token().token_type {
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();
                name
            }
            _ => return Err("Expected identifier after 'Let'".to_string()),
        };

        // Consume 'be'
        self.expect_token(TokenType::Be)?;

        // Parse value expression
        let value = self.parse_expression()?;

        Ok(AstNode::LetStatement {
            variable,
            value: Box::new(value),
        })
    }

    fn parse_set_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'Set'
        self.expect_token(TokenType::Set)?;

        // Get variable name
        let variable = match &self.current_token().token_type {
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();
                name
            }
            _ => return Err("Expected identifier after 'Set'".to_string()),
        };

        // Consume 'to'
        self.expect_token(TokenType::To)?;

        // Parse value expression
        let value = self.parse_expression()?;

        Ok(AstNode::SetStatement {
            variable,
            value: Box::new(value),
        })
    }

    fn parse_display_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'Display'
        self.expect_token(TokenType::Display)?;

        // Parse value expression
        let value = self.parse_expression()?;

        Ok(AstNode::DisplayStatement {
            value: Box::new(value),
        })
    }

    fn parse_note_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'Note'
        self.expect_token(TokenType::Note)?;

        // Expect colon
        self.expect_token(TokenType::Colon)?;

        // Read all tokens until we reach the end of the current line
        let mut content = String::new();
        let note_line = self.current_token().line;

        while !self.is_at_end() && self.current_token().line == note_line {
            match &self.current_token().token_type {
                TokenType::StringLiteral(s) => {
                    if !content.is_empty() { content.push(' '); }
                    content.push_str(s);
                    self.advance();
                }
                TokenType::Identifier(s) => {
                    if !content.is_empty() { content.push(' '); }
                    content.push_str(s);
                    self.advance();
                }
                TokenType::Type => {
                    if !content.is_empty() { content.push(' '); }
                    content.push_str("Type");
                    self.advance();
                }
                TokenType::If => {
                    if !content.is_empty() { content.push(' '); }
                    content.push_str("If");
                    self.advance();
                }
                TokenType::While => {
                    if !content.is_empty() { content.push(' '); }
                    content.push_str("While");
                    self.advance();
                }
                TokenType::Process => {
                    if !content.is_empty() { content.push(' '); }
                    content.push_str("Process");
                    self.advance();
                }
                TokenType::Eof => {
                    break;
                }
                _ => {
                    // For other tokens, convert to string representation
                    self.advance();
                }
            }
        }

        Ok(AstNode::NoteStatement { content })
    }

    fn parse_return_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'Return'
        self.expect_token(TokenType::Return)?;

        // Check if there's a value to return
        let value = if matches!(self.current_token().token_type, TokenType::Eof) {
            None
        } else {
            Some(Box::new(self.parse_expression()?))
        };

        Ok(AstNode::ReturnStatement { value })
    }

    fn parse_if_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'If'
        self.expect_token(TokenType::If)?;

        // Parse condition
        let condition = self.parse_expression()?;

        // Expect colon
        self.expect_token(TokenType::Colon)?;

        // Parse then block
        let mut then_block = Vec::new();
        while !matches!(self.current_token().token_type, TokenType::Otherwise | TokenType::End | TokenType::Eof) {
            let stmt = self.parse_statement()?;
            then_block.push(stmt);
        }

        // Parse else block if present
        let else_block = if matches!(self.current_token().token_type, TokenType::Otherwise) {
            self.advance(); // consume 'Otherwise'
            // Expect colon after Otherwise
            self.expect_token(TokenType::Colon)?;
            let mut statements = Vec::new();
            while !matches!(self.current_token().token_type, TokenType::End | TokenType::Eof) {
                let stmt = self.parse_statement()?;
                statements.push(stmt);
            }
            Some(statements)
        } else {
            None
        };

        // Consume 'End If'
        if matches!(self.current_token().token_type, TokenType::End) {
            self.advance(); // consume 'End'
            // Expect 'If' after 'End'
            self.expect_token(TokenType::If)?;
        }

        Ok(AstNode::IfStatement {
            condition: Box::new(condition),
            then_block,
            else_block,
        })
    }

    fn parse_while_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'While'
        self.expect_token(TokenType::While)?;

        // Parse condition
        let condition = self.parse_expression()?;

        // Expect colon
        self.expect_token(TokenType::Colon)?;

        // Parse loop body
        let mut body = Vec::new();
        while !matches!(self.current_token().token_type, TokenType::End | TokenType::Eof) {
            let stmt = self.parse_statement()?;
            body.push(stmt);
        }

        // Consume 'End'
        if matches!(self.current_token().token_type, TokenType::End) {
            self.advance();
            // Optionally consume 'While' after 'End' for proper syntax validation
            if matches!(self.current_token().token_type, TokenType::While) {
                self.advance();
            }
            // Note: We allow both "End" and "End While" for flexibility in the bootstrap compiler
        }

        Ok(AstNode::WhileStatement {
            condition: Box::new(condition),
            body,
        })
    }

    fn parse_process_definition(&mut self) -> Result<AstNode, String> {
        // Consume 'Process'
        self.expect_token(TokenType::Process)?;

        // Consume 'called'
        self.expect_token(TokenType::Called)?;

        // Get process name (should be a string literal)
        let name = match &self.current_token().token_type {
            TokenType::StringLiteral(name) => {
                let name = name.clone();
                self.advance();
                name
            }
            TokenType::Identifier(name) => {
                // For now, also accept identifiers
                let name = name.clone();
                self.advance();
                name
            }
            _ => return Err("Expected process name after 'called'".to_string()),
        };

        // Check if we have 'that' (for parameters/returns) or go directly to colon for minimal syntax
        let mut parameters = Vec::new();
        let return_type = if matches!(self.current_token().token_type, TokenType::That) {
            // Consume 'that'
            self.advance();

            // Parse parameters - check for 'takes' or directly 'returns'
            if matches!(self.current_token().token_type, TokenType::Takes) {
                // Consume 'takes'
                self.advance();

                // Parse parameter list (at least one parameter expected after 'takes')
                loop {
                    // Get parameter name
                    let param_name = match &self.current_token().token_type {
                        TokenType::Identifier(name) => {
                            let name = name.clone();
                            self.advance();
                            name
                        }
                        _ => return Err("Expected parameter name after 'takes'".to_string()),
                    };

                    // Expect 'as'
                    self.expect_token(TokenType::As)?;

                    // Get parameter type
                    let param_type = match &self.current_token().token_type {
                        TokenType::Identifier(type_name) => {
                            let type_name = type_name.clone();
                            self.advance();
                            type_name
                        }
                        _ => return Err("Expected parameter type after 'as'".to_string()),
                    };

                    parameters.push(Parameter {
                        name: param_name,
                        param_type,
                    });

                    // Check for comma (more parameters) or break
                    if matches!(self.current_token().token_type, TokenType::Comma) {
                        self.advance(); // consume comma
                        continue;
                    } else {
                        break;
                    }
                }
            }

            // Parse optional return type after 'that'
            if matches!(self.current_token().token_type, TokenType::Returns) {
                // Consume 'returns'
                self.advance();

                // Get return type
                match &self.current_token().token_type {
                    TokenType::Identifier(type_name) => {
                        let type_name = type_name.clone();
                        self.advance();
                        Some(type_name)
                    }
                    _ => None, // Optional return type after 'returns'
                }
            } else {
                None // No 'returns' keyword means void function
            }
        } else {
            None // No 'that' means completely minimal function (no params, no return)
        };

        // Expect colon
        self.expect_token(TokenType::Colon)?;

        // Parse function body
        let mut body = Vec::new();
        while !matches!(self.current_token().token_type, TokenType::End | TokenType::Eof) {
            let stmt = self.parse_statement()?;
            body.push(stmt);
        }

        // Consume 'End'
        if matches!(self.current_token().token_type, TokenType::End) {
            self.advance();
            // Optionally consume 'Process' after 'End'
            if matches!(self.current_token().token_type, TokenType::Process) {
                self.advance();
            }
        }

        Ok(AstNode::ProcessDefinition {
            name,
            parameters,
            return_type,
            body,
        })
    }

    fn parse_type_definition(&mut self) -> Result<AstNode, String> {
        // Consume 'Type'
        self.expect_token(TokenType::Type)?;

        // Consume 'called'
        self.expect_token(TokenType::Called)?;

        // Get type name (should be a string literal or identifier)
        let name = match &self.current_token().token_type {
            TokenType::StringLiteral(name) => {
                let name = name.clone();
                self.advance();
                name
            }
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();
                name
            }
            _ => return Err("Expected type name after 'called'".to_string()),
        };

        // Expect colon
        self.expect_token(TokenType::Colon)?;

        // Parse fields
        let mut fields = Vec::new();
        while !matches!(self.current_token().token_type, TokenType::End | TokenType::Eof) {
            // Get field name
            let field_name = match &self.current_token().token_type {
                TokenType::Identifier(name) => {
                    let name = name.clone();
                    self.advance();
                    name
                }
                _ => return Err("Expected field name in type definition".to_string()),
            };

            // Expect 'as'
            self.expect_token(TokenType::As)?;

            // Get field type
            let field_type = match &self.current_token().token_type {
                TokenType::Identifier(type_name) => {
                    let type_name = type_name.clone();
                    self.advance();
                    type_name
                }
                _ => return Err("Expected field type after 'as'".to_string()),
            };

            fields.push(Field {
                name: field_name,
                field_type,
            });
        }

        // Consume 'End'
        if matches!(self.current_token().token_type, TokenType::End) {
            self.advance();
            // Optionally consume 'Type' after 'End'
            if matches!(self.current_token().token_type, TokenType::Type) {
                self.advance();
            }
        }

        Ok(AstNode::TypeDefinition {
            name,
            fields,
        })
    }

    fn parse_expression(&mut self) -> Result<AstNode, String> {
        self.parse_logical_or_expression()
    }

    fn parse_logical_or_expression(&mut self) -> Result<AstNode, String> {
        let mut left = self.parse_logical_and_expression()?;

        while matches!(self.current_token().token_type, TokenType::Or) {
            self.advance(); // consume 'Or'
            let right = self.parse_logical_and_expression()?;

            left = AstNode::BinaryExpression {
                left: Box::new(left),
                operator: BinaryOperator::LogicalOr,
                right: Box::new(right),
            };
        }

        Ok(left)
    }

    fn parse_logical_and_expression(&mut self) -> Result<AstNode, String> {
        let mut left = self.parse_comparison_expression()?;

        while matches!(self.current_token().token_type, TokenType::And) {
            self.advance(); // consume 'And'
            let right = self.parse_comparison_expression()?;

            left = AstNode::BinaryExpression {
                left: Box::new(left),
                operator: BinaryOperator::LogicalAnd,
                right: Box::new(right),
            };
        }

        Ok(left)
    }

    fn parse_comparison_expression(&mut self) -> Result<AstNode, String> {
        let mut left = self.parse_additive_expression()?;

        while matches!(self.current_token().token_type,
                      TokenType::IsEqualTo | TokenType::IsNotEqualTo |
                      TokenType::IsLessThan | TokenType::IsGreaterThan) {
            let operator = match self.current_token().token_type {
                TokenType::IsEqualTo => BinaryOperator::Equal,
                TokenType::IsNotEqualTo => BinaryOperator::NotEqual,
                TokenType::IsLessThan => BinaryOperator::LessThan,
                TokenType::IsGreaterThan => BinaryOperator::GreaterThan,
                _ => unreachable!(),
            };
            self.advance();

            let right = self.parse_additive_expression()?;

            left = AstNode::BinaryExpression {
                left: Box::new(left),
                operator,
                right: Box::new(right),
            };
        }

        Ok(left)
    }

    fn parse_additive_expression(&mut self) -> Result<AstNode, String> {
        let mut left = self.parse_primary_expression()?;

        while matches!(self.current_token().token_type, TokenType::Plus | TokenType::Minus) {
            let operator = match self.current_token().token_type {
                TokenType::Plus => BinaryOperator::Add,
                TokenType::Minus => BinaryOperator::Subtract,
                _ => unreachable!(),
            };
            self.advance();

            let right = self.parse_primary_expression()?;

            left = AstNode::BinaryExpression {
                left: Box::new(left),
                operator,
                right: Box::new(right),
            };
        }

        Ok(left)
    }

    fn parse_primary_expression(&mut self) -> Result<AstNode, String> {
        match &self.current_token().token_type {
            TokenType::Integer(value) => {
                let value = *value;
                self.advance();
                Ok(AstNode::IntegerLiteral(value))
            }
            TokenType::StringLiteral(value) => {
                let value = value.clone();
                self.advance();
                Ok(AstNode::StringLiteral(value))
            }
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();

                // Check for list literal syntax: "a list containing..."
                if name == "a" && matches!(self.current_token().token_type, TokenType::List) {
                    return self.parse_list_literal();
                }

                // Check for struct creation syntax: "a value of type TypeName"
                if name == "a" && matches!(self.current_token().token_type, TokenType::Identifier(ref word) if word == "value") {
                    return self.parse_struct_creation();
                }

                // Check if this is a function call (identifier followed by left paren)
                if matches!(self.current_token().token_type, TokenType::LeftParen) {
                    self.advance(); // consume '('

                    let mut arguments = Vec::new();

                    // Parse arguments if any
                    if !matches!(self.current_token().token_type, TokenType::RightParen) {
                        loop {
                            let arg = self.parse_expression()?;
                            arguments.push(arg);

                            if matches!(self.current_token().token_type, TokenType::Comma) {
                                self.advance(); // consume comma
                                continue;
                            } else {
                                break;
                            }
                        }
                    }

                    // Expect closing parenthesis
                    self.expect_token(TokenType::RightParen)?;

                    Ok(AstNode::FunctionCall { name, arguments })
                } else {
                    // Check for field access (dot notation) and index access (bracket notation)
                    let mut current_expr = AstNode::Identifier(name);

                    while matches!(self.current_token().token_type, TokenType::Dot | TokenType::LeftBracket) {
                        match self.current_token().token_type {
                            TokenType::Dot => {
                                self.advance(); // consume dot

                                // Get field name
                                let field_name = match &self.current_token().token_type {
                                    TokenType::Identifier(field) => {
                                        let field = field.clone();
                                        self.advance();
                                        field
                                    }
                                    _ => return Err("Expected field name after '.'".to_string()),
                                };

                                current_expr = AstNode::FieldAccess {
                                    object: Box::new(current_expr),
                                    field: field_name,
                                };
                            }
                            TokenType::LeftBracket => {
                                self.advance(); // consume '['

                                // Parse index expression
                                let index_expr = self.parse_expression()?;

                                // Expect closing bracket
                                self.expect_token(TokenType::RightBracket)?;

                                current_expr = AstNode::IndexAccess {
                                    object: Box::new(current_expr),
                                    index: Box::new(index_expr),
                                };
                            }
                            _ => break,
                        }
                    }

                    Ok(current_expr)
                }
            }
            _ => Err(format!("Unexpected token in expression: {:?}", self.current_token().token_type)),
        }
    }

    fn parse_list_literal(&mut self) -> Result<AstNode, String> {
        // We already consumed "a", now expect "list"
        self.expect_token(TokenType::List)?;

        // Expect "containing"
        self.expect_token(TokenType::Containing)?;

        let mut elements = Vec::new();

        // Parse the first element
        let first_element = self.parse_expression()?;
        elements.push(first_element);

        // Check for more elements
        loop {
            if matches!(self.current_token().token_type, TokenType::Comma) {
                self.advance(); // consume comma

                // Check if this is the last element with "and"
                if matches!(self.current_token().token_type, TokenType::And) {
                    self.advance(); // consume "and"
                    let last_element = self.parse_expression()?;
                    elements.push(last_element);
                    break;
                } else {
                    let element = self.parse_expression()?;
                    elements.push(element);
                }
            } else if matches!(self.current_token().token_type, TokenType::And) {
                // Handle direct "and" for two-element lists
                self.advance(); // consume "and"
                let last_element = self.parse_expression()?;
                elements.push(last_element);
                break;
            } else {
                // No more elements
                break;
            }
        }

        Ok(AstNode::ListLiteral { elements })
    }

    fn parse_struct_creation(&mut self) -> Result<AstNode, String> {
        // We already consumed "a", now expect "value"
        self.expect_token(TokenType::Identifier("value".to_string()))?;

        // Expect "of"
        if !matches!(self.current_token().token_type, TokenType::Identifier(ref word) if word == "of") {
            return Err("Expected 'of' after 'value'".to_string());
        }
        self.advance();

        // Expect "type"
        if !matches!(self.current_token().token_type, TokenType::Identifier(ref word) if word == "type") {
            return Err("Expected 'type' after 'of'".to_string());
        }
        self.advance();

        // Get type name
        let type_name = match &self.current_token().token_type {
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();
                name
            }
            _ => return Err("Expected type name after 'type'".to_string()),
        };

        // Check for optional field initialization with "with"
        let mut field_values = Vec::new();
        if matches!(self.current_token().token_type, TokenType::Identifier(ref word) if word == "with") {
            self.advance(); // consume "with"

            // Parse field assignments
            loop {
                // Get field name
                let field_name = match &self.current_token().token_type {
                    TokenType::Identifier(name) => {
                        let name = name.clone();
                        self.advance();
                        name
                    }
                    _ => return Err("Expected field name in struct creation".to_string()),
                };

                // Expect 'as'
                self.expect_token(TokenType::As)?;

                // Get field value
                let field_value = self.parse_expression()?;

                field_values.push((field_name, field_value));

                // Check for comma (more fields) or break
                if matches!(self.current_token().token_type, TokenType::Comma) {
                    self.advance(); // consume comma
                    continue;
                } else {
                    break;
                }
            }
        }

        Ok(AstNode::StructCreation {
            type_name,
            field_values,
        })
    }

    fn expect_token(&mut self, expected: TokenType) -> Result<(), String> {
        if std::mem::discriminant(&self.current_token().token_type) == std::mem::discriminant(&expected) {
            self.advance();
            Ok(())
        } else {
            Err(format!("Expected {:?}, found {:?}", expected, self.current_token().token_type))
        }
    }

    fn current_token(&self) -> &Token {
        if self.current < self.tokens.len() {
            &self.tokens[self.current]
        } else {
            &self.tokens[self.tokens.len() - 1] // EOF token
        }
    }

    fn advance(&mut self) {
        if self.current < self.tokens.len() - 1 {
            self.current += 1;
        }
    }

    fn is_at_end(&self) -> bool {
        matches!(self.current_token().token_type, TokenType::Eof)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::Lexer;

    #[test]
    fn test_let_statement() {
        let mut lexer = Lexer::new("Let x be 42");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::LetStatement { variable, value } => {
                        assert_eq!(variable, "x");
                        match value.as_ref() {
                            AstNode::IntegerLiteral(42) => {},
                            _ => panic!("Expected integer literal 42"),
                        }
                    }
                    _ => panic!("Expected let statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_print_statement() {
        let mut lexer = Lexer::new("Print x");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::PrintStatement { value } => {
                        match value.as_ref() {
                            AstNode::Identifier(name) => assert_eq!(name, "x"),
                            _ => panic!("Expected identifier 'x'"),
                        }
                    }
                    _ => panic!("Expected print statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_multiple_statements() {
        let mut lexer = Lexer::new("Let x be 42\nPrint x");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 2);
                // First statement: Let x be 42
                match &stmts[0] {
                    AstNode::LetStatement { variable, .. } => {
                        assert_eq!(variable, "x");
                    }
                    _ => panic!("Expected let statement"),
                }
                // Second statement: Print x
                match &stmts[1] {
                    AstNode::PrintStatement { .. } => {},
                    _ => panic!("Expected print statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_arithmetic_expression() {
        let mut lexer = Lexer::new("Let x be 1 plus 2");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::LetStatement { variable, value } => {
                        assert_eq!(variable, "x");
                        match value.as_ref() {
                            AstNode::BinaryExpression { left, operator, right } => {
                                match left.as_ref() {
                                    AstNode::IntegerLiteral(1) => {},
                                    _ => panic!("Expected left operand to be 1"),
                                }
                                match operator {
                                    BinaryOperator::Add => {},
                                    _ => panic!("Expected addition operator"),
                                }
                                match right.as_ref() {
                                    AstNode::IntegerLiteral(2) => {},
                                    _ => panic!("Expected right operand to be 2"),
                                }
                            }
                            _ => panic!("Expected binary expression"),
                        }
                    }
                    _ => panic!("Expected let statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_chained_arithmetic() {
        let mut lexer = Lexer::new("Let x be 1 plus 2 minus 3");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::LetStatement { value, .. } => {
                        // Should parse as ((1 + 2) - 3)
                        match value.as_ref() {
                            AstNode::BinaryExpression { left, operator: BinaryOperator::Subtract, right } => {
                                match left.as_ref() {
                                    AstNode::BinaryExpression { operator: BinaryOperator::Add, .. } => {},
                                    _ => panic!("Expected left side to be addition"),
                                }
                                match right.as_ref() {
                                    AstNode::IntegerLiteral(3) => {},
                                    _ => panic!("Expected right operand to be 3"),
                                }
                            }
                            _ => panic!("Expected binary expression for subtraction"),
                        }
                    }
                    _ => panic!("Expected let statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_if_statement() {
        let mut lexer = Lexer::new("If x is equal to 5:\nPrint 1\nEnd If");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::IfStatement { condition, then_block, else_block } => {
                        // Check condition: x is equal to 5
                        match condition.as_ref() {
                            AstNode::BinaryExpression { operator: BinaryOperator::Equal, .. } => {},
                            _ => panic!("Expected equality comparison"),
                        }
                        // Check then block
                        assert_eq!(then_block.len(), 1);
                        match &then_block[0] {
                            AstNode::PrintStatement { .. } => {},
                            _ => panic!("Expected print statement in then block"),
                        }
                        // Check no else block
                        assert!(else_block.is_none());
                    }
                    _ => panic!("Expected if statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_if_else_statement() {
        let mut lexer = Lexer::new("If x is equal to 5:\nPrint 1\nOtherwise:\nPrint 2\nEnd If");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::IfStatement { then_block, else_block, .. } => {
                        assert_eq!(then_block.len(), 1);
                        assert!(else_block.is_some());
                        let else_stmts = else_block.as_ref().unwrap();
                        assert_eq!(else_stmts.len(), 1);
                    }
                    _ => panic!("Expected if statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_process_definition_simple() {
        let mut lexer = Lexer::new("Process called \"add\" that takes x as Integer, y as Integer returns Integer:\nLet result be x plus y\nPrint result\nEnd");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::ProcessDefinition { name, parameters, return_type, body } => {
                        assert_eq!(name, "add");
                        assert_eq!(parameters.len(), 2);
                        assert_eq!(parameters[0].name, "x");
                        assert_eq!(parameters[0].param_type, "Integer");
                        assert_eq!(parameters[1].name, "y");
                        assert_eq!(parameters[1].param_type, "Integer");
                        assert_eq!(return_type.as_ref().unwrap(), "Integer");
                        assert_eq!(body.len(), 2);
                    }
                    _ => panic!("Expected process definition"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_process_definition_no_params() {
        let mut lexer = Lexer::new("Process called greet that takes returns String:\nPrint \"Hello\"\nEnd");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::ProcessDefinition { name, parameters, return_type, body } => {
                        assert_eq!(name, "greet");
                        assert_eq!(parameters.len(), 0);
                        assert_eq!(return_type.as_ref().unwrap(), "String");
                        assert_eq!(body.len(), 1);
                    }
                    _ => panic!("Expected process definition"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_string_literal() {
        let mut lexer = Lexer::new("Print \"Hello, World!\"");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::PrintStatement { value } => {
                        match value.as_ref() {
                            AstNode::StringLiteral(text) => assert_eq!(text, "Hello, World!"),
                            _ => panic!("Expected string literal"),
                        }
                    }
                    _ => panic!("Expected print statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_function_call_no_args() {
        let mut lexer = Lexer::new("Print greet()");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::PrintStatement { value } => {
                        match value.as_ref() {
                            AstNode::FunctionCall { name, arguments } => {
                                assert_eq!(name, "greet");
                                assert_eq!(arguments.len(), 0);
                            }
                            _ => panic!("Expected function call"),
                        }
                    }
                    _ => panic!("Expected print statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_function_call_with_args() {
        let mut lexer = Lexer::new("Let result be add(5, 3)");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::LetStatement { variable, value } => {
                        assert_eq!(variable, "result");
                        match value.as_ref() {
                            AstNode::FunctionCall { name, arguments } => {
                                assert_eq!(name, "add");
                                assert_eq!(arguments.len(), 2);
                                match &arguments[0] {
                                    AstNode::IntegerLiteral(5) => {},
                                    _ => panic!("Expected first argument to be 5"),
                                }
                                match &arguments[1] {
                                    AstNode::IntegerLiteral(3) => {},
                                    _ => panic!("Expected second argument to be 3"),
                                }
                            }
                            _ => panic!("Expected function call"),
                        }
                    }
                    _ => panic!("Expected let statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_while_statement() {
        let mut lexer = Lexer::new("While x is less than 5:\nLet x be x plus 1\nPrint x\nEnd");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::WhileStatement { condition, body } => {
                        // Check condition: x is less than 5
                        match condition.as_ref() {
                            AstNode::BinaryExpression { operator: BinaryOperator::LessThan, .. } => {},
                            _ => panic!("Expected less than comparison"),
                        }
                        // Check body has 2 statements
                        assert_eq!(body.len(), 2);
                        match &body[0] {
                            AstNode::LetStatement { .. } => {},
                            _ => panic!("Expected let statement in while body"),
                        }
                        match &body[1] {
                            AstNode::PrintStatement { .. } => {},
                            _ => panic!("Expected print statement in while body"),
                        }
                    }
                    _ => panic!("Expected while statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_simple_list_literal() {
        let mut lexer = Lexer::new("Let x be a list containing 1, 2, and 3");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::LetStatement { variable, value } => {
                        assert_eq!(variable, "x");
                        match value.as_ref() {
                            AstNode::ListLiteral { elements } => {
                                assert_eq!(elements.len(), 3);
                                match &elements[0] {
                                    AstNode::IntegerLiteral(val) => assert_eq!(*val, 1),
                                    _ => panic!("Expected integer literal"),
                                }
                                match &elements[1] {
                                    AstNode::IntegerLiteral(val) => assert_eq!(*val, 2),
                                    _ => panic!("Expected integer literal"),
                                }
                                match &elements[2] {
                                    AstNode::IntegerLiteral(val) => assert_eq!(*val, 3),
                                    _ => panic!("Expected integer literal"),
                                }
                            }
                            _ => panic!("Expected list literal"),
                        }
                    }
                    _ => panic!("Expected let statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }

    #[test]
    fn test_list_literal_two_elements() {
        let mut lexer = Lexer::new("Print a list containing 5 and 10");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        match ast {
            AstNode::Program(ref stmts) => {
                assert_eq!(stmts.len(), 1);
                match &stmts[0] {
                    AstNode::PrintStatement { value } => {
                        match value.as_ref() {
                            AstNode::ListLiteral { elements } => {
                                assert_eq!(elements.len(), 2);
                                match &elements[0] {
                                    AstNode::IntegerLiteral(val) => assert_eq!(*val, 5),
                                    _ => panic!("Expected integer literal"),
                                }
                                match &elements[1] {
                                    AstNode::IntegerLiteral(val) => assert_eq!(*val, 10),
                                    _ => panic!("Expected integer literal"),
                                }
                            }
                            _ => panic!("Expected list literal"),
                        }
                    }
                    _ => panic!("Expected print statement"),
                }
            }
            _ => panic!("Expected program node"),
        }
    }
}