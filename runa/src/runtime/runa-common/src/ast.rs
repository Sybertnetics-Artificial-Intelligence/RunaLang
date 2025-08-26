//! Defines the Abstract Syntax Tree (AST) for the Runa language.

use crate::token::Token;
use crate::bytecode::Value;

// Using Box<Expr> for recursive enum variants
// See: https://doc.rust-lang.org/book/ch15-01-box.html#enabling-recursive-types-with-boxes

#[derive(Debug, PartialEq, Clone)]
pub enum Expr {
    Assign(AssignExpr),
    Binary(BinaryExpr),
    Grouping(GroupingExpr),
    Literal(LiteralExpr),
    Unary(UnaryExpr),
    Variable(VariableExpr),
    Call(CallExpr),
    Index(IndexAccessExpr),
    List(ListExpr),
    InterpolatedString(InterpolatedStringExpr),
}

// Legacy ASTNode type for compatibility with AOTT compiler
#[derive(Debug, PartialEq, Clone)]
pub enum ASTNode {
    Literal(Value),
    Identifier(String),
    BinaryOp {
        left: Box<ASTNode>,
        op: String,
        right: Box<ASTNode>,
    },
    UnaryOp {
        op: String,
        operand: Box<ASTNode>,
    },
    FunctionCall {
        name: String,
        args: Vec<ASTNode>,
    },
    Block(Vec<ASTNode>),
    Assignment {
        name: String,
        value: Box<ASTNode>,
    },
    If {
        condition: Box<ASTNode>,
        then_branch: Box<ASTNode>,
        else_branch: Option<Box<ASTNode>>,
    },
    While {
        condition: Box<ASTNode>,
        body: Box<ASTNode>,
    },
    Return(Option<Box<ASTNode>>),
}

#[derive(Debug, PartialEq, Clone)]
pub struct AssignExpr {
    pub name: Token,
    pub value: Box<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct BinaryExpr {
    pub left: Box<Expr>,
    pub operator: Token,
    pub right: Box<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct GroupingExpr {
    pub expression: Box<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct LiteralExpr {
    pub value: LiteralValue,
}

#[derive(Debug, PartialEq, Clone)]
pub enum LiteralValue {
    String(String),
    Integer(i64),
    Float(f64),
    Boolean(bool),
    Nil,
}

#[derive(Debug, PartialEq, Clone)]
pub struct UnaryExpr {
    pub operator: Token,
    pub right: Box<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct VariableExpr {
    pub name: Token,
}

#[derive(Debug, PartialEq, Clone)]
pub struct CallExpr {
    pub callee: Box<Expr>,
    pub arguments: Vec<Expr>,
    pub paren: Token, // Closing parenthesis for error reporting
}

#[derive(Debug, PartialEq, Clone)]
pub struct IndexAccessExpr {
    pub target: Box<Expr>,
    pub index: Box<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct ListExpr {
    pub elements: Vec<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct InterpolatedStringExpr {
    pub parts: Vec<InterpolatedStringPart>,
}

#[derive(Debug, PartialEq, Clone)]
pub enum InterpolatedStringPart {
    String(String),
    Expression(Box<Expr>),
}

// === STATEMENTS ===

#[derive(Debug, PartialEq, Clone)]
pub enum Stmt {
    Let(LetStmt),
    Expression(ExprStmt),
    If(IfStmt),
    While(WhileStmt),
    For(ForStmt),
    Block(BlockStmt),
    Return(ReturnStmt),
    Function(FunctionStmt),
    Print(PrintStmt),
    Match(MatchStmt),
    TypeDef(TypeDefStmt),
    EnumDef(EnumDefStmt),
    Annotation(AnnotationStmt),
}

#[derive(Debug, PartialEq, Clone)]
pub struct LetStmt {
    pub name: Token,
    pub initializer: Option<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct ExprStmt {
    pub expr: Expr,
}

#[derive(Debug, PartialEq, Clone)]
pub struct IfStmt {
    pub condition: Expr,
    pub then_branch: BlockStmt,
    pub else_branch: Option<Box<Stmt>>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct WhileStmt {
    pub condition: Expr,
    pub body: BlockStmt,
}

#[derive(Debug, PartialEq, Clone)]
pub struct ForStmt {
    pub variable: Token,
    pub start: Box<Expr>,
    pub end: Box<Expr>,
    pub step: Option<Box<Expr>>,
    pub body: BlockStmt,
}

#[derive(Debug, PartialEq, Clone)]
pub struct ReturnStmt {
    pub value: Option<Expr>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct BlockStmt {
    pub statements: Vec<Stmt>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct FunctionStmt {
    pub name: Token,
    pub params: Vec<Token>,
    pub body: Vec<Stmt>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct PrintStmt {
    pub value: Expr,
}

#[derive(Debug, PartialEq, Clone)]
pub struct MatchStmt {
    pub expr: Expr,
    pub cases: Vec<WhenCase>,
    pub default_case: Option<BlockStmt>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct WhenCase {
    pub pattern: Expr,
    pub body: BlockStmt,
}

#[derive(Debug, PartialEq, Clone)]
pub struct TypeDefStmt {
    pub name: Token,
    pub fields: Vec<TypeField>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct TypeField {
    pub name: Token,
    pub field_type: Token,
}

#[derive(Debug, PartialEq, Clone)]
pub struct EnumDefStmt {
    pub name: Token,
    pub variants: Vec<Token>,
}

#[derive(Debug, PartialEq, Clone)]
pub struct AnnotationStmt {
    pub annotation_type: String,
    pub content: String,
    pub location: crate::annotations::SourceLocation,
} 