use anyhow::{anyhow, Result};
use crate::lexer::{Token, TokenType};
use crate::types::Type;

#[derive(Debug, Clone)]
pub struct Program {
    pub items: Vec<Item>,
}

#[derive(Debug, Clone)]
pub enum Item {
    Function(Function),
    TypeDef(TypeDefinition),
    Import(ImportStatement),
}

#[derive(Debug, Clone)]
pub struct Function {
    pub name: String,
    pub parameters: Vec<Parameter>,
    pub return_type: Type,
    pub body: Block,
}

#[derive(Debug, Clone)]
pub struct Parameter {
    pub name: String,
    pub param_type: Type,
}

#[derive(Debug, Clone)]
pub struct TypeDefinition {
    pub name: String,
    pub kind: TypeDefinitionKind,
}

#[derive(Debug, Clone)]
pub enum TypeDefinitionKind {
    Struct { fields: Vec<Field> },
    Enum { variants: Vec<EnumVariant> },
}

#[derive(Debug, Clone)]
pub struct EnumVariant {
    pub name: String,
    pub data_type: Option<Type>,
}

#[derive(Debug, Clone)]
pub struct Field {
    pub name: String,
    pub field_type: Type,
}

#[derive(Debug, Clone)]
pub struct ImportStatement {
    pub path: String,
    pub alias: Option<String>,
}

#[derive(Debug, Clone)]
pub struct Block {
    pub statements: Vec<Statement>,
}

#[derive(Debug, Clone)]
pub enum Statement {
    Let(LetStatement),
    Set(SetStatement),
    If(IfStatement),
    While(WhileStatement),
    ForEach(ForEachStatement),
    Return(ReturnStatement),
    WriteFile(WriteFileStatement),
    AddToList(AddToListStatement),
    Match(MatchStatement),
    Expression(Expression),
}

#[derive(Debug, Clone)]
pub struct MatchStatement {
    pub expression: Expression,
    pub cases: Vec<MatchCase>,
}

#[derive(Debug, Clone)]
pub struct MatchCase {
    pub pattern: Expression,
    pub body: Block,
}

#[derive(Debug, Clone)]
pub struct AddToListStatement {
    pub value: Expression,
    pub list: Expression,
}

#[derive(Debug, Clone)]
pub struct LetStatement {
    pub name: String,
    pub value: Expression,
}

#[derive(Debug, Clone)]
pub struct SetStatement {
    pub target: Expression,
    pub value: Expression,
}

#[derive(Debug, Clone)]
pub struct IfStatement {
    pub condition: Expression,
    pub then_block: Block,
    pub else_if_branches: Vec<ElseIfBranch>,
    pub else_block: Option<Block>,
}

#[derive(Debug, Clone)]
pub struct ElseIfBranch {
    pub condition: Expression,
    pub block: Block,
}

#[derive(Debug, Clone)]
pub struct WhileStatement {
    pub condition: Expression,
    pub body: Block,
}

#[derive(Debug, Clone)]
pub struct ForEachStatement {
    pub variable: String,
    pub collection: Expression,
    pub body: Block,
}

#[derive(Debug, Clone)]
pub struct ReturnStatement {
    pub value: Option<Expression>,
}

#[derive(Debug, Clone)]
pub struct WriteFileStatement {
    pub content: Expression,
    pub filename: Expression,
}

#[derive(Debug, Clone)]
pub enum Expression {
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),
    Identifier(String),
    Binary(Box<BinaryExpression>),
    Unary(Box<UnaryExpression>),
    Call(Box<CallExpression>),
    MethodCall(Box<MethodCallExpression>),
    FieldAccess(Box<FieldAccessExpression>),
    ListLiteral(Vec<Expression>),
    DictionaryLiteral(Vec<(Expression, Expression)>),
    ArrayLiteral(Vec<Expression>),
    IndexAccess(Box<IndexAccessExpression>),
    LengthOf(Box<Expression>),
    TypeConstruction(Box<TypeConstructionExpression>),
    Nothing,
}

#[derive(Debug, Clone)]
pub struct TypeConstructionExpression {
    pub type_name: String,
    pub fields: Vec<(String, Expression)>,
}

#[derive(Debug, Clone)]
pub struct BinaryExpression {
    pub left: Expression,
    pub operator: BinaryOperator,
    pub right: Expression,
}

#[derive(Debug, Clone)]
pub enum BinaryOperator {
    Plus,
    Minus,
    MultipliedBy,
    DividedBy,
    IsGreaterThan,
    IsLessThan,
    IsEqualTo,
    IsNotEqualTo,
    And,
    Or,
}

#[derive(Debug, Clone)]
pub struct UnaryExpression {
    pub operator: UnaryOperator,
    pub operand: Expression,
}

#[derive(Debug, Clone)]
pub enum UnaryOperator {
    Not,
}

#[derive(Debug, Clone)]
pub struct CallExpression {
    pub function: String,
    pub arguments: Vec<Expression>,
}

#[derive(Debug, Clone)]
pub struct FieldAccessExpression {
    pub object: Expression,
    pub field: String,
}

#[derive(Debug, Clone)]
pub struct IndexAccessExpression {
    pub object: Expression,
    pub index: Expression,
}

#[derive(Debug, Clone)]
pub struct MethodCallExpression {
    pub object: Expression,
    pub method: String,
    pub arguments: Vec<Expression>,
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

    pub fn parse(&mut self) -> Result<Program> {
        let mut items = Vec::new();

        while !self.is_at_end() {
            let item = self.parse_item()?;
            if let Some(i) = item {
                items.push(i);
            }
        }

        Ok(Program { items })
    }

    fn parse_item(&mut self) -> Result<Option<Item>> {
        match &self.peek().token_type {
            TokenType::Process => Ok(Some(Item::Function(self.parse_function()?))),
            TokenType::Type => Ok(Some(Item::TypeDef(self.parse_type_definition()?))),
            TokenType::Import => Ok(Some(Item::Import(self.parse_import()?))),
            TokenType::Eof => Ok(None),
            _ => Err(anyhow!("Unexpected token at top level: {:?}", self.peek())),
        }
    }

    fn parse_function(&mut self) -> Result<Function> {
        self.consume(TokenType::Process)?;
        self.consume(TokenType::Called)?;

        let name = self.consume_identifier_or_string()?;

        let mut parameters = Vec::new();
        if self.check(&TokenType::That) {
            self.advance();
            self.consume(TokenType::Takes)?;
            parameters = self.parse_parameters()?;
        }

        let return_type = if self.check(&TokenType::Returns) {
            self.advance();
            self.parse_type()?
        } else {
            Type::Void
        };

        self.consume(TokenType::Colon)?;

        let body = self.parse_block("Process")?;

        Ok(Function {
            name,
            parameters,
            return_type,
            body,
        })
    }

    fn parse_parameters(&mut self) -> Result<Vec<Parameter>> {
        let mut parameters = Vec::new();

        loop {
            let name = self.consume_identifier()?;
            self.consume(TokenType::As)?;
            let param_type = self.parse_type()?;

            parameters.push(Parameter {
                name,
                param_type,
            });

            if !self.check(&TokenType::Comma) {
                break;
            }
            self.advance();
        }

        Ok(parameters)
    }

    fn parse_type(&mut self) -> Result<Type> {
        match &self.peek().token_type {
            TokenType::Identifier(name) => {
                let type_name = name.clone();
                self.advance();
                match type_name.as_str() {
                    "Integer" => Ok(Type::Integer),
                    "Float" => Ok(Type::Float),
                    "String" => Ok(Type::String),
                    "Boolean" => Ok(Type::Boolean),
                    "Nothing" => Ok(Type::Void),
                    _ => Ok(Type::Custom(type_name)),
                }
            },
            TokenType::List => {
                self.advance();
                if self.peek().token_type == TokenType::LeftBracket {
                    self.consume(TokenType::LeftBracket)?;
                    let element_type = self.parse_type()?;
                    self.consume(TokenType::RightBracket)?;
                    Ok(Type::List(Box::new(element_type)))
                } else {
                    Ok(Type::Custom("List".to_string()))
                }
            },
            TokenType::Array => {
                self.advance();
                if self.peek().token_type == TokenType::LeftBracket {
                    self.consume(TokenType::LeftBracket)?;
                    let element_type = self.parse_type()?;
                    self.consume(TokenType::Comma)?;
                    let size_token = self.consume_integer()?;
                    let size = size_token.parse::<usize>()
                        .map_err(|_| anyhow!("Invalid array size: {}", size_token))?;
                    self.consume(TokenType::RightBracket)?;
                    Ok(Type::Array(Box::new(element_type), size))
                } else {
                    Ok(Type::Custom("Array".to_string()))
                }
            },
            TokenType::Dictionary => {
                self.advance();
                if self.peek().token_type == TokenType::LeftBracket {
                    self.consume(TokenType::LeftBracket)?;
                    let key_type = self.parse_type()?;
                    self.consume(TokenType::Comma)?;
                    let value_type = self.parse_type()?;
                    self.consume(TokenType::RightBracket)?;
                    Ok(Type::Dictionary(Box::new(key_type), Box::new(value_type)))
                } else {
                    Ok(Type::Custom("Dictionary".to_string()))
                }
            },
            _ => Err(anyhow!("Expected type name, got {:?}", self.peek())),
        }
    }

    fn parse_type_definition(&mut self) -> Result<TypeDefinition> {
        self.consume(TokenType::Type)?;

        if self.check(&TokenType::Called) {
            // Struct syntax: Type called "Name":
            self.consume(TokenType::Called)?;
            let name = self.consume_identifier_or_string()?;
            self.consume(TokenType::Colon)?;

            let mut fields = Vec::new();
            while !self.check_end("Type") {
                let field_name = self.consume_identifier()?;
                self.consume(TokenType::As)?;
                let field_type = self.parse_type()?;

                fields.push(Field {
                    name: field_name,
                    field_type,
                });
            }

            self.consume_end("Type")?;

            Ok(TypeDefinition {
                name,
                kind: TypeDefinitionKind::Struct { fields }
            })
        } else {
            // Enum syntax: Type Name is:
            let name = self.consume_identifier()?;
            self.consume(TokenType::Is)?;
            self.consume(TokenType::Colon)?;

            let mut variants = Vec::new();
            while !self.check_end("Type") {
                if self.check(&TokenType::Pipe) {
                    self.consume(TokenType::Pipe)?;
                }

                let variant_name = self.consume_identifier()?;

                // Check for optional data type: | VariantWithData as String
                let data_type = if self.check(&TokenType::As) {
                    self.consume(TokenType::As)?;
                    Some(self.parse_type()?)
                } else {
                    None
                };

                variants.push(EnumVariant {
                    name: variant_name,
                    data_type,
                });
            }

            self.consume_end("Type")?;

            Ok(TypeDefinition {
                name,
                kind: TypeDefinitionKind::Enum { variants }
            })
        }
    }

    fn parse_import(&mut self) -> Result<ImportStatement> {
        self.consume(TokenType::Import)?;

        let path = self.consume_string()?;

        let alias = if self.check(&TokenType::As) {
            self.advance();
            Some(self.consume_identifier()?)
        } else {
            None
        };

        Ok(ImportStatement { path, alias })
    }

    fn parse_block(&mut self, end_keyword: &str) -> Result<Block> {
        let mut statements = Vec::new();

        while !self.check_end(end_keyword) {
            if self.is_at_end() {
                return Err(anyhow!("Unexpected end of file, expected 'End {}'", end_keyword));
            }

            if let Some(stmt) = self.parse_statement()? {
                statements.push(stmt);
            } else if !self.check_end(end_keyword) {
                // If we got None but we're not at the end, something is wrong
                return Err(anyhow!("Unexpected token in block: {:?}", self.peek()));
            }
        }

        self.consume_end(end_keyword)?;

        Ok(Block { statements })
    }

    fn parse_statement(&mut self) -> Result<Option<Statement>> {
        match &self.peek().token_type {
            TokenType::Let => Ok(Some(Statement::Let(self.parse_let()?))),
            TokenType::Set => Ok(Some(Statement::Set(self.parse_set()?))),
            TokenType::If => Ok(Some(Statement::If(self.parse_if()?))),
            TokenType::While => Ok(Some(Statement::While(self.parse_while()?))),
            TokenType::For => Ok(Some(Statement::ForEach(self.parse_for_each()?))),
            TokenType::Return => Ok(Some(Statement::Return(self.parse_return()?))),
            TokenType::WriteFile => Ok(Some(Statement::WriteFile(self.parse_write_file()?))),
            TokenType::Add => Ok(Some(Statement::AddToList(self.parse_add_to_list()?))),
            TokenType::Match => Ok(Some(Statement::Match(self.parse_match()?))),
            TokenType::Eof | TokenType::End => Ok(None),
            _ => Ok(Some(Statement::Expression(self.parse_expression()?))),
        }
    }

    fn parse_let(&mut self) -> Result<LetStatement> {
        self.consume(TokenType::Let)?;
        let name = self.consume_identifier()?;
        self.consume(TokenType::Be)?;

        // Check for collection literals
        let value = if let TokenType::Identifier(s) = &self.peek().token_type {
            if s == "a" {
                self.advance(); // consume "a"
                if self.check(&TokenType::List) {
                    self.advance();
                    self.consume(TokenType::Containing)?;
                    self.parse_list_literal()?
                } else if self.check(&TokenType::Dictionary) {
                    self.advance();
                    self.consume(TokenType::Containing)?;
                    self.consume(TokenType::Colon)?;
                    self.parse_dictionary_literal()?
                } else if self.check(&TokenType::Array) {
                    self.advance();
                    self.consume(TokenType::Of)?;
                    // Parse array type and size
                    let size = if let TokenType::Integer(n) = self.peek().token_type {
                        let size = n as usize;
                        self.advance();
                        size
                    } else {
                        return Err(anyhow!("Expected array size"));
                    };
                    // Skip type name for now, arrays are homogeneous
                    self.consume_identifier()?;
                    Expression::ArrayLiteral(vec![Expression::Integer(0); size])
                } else if let TokenType::Identifier(id) = &self.peek().token_type {
                    if id == "value" {
                        self.advance(); // consume "value"
                        self.consume(TokenType::Of)?;
                        self.consume(TokenType::Type)?;
                        let type_name = self.consume_identifier()?;

                        // Check if there are field initializers
                        let fields = if let TokenType::Identifier(w) = &self.peek().token_type {
                            if w == "with" {
                                self.advance(); // consume "with"
                                self.parse_type_construction_fields()?
                            } else {
                                Vec::new()
                            }
                        } else {
                            Vec::new()
                        };

                        Expression::TypeConstruction(Box::new(TypeConstructionExpression {
                            type_name,
                            fields,
                        }))
                    } else {
                        return Err(anyhow!("Expected 'list', 'dictionary', 'array', or 'value' after 'a'"));
                    }
                } else {
                    return Err(anyhow!("Expected 'list', 'dictionary', 'array', or 'value' after 'a'"));
                }
            } else {
                self.parse_expression()?
            }
        } else if self.check(&TokenType::Length) {
            self.advance();
            self.consume(TokenType::Of)?;
            let expr = self.parse_expression()?;
            Expression::LengthOf(Box::new(expr))
        } else {
            self.parse_expression()?
        };

        Ok(LetStatement { name, value })
    }

    fn parse_set(&mut self) -> Result<SetStatement> {
        self.consume(TokenType::Set)?;
        let target = self.parse_primary()?;
        self.consume(TokenType::To)?;
        let value = self.parse_expression()?;

        Ok(SetStatement { target, value })
    }

    fn parse_if(&mut self) -> Result<IfStatement> {
        self.consume(TokenType::If)?;
        let condition = self.parse_expression()?;
        self.consume(TokenType::Colon)?;

        let mut then_statements = Vec::new();
        while !self.check(&TokenType::Otherwise) && !self.check_end("If") {
            if let Some(stmt) = self.parse_statement()? {
                then_statements.push(stmt);
            }
        }

        let mut else_if_branches = Vec::new();
        let mut else_block = None;

        // Parse Otherwise If branches
        while self.check(&TokenType::Otherwise) {
            self.advance(); // consume 'Otherwise'

            if self.check(&TokenType::If) {
                // This is an 'Otherwise If' branch
                self.advance(); // consume 'If'
                let else_if_condition = self.parse_expression()?;
                self.consume(TokenType::Colon)?;

                let mut else_if_statements = Vec::new();
                while !self.check(&TokenType::Otherwise) && !self.check_end("If") {
                    if let Some(stmt) = self.parse_statement()? {
                        else_if_statements.push(stmt);
                    }
                }

                else_if_branches.push(ElseIfBranch {
                    condition: else_if_condition,
                    block: Block { statements: else_if_statements },
                });
            } else {
                // This is a final 'Otherwise' clause
                self.consume(TokenType::Colon)?;
                let mut else_statements = Vec::new();
                while !self.check_end("If") {
                    if let Some(stmt) = self.parse_statement()? {
                        else_statements.push(stmt);
                    }
                }
                else_block = Some(Block { statements: else_statements });
                break; // Final else clause, no more branches
            }
        }

        self.consume_end("If")?;

        Ok(IfStatement {
            condition,
            then_block: Block { statements: then_statements },
            else_if_branches,
            else_block,
        })
    }

    fn parse_while(&mut self) -> Result<WhileStatement> {
        self.consume(TokenType::While)?;
        let condition = self.parse_expression()?;
        self.consume(TokenType::Colon)?;
        let body = self.parse_block("While")?;

        Ok(WhileStatement { condition, body })
    }

    fn parse_for_each(&mut self) -> Result<ForEachStatement> {
        self.consume(TokenType::For)?;
        self.consume(TokenType::Each)?;
        let variable = self.consume_identifier()?;
        self.consume(TokenType::In)?;
        let collection = self.parse_expression()?;
        self.consume(TokenType::Colon)?;
        let body = self.parse_block("For")?;

        Ok(ForEachStatement {
            variable,
            collection,
            body,
        })
    }

    fn parse_return(&mut self) -> Result<ReturnStatement> {
        self.consume(TokenType::Return)?;

        let value = if self.check(&TokenType::Eof) || self.check(&TokenType::End) {
            None
        } else {
            Some(self.parse_expression()?)
        };

        Ok(ReturnStatement { value })
    }

    fn parse_write_file(&mut self) -> Result<WriteFileStatement> {
        self.consume(TokenType::WriteFile)?;
        let content = self.parse_expression()?;
        self.consume(TokenType::To)?;
        let filename = self.parse_expression()?;

        Ok(WriteFileStatement {
            content,
            filename,
        })
    }

    fn parse_match(&mut self) -> Result<MatchStatement> {
        self.consume(TokenType::Match)?;
        let expression = self.parse_expression()?;
        self.consume(TokenType::Colon)?;

        let mut cases = Vec::new();
        while !self.check_end("Match") {
            if self.check(&TokenType::When) {
                self.advance();
                let pattern = self.parse_expression()?;
                self.consume(TokenType::Colon)?;

                let mut statements = Vec::new();
                while !self.check(&TokenType::When) && !self.check_end("Match") {
                    if let Some(stmt) = self.parse_statement()? {
                        statements.push(stmt);
                    }
                }

                cases.push(MatchCase {
                    pattern,
                    body: Block { statements },
                });
            } else if !self.check_end("Match") {
                return Err(anyhow!("Expected 'When' in Match statement"));
            }
        }

        self.consume_end("Match")?;
        Ok(MatchStatement { expression, cases })
    }

    fn parse_add_to_list(&mut self) -> Result<AddToListStatement> {
        self.consume(TokenType::Add)?;
        let value = self.parse_expression()?;
        self.consume(TokenType::To)?;
        // Skip "end of" if present
        if let TokenType::Identifier(s) = &self.peek().token_type {
            if s == "end" {
                self.advance(); // consume "end"
                self.consume(TokenType::Of)?;
            }
        }
        let list = self.parse_expression()?;

        Ok(AddToListStatement { value, list })
    }

    fn parse_list_literal(&mut self) -> Result<Expression> {
        let mut elements = Vec::new();

        // Parse comma-separated elements
        loop {
            elements.push(self.parse_expression()?);
            if !self.check(&TokenType::Comma) {
                break;
            }
            self.advance();
        }

        Ok(Expression::ListLiteral(elements))
    }

    fn parse_type_construction_fields(&mut self) -> Result<Vec<(String, Expression)>> {
        let mut fields = Vec::new();

        // Parse field assignments: field_name as value
        loop {
            let field_name = self.consume_identifier()?;
            self.consume(TokenType::As)?;
            let value = self.parse_expression()?;
            fields.push((field_name, value));

            // Check for more fields
            if !self.check(&TokenType::Comma) {
                break;
            }
            self.advance();
        }

        Ok(fields)
    }

    fn parse_dictionary_literal(&mut self) -> Result<Expression> {
        let mut pairs = Vec::new();

        // Parse key-value pairs until "End Dictionary"
        while !self.check_end("Dictionary") {
            let key = self.parse_expression()?;
            self.consume(TokenType::As)?;
            let value = self.parse_expression()?;
            pairs.push((key, value));

            // Optional comma
            if self.check(&TokenType::Comma) {
                self.advance();
            }
        }

        self.consume_end("Dictionary")?;
        Ok(Expression::DictionaryLiteral(pairs))
    }

    fn parse_expression(&mut self) -> Result<Expression> {
        self.parse_or()
    }

    fn parse_or(&mut self) -> Result<Expression> {
        let mut left = self.parse_and()?;

        while self.check(&TokenType::Or) {
            self.advance();
            let right = self.parse_and()?;
            left = Expression::Binary(Box::new(BinaryExpression {
                left,
                operator: BinaryOperator::Or,
                right,
            }));
        }

        Ok(left)
    }

    fn parse_and(&mut self) -> Result<Expression> {
        let mut left = self.parse_comparison()?;

        while self.check(&TokenType::And) {
            self.advance();
            let right = self.parse_comparison()?;
            left = Expression::Binary(Box::new(BinaryExpression {
                left,
                operator: BinaryOperator::And,
                right,
            }));
        }

        Ok(left)
    }

    fn parse_comparison(&mut self) -> Result<Expression> {
        let mut left = self.parse_arithmetic()?;

        while let Some(op) = self.match_comparison_operator() {
            let right = self.parse_arithmetic()?;
            left = Expression::Binary(Box::new(BinaryExpression {
                left,
                operator: op,
                right,
            }));
        }

        Ok(left)
    }

    fn parse_arithmetic(&mut self) -> Result<Expression> {
        let mut left = self.parse_term()?;

        while let Some(op) = self.match_additive_operator() {
            let right = self.parse_term()?;
            left = Expression::Binary(Box::new(BinaryExpression {
                left,
                operator: op,
                right,
            }));
        }

        Ok(left)
    }

    fn parse_term(&mut self) -> Result<Expression> {
        let mut left = self.parse_unary()?;

        while let Some(op) = self.match_multiplicative_operator() {
            let right = self.parse_unary()?;
            left = Expression::Binary(Box::new(BinaryExpression {
                left,
                operator: op,
                right,
            }));
        }

        Ok(left)
    }

    fn parse_unary(&mut self) -> Result<Expression> {
        if self.check(&TokenType::Not) {
            self.advance();
            let operand = self.parse_unary()?;
            return Ok(Expression::Unary(Box::new(UnaryExpression {
                operator: UnaryOperator::Not,
                operand,
            })));
        }

        self.parse_postfix()
    }

    fn parse_postfix(&mut self) -> Result<Expression> {
        let mut expr = self.parse_primary()?;

        loop {
            if self.check(&TokenType::Dot) {
                self.advance();
                let field = self.consume_identifier()?;
                expr = Expression::FieldAccess(Box::new(FieldAccessExpression {
                    object: expr,
                    field,
                }));
            } else if self.check(&TokenType::At) {
                self.advance();
                if self.check(&TokenType::Index) {
                    self.advance();
                    let index = self.parse_unary()?;
                    expr = Expression::IndexAccess(Box::new(IndexAccessExpression {
                        object: expr,
                        index,
                    }));
                } else if self.check(&TokenType::Key) {
                    self.advance();
                    let key = self.parse_unary()?;
                    expr = Expression::IndexAccess(Box::new(IndexAccessExpression {
                        object: expr,
                        index: key,
                    }));
                } else {
                    return Err(anyhow!("Expected 'index' or 'key' after 'at'"));
                }
            } else if self.check(&TokenType::LeftParen) {
                self.advance();
                let mut arguments = Vec::new();

                while !self.check(&TokenType::RightParen) {
                    arguments.push(self.parse_expression()?);
                    if !self.check(&TokenType::Comma) {
                        break;
                    }
                    self.advance();
                }

                self.consume(TokenType::RightParen)?;

                if let Expression::Identifier(name) = expr {
                    expr = Expression::Call(Box::new(CallExpression {
                        function: name,
                        arguments,
                    }));
                } else if let Expression::FieldAccess(field_access) = expr {
                    expr = Expression::MethodCall(Box::new(MethodCallExpression {
                        object: field_access.object,
                        method: field_access.field,
                        arguments,
                    }));
                } else {
                    return Err(anyhow!("Can only call functions by name or methods on objects"));
                }
            } else {
                break;
            }
        }

        Ok(expr)
    }

    fn parse_primary(&mut self) -> Result<Expression> {
        match &self.peek().token_type {
            TokenType::Integer(n) => {
                let value = *n;
                self.advance();
                Ok(Expression::Integer(value))
            }
            TokenType::Float(f) => {
                let value = *f;
                self.advance();
                Ok(Expression::Float(value))
            }
            TokenType::String(s) => {
                let value = s.clone();
                self.advance();
                Ok(Expression::String(value))
            }
            TokenType::True => {
                self.advance();
                Ok(Expression::Boolean(true))
            }
            TokenType::False => {
                self.advance();
                Ok(Expression::Boolean(false))
            }
            TokenType::Nothing => {
                self.advance();
                Ok(Expression::Nothing)
            }
            TokenType::ReadFile => {
                // Treat ReadFile as a built-in function identifier
                self.advance();
                Ok(Expression::Identifier("ReadFile".to_string()))
            }
            TokenType::Length => {
                self.advance();
                self.consume(TokenType::Of)?;
                let expr = self.parse_expression()?;
                Ok(Expression::LengthOf(Box::new(expr)))
            }
            TokenType::Identifier(name) => {
                let value = name.clone();
                self.advance();
                Ok(Expression::Identifier(value))
            }
            TokenType::LeftParen => {
                self.advance();
                let expr = self.parse_expression()?;
                self.consume(TokenType::RightParen)?;
                Ok(expr)
            }
            _ => Err(anyhow!("Expected expression, got {:?}", self.peek())),
        }
    }

    fn match_comparison_operator(&mut self) -> Option<BinaryOperator> {
        match &self.peek().token_type {
            TokenType::IsGreaterThan => {
                self.advance();
                Some(BinaryOperator::IsGreaterThan)
            }
            TokenType::IsLessThan => {
                self.advance();
                Some(BinaryOperator::IsLessThan)
            }
            TokenType::IsEqualTo => {
                self.advance();
                Some(BinaryOperator::IsEqualTo)
            }
            TokenType::IsNotEqualTo => {
                self.advance();
                Some(BinaryOperator::IsNotEqualTo)
            }
            _ => None,
        }
    }

    fn match_additive_operator(&mut self) -> Option<BinaryOperator> {
        match &self.peek().token_type {
            TokenType::Plus => {
                self.advance();
                Some(BinaryOperator::Plus)
            }
            TokenType::Minus => {
                self.advance();
                Some(BinaryOperator::Minus)
            }
            _ => None,
        }
    }

    fn match_multiplicative_operator(&mut self) -> Option<BinaryOperator> {
        match &self.peek().token_type {
            TokenType::MultipliedBy => {
                self.advance();
                Some(BinaryOperator::MultipliedBy)
            }
            TokenType::DividedBy => {
                self.advance();
                Some(BinaryOperator::DividedBy)
            }
            _ => None,
        }
    }

    fn check_end(&self, keyword: &str) -> bool {
        if !self.check(&TokenType::End) {
            return false;
        }

        if self.current + 1 < self.tokens.len() {
            let next_token = &self.tokens[self.current + 1].token_type;
            match (keyword, next_token) {
                ("Process", TokenType::Process) => true,
                ("If", TokenType::If) => true,
                ("While", TokenType::While) => true,
                ("For", TokenType::For) => true,
                ("Type", TokenType::Type) => true,
                ("Match", TokenType::Match) => true,
                (kw, TokenType::Identifier(name)) => name == kw,
                _ => false
            }
        } else {
            false
        }
    }

    fn consume_end(&mut self, keyword: &str) -> Result<()> {
        self.consume(TokenType::End)?;

        // "Process" is a keyword, not an identifier
        let next_token = self.peek();
        let name = match &next_token.token_type {
            TokenType::Process => {
                self.advance();
                "Process".to_string()
            }
            TokenType::If => {
                self.advance();
                "If".to_string()
            }
            TokenType::While => {
                self.advance();
                "While".to_string()
            }
            TokenType::For => {
                self.advance();
                "For".to_string()
            }
            TokenType::Type => {
                self.advance();
                "Type".to_string()
            }
            TokenType::Match => {
                self.advance();
                "Match".to_string()
            }
            TokenType::Identifier(name) => {
                let n = name.clone();
                self.advance();
                n
            }
            _ => return Err(anyhow!("Expected keyword after 'End', got {:?}", next_token))
        };

        if name != keyword {
            return Err(anyhow!("Expected 'End {}', got 'End {}'", keyword, name));
        }
        Ok(())
    }

    fn consume(&mut self, expected: TokenType) -> Result<()> {
        if std::mem::discriminant(&self.peek().token_type) == std::mem::discriminant(&expected) {
            self.advance();
            Ok(())
        } else {
            Err(anyhow!("Expected {:?}, got {:?}", expected, self.peek()))
        }
    }

    fn consume_identifier(&mut self) -> Result<String> {
        if let TokenType::Identifier(name) = &self.peek().token_type {
            let result = name.clone();
            self.advance();
            Ok(result)
        } else {
            Err(anyhow!("Expected identifier, got {:?}", self.peek()))
        }
    }

    fn consume_identifier_or_string(&mut self) -> Result<String> {
        match &self.peek().token_type {
            TokenType::Identifier(name) => {
                let result = name.clone();
                self.advance();
                Ok(result)
            }
            TokenType::String(value) => {
                let result = value.clone();
                self.advance();
                Ok(result)
            }
            _ => Err(anyhow!("Expected identifier or string, got {:?}", self.peek()))
        }
    }

    fn consume_string(&mut self) -> Result<String> {
        if let TokenType::String(s) = &self.peek().token_type {
            let result = s.clone();
            self.advance();
            Ok(result)
        } else {
            Err(anyhow!("Expected string literal, got {:?}", self.peek()))
        }
    }

    fn consume_integer(&mut self) -> Result<String> {
        if let TokenType::Integer(n) = self.peek().token_type {
            let result = n.to_string();
            self.advance();
            Ok(result)
        } else {
            Err(anyhow!("Expected integer literal, got {:?}", self.peek()))
        }
    }

    fn check(&self, token_type: &TokenType) -> bool {
        if self.is_at_end() {
            return false;
        }
        std::mem::discriminant(&self.peek().token_type) == std::mem::discriminant(token_type)
    }

    fn peek(&self) -> &Token {
        &self.tokens[self.current]
    }

    fn advance(&mut self) {
        if !self.is_at_end() {
            self.current += 1;
        }
    }

    fn is_at_end(&self) -> bool {
        matches!(self.peek().token_type, TokenType::Eof)
    }
}