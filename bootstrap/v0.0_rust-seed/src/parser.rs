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
    PrintStatement {
        value: Box<AstNode>,
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
pub enum BinaryOperator {
    Add,
    Subtract,
    Equal,
    NotEqual,
    LessThan,
    GreaterThan,
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
            TokenType::Print => self.parse_print_statement(),
            TokenType::Return => self.parse_return_statement(),
            TokenType::If => self.parse_if_statement(),
            TokenType::While => self.parse_while_statement(),
            TokenType::Process => self.parse_process_definition(),
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

    fn parse_print_statement(&mut self) -> Result<AstNode, String> {
        // Consume 'Print'
        self.expect_token(TokenType::Print)?;

        // Parse value expression
        let value = self.parse_expression()?;

        Ok(AstNode::PrintStatement {
            value: Box::new(value),
        })
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
            // We should also check for 'While' after 'End' but we'll skip that for now
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

        // Consume 'that'
        self.expect_token(TokenType::That)?;

        // Consume 'takes'
        self.expect_token(TokenType::Takes)?;

        // Parse parameters
        let mut parameters = Vec::new();

        // Handle no parameters case
        if matches!(self.current_token().token_type, TokenType::Returns) {
            // No parameters, skip to returns
        } else {
            // Parse parameter list
            loop {
                // Get parameter name
                let param_name = match &self.current_token().token_type {
                    TokenType::Identifier(name) => {
                        let name = name.clone();
                        self.advance();
                        name
                    }
                    _ => return Err("Expected parameter name".to_string()),
                };

                // Expect 'as'
                if !matches!(self.current_token().token_type, TokenType::Identifier(ref word) if word == "as") {
                    return Err("Expected 'as' after parameter name".to_string());
                }
                self.advance();

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

        // Consume 'returns'
        self.expect_token(TokenType::Returns)?;

        // Get return type
        let return_type = match &self.current_token().token_type {
            TokenType::Identifier(type_name) => {
                let type_name = type_name.clone();
                self.advance();
                Some(type_name)
            }
            _ => None, // Optional return type
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

    fn parse_expression(&mut self) -> Result<AstNode, String> {
        self.parse_comparison_expression()
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
                    Ok(AstNode::Identifier(name))
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