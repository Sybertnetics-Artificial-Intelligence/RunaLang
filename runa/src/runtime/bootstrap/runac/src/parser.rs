//! The Runa parser, which builds an AST from a token stream.

use runa_common::token::{Token, TokenType};
use runa_common::ast::{Expr, LiteralExpr, VariableExpr, GroupingExpr, UnaryExpr, BinaryExpr, Stmt, LetStmt, ExprStmt, IfStmt, WhileStmt, ForStmt, BlockStmt, AssignExpr, ReturnStmt, FunctionStmt, CallExpr, PrintStmt, IndexAccessExpr};

pub struct Parser {
    tokens: Vec<Token>,
    current: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Parser {
            tokens,
            current: 0,
        }
    }

    pub fn parse(&mut self) -> Result<Vec<Stmt>, String> {
        let mut statements = Vec::new();
        // Consume any leading newlines from the lexer hack
        while self.match_token(TokenType::Newline) {}
        while !self.is_at_end() {
            let stmt = self.declaration()?;
            statements.push(stmt);
            // Consume any trailing newlines before the next statement or EOF
            while self.match_token(TokenType::Newline) {}
        }
        Ok(statements)
    }

    fn declaration(&mut self) -> Result<Stmt, String> {
        if self.match_token(TokenType::Let) {
            self.let_declaration()
        } else if self.match_token(TokenType::Define) {
            self.define_declaration()
        } else if self.match_token(TokenType::Set) {
            self.set_statement()
        } else if self.match_token(TokenType::Process) {
            self.function_declaration()
        } else {
            self.statement()
        }
    }

    // Process called "name" that takes param1 as Type and param2 as Type returns Type:
    fn function_declaration(&mut self) -> Result<Stmt, String> {
        self.consume(TokenType::Called, "Expect 'called' after 'Process'.")?;
        let name = self.consume(TokenType::String, "Expect function name in quotes.")?.clone();
        
        let mut params = Vec::new();
        // Parse "that takes" part
        if self.match_token(TokenType::That) {
            self.consume(TokenType::Takes, "Expect 'takes' after 'that'.")?;
            loop {
                // Stop if we see 'returns' or ':' (end of parameter list)
                if self.check(TokenType::Returns) || self.check(TokenType::Colon) {
                    break;
                }
                // Only parse parameter if next token is an identifier
                if !self.check(TokenType::Identifier) {
                    break;
                }
                let param_name = self.consume(TokenType::Identifier, "Expect parameter name.")?.clone();
                if self.match_token(TokenType::As) {
                    let _param_type = self.consume(TokenType::Identifier, "Expect parameter type.")?.clone();
                    params.push(param_name); // For now, just store the name
                } else {
                    params.push(param_name);
                }
                // If next token is 'and', continue; else break
                if self.match_token(TokenType::And) {
                    continue;
                } else {
                    break;
                }
            }
        }
        // Parse optional return type
        if self.match_token(TokenType::Returns) {
            let _return_type = self.consume(TokenType::Identifier, "Expect return type.")?.clone();
        }
        self.consume(TokenType::Colon, "Expect ':' after function signature.")?;
        self.consume(TokenType::Newline, "Expect newline after function signature.")?;
        self.consume(TokenType::Indent, "Expect indent for function body.")?;
        let mut body = Vec::new();
        while !self.check(TokenType::Dedent) && !self.is_at_end() {
            body.push(self.statement()?);
        }
        self.consume(TokenType::Dedent, "Expect dedent after function body.")?;
        Ok(Stmt::Function(FunctionStmt { name, params, body }))
    }

    // Let x be expression
    // Let x (Type) be expression
    fn let_declaration(&mut self) -> Result<Stmt, String> {
        let name = self.consume(TokenType::Identifier, "Expect variable name.")?.clone();
        
        // Optional type annotation
        if self.match_token(TokenType::LParen) {
            self.consume(TokenType::Identifier, "Expect type name.")?;
            self.consume(TokenType::RParen, "Expect ')' after type.")?;
        }
        
        self.consume(TokenType::Be, "Expect 'be' after variable name.")?;
        println!("DEBUG: After 'be', next token is {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        let initializer = Some(self.expression()?);
        
        self.consume(TokenType::Newline, "Expect newline after let declaration.")?;
        Ok(Stmt::Let(LetStmt { name, initializer }))
    }

    // Define x as expression
    fn define_declaration(&mut self) -> Result<Stmt, String> {
        let name = self.consume(TokenType::Identifier, "Expect variable name.")?.clone();
        self.consume(TokenType::As, "Expect 'as' after variable name.")?;
        let initializer = Some(self.expression()?);
        self.consume(TokenType::Newline, "Expect newline after define declaration.")?;
        Ok(Stmt::Let(LetStmt { name, initializer }))
    }

    // Set x to expression
    fn set_statement(&mut self) -> Result<Stmt, String> {
        let name = self.consume(TokenType::Identifier, "Expect variable name.")?.clone();
        self.consume(TokenType::To, "Expect 'to' after variable name.")?;
        let value = self.expression()?;
        self.consume(TokenType::Newline, "Expect newline after set statement.")?;
        
        Ok(Stmt::Expression(ExprStmt { 
            expr: Expr::Assign(AssignExpr { 
                name: Token { token_type: TokenType::Identifier, lexeme: name.lexeme, line: name.line, column: name.column }, 
                value: Box::new(value) 
            }) 
        }))
    }

    fn statement(&mut self) -> Result<Stmt, String> {
        if self.match_token(TokenType::If) {
            return self.if_statement();
        }
        if self.match_token(TokenType::Unless) {
            return self.unless_statement();
        }
        if self.match_token(TokenType::When) {
            return self.when_statement();
        }
        if self.match_token(TokenType::While) {
            return self.while_statement();
        }
        if self.match_token(TokenType::For) {
            return self.for_statement();
        }
        if self.match_token(TokenType::Return) {
            return self.return_statement();
        }
        if self.match_token(TokenType::Display) {
            return self.display_statement();
        }
        self.expression_statement()
    }

    // If condition: block Otherwise if condition: block Otherwise: block
    fn if_statement(&mut self) -> Result<Stmt, String> {
        let condition = self.expression()?;
        self.consume(TokenType::Colon, "Expect ':' after if condition.")?;
        self.consume(TokenType::Newline, "Expect newline after if condition.")?;
        self.consume(TokenType::Indent, "Expect indent for if block.")?;
        let then_branch = self.block_statement()?;

        let mut else_branch = None;
        while self.match_token(TokenType::Otherwise) {
            if self.match_token(TokenType::If) {
                // Otherwise if
                let else_condition = self.expression()?;
                self.consume(TokenType::Colon, "Expect ':' after else if condition.")?;
                self.consume(TokenType::Newline, "Expect newline after else if condition.")?;
                self.consume(TokenType::Indent, "Expect indent for else if block.")?;
                let else_body = self.block_statement()?;
                
                else_branch = Some(Box::new(Stmt::If(IfStmt {
                    condition: else_condition,
                    then_branch: else_body,
                    else_branch: None,
                })));
            } else {
                // Final Otherwise
                self.consume(TokenType::Colon, "Expect ':' after 'Otherwise'.")?;
                self.consume(TokenType::Newline, "Expect newline after 'Otherwise'.")?;
                self.consume(TokenType::Indent, "Expect indent for 'Otherwise' block.")?;
                let else_body = self.block_statement()?;
                else_branch = Some(Box::new(Stmt::Block(else_body)));
                break;
            }
        }

        Ok(Stmt::If(IfStmt {
            condition,
            then_branch,
            else_branch,
        }))
    }

    // Unless condition: block
    fn unless_statement(&mut self) -> Result<Stmt, String> {
        let condition = self.expression()?;
        self.consume(TokenType::Colon, "Expect ':' after unless condition.")?;
        self.consume(TokenType::Newline, "Expect newline after unless condition.")?;
        self.consume(TokenType::Indent, "Expect indent for unless block.")?;
        let body = self.block_statement()?;

        // Unless is equivalent to "If not condition"
        let not_condition = Expr::Unary(UnaryExpr {
            operator: Token { token_type: TokenType::Not, lexeme: "not".to_string(), line: 0, column: 0 },
            right: Box::new(condition),
        });

        Ok(Stmt::If(IfStmt {
            condition: not_condition,
            then_branch: body,
            else_branch: None,
        }))
    }

    // When condition: block
    fn when_statement(&mut self) -> Result<Stmt, String> {
        let condition = self.expression()?;
        self.consume(TokenType::Colon, "Expect ':' after when condition.")?;
        self.consume(TokenType::Newline, "Expect newline after when condition.")?;
        self.consume(TokenType::Indent, "Expect indent for when block.")?;
        let body = self.block_statement()?;

        Ok(Stmt::If(IfStmt {
            condition,
            then_branch: body,
            else_branch: None,
        }))
    }

    // For each item in collection: block
    // For i from 0 to 10: block
    fn for_statement(&mut self) -> Result<Stmt, String> {
        if self.match_token(TokenType::Each) {
            // For each item in collection
            let variable = self.consume(TokenType::Identifier, "Expect identifier after 'each'.")?.clone();
            self.consume(TokenType::In, "Expect 'in' after loop variable.")?;
            let collection = self.expression()?;
            self.consume(TokenType::Colon, "Expect ':' after for clause.")?;
            self.consume(TokenType::Newline, "Expect newline after for clause.")?;
            self.consume(TokenType::Indent, "Expect indent for for block.")?;
            let body = self.block_statement()?;

            Ok(Stmt::For(ForStmt {
                variable,
                start: Box::new(collection),
                end: Box::new(Expr::Literal(LiteralExpr { value: Token { token_type: TokenType::Integer, lexeme: "0".to_string(), line: 0, column: 0 } })),
                step: None,
                body,
            }))
        } else {
            // For i from 0 to 10
            let variable = self.consume(TokenType::Identifier, "Expect identifier after 'for'.")?.clone();
            self.consume(TokenType::From, "Expect 'from' after loop variable.")?;
            let start = self.expression()?;
            self.consume(TokenType::To, "Expect 'to' after 'from' expression.")?;
            let end = self.expression()?;

            let step = if self.match_token(TokenType::By) {
                Some(Box::new(self.expression()?))
            } else {
                None
            };

            self.consume(TokenType::Colon, "Expect ':' after for clause.")?;
            self.consume(TokenType::Newline, "Expect newline after for clause.")?;
            self.consume(TokenType::Indent, "Expect indent for for block.")?;
            let body = self.block_statement()?;

            Ok(Stmt::For(ForStmt {
                variable,
                start: Box::new(start),
                end: Box::new(end),
                step,
                body,
            }))
        }
    }

    // While condition: block
    fn while_statement(&mut self) -> Result<Stmt, String> {
        let condition = self.expression()?;
        self.consume(TokenType::Colon, "Expect ':' after while condition.")?;
        self.consume(TokenType::Newline, "Expect newline after while condition.")?;
        self.consume(TokenType::Indent, "Expect indent for while block.")?;
        let body = self.block_statement()?;

        Ok(Stmt::While(WhileStmt { condition, body }))
    }
    
    // Return expression
    fn return_statement(&mut self) -> Result<Stmt, String> {
        let value = if !self.check(TokenType::Newline) {
            Some(self.expression()?)
        } else {
            None
        };
        self.consume(TokenType::Newline, "Expect newline after return value.")?;
        Ok(Stmt::Return(ReturnStmt { value }))
    }

    // Display expression
    fn display_statement(&mut self) -> Result<Stmt, String> {
        let value = self.expression()?;
        self.consume(TokenType::Newline, "Expect newline after display value.")?;
        Ok(Stmt::Print(PrintStmt { value }))
    }

    fn block_statement(&mut self) -> Result<BlockStmt, String> {
        let mut statements = Vec::new();

        while !self.check(TokenType::Dedent) && !self.is_at_end() {
            statements.push(self.declaration()?);
        }

        self.consume(TokenType::Dedent, "Expect dedent after block.")?;
        Ok(BlockStmt { statements })
    }

    fn expression_statement(&mut self) -> Result<Stmt, String> {
        let expr = self.expression()?;
        self.consume(TokenType::Newline, "Expect newline after expression.")?;
        Ok(Stmt::Expression(ExprStmt { expr }))
    }

    // expression → ternary_expression
    fn expression(&mut self) -> Result<Expr, String> {
        self.ternary_expression()
    }

    // ternary_expression → or_expression ("if" or_expression "else" or_expression)?
    fn ternary_expression(&mut self) -> Result<Expr, String> {
        let condition = self.or_expression()?;
        
        if self.match_token(TokenType::If) {
            let then_expr = self.or_expression()?;
            self.consume(TokenType::Else, "Expect 'else' in ternary expression.")?;
            let _else_expr = self.or_expression()?;
            
            // For now, we'll use a binary expression to represent ternary
            // In a full implementation, we'd need a TernaryExpr variant
            Ok(Expr::Binary(BinaryExpr {
                left: Box::new(condition),
                operator: Token { token_type: TokenType::If, lexeme: "if".to_string(), line: 0, column: 0 },
                right: Box::new(then_expr),
            }))
        } else {
            Ok(condition)
        }
    }

    // or_expression → and_expression ("or" and_expression)*
    fn or_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.and_expression()?;

        while self.match_token(TokenType::Or) {
            let operator = self.previous().clone();
            let right = self.and_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }

    // and_expression → not_expression ("and" not_expression)*
    fn and_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.not_expression()?;

        while self.match_token(TokenType::And) {
            let operator = self.previous().clone();
            let right = self.not_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }

    // not_expression → "not" not_expression | comparison_expression
    fn not_expression(&mut self) -> Result<Expr, String> {
        if self.match_token(TokenType::Not) {
            let operator = self.previous().clone();
            let right = self.not_expression()?;
            return Ok(Expr::Unary(UnaryExpr {
                operator,
                right: Box::new(right),
            }));
        }
        self.comparison_expression()
    }

    // comparison_expression → additive_expression (comparison_op additive_expression)*
    fn comparison_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.additive_expression()?;

        while self.match_token(TokenType::IsEqualTo) 
            || self.match_token(TokenType::IsNotEqualTo)
            || self.match_token(TokenType::IsGreaterThan)
            || self.match_token(TokenType::IsLessThan)
            || self.match_token(TokenType::IsGreaterThanOrEqualTo)
            || self.match_token(TokenType::IsLessThanOrEqualTo)
        {
            let operator = self.previous().clone();
            let right = self.additive_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }

    // additive_expression → multiplicative_expression (additive_op multiplicative_expression)*
    fn additive_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.multiplicative_expression()?;

        while self.match_token(TokenType::Plus) || self.match_token(TokenType::Minus) {
            let operator = self.previous().clone();
            let right = self.multiplicative_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }

    // multiplicative_expression → unary_expression (multiplicative_op unary_expression)*
    fn multiplicative_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.unary_expression()?;

        while self.match_token(TokenType::MultipliedBy) || self.match_token(TokenType::DividedBy) {
            let operator = self.previous().clone();
            let right = self.unary_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }

    // unary_expression → unary_op unary_expression | power_expression
    fn unary_expression(&mut self) -> Result<Expr, String> {
        if self.match_token(TokenType::Minus) || self.match_token(TokenType::Not) {
            let operator = self.previous().clone();
            let right = self.unary_expression()?;
            return Ok(Expr::Unary(UnaryExpr {
                operator,
                right: Box::new(right),
            }));
        }
        self.power_expression()
    }

    // power_expression → postfix_expression ("to" "the" "power" "of" postfix_expression)*
    fn power_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.postfix_expression()?;

        while self.match_token(TokenType::ToThePowerOf) {
            let operator = self.previous().clone();
            let right = self.postfix_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }

    // postfix_expression → primary_expression postfix_op*
    fn postfix_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.primary_expression()?;

        loop {
            if self.match_token(TokenType::LParen) {
                expr = self.finish_call(expr)?;
            } else if self.match_token(TokenType::LBracket) {
                expr = self.finish_index_access(expr)?;
            } else if self.match_token(TokenType::Dot) {
                expr = self.finish_member_access(expr)?;
            } else {
                break;
            }
        }

        Ok(expr)
    }

    // primary_expression → literal | identifier | "(" expression ")"
    fn primary_expression(&mut self) -> Result<Expr, String> {
        if self.match_token(TokenType::Integer) || self.match_token(TokenType::Float) {
            Ok(Expr::Literal(LiteralExpr { value: self.previous().clone() }))
        } else if self.match_token(TokenType::String) {
            Ok(Expr::Literal(LiteralExpr { value: self.previous().clone() }))
        } else if self.match_token(TokenType::Boolean) {
            Ok(Expr::Literal(LiteralExpr { value: self.previous().clone() }))
        } else if self.match_token(TokenType::Identifier) {
            let ident_token = self.previous().clone();
            // Check for natural function call: Identifier CalledWith ...
            if self.match_token(TokenType::CalledWith) {
                let mut arguments = Vec::new();
                // At least one argument is required
                arguments.push(self.expression()?);
                while self.match_token(TokenType::And) {
                    arguments.push(self.expression()?);
                }
                // Build CallExpr node
                return Ok(Expr::Call(CallExpr {
                    callee: Box::new(Expr::Variable(VariableExpr { name: ident_token })),
                    arguments,
                    paren: Token { token_type: TokenType::CalledWith, lexeme: "called with".to_string(), line: 0, column: 0 },
                }));
            } else {
                Ok(Expr::Variable(VariableExpr { name: ident_token }))
            }
        } else if self.match_token(TokenType::LParen) {
            let expr = self.expression()?;
            self.consume(TokenType::RParen, "Expect ')' after expression.")?;
            Ok(Expr::Grouping(GroupingExpr { expression: Box::new(expr) }))
        } else {
            Err("Expect expression.".to_string())
        }
    }

    fn finish_call(&mut self, callee: Expr) -> Result<Expr, String> {
        let mut arguments = Vec::new();
        if !self.check(TokenType::RParen) {
            loop {
                arguments.push(self.expression()?);
                if !self.match_token(TokenType::Comma) {
                    break;
                }
            }
        }
        let paren = self.consume(TokenType::RParen, "Expect ')' after arguments.")?.clone();
        Ok(Expr::Call(CallExpr { callee: Box::new(callee), arguments, paren }))
    }

    fn finish_index_access(&mut self, target: Expr) -> Result<Expr, String> {
        let index = self.expression()?;
        self.consume(TokenType::RBracket, "Expect ']' after index.")?;
        Ok(Expr::Index(IndexAccessExpr {
            target: Box::new(target),
            index: Box::new(index),
        }))
    }

    fn finish_member_access(&mut self, target: Expr) -> Result<Expr, String> {
        let member = self.consume(TokenType::Identifier, "Expect member name after '.'.")?.clone();
        
        // For now, we'll use a binary expression to represent member access
        // In a full implementation, we'd need a MemberAccessExpr variant
        Ok(Expr::Binary(BinaryExpr {
            left: Box::new(target),
            operator: Token { token_type: TokenType::Dot, lexeme: ".".to_string(), line: 0, column: 0 },
            right: Box::new(Expr::Variable(VariableExpr { name: member })),
        }))
    }
    
    fn match_token(&mut self, token_type: TokenType) -> bool {
        if self.check(token_type) {
            self.advance();
            true
        } else {
            false
        }
    }

    fn consume(&mut self, token_type: TokenType, message: &str) -> Result<&Token, String> {
        if self.check(token_type) {
            let token = self.advance();
            return Ok(token);
        }

        // Allow EOF to terminate the final statement
        if self.peek().token_type == TokenType::Eof {
             if token_type == TokenType::Newline {
                 return Ok(self.peek());
             }
        }

        Err(format!("{} Found {:?}.", message, self.peek()))
    }

    // Helper functions for navigating the token stream
    
    fn peek(&self) -> &Token {
        &self.tokens[self.current]
    }

    fn previous(&self) -> &Token {
        &self.tokens[self.current - 1]
    }

    fn is_at_end(&self) -> bool {
        self.peek().token_type == TokenType::Eof
    }

    fn advance(&mut self) -> &Token {
        if !self.is_at_end() {
            self.current += 1;
        }
        self.previous()
    }

    fn check(&self, token_type: TokenType) -> bool {
        if self.is_at_end() {
            return false;
        }
        self.peek().token_type == token_type
    }
} 