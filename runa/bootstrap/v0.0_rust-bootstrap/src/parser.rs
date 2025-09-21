// Minimal Viable Parser for Runa Bootstrap
// Only supports the MVL subset - brutally simple

use crate::lexer::{Lexer, TokenType};

#[derive(Debug, Clone)]
pub enum AstNode {
    // Program root
    Program(Vec<AstNode>),

    // Definitions
    FunctionDef {
        name: String,
        params: Vec<(String, String)>, // (name, type)
        return_type: String,
        body: Vec<AstNode>,
    },
    StructDef {
        name: String,
        fields: Vec<(String, String)>, // (name, type)
    },

    // Statements
    LetStatement {
        name: String,
        value: Box<AstNode>,
    },
    IfStatement {
        condition: Box<AstNode>,
        then_branch: Vec<AstNode>,
        else_branch: Option<Vec<AstNode>>,
    },
    WhileStatement {
        condition: Box<AstNode>,
        body: Vec<AstNode>,
    },
    ReturnStatement {
        value: Box<AstNode>,
    },
    ExpressionStatement {
        expr: Box<AstNode>,
    },

    // Expressions
    IntegerLiteral(i64),
    StringLiteral(String),
    Identifier(String),
    FunctionCall {
        name: String,
        args: Vec<AstNode>,
    },
    FieldAccess {
        object: Box<AstNode>,
        field: String,
    },
    ListLiteral {
        elements: Vec<AstNode>,
    },

    // Conditions (for If/While)
    Comparison {
        left: Box<AstNode>,
        op: ComparisonOp,
        right: Box<AstNode>,
    },
}

#[derive(Debug, Clone)]
pub enum ComparisonOp {
    Equal,
    LessThan,
    GreaterThan,
}

pub struct Parser {
    tokens: Vec<TokenType>,
    current: usize,
}

impl Parser {
    pub fn new(tokens: Vec<TokenType>) -> Self {
        Parser {
            tokens,
            current: 0,
        }
    }

    fn peek(&self) -> &TokenType {
        self.tokens.get(self.current).unwrap_or(&TokenType::Eof)
    }

    fn advance(&mut self) -> TokenType {
        let token = self.peek().clone();
        if !matches!(token, TokenType::Eof) {
            self.current += 1;
        }
        token
    }

    fn expect(&mut self, expected: TokenType) -> Result<(), String> {
        let token = self.advance();
        if std::mem::discriminant(&token) != std::mem::discriminant(&expected) {
            return Err(format!("Expected {:?}, got {:?}", expected, token));
        }
        Ok(())
    }

    fn skip_newlines(&mut self) {
        while matches!(self.peek(), TokenType::Newline) {
            self.advance();
        }
    }

    pub fn parse(&mut self) -> Result<AstNode, String> {
        let mut items = Vec::new();

        while !matches!(self.peek(), TokenType::Eof) {
            self.skip_newlines();

            match self.peek() {
                TokenType::Process => items.push(self.parse_function()?),
                TokenType::Type => items.push(self.parse_struct()?),
                TokenType::Eof => break,
                _ => items.push(self.parse_statement()?),
            }

            self.skip_newlines();
        }

        Ok(AstNode::Program(items))
    }

    fn parse_function(&mut self) -> Result<AstNode, String> {
        // Process called "name" takes x as Type, y as Type returns Type:
        self.expect(TokenType::Process)?;
        self.expect(TokenType::Called)?;

        let name = match self.advance() {
            TokenType::String(s) => s,
            _ => return Err("Expected function name string".to_string()),
        };

        let mut params = Vec::new();

        // Check for parameters
        if matches!(self.peek(), TokenType::Takes) {
            self.advance(); // takes

            // Parse parameters
            loop {
                let param_name = match self.advance() {
                    TokenType::Identifier(s) => s,
                    _ => break,
                };

                self.expect(TokenType::As)?;

                let param_type = match self.advance() {
                    TokenType::Identifier(s) => s,
                    _ => return Err("Expected parameter type".to_string()),
                };

                params.push((param_name, param_type));

                if !matches!(self.peek(), TokenType::Comma) {
                    break;
                }
                self.advance(); // comma
            }
        }

        self.expect(TokenType::Returns)?;

        let return_type = match self.advance() {
            TokenType::Identifier(s) => s,
            _ => return Err("Expected return type".to_string()),
        };

        self.expect(TokenType::Colon)?;
        self.skip_newlines();

        // Parse body until End Process
        let mut body = Vec::new();
        while !matches!(self.peek(), TokenType::End) {
            body.push(self.parse_statement()?);
            self.skip_newlines();
        }

        self.expect(TokenType::End)?;
        self.expect(TokenType::Process)?;

        Ok(AstNode::FunctionDef {
            name,
            params,
            return_type,
            body,
        })
    }

    fn parse_struct(&mut self) -> Result<AstNode, String> {
        // Type called "Name":
        //     field as Type
        // End Type
        self.expect(TokenType::Type)?;
        self.expect(TokenType::Called)?;

        let name = match self.advance() {
            TokenType::String(s) => s,
            _ => return Err("Expected struct name string".to_string()),
        };

        self.expect(TokenType::Colon)?;
        self.skip_newlines();

        let mut fields = Vec::new();

        while !matches!(self.peek(), TokenType::End) {
            let field_name = match self.advance() {
                TokenType::Identifier(s) => s,
                _ => break,
            };

            self.expect(TokenType::As)?;

            let field_type = match self.advance() {
                TokenType::Identifier(s) => s,
                _ => return Err("Expected field type".to_string()),
            };

            fields.push((field_name, field_type));
            self.skip_newlines();
        }

        self.expect(TokenType::End)?;
        self.expect(TokenType::Type)?;

        Ok(AstNode::StructDef { name, fields })
    }

    fn parse_statement(&mut self) -> Result<AstNode, String> {
        match self.peek() {
            TokenType::Let => self.parse_let(),
            TokenType::If => self.parse_if(),
            TokenType::While => self.parse_while(),
            TokenType::Return => self.parse_return(),
            _ => {
                // Expression statement (function call)
                let expr = self.parse_expression()?;
                Ok(AstNode::ExpressionStatement { expr: Box::new(expr) })
            }
        }
    }

    fn parse_let(&mut self) -> Result<AstNode, String> {
        // Let name be value
        self.expect(TokenType::Let)?;

        let name = match self.advance() {
            TokenType::Identifier(s) => s,
            _ => return Err("Expected variable name".to_string()),
        };

        self.expect(TokenType::Be)?;

        // Check for list literal
        if matches!(self.peek(), TokenType::Identifier(s) if s == "a") {
            self.advance(); // 'a'
            if matches!(self.peek(), TokenType::Identifier(s) if s == "list") {
                self.advance(); // 'list'
                if matches!(self.peek(), TokenType::Identifier(s) if s == "containing") {
                    self.advance(); // 'containing'
                    let elements = self.parse_list_elements()?;
                    return Ok(AstNode::LetStatement {
                        name,
                        value: Box::new(AstNode::ListLiteral { elements }),
                    });
                }
            }
        }

        let value = self.parse_expression()?;

        Ok(AstNode::LetStatement {
            name,
            value: Box::new(value),
        })
    }

    fn parse_list_elements(&mut self) -> Result<Vec<AstNode>, String> {
        let mut elements = Vec::new();

        loop {
            elements.push(self.parse_expression()?);

            if !matches!(self.peek(), TokenType::Comma) {
                break;
            }
            self.advance(); // comma
        }

        Ok(elements)
    }

    fn parse_if(&mut self) -> Result<AstNode, String> {
        // If condition:
        //     body
        // Otherwise:
        //     else_body
        // End If
        self.expect(TokenType::If)?;

        let condition = self.parse_condition()?;

        self.expect(TokenType::Colon)?;
        self.skip_newlines();

        let mut then_branch = Vec::new();
        while !matches!(self.peek(), TokenType::Otherwise) && !matches!(self.peek(), TokenType::End) {
            then_branch.push(self.parse_statement()?);
            self.skip_newlines();
        }

        let else_branch = if matches!(self.peek(), TokenType::Otherwise) {
            self.advance(); // Otherwise

            // Check for "Otherwise If"
            if matches!(self.peek(), TokenType::If) {
                // Convert Otherwise If to nested If
                let nested_if = self.parse_if()?;
                Some(vec![nested_if])
            } else {
                self.expect(TokenType::Colon)?;
                self.skip_newlines();

                let mut else_body = Vec::new();
                while !matches!(self.peek(), TokenType::End) {
                    else_body.push(self.parse_statement()?);
                    self.skip_newlines();
                }
                Some(else_body)
            }
        } else {
            None
        };

        if !matches!(self.peek(), TokenType::End) {
            return Err("Expected End If".to_string());
        }
        self.expect(TokenType::End)?;
        self.expect(TokenType::If)?;

        Ok(AstNode::IfStatement {
            condition: Box::new(condition),
            then_branch,
            else_branch,
        })
    }

    fn parse_while(&mut self) -> Result<AstNode, String> {
        // While condition:
        //     body
        // End While
        self.expect(TokenType::While)?;

        let condition = self.parse_condition()?;

        self.expect(TokenType::Colon)?;
        self.skip_newlines();

        let mut body = Vec::new();
        while !matches!(self.peek(), TokenType::End) {
            body.push(self.parse_statement()?);
            self.skip_newlines();
        }

        self.expect(TokenType::End)?;
        self.expect(TokenType::While)?;

        Ok(AstNode::WhileStatement {
            condition: Box::new(condition),
            body,
        })
    }

    fn parse_return(&mut self) -> Result<AstNode, String> {
        self.expect(TokenType::Return)?;

        let value = self.parse_expression()?;

        Ok(AstNode::ReturnStatement {
            value: Box::new(value),
        })
    }

    fn parse_condition(&mut self) -> Result<AstNode, String> {
        // Parse: x is y, x is less than y, x is greater than y
        let left = self.parse_expression()?;

        if !matches!(self.peek(), TokenType::Is) {
            return Ok(left); // Simple expression as condition
        }

        self.expect(TokenType::Is)?;

        // Check for less/greater
        let op = if matches!(self.peek(), TokenType::Less) {
            self.advance(); // less
            self.expect(TokenType::Than)?;
            ComparisonOp::LessThan
        } else if matches!(self.peek(), TokenType::Greater) {
            self.advance(); // greater
            self.expect(TokenType::Than)?;
            ComparisonOp::GreaterThan
        } else {
            ComparisonOp::Equal
        };

        let right = self.parse_expression()?;

        Ok(AstNode::Comparison {
            left: Box::new(left),
            op,
            right: Box::new(right),
        })
    }

    fn parse_expression(&mut self) -> Result<AstNode, String> {
        match self.peek() {
            TokenType::Integer(n) => {
                let val = *n;
                self.advance();
                Ok(AstNode::IntegerLiteral(val))
            }
            TokenType::String(s) => {
                let val = s.clone();
                self.advance();
                Ok(AstNode::StringLiteral(val))
            }
            TokenType::Identifier(name) => {
                let name = name.clone();
                self.advance();

                // Check for function call
                if matches!(self.peek(), TokenType::LeftParen) {
                    self.advance(); // (

                    let mut args = Vec::new();
                    while !matches!(self.peek(), TokenType::RightParen) {
                        args.push(self.parse_expression()?);

                        if matches!(self.peek(), TokenType::Comma) {
                            self.advance();
                        }
                    }

                    self.expect(TokenType::RightParen)?;

                    Ok(AstNode::FunctionCall { name, args })
                }
                // Check for field access
                else if matches!(self.peek(), TokenType::Dot) {
                    self.advance(); // .

                    let field = match self.advance() {
                        TokenType::Identifier(s) => s,
                        _ => return Err("Expected field name".to_string()),
                    };

                    Ok(AstNode::FieldAccess {
                        object: Box::new(AstNode::Identifier(name)),
                        field,
                    })
                } else {
                    Ok(AstNode::Identifier(name))
                }
            }
            TokenType::Add => {
                // Special case for add_to_list(list, item)
                self.advance(); // add
                self.expect(TokenType::To)?;

                if !matches!(self.peek(), TokenType::Identifier(s) if s == "list") {
                    return Err("Expected 'list' after 'add to'".to_string());
                }
                self.advance(); // list

                self.expect(TokenType::LeftParen)?;
                let list_arg = self.parse_expression()?;
                self.expect(TokenType::Comma)?;
                let item_arg = self.parse_expression()?;
                self.expect(TokenType::RightParen)?;

                Ok(AstNode::FunctionCall {
                    name: "add_to_list".to_string(),
                    args: vec![list_arg, item_arg],
                })
            }
            _ => Err(format!("Unexpected token in expression: {:?}", self.peek())),
        }
    }
}