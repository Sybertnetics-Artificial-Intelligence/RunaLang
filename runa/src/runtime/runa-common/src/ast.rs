//! Defines the Abstract Syntax Tree (AST) for the Runa language.

use crate::token::Token;

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
    // We can use an enum for different literal types later
    // e.g., String, Number, Bool, Nil
    pub value: Token, 
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