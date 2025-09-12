//! The Runa parser, which builds an AST from a token stream.

use runa_common::token::{Token, TokenType};
use runa_common::ast::{Expr, LiteralExpr, ListExpr, VariableExpr, GroupingExpr, UnaryExpr, BinaryExpr, Stmt, LetStmt, ExprStmt, IfStmt, WhileStmt, ForStmt, BlockStmt, AssignExpr, ReturnStmt, FunctionStmt, CallExpr, PrintStmt, IndexAccessExpr, AnnotationStmt, InterpolatedStringExpr, InterpolatedStringPart, MatchStmt, WhenCase, TypeDefStmt, TypeField, EnumDefStmt};
use runa_common::types::RunaType;

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

        // The main parsing loop with robust synchronization
        while !self.is_at_end() { // Use the trusted `is_at_end` for the main condition
            // 1. Synchronize: Skip any leading blank lines.
            while self.match_token(TokenType::Newline) {}

            // 2. Re-check for EOF after skipping newlines.
            if self.is_at_end() { 
                break; 
            }

            // 3. Parse one statement.
            // Use a synchronizing error recovery mechanism here.
            match self.declaration() {
                Ok(stmt) => {
                    statements.push(stmt);
                    
                    // Check for inline Note comment after the statement
                    if let Some(inline_comment) = self.try_parse_inline_comment() {
                        // Create an inline comment annotation
                        let inline_stmt = Stmt::Annotation(AnnotationStmt {
                            annotation_type: "Context".to_string(),
                            content: format!("InlineComment: {}", inline_comment),
                            location: runa_common::annotations::SourceLocation {
                                start_line: 0,
                                start_column: 0,
                                end_line: 0,
                                end_column: 0,
                                file_path: Some("current".to_string()),
                            },
                        });
                        statements.push(inline_stmt);
                    }
                },
                Err(e) => {
                    // If parsing a statement fails, don't just stop.
                    // Call a recovery function that advances the parser to the
                    // next likely start of a statement (usually the next newline).
                    return Err(e); // For now, just return the error
                }
            }
        }
        
        Ok(statements)
    }

    fn declaration(&mut self) -> Result<Stmt, String> {
        println!("DEBUG: declaration() - current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        
        // Check for annotation tokens first
        if self.check_annotation_start() {
            println!("DEBUG: Routing to annotation_declaration");
            self.annotation_declaration()
        } else if self.match_token(TokenType::Note) {
            println!("DEBUG: Routing to note_comment");
            self.note_comment()
        } else if self.match_token(TokenType::Let) {
            println!("DEBUG: Routing to let_declaration");
            self.let_declaration()
        } else if self.match_token(TokenType::Define) {
            println!("DEBUG: Routing to define_declaration");
            self.define_declaration()
        } else if self.match_token(TokenType::Set) {
            println!("DEBUG: Routing to set_statement");
            self.set_statement()
        } else if self.match_token(TokenType::Process) {
            println!("DEBUG: Routing to function_declaration");
            self.function_declaration()
        } else {
            println!("DEBUG: Routing to statement (fallback)");
            self.statement()
        }
    }

    // Process called "name" that takes param1 as Type and param2 as Type returns Type:
    fn function_declaration(&mut self) -> Result<Stmt, String> {
        println!("DEBUG: Starting function_declaration");
        self.consume(TokenType::Called, "Expect 'called' after 'Process'.")?;
        println!("DEBUG: Successfully consumed 'called'");
        let name = self.consume(TokenType::String, "Expect function name in quotes.")?.clone();
        println!("DEBUG: Successfully consumed function name: '{}'", name.lexeme);
        
        let mut params = Vec::new();
        let mut param_types = Vec::new();
        
        // Parse "that takes" part
        if self.match_token(TokenType::That) {
            println!("DEBUG: Successfully consumed 'that'");
            self.consume(TokenType::Takes, "Expect 'takes' after 'that'.")?;
            println!("DEBUG: Successfully consumed 'takes'");
            loop {
                // Stop if we see 'returns' or ':' (end of parameter list)
                if self.check(TokenType::Returns) || self.check(TokenType::Colon) {
                    break;
                }
                // Only parse parameter if next token is an identifier
                if !self.check(TokenType::Identifier) {
                    break;
                }
                // Parse parameter with proper type annotation and validation
                let param_token = self.advance().clone();
                let param_name = param_token.lexeme.clone();
                println!("DEBUG: Parsing parameter: '{}'", param_name);
                
                // Check for type annotation using 'as' keyword
                let param_type = if self.match_token(TokenType::As) {
                    println!("DEBUG: Found 'as', parsing type annotation");
                    let type_result = self.parse_type_annotation()?;
                    println!("DEBUG: Successfully parsed type annotation: {:?}", type_result);
                    type_result
                } else {
                    println!("DEBUG: No 'as' found, using Any type");
                    // Default to dynamic type if no annotation provided
                    RunaType::Any
                };
                
                // Validate parameter name
                if param_name.is_empty() {
                    return Err("Parameter name cannot be empty".to_string());
                }
                
                // Check for duplicate parameters
                if params.iter().any(|p: &Token| p.lexeme == param_name) {
                    return Err(format!("Duplicate parameter name: {}", param_name));
                }
                
                // Store parameter with type information
                params.push(param_token);
                param_types.push(param_type);
                
                // If next token is 'and', continue; else break
                println!("DEBUG: After parameter parsing, current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
                if self.match_token(TokenType::And) {
                    println!("DEBUG: Found 'and', continuing to next parameter");
                    continue;
                } else {
                    println!("DEBUG: No 'and' found, breaking from parameter loop");
                    break;
                }
            }
        }
        // Parse optional return type
        println!("DEBUG: After parameter parsing loop, current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        if self.match_token(TokenType::Returns) {
            println!("DEBUG: Found 'returns', parsing return type");
            println!("DEBUG: Current token for return type: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
            let _return_type = self.consume(TokenType::Identifier, "Expect return type.")?.clone();
            println!("DEBUG: Successfully parsed return type: '{}'", _return_type.lexeme);
        }
        self.consume(TokenType::Colon, "Expect ':' after function signature.")?;
        
        // Handle inline comments before newline - for function declarations, we need special handling
        // since we need to continue parsing the function body after the inline comment
        if self.check(TokenType::Note) {
            println!("DEBUG: Found Note token for inline comment after function signature, parsing it now");
            // Parse the inline comment ourselves rather than leaving it for main loop
            // since we need to continue with function body parsing
            if let Some(_inline_comment) = self.try_parse_inline_comment() {
                println!("DEBUG: Successfully parsed inline comment in function signature");
            }
        }
        
        // Now expect newline and indent
        if !self.check(TokenType::Newline) && !self.check(TokenType::Indent) {
            return Err("Expect newline after function signature.".to_string());
        }
        
        if self.check(TokenType::Newline) {
            self.advance(); // consume newline
        }
        
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
    // Let multi word identifier be expression
    fn let_declaration(&mut self) -> Result<Stmt, String> {
        println!("DEBUG: Starting let_declaration");
        
        // Parse multi-word identifier: collect all tokens until we see 'be' or '('
        let mut name_parts = Vec::new();
        let mut type_annotation = false;
        
        // Keep parsing tokens until we find 'be' or '(' (type annotation)
        while !self.check(TokenType::Be) && !self.check(TokenType::LParen) && !self.is_at_end() {
            let token = self.advance().clone();
            
            // Accept identifiers and keywords as part of multi-word identifiers
            match token.token_type {
                TokenType::Identifier => {
                    name_parts.push(token.lexeme);
                },
                // Allow keywords to be part of variable names in this context
                TokenType::Is | TokenType::Not | TokenType::IsNot | TokenType::And | TokenType::Or | 
                TokenType::If | TokenType::While | TokenType::For | TokenType::In |
                TokenType::Each | TokenType::From | TokenType::To | TokenType::By |
                TokenType::That | TokenType::Takes | TokenType::Returns |
                TokenType::As | TokenType::With | TokenType::List | TokenType::Dictionary => {
                    name_parts.push(token.lexeme);
                },
                _ => {
                    return Err(format!("Unexpected token '{}' in variable name. Expected identifier or 'be'.", token.lexeme));
                }
            }
        }
        
        if name_parts.is_empty() {
            return Err("Expect variable name after 'Let'.".to_string());
        }
        
        // Combine all parts into a single multi-word identifier
        let variable_name = name_parts.join(" ");
        println!("DEBUG: Parsed multi-word variable name: '{}'", variable_name);
        
        // Create a synthetic token for the multi-word identifier
        let name = Token {
            token_type: TokenType::Identifier,
            lexeme: variable_name,
            line: self.peek().line,
            column: self.peek().column,
        };
        
        // Optional type annotation
        if self.match_token(TokenType::LParen) {
            println!("DEBUG: Found type annotation");
            self.consume(TokenType::Identifier, "Expect type name.")?;
            self.consume(TokenType::RParen, "Expect ')' after type.")?;
            type_annotation = true;
        }
        
        println!("DEBUG: About to consume 'be', current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        self.consume(TokenType::Be, "Expect 'be' after variable name.")?;
        println!("DEBUG: Successfully consumed 'be', next token is {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        let initializer = Some(self.expression()?);
        println!("DEBUG: Parsed expression, next token is {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        
        // Accept either newline, dedent, or Note (for inline comments) after let declaration
        if self.check(TokenType::Newline) {
            self.advance();
            println!("DEBUG: Successfully consumed newline");
        } else if self.check(TokenType::Dedent) {
            // Don't consume dedent here - let the block parser handle it
            println!("DEBUG: Found dedent, letting block parser handle it");
        } else if self.check(TokenType::Note) {
            // Don't consume Note here - let the main loop handle inline comments
            println!("DEBUG: Found Note token for inline comment, letting main loop handle it");
        } else if !self.is_at_end() {
            return Err("Expect newline or end of block after let declaration.".to_string());
        }
        
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
        
        // Accept either newline or dedent (end of indented block) after set statement
        if self.check(TokenType::Newline) {
            self.advance();
        } else if self.check(TokenType::Dedent) {
            // Don't consume dedent here - let the block parser handle it
        } else if !self.is_at_end() {
            return Err("Expect newline or end of block after set statement.".to_string());
        }
        
        Ok(Stmt::Expression(ExprStmt { 
            expr: Expr::Assign(AssignExpr { 
                name: Token { token_type: TokenType::Identifier, lexeme: name.lexeme, line: name.line, column: name.column }, 
                value: Box::new(value) 
            }) 
        }))
    }

    fn statement(&mut self) -> Result<Stmt, String> {
        println!("DEBUG: statement() - current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
        
        if self.match_token(TokenType::Let) {
            println!("DEBUG: statement() - matched Let, calling let_declaration");
            return self.let_declaration();
        }
        if self.match_token(TokenType::If) {
            println!("DEBUG: statement() - matched If, calling if_statement");
            return self.if_statement();
        }
        if self.match_token(TokenType::Unless) {
            println!("DEBUG: statement() - matched Unless, calling unless_statement");
            return self.unless_statement();
        }
        if self.match_token(TokenType::When) {
            return self.when_statement();
        }
        if self.match_token(TokenType::Match) {
            return self.match_statement();
        }
        if self.match_token(TokenType::Type) {
            return self.type_definition();
        }
        if self.match_token(TokenType::Enum) {
            return self.enum_definition();
        }
        if self.match_token(TokenType::While) {
            println!("DEBUG: statement() - matched While, calling while_statement");
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
        if self.match_token(TokenType::Note) {
            println!("DEBUG: statement() - matched Note, calling note_comment");
            return self.note_comment();
        }
        println!("DEBUG: statement() - falling through to expression_statement");
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

    // Match expression: When pattern: block, When pattern: block, Otherwise: block
    fn match_statement(&mut self) -> Result<Stmt, String> {
        // Parse the expression to match against
        let expr = self.expression()?;
        self.consume(TokenType::Colon, "Expect ':' after match expression.")?;
        self.consume(TokenType::Newline, "Expect newline after match expression.")?;
        self.consume(TokenType::Indent, "Expect indent for match block.")?;
        
        let mut cases = Vec::new();
        let mut default_case = None;
        
        // Parse when cases
        while !self.check(TokenType::Dedent) && !self.is_at_end() {
            if self.match_token(TokenType::When) {
                // Parse when case: "When pattern:"
                let pattern = self.expression()?;
                self.consume(TokenType::Colon, "Expect ':' after when pattern.")?;
                self.consume(TokenType::Newline, "Expect newline after when pattern.")?;
                self.consume(TokenType::Indent, "Expect indent for when case body.")?;
                
                let body = self.block_statement()?;
                
                cases.push(WhenCase {
                    pattern,
                    body,
                });
            } else if self.match_token(TokenType::Otherwise) {
                // Parse default case: "Otherwise:"
                self.consume(TokenType::Colon, "Expect ':' after 'Otherwise'.")?;
                self.consume(TokenType::Newline, "Expect newline after 'Otherwise'.")?;
                self.consume(TokenType::Indent, "Expect indent for otherwise case body.")?;
                
                default_case = Some(self.block_statement()?);
                break; // Otherwise should be the last case
            } else {
                return Err("Expected 'When' or 'Otherwise' in match statement.".to_string());
            }
        }
        
        // Consume the dedent for the match block
        if self.check(TokenType::Dedent) {
            self.advance();
        }
        
        Ok(Stmt::Match(MatchStmt {
            expr,
            cases,
            default_case,
        }))
    }

    // Type called "TypeName": field1 as Type1, field2 as Type2, ...
    fn type_definition(&mut self) -> Result<Stmt, String> {
        self.consume(TokenType::Called, "Expect 'called' after 'Type'.")?;
        let type_name = self.consume(TokenType::String, "Expect type name after 'called'.")?.clone();
        self.consume(TokenType::Colon, "Expect ':' after type name.")?;
        self.consume(TokenType::Newline, "Expect newline after type definition header.")?;
        self.consume(TokenType::Indent, "Expect indent for type body.")?;
        
        let mut fields = Vec::new();
        
        // Parse type fields
        while !self.check(TokenType::Dedent) && !self.is_at_end() {
            let field_name = self.consume(TokenType::Identifier, "Expect field name.")?.clone();
            self.consume(TokenType::As, "Expect 'as' after field name.")?;
            let field_type = self.consume(TokenType::Identifier, "Expect field type after 'as'.")?.clone();
            
            fields.push(TypeField {
                name: field_name,
                field_type,
            });
            
            // Consume newline if present
            if self.match_token(TokenType::Newline) {
                // Continue to next field
            }
        }
        
        // Consume the dedent for the type block
        if self.check(TokenType::Dedent) {
            self.advance();
        }
        
        Ok(Stmt::TypeDef(TypeDefStmt {
            name: type_name,
            fields,
        }))
    }

    // Enum called "EnumName": Variant1, Variant2, Variant3, ...
    fn enum_definition(&mut self) -> Result<Stmt, String> {
        self.consume(TokenType::Called, "Expect 'called' after 'Enum'.")?;
        let enum_name = self.consume(TokenType::String, "Expect enum name after 'called'.")?.clone();
        self.consume(TokenType::Colon, "Expect ':' after enum name.")?;
        self.consume(TokenType::Newline, "Expect newline after enum definition header.")?;
        self.consume(TokenType::Indent, "Expect indent for enum body.")?;
        
        let mut variants = Vec::new();
        
        // Parse enum variants
        while !self.check(TokenType::Dedent) && !self.is_at_end() {
            let variant_name = self.consume(TokenType::Identifier, "Expect variant name.")?.clone();
            variants.push(variant_name);
            
            // Consume newline if present
            if self.match_token(TokenType::Newline) {
                // Continue to next variant
            }
        }
        
        // Consume the dedent for the enum block
        if self.check(TokenType::Dedent) {
            self.advance();
        }
        
        Ok(Stmt::EnumDef(EnumDefStmt {
            name: enum_name,
            variants,
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
                end: Box::new(Expr::Literal(LiteralExpr { value: runa_common::ast::LiteralValue::Integer(0) })),
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
        let value = if !self.check(TokenType::Newline) && !self.check(TokenType::Dedent) {
            Some(self.expression()?)
        } else {
            None
        };
        
        // Accept either newline or dedent (end of indented block)
        if self.check(TokenType::Newline) {
            self.advance();
        } else if self.check(TokenType::Dedent) {
            // Don't consume dedent here - let the block parser handle it
        } else {
            return Err("Expect newline or end of block after return value.".to_string());
        }
        
        Ok(Stmt::Return(ReturnStmt { value }))
    }

    // Display expression
    fn display_statement(&mut self) -> Result<Stmt, String> {
        let value = self.expression()?;
        
        // Only consume newline - let block_statement handle Dedent
        if !self.match_token(TokenType::Newline) && !self.check(TokenType::Dedent) && !self.is_at_end() {
            return Err("Expect newline after display value.".to_string());
        }
        
        Ok(Stmt::Print(PrintStmt { value }))
    }

    fn block_statement(&mut self) -> Result<BlockStmt, String> {
        let mut statements = Vec::new();

        while !self.check(TokenType::Dedent) && !self.is_at_end() {
            statements.push(self.declaration()?);
        }

        // Consume Dedent if present, otherwise we're at EOF
        if !self.is_at_end() {
            self.consume(TokenType::Dedent, "Expect dedent after block.")?;
        }
        
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

    // not_expression → "not" not_expression | "is not" expression | comparison_expression
    fn not_expression(&mut self) -> Result<Expr, String> {
        if self.match_token(TokenType::Not) {
            let operator = self.previous().clone();
            let right = self.not_expression()?;
            return Ok(Expr::Unary(UnaryExpr {
                operator,
                right: Box::new(right),
            }));
        }
        
        // Handle natural negation pattern: "is not active"
        if self.match_token(TokenType::IsNot) {
            let operator = self.previous().clone();
            let right = self.comparison_expression()?;
            return Ok(Expr::Unary(UnaryExpr {
                operator,
                right: Box::new(right),
            }));
        }
        self.comparison_expression()
    }

    // comparison_expression → additive_expression (comparison_op additive_expression)*
    fn comparison_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.concatenation_expression()?;

        while self.match_token(TokenType::IsEqualTo) 
            || self.match_token(TokenType::IsNotEqualTo)
            || self.match_token(TokenType::IsGreaterThan)
            || self.match_token(TokenType::IsLessThan)
            || self.match_token(TokenType::IsGreaterThanOrEqualTo)
            || self.match_token(TokenType::IsLessThanOrEqualTo)
        {
            let operator = self.previous().clone();
            let right = self.concatenation_expression()?;
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        Ok(expr)
    }
    
    // concatenation_expression → additive_expression (concatenation_op additive_expression)*
    fn concatenation_expression(&mut self) -> Result<Expr, String> {
        let mut expr = self.additive_expression()?;

        while self.match_token(TokenType::FollowedBy) {
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
        println!("DEBUG: Entering multiplicative_expression");
        let mut expr = self.unary_expression()?;
        println!("DEBUG: After unary_expression, current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);

        while self.match_token(TokenType::MultipliedBy) || self.match_token(TokenType::DividedBy) || self.match_token(TokenType::Modulo) {
            println!("DEBUG: Found multiplicative operator: {:?} '{}'", self.previous().token_type, self.previous().lexeme);
            let operator = self.previous().clone();
            let right = self.unary_expression()?;
            println!("DEBUG: After parsing right operand, current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
            expr = Expr::Binary(BinaryExpr {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
            });
        }

        println!("DEBUG: Exiting multiplicative_expression, current token: {:?} '{}'", self.peek().token_type, self.peek().lexeme);
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
        } else if self.match_token(TokenType::Is) {
            // Handle natural language boolean expressions: "is active", "is not active"
            if self.match_token(TokenType::Not) {
                // "is not active" - parse as boolean access with negation
                let variable_expr = self.primary_expression()?;
                let is_not_token = Token {
                    token_type: TokenType::IsNot,
                    lexeme: "is not".to_string(),
                    line: self.previous().line,
                    column: self.previous().column,
                };
                return Ok(Expr::Unary(UnaryExpr {
                    operator: is_not_token,
                    right: Box::new(variable_expr),
                }));
            } else {
                // "is active" - parse as boolean variable access
                let variable_expr = self.primary_expression()?;
                // For "is active", we treat it as just accessing the variable "active"
                // The "is" serves as a natural language marker but doesn't change semantics
                return Ok(variable_expr);
            }
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
            } else if self.match_token(TokenType::AtWord) {
                // Handle "my list at index 0" or "my dictionary at key name"
                expr = self.finish_natural_indexing(expr)?;
            } else {
                break;
            }
        }

        Ok(expr)
    }

    // primary_expression → literal | identifier | "(" expression ")"
    fn primary_expression(&mut self) -> Result<Expr, String> {
        if self.match_token(TokenType::Integer) {
            let token = self.previous();
            let int_val = token.lexeme.parse::<i64>().map_err(|_| "Invalid integer")?;
            Ok(Expr::Literal(LiteralExpr { value: runa_common::ast::LiteralValue::Integer(int_val) }))
        } else if self.match_token(TokenType::Float) {
            let token = self.previous();
            let float_val = token.lexeme.parse::<f64>().map_err(|_| "Invalid float")?;
            Ok(Expr::Literal(LiteralExpr { value: runa_common::ast::LiteralValue::Float(float_val) }))
        } else if self.match_token(TokenType::String) {
            let token = self.previous();
            Ok(Expr::Literal(LiteralExpr { value: runa_common::ast::LiteralValue::String(token.lexeme.clone()) }))
        } else if self.match_token(TokenType::InterpolatedString) {
            self.parse_interpolated_string()
        } else if self.match_token(TokenType::Boolean) {
            let token = self.previous();
            let bool_val = token.lexeme == "true";
            Ok(Expr::Literal(LiteralExpr { value: runa_common::ast::LiteralValue::Boolean(bool_val) }))
        } else if self.match_token(TokenType::List) {
            // Parse "list containing element1, element2, ..."
            self.consume(TokenType::Containing, "Expect 'containing' after 'list'.")?;
            
            let mut elements = Vec::new();
            
            // Parse elements
            if !self.check(TokenType::Newline) && !self.check(TokenType::Eof) {
                elements.push(self.expression()?);
                
                while self.match_token(TokenType::Comma) {
                    elements.push(self.expression()?);
                }
            }
            
            Ok(Expr::List(ListExpr { elements }))
        } else if self.match_token(TokenType::Dictionary) {
            // Parse "dictionary with: key as value, key as value, ..."
            self.consume(TokenType::With, "Expect 'with' after 'dictionary'.")?;
            self.consume(TokenType::Colon, "Expect ':' after 'dictionary with'.")?;
            
            // For now, create a simplified dictionary literal expression
            // In a full implementation, we'd have a DictionaryExpr variant
            // For the bootstrap, we'll create a simple placeholder
            
            // Skip parsing the dictionary contents for now - just consume until newline
            // This is a simplified implementation for the bootstrap compiler
            let mut entries = Vec::new();
            
            // Create placeholder dictionary expression using List variant
            // In production, this would be a proper DictionaryExpr
            Ok(Expr::List(ListExpr { elements: entries }))
        } else if self.match_token(TokenType::Get) {
            // Handle natural language indexing: "get item 2 from my list", "get first item from my list", etc.
            self.parse_natural_indexing()
        } else if self.match_token(TokenType::Call) || self.match_token(TokenType::Invoke) || self.match_token(TokenType::Execute) {
            // Handle natural language function calls: "call my function with arg1 and arg2"
            self.parse_natural_function_call()
        } else if self.match_token(TokenType::Identifier) {
            let mut ident_parts = vec![self.previous().lexeme.clone()];
            
            // Look ahead for multi-word identifiers
            // Keep collecting tokens that can be part of variable names
            while self.can_be_identifier_part() && !self.is_natural_operator_start() {
                self.advance();
                ident_parts.push(self.previous().lexeme.clone());
            }
            
            let multi_word_name = ident_parts.join(" ");
            println!("DEBUG: Parsed multi-word variable reference: '{}'", multi_word_name);
            
            // Create a combined token for the multi-word identifier
            let ident_token = Token {
                token_type: TokenType::Identifier,
                lexeme: multi_word_name,
                line: self.previous().line,
                column: self.previous().column,
            };
            
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

    fn finish_natural_indexing(&mut self, target: Expr) -> Result<Expr, String> {
        // We've already consumed "at"
        // Now we expect either "index" or "key"
        
        if self.match_token(TokenType::Index) {
            // Pattern: "my list at index 0"
            let index_expr = self.expression()?;
            Ok(Expr::Index(IndexAccessExpr {
                target: Box::new(target),
                index: Box::new(index_expr),
            }))
        } else if self.match_token(TokenType::Key) {
            // Pattern: "my dictionary at key name"
            let key_expr = self.expression()?;
            Ok(Expr::Index(IndexAccessExpr {
                target: Box::new(target),
                index: Box::new(key_expr),
            }))
        } else {
            Err("Expected 'index' or 'key' after 'at' in natural indexing.".to_string())
        }
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

    fn peek_ahead(&self, offset: usize) -> Option<&Token> {
        let index = self.current + offset;
        if index < self.tokens.len() {
            Some(&self.tokens[index])
        } else {
            None
        }
    }

    fn check(&self, token_type: TokenType) -> bool {
        // Simply check the type of the current token. Don't add extra logic.
        // The `peek` method should handle the "am I at the end?" question internally.
        self.peek().token_type == token_type
    }

    fn can_be_identifier_part(&self) -> bool {
        // Check if the current token can be part of a multi-word identifier
        match self.peek().token_type {
            TokenType::Identifier => true,
            // Allow certain keywords to be part of variable names
            TokenType::List | TokenType::Dictionary | TokenType::Key | TokenType::Value |
            TokenType::Item | TokenType::Index | TokenType::First | TokenType::Last |
            TokenType::Type | TokenType::A | TokenType::An | TokenType::The => true,
            _ => false,
        }
    }

    fn is_natural_operator_start(&self) -> bool {
        // Check if the current identifier starts a natural language operator
        // This prevents multi-word identifier parsing from consuming natural operators
        if !self.check(TokenType::Identifier) {
            return false;
        }
        
        let current_token = self.peek();
        match current_token.lexeme.as_str() {
            // Comparison operators
            "is" | "and" | "or" | "not" |
            // Arithmetic operators  
            "plus" | "minus" | "times" | "multiplied" | "divided" | "modulo" |
            // Other operators and keywords that shouldn't be part of variable names
            "to" | "by" | "with" | "as" | "in" | "from" | "that" | "takes" | "returns" |
            "called" | "containing" | "at" | "key" | "list" | "dictionary" => true,
            _ => {
                // Check for compound operators by looking ahead
                if current_token.lexeme == "greater" {
                    if let Some(next) = self.peek_ahead(1) {
                        return next.lexeme == "than";
                    }
                }
                if current_token.lexeme == "less" {
                    if let Some(next) = self.peek_ahead(1) {
                        return next.lexeme == "than";
                    }
                }
                if current_token.lexeme == "equal" {
                    if let Some(next) = self.peek_ahead(1) {
                        return next.lexeme == "to";
                    }
                }
                false
            }
        }
    }

    fn parse_interpolated_string(&mut self) -> Result<Expr, String> {
        let token = self.previous().clone();
        let content = &token.lexeme[1..token.lexeme.len()-1]; // Remove quotes
        
        let mut parts = Vec::new();
        let mut current_str = String::new();
        let mut chars = content.chars().peekable();
        
        while let Some(ch) = chars.next() {
            if ch == '{' {
                // Found start of interpolation
                if !current_str.is_empty() {
                    parts.push(InterpolatedStringPart::String(current_str.clone()));
                    current_str.clear();
                }
                
                // Parse the expression inside {}
                let mut expr_content = String::new();
                let mut brace_depth = 1;
                
                while let Some(expr_ch) = chars.next() {
                    if expr_ch == '{' {
                        brace_depth += 1;
                    } else if expr_ch == '}' {
                        brace_depth -= 1;
                        if brace_depth == 0 {
                            break;
                        }
                    }
                    expr_content.push(expr_ch);
                }
                
                // Parse the expression content as a mini Runa expression
                if !expr_content.is_empty() {
                    let expr = self.parse_expression_from_string(&expr_content)?;
                    parts.push(InterpolatedStringPart::Expression(Box::new(expr)));
                }
            } else {
                current_str.push(ch);
            }
        }
        
        // Add any remaining string content
        if !current_str.is_empty() {
            parts.push(InterpolatedStringPart::String(current_str));
        }
        
        Ok(Expr::InterpolatedString(InterpolatedStringExpr { parts }))
    }

    fn parse_expression_from_string(&mut self, content: &str) -> Result<Expr, String> {
        // For now, we'll implement simple variable references
        // In a full implementation, we'd need to tokenize and parse the content
        let trimmed = content.trim();
        
        // Simple case: just a variable name
        if trimmed.chars().all(|c| c.is_alphanumeric() || c == '_' || c == ' ') {
            // Handle multi-word identifiers
            Ok(Expr::Variable(VariableExpr {
                name: Token {
                    token_type: TokenType::Identifier,
                    lexeme: trimmed.to_string(),
                    line: 0, // We don't have line info here
                    column: 0,
                }
            }))
        } else {
            Err(format!("Complex expressions in string interpolation not yet supported: '{}'", content))
        }
    }

    fn parse_identifier(&mut self) -> Result<String, String> {
        if self.match_token(TokenType::Identifier) {
            Ok(self.previous().lexeme.clone())
        } else {
            Err("Expect identifier.".to_string())
        }
    }

    fn parse_type_annotation(&mut self) -> Result<RunaType, String> {
        if self.match_token(TokenType::Identifier) {
            let type_name = self.previous().lexeme.clone();
            
            // Check for generic type like List[Integer]
            if self.match_token(TokenType::LBracket) {
                // Parse inner type
                let inner_type = self.parse_type_annotation()?;
                self.consume(TokenType::RBracket, "Expect ']' after generic type parameter.")?;
                
                match type_name.as_str() {
                    "List" => Ok(RunaType::List(Box::new(inner_type))),
                    "Dict" | "Dictionary" => {
                        // For Dictionary, we need a second type parameter (key, value)
                        // For now, assume String keys
                        Ok(RunaType::Dictionary {
                            key: Box::new(RunaType::String),
                            value: Box::new(inner_type),
                        })
                    },
                    _ => Err(format!("Unknown generic type: {}", type_name)),
                }
            } else {
                // Simple type
                match type_name.as_str() {
                    "Int" => Ok(RunaType::Integer),
                    "Integer" => Ok(RunaType::Integer),
                    "Float" => Ok(RunaType::Float),
                    "String" => Ok(RunaType::String),
                    "Boolean" => Ok(RunaType::Boolean),
                    "Dynamic" => Ok(RunaType::Any),
                    _ => Err(format!("Unknown type: {}", type_name)),
                }
            }
        } else {
            Err("Expect type name after 'as'.".to_string())
        }
    }

    fn note_comment(&mut self) -> Result<Stmt, String> {
        // Consume the colon after "Note"
        self.consume(TokenType::Colon, "Expect ':' after 'Note'.")?;
        
        let mut comment_content = String::new();
        let mut is_multiline = false;
        
        // Check if this is a single-line comment (has content on same line)
        // or multi-line comment (Note: followed by newline)
        if self.check(TokenType::Newline) {
            // Multi-line comment: Note: followed immediately by newline
            is_multiline = true;
            self.advance(); // consume the newline
            
            // Parse multi-line content until ":End Note"
            while !self.is_at_end() {
                // Check for ":End Note" pattern
                if self.check(TokenType::Colon) {
                    let colon_pos = self.current;
                    self.advance(); // consume ':'
                    
                    if self.check(TokenType::End) {
                        self.advance(); // consume 'End'
                        if self.check(TokenType::Note) {
                            self.advance(); // consume 'Note'
                            // Found ":End Note" - end of multi-line comment
                            break;
                        } else {
                            // False alarm, backtrack and include the colon and End in content
                            self.current = colon_pos;
                            let token = self.advance();
                            if !comment_content.is_empty() {
                                comment_content.push(' ');
                            }
                            comment_content.push_str(&token.lexeme);
                        }
                    } else {
                        // False alarm, backtrack and include the colon in content  
                        self.current = colon_pos;
                        let token = self.advance();
                        if !comment_content.is_empty() {
                            comment_content.push(' ');
                        }
                        comment_content.push_str(&token.lexeme);
                    }
                } else {
                    // Regular content token
                    let token = self.advance();
                    if !comment_content.is_empty() && !comment_content.ends_with('\n') {
                        if token.token_type == TokenType::Newline {
                            comment_content.push('\n');
                        } else {
                            comment_content.push(' ');
                        }
                    }
                    if token.token_type != TokenType::Newline {
                        comment_content.push_str(&token.lexeme);
                    } else {
                        comment_content.push('\n');
                    }
                }
            }
        } else {
            // Single-line comment: consume all tokens until newline
            while !self.is_at_end() && !self.check(TokenType::Newline) && !self.check(TokenType::Eof) {
                let token = self.advance();
                if !comment_content.is_empty() {
                    comment_content.push(' ');
                }
                comment_content.push_str(&token.lexeme);
            }
            
            // Consume the newline if present
            if self.match_token(TokenType::Newline) {
                // Newline consumed
            }
        }
        
        // Create an annotation statement to represent the note comment
        let comment_type = if is_multiline { "MultilineComment" } else { "Comment" };
        Ok(Stmt::Annotation(AnnotationStmt {
            annotation_type: "Context".to_string(),
            content: format!("{}: {}", comment_type, comment_content.trim()),
            location: runa_common::annotations::SourceLocation {
                start_line: 0,
                start_column: 0,
                end_line: 0,
                end_column: 0,
                file_path: Some("current".to_string()),
            },
        }))
    }

    // Helper function to check for and parse inline Note comments
    fn try_parse_inline_comment(&mut self) -> Option<String> {
        // Check if we have "Note:" after some content on the same line
        if self.check(TokenType::Note) {
            let note_pos = self.current;
            self.advance(); // consume 'Note'
            
            if self.check(TokenType::Colon) {
                self.advance(); // consume ':'
                
                let mut comment_content = String::new();
                // Consume rest of line as inline comment
                while !self.is_at_end() && !self.check(TokenType::Newline) && !self.check(TokenType::Eof) {
                    let token = self.advance();
                    if !comment_content.is_empty() {
                        comment_content.push(' ');
                    }
                    comment_content.push_str(&token.lexeme);
                }
                
                Some(comment_content.trim().to_string())
            } else {
                // Not a Note: comment, backtrack
                self.current = note_pos;
                None
            }
        } else {
            None
        }
    }

    fn check_annotation_start(&self) -> bool {
        matches!(
            self.peek().token_type,
            TokenType::AtReasoning
                | TokenType::AtImplementation
                | TokenType::AtUncertainty
                | TokenType::AtRequestClarification
                | TokenType::AtKnowledgeReference
                | TokenType::AtTestCases
                | TokenType::AtResourceConstraints
                | TokenType::AtSecurityScope
                | TokenType::AtExecutionModel
                | TokenType::AtPerformanceHints
                | TokenType::AtProgress
                | TokenType::AtFeedback
                | TokenType::AtTranslationNote
                | TokenType::AtErrorHandling
        )
    }

    fn annotation_declaration(&mut self) -> Result<Stmt, String> {
        let start_token = self.advance().clone();
        let annotation_type = self.get_annotation_type(&start_token.token_type)?;
        
        // Parse the annotation content until we find the end token
        let mut content = String::new();
        let mut structured_data = std::collections::HashMap::new();
        
        // Consume the colon after the annotation type
        if self.match_token(TokenType::Colon) {
            // Parse the content until we find the end token
            while !self.is_at_end() && !self.check_annotation_end(&annotation_type) {
                let token = self.advance();
                content.push_str(&token.lexeme);
                content.push(' ');
            }
        }
        
        // Consume the end token
        let end_token_type = self.get_end_token_type(&annotation_type)?;
        self.consume(end_token_type, &format!("Expect end token for {:?}", annotation_type))?;
        
        // Consume any trailing whitespace after the end token
        while self.match_token(TokenType::Newline) || self.match_token(TokenType::Indent) || self.match_token(TokenType::Dedent) {}
        
        // Create source location
        let location = runa_common::annotations::SourceLocation::new(
            start_token.line,
            start_token.column,
            self.previous().line,
            self.previous().column,
        );
        
        // Parse structured data from content
        structured_data = self.parse_annotation_structured_data(&content, &annotation_type)?;
        
        Ok(Stmt::Annotation(runa_common::ast::AnnotationStmt {
            annotation_type: format!("{:?}", annotation_type),
            content: content.trim().to_string(),
            location,
        }))
    }

    fn get_annotation_type(&self, token_type: &TokenType) -> Result<runa_common::annotations::AnnotationType, String> {
        match token_type {
            TokenType::AtReasoning => Ok(runa_common::annotations::AnnotationType::Reasoning),
            TokenType::AtImplementation => Ok(runa_common::annotations::AnnotationType::Implementation),
            TokenType::AtUncertainty => Ok(runa_common::annotations::AnnotationType::Uncertainty),
            TokenType::AtRequestClarification => Ok(runa_common::annotations::AnnotationType::RequestClarification),
            TokenType::AtKnowledgeReference => Ok(runa_common::annotations::AnnotationType::KnowledgeReference),
            TokenType::AtTestCases => Ok(runa_common::annotations::AnnotationType::TestCases),
            TokenType::AtResourceConstraints => Ok(runa_common::annotations::AnnotationType::ResourceConstraints),
            TokenType::AtSecurityScope => Ok(runa_common::annotations::AnnotationType::SecurityScope),
            TokenType::AtExecutionModel => Ok(runa_common::annotations::AnnotationType::ExecutionModel),
            TokenType::AtPerformanceHints => Ok(runa_common::annotations::AnnotationType::PerformanceHints),
            TokenType::AtProgress => Ok(runa_common::annotations::AnnotationType::Progress),
            TokenType::AtFeedback => Ok(runa_common::annotations::AnnotationType::Feedback),
            TokenType::AtTranslationNote => Ok(runa_common::annotations::AnnotationType::TranslationNote),
            TokenType::AtErrorHandling => Ok(runa_common::annotations::AnnotationType::ErrorHandling),
            TokenType::AtRequest => Ok(runa_common::annotations::AnnotationType::Request),
            TokenType::AtContext => Ok(runa_common::annotations::AnnotationType::Context),
            TokenType::AtTask => Ok(runa_common::annotations::AnnotationType::Task),
            TokenType::AtRequirements => Ok(runa_common::annotations::AnnotationType::Requirements),
            TokenType::AtVerify => Ok(runa_common::annotations::AnnotationType::Verify),
            TokenType::AtCollaboration => Ok(runa_common::annotations::AnnotationType::Collaboration),
            TokenType::AtIteration => Ok(runa_common::annotations::AnnotationType::Iteration),
            TokenType::AtClarification => Ok(runa_common::annotations::AnnotationType::Clarification),
            _ => Err(format!("Unknown annotation type: {:?}", token_type)),
        }
    }

    fn get_end_token_type(&self, annotation_type: &runa_common::annotations::AnnotationType) -> Result<TokenType, String> {
        match annotation_type {
            runa_common::annotations::AnnotationType::Reasoning => Ok(TokenType::AtEndReasoning),
            runa_common::annotations::AnnotationType::Implementation => Ok(TokenType::AtEndImplementation),
            runa_common::annotations::AnnotationType::Uncertainty => Ok(TokenType::AtEndUncertainty),
            runa_common::annotations::AnnotationType::RequestClarification => Ok(TokenType::AtEndRequestClarification),
            runa_common::annotations::AnnotationType::KnowledgeReference => Ok(TokenType::AtEndKnowledgeReference),
            runa_common::annotations::AnnotationType::TestCases => Ok(TokenType::AtEndTestCases),
            runa_common::annotations::AnnotationType::ResourceConstraints => Ok(TokenType::AtEndResourceConstraints),
            runa_common::annotations::AnnotationType::SecurityScope => Ok(TokenType::AtEndSecurityScope),
            runa_common::annotations::AnnotationType::ExecutionModel => Ok(TokenType::AtEndExecutionModel),
            runa_common::annotations::AnnotationType::PerformanceHints => Ok(TokenType::AtEndPerformanceHints),
            runa_common::annotations::AnnotationType::Progress => Ok(TokenType::AtEndProgress),
            runa_common::annotations::AnnotationType::Feedback => Ok(TokenType::AtEndFeedback),
            runa_common::annotations::AnnotationType::TranslationNote => Ok(TokenType::AtEndTranslationNote),
            runa_common::annotations::AnnotationType::ErrorHandling => Ok(TokenType::AtEndErrorHandling),
            runa_common::annotations::AnnotationType::Request => Ok(TokenType::AtEndRequest),
            runa_common::annotations::AnnotationType::Context => Ok(TokenType::AtEndContext),
            runa_common::annotations::AnnotationType::Task => Ok(TokenType::AtEndTask),
            runa_common::annotations::AnnotationType::Requirements => Ok(TokenType::AtEndRequirements),
            runa_common::annotations::AnnotationType::Verify => Ok(TokenType::AtEndVerify),
            runa_common::annotations::AnnotationType::Collaboration => Ok(TokenType::AtEndCollaboration),
            runa_common::annotations::AnnotationType::Iteration => Ok(TokenType::AtEndIteration),
            runa_common::annotations::AnnotationType::Clarification => Ok(TokenType::AtEndClarification),
        }
    }

    fn check_annotation_end(&self, annotation_type: &runa_common::annotations::AnnotationType) -> bool {
        let end_token_type = match self.get_end_token_type(annotation_type) {
            Ok(token_type) => token_type,
            Err(_) => return false,
        };
        self.check(end_token_type)
    }

    fn parse_annotation_structured_data(
        &self,
        content: &str,
        annotation_type: &runa_common::annotations::AnnotationType,
    ) -> Result<std::collections::HashMap<String, serde_json::Value>, String> {
        let mut structured_data = std::collections::HashMap::new();
        
        // For now, we'll do basic parsing. In a full implementation,
        // this would parse the content into structured data based on the annotation type.
        match annotation_type {
            runa_common::annotations::AnnotationType::Uncertainty => {
                // Parse uncertainty expressions like "?[option1, option2] with confidence 0.8"
                if let Some(confidence_match) = content.find("confidence") {
                    if let Some(value_start) = content[confidence_match..].find(char::is_numeric) {
                        if let Ok(confidence) = content[confidence_match + value_start..]
                            .split_whitespace()
                            .next()
                            .unwrap_or("0.5")
                            .parse::<f64>()
                        {
                            structured_data.insert("confidence".to_string(), serde_json::Value::Number(serde_json::Number::from_f64(confidence).unwrap()));
                        }
                    }
                }
            }
            runa_common::annotations::AnnotationType::ResourceConstraints => {
                // Parse resource constraints like "memory_limit: 256MB"
                for line in content.lines() {
                    if let Some(colon_pos) = line.find(':') {
                        let key = line[..colon_pos].trim().to_string();
                        let value = line[colon_pos + 1..].trim().to_string();
                        structured_data.insert(key, serde_json::Value::String(value));
                    }
                }
            }
            _ => {
                // For other annotation types, store the raw content
                structured_data.insert("content".to_string(), serde_json::Value::String(content.to_string()));
            }
        }
        
        Ok(structured_data)
    }

    // Parse natural language indexing expressions like:
    // "get item 2 from my list"
    // "get first item from my list"
    // "get last item from my list"
    // "get value for key name from my dictionary"
    fn parse_natural_indexing(&mut self) -> Result<Expr, String> {
        // We've already consumed "get"
        
        // Handle ordinal patterns first: "get first item", "get last item"
        if self.match_token(TokenType::First) {
            // Pattern: "get first item from COLLECTION"
            self.consume(TokenType::Item, "Expect 'item' after 'first'.")?;
            self.consume(TokenType::From, "Expect 'from' after 'first item'.")?;
            
            let collection = self.expression()?;
            let first_index = Expr::Literal(LiteralExpr {
                value: runa_common::ast::LiteralValue::Integer(0)
            });
            
            Ok(Expr::Index(IndexAccessExpr {
                target: Box::new(collection),
                index: Box::new(first_index),
            }))
        } else if self.match_token(TokenType::Last) {
            // Pattern: "get last item from COLLECTION"
            self.consume(TokenType::Item, "Expect 'item' after 'last'.")?;
            self.consume(TokenType::From, "Expect 'from' after 'last item'.")?;
            
            let collection = self.expression()?;
            let last_index = Expr::Literal(LiteralExpr {
                value: runa_common::ast::LiteralValue::Integer(-1)
            });
            
            Ok(Expr::Index(IndexAccessExpr {
                target: Box::new(collection),
                index: Box::new(last_index),
            }))
        } else if self.match_token(TokenType::Item) {
            // Pattern: "get item INDEX from COLLECTION"
            let index_expr = self.expression()?;
            
            // Consume "from"
            self.consume(TokenType::From, "Expect 'from' after item index in natural indexing.")?;
            
            // Parse the collection expression
            let collection = self.expression()?;
            
            Ok(Expr::Index(IndexAccessExpr {
                target: Box::new(collection),
                index: Box::new(index_expr),
            }))
        } else if self.match_token(TokenType::Value) {
            // Pattern: "get value for key KEY from DICTIONARY"
            self.consume(TokenType::For, "Expect 'for' after 'value' in dictionary access.")?;
            self.consume(TokenType::Key, "Expect 'key' after 'for' in dictionary access.")?;
            
            // Parse the key expression
            let key_expr = self.expression()?;
            
            // Consume "from"
            self.consume(TokenType::From, "Expect 'from' after key in dictionary access.")?;
            
            // Parse the dictionary expression
            let dictionary = self.expression()?;
            
            Ok(Expr::Index(IndexAccessExpr {
                target: Box::new(dictionary),
                index: Box::new(key_expr),
            }))
        } else {
            Err("Expected 'first', 'last', 'item', or 'value' after 'get' in natural indexing.".to_string())
        }
    }
    
    fn parse_natural_function_call(&mut self) -> Result<Expr, String> {
        // We've already consumed "call", "invoke", or "execute"
        let call_type = self.previous().clone();
        
        // Parse the function name (can be multi-word)
        let mut function_name_parts = Vec::new();
        
        if !self.check(TokenType::Identifier) {
            return Err(format!("Expected function name after '{}'.", call_type.lexeme));
        }
        
        // Collect multi-word function name
        while self.check(TokenType::Identifier) || self.can_be_identifier_part() {
            if self.check(TokenType::With) {
                // Stop if we encounter "with" as it indicates start of parameters
                break;
            }
            self.advance();
            function_name_parts.push(self.previous().lexeme.clone());
        }
        
        let function_name = function_name_parts.join(" ");
        
        // Create function name token
        let function_token = Token {
            token_type: TokenType::Identifier,
            lexeme: function_name,
            line: call_type.line,
            column: call_type.column,
        };
        
        // Parse arguments
        let mut arguments = Vec::new();
        
        if self.match_token(TokenType::With) {
            // Pattern: "call function with arg1 and arg2"
            // Parse first argument
            arguments.push(self.expression()?);
            
            // Parse additional arguments separated by "and"
            while self.match_token(TokenType::And) {
                arguments.push(self.expression()?);
            }
        }
        // If no "with" is found, it's a function call with no arguments
        
        // Create CallExpr node
        Ok(Expr::Call(CallExpr {
            callee: Box::new(Expr::Variable(VariableExpr { name: function_token })),
            arguments,
            paren: call_type, // Use the original call token as the paren token
        }))
    }
} 