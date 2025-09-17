#[derive(Debug, Clone, PartialEq)]
pub enum Type {
    Integer,
    Float,
    String,
    Boolean,
    Void,
    List(Box<Type>),
    Array(Box<Type>, usize),
    Dictionary(Box<Type>, Box<Type>),
    Custom(String),
}

impl Type {
    pub fn is_numeric(&self) -> bool {
        matches!(self, Type::Integer | Type::Float)
    }

    pub fn is_comparable(&self) -> bool {
        matches!(self, Type::Integer | Type::Float | Type::String)
    }

    pub fn is_logical(&self) -> bool {
        matches!(self, Type::Boolean)
    }

    pub fn to_llvm_type(&self) -> String {
        match self {
            Type::Integer => "i64".to_string(),
            Type::Float => "double".to_string(),
            Type::Boolean => "i1".to_string(),
            Type::String => "%struct.String*".to_string(),
            Type::Void => "void".to_string(),
            Type::List(_) => "%struct.List*".to_string(),
            Type::Array(elem_type, size) => {
                format!("[{} x {}]", size, elem_type.to_llvm_type())
            }
            Type::Dictionary(_, _) => "%struct.Dictionary*".to_string(),
            Type::Custom(name) => format!("%struct.{}*", name),
        }
    }
}