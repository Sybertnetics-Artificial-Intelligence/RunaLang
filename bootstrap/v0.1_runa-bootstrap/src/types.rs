#[derive(Debug, Clone, PartialEq)]
pub enum Type {
    Integer,
    Float,
    String,
    Boolean,
    Void,
    Named(String),
}

#[derive(Debug, Clone)]
pub struct Function {
    pub name: String,
    pub params: Vec<(String, Type)>,
    pub return_type: Type,
    pub body: Vec<Statement>,
}

#[derive(Debug, Clone)]
pub enum Statement {
    Let { name: String, value: Expression },
    Set { name: String, value: Expression },
    Return { value: Option<Expression> },
    Expression(Expression),
    If { 
        condition: Expression, 
        then_body: Vec<Statement>,
        else_ifs: Vec<(Expression, Vec<Statement>)>,
        else_body: Option<Vec<Statement>>
    },
    While { condition: Expression, body: Vec<Statement> },
    ForEach { variable: String, collection: Expression, body: Vec<Statement> },
    Print { message: Expression },
    ReadFile { filename: Expression, target: String },
    WriteFile { filename: Expression, content: Expression },
    InlineAssembly {
        instructions: Vec<String>,
        output_constraints: Vec<(String, String)>, // (constraint, variable)
        input_constraints: Vec<(String, String)>,  // (constraint, variable)
        clobbers: Vec<String>,
    },
}

#[derive(Debug, Clone)]
pub enum Expression {
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),
    Variable(String),
    Call { name: String, args: Vec<Expression> },
    Binary { left: Box<Expression>, op: BinOp, right: Box<Expression> },
    FieldAccess { object: Box<Expression>, field: String },
    Constructor { type_name: String, fields: Vec<(String, Expression)> },
}

#[derive(Debug, Clone)]
pub enum BinOp {
    Add, Sub, Mul, Div,
    // Comparison operators
    Equal, NotEqual,
    Greater, Less,
    GreaterOrEqual, LessOrEqual,
    // Logical operators
    And, Or,
}

#[derive(Debug, Clone)]
pub struct TypeDefinition {
    pub name: String,
    pub fields: Vec<(String, Type)>,
}

#[derive(Debug, Clone)]
pub struct Import {
    pub module_name: String,
    pub alias: String,
}

#[derive(Debug, Clone)]
pub struct Program {
    pub imports: Vec<Import>,
    pub functions: Vec<Function>,
    pub types: Vec<TypeDefinition>,
}