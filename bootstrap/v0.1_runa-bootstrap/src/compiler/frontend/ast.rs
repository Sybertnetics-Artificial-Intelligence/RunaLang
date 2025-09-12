use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum Type {
    Integer,
    Float,
    String,
    Boolean,
    Named(String),
    Array(Box<Type>),
    Dictionary(Box<Type>, Box<Type>),
    Function {
        params: Vec<Type>,
        return_type: Box<Type>,
    },
    Void,
}

#[derive(Debug, Clone)]
pub struct Parameter {
    pub name: String,
    pub param_type: Type,
}

#[derive(Debug, Clone)]
pub struct Field {
    pub name: String,
    pub field_type: Type,
}

#[derive(Debug, Clone)]
pub enum TypeDefinition {
    Struct {
        name: String,
        fields: Vec<Field>,
    },
    Enum {
        name: String,
        variants: Vec<String>,
    },
}

#[derive(Debug, Clone)]
pub enum Expression {
    Literal {
        value: LiteralValue,
    },
    Variable {
        name: String,
    },
    FieldAccess {
        object: Box<Expression>,
        field: String,
    },
    FunctionCall {
        name: String,
        args: Vec<Expression>,
    },
    BinaryOperation {
        left: Box<Expression>,
        operator: BinaryOperator,
        right: Box<Expression>,
    },
    UnaryOperation {
        operator: UnaryOperator,
        operand: Box<Expression>,
    },
    Constructor {
        type_name: String,
        fields: HashMap<String, Expression>,
    },
}

#[derive(Debug, Clone)]
pub enum LiteralValue {
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),
}

#[derive(Debug, Clone)]
pub enum BinaryOperator {
    Add,
    Subtract,
    Multiply,
    Divide,
    Modulo,
    Equal,
    NotEqual,
    LessThan,
    LessThanEqual,
    GreaterThan,
    GreaterThanEqual,
    And,
    Or,
}

#[derive(Debug, Clone)]
pub enum UnaryOperator {
    Negate,
    Not,
}

#[derive(Debug, Clone)]
pub enum Statement {
    VariableDeclaration {
        name: String,
        var_type: Option<Type>,
        initializer: Expression,
    },
    Assignment {
        target: String,
        value: Expression,
    },
    FieldAssignment {
        object: String,
        field: String,
        value: Expression,
    },
    FunctionCall {
        name: String,
        args: Vec<Expression>,
    },
    If {
        condition: Expression,
        then_branch: Vec<Statement>,
        else_branch: Option<Vec<Statement>>,
    },
    While {
        condition: Expression,
        body: Vec<Statement>,
    },
    For {
        variable: String,
        iterable: Expression,
        body: Vec<Statement>,
    },
    Return {
        value: Option<Expression>,
    },
    Expression(Expression),
}

#[derive(Debug, Clone)]
pub struct Function {
    pub name: String,
    pub parameters: Vec<Parameter>,
    pub return_type: Type,
    pub body: Vec<Statement>,
}

#[derive(Debug, Clone)]
pub struct Import {
    pub module: String,
    pub items: Vec<String>, // Empty for wildcard imports
}

#[derive(Debug, Clone)]
pub struct Program {
    pub imports: Vec<Import>,
    pub type_definitions: Vec<TypeDefinition>,
    pub functions: Vec<Function>,
    pub constants: HashMap<String, Expression>,
}

// Helper implementations
impl Type {
    pub fn is_numeric(&self) -> bool {
        matches!(self, Type::Integer | Type::Float)
    }
    
    pub fn is_primitive(&self) -> bool {
        matches!(self, Type::Integer | Type::Float | Type::String | Type::Boolean)
    }
    
    pub fn size_hint(&self) -> Option<usize> {
        match self {
            Type::Integer => Some(8),
            Type::Float => Some(8),
            Type::Boolean => Some(1),
            Type::String => None, // Variable size
            Type::Named(_) => None, // Depends on definition
            Type::Array(_) => None, // Variable size
            Type::Dictionary(_, _) => None, // Variable size
            Type::Function { .. } => Some(8), // Pointer size
            Type::Void => Some(0),
        }
    }
}

impl Expression {
    pub fn get_type_hint(&self) -> Option<Type> {
        match self {
            Expression::Literal { value } => Some(match value {
                LiteralValue::Integer(_) => Type::Integer,
                LiteralValue::Float(_) => Type::Float,
                LiteralValue::String(_) => Type::String,
                LiteralValue::Boolean(_) => Type::Boolean,
            }),
            Expression::BinaryOperation { left, operator, right: _ } => {
                match operator {
                    BinaryOperator::Equal | BinaryOperator::NotEqual 
                    | BinaryOperator::LessThan | BinaryOperator::LessThanEqual
                    | BinaryOperator::GreaterThan | BinaryOperator::GreaterThanEqual
                    | BinaryOperator::And | BinaryOperator::Or => Some(Type::Boolean),
                    _ => left.get_type_hint(),
                }
            },
            Expression::UnaryOperation { operator, operand } => {
                match operator {
                    UnaryOperator::Not => Some(Type::Boolean),
                    UnaryOperator::Negate => operand.get_type_hint(),
                }
            },
            _ => None,
        }
    }
}