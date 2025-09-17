use crate::parser::{AstNode, Field};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum Type {
    Integer,
    String,
    Void,
    Unknown,
    Custom(String), // For user-defined types/structs
    List(Box<Type>), // List type with element type
}

#[derive(Debug, Clone)]
pub struct StructDefinition {
    pub name: String,
    pub fields: Vec<Field>,
}

pub struct TypeChecker {
    variables: HashMap<String, Type>,
    functions: HashMap<String, FunctionSignature>,
    structs: HashMap<String, StructDefinition>,
    current_function_return_type: Option<Type>,
}

#[derive(Debug, Clone)]
pub struct FunctionSignature {
    pub parameters: Vec<Type>,
    pub return_type: Type,
}

impl TypeChecker {
    pub fn new() -> Self {
        let mut functions = HashMap::new();

        // Add built-in function signatures
        functions.insert("length_of".to_string(), FunctionSignature {
            parameters: vec![Type::String],
            return_type: Type::Integer,
        });
        functions.insert("char_at".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::Integer],
            return_type: Type::Integer,
        });
        functions.insert("substring".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::Integer, Type::Integer],
            return_type: Type::String,
        });
        functions.insert("concat".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String],
            return_type: Type::String,
        });
        functions.insert("to_string".to_string(), FunctionSignature {
            parameters: vec![Type::Integer],
            return_type: Type::String,
        });
        functions.insert("print_string".to_string(), FunctionSignature {
            parameters: vec![Type::String],
            return_type: Type::Void,
        });
        functions.insert("read_file".to_string(), FunctionSignature {
            parameters: vec![Type::String],
            return_type: Type::String,
        });
        functions.insert("write_file".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String],
            return_type: Type::Void,
        });

        // String utility functions
        functions.insert("split".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String],
            return_type: Type::Integer, // Placeholder - will return array count
        });
        functions.insert("trim".to_string(), FunctionSignature {
            parameters: vec![Type::String],
            return_type: Type::String,
        });
        functions.insert("starts_with".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String],
            return_type: Type::Integer, // Boolean as integer (0/1)
        });
        functions.insert("ends_with".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String],
            return_type: Type::Integer, // Boolean as integer (0/1)
        });
        functions.insert("contains".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String],
            return_type: Type::Integer, // Boolean as integer (0/1)
        });
        functions.insert("replace".to_string(), FunctionSignature {
            parameters: vec![Type::String, Type::String, Type::String],
            return_type: Type::String,
        });
        functions.insert("to_upper".to_string(), FunctionSignature {
            parameters: vec![Type::String],
            return_type: Type::String,
        });
        functions.insert("to_lower".to_string(), FunctionSignature {
            parameters: vec![Type::String],
            return_type: Type::String,
        });

        Self {
            variables: HashMap::new(),
            functions,
            structs: HashMap::new(),
            current_function_return_type: None,
        }
    }

    pub fn check(&mut self, ast: &AstNode) -> Result<(), String> {
        self.check_node(ast)
    }

    fn check_node(&mut self, node: &AstNode) -> Result<(), String> {
        match node {
            AstNode::Program(statements) => {
                // First pass: collect function signatures and struct definitions
                for stmt in statements {
                    match stmt {
                        AstNode::ProcessDefinition { name, parameters, return_type, .. } => {
                            let param_types: Vec<Type> = parameters.iter()
                                .map(|p| self.parse_type(&p.param_type))
                                .collect();

                            let ret_type = if let Some(type_str) = return_type {
                                self.parse_type(type_str)
                            } else {
                                Type::Void
                            };

                            let signature = FunctionSignature {
                                parameters: param_types,
                                return_type: ret_type,
                            };

                            self.functions.insert(name.clone(), signature);
                        }
                        AstNode::TypeDefinition { name, fields } => {
                            let struct_def = StructDefinition {
                                name: name.clone(),
                                fields: fields.clone(),
                            };
                            self.structs.insert(name.clone(), struct_def);
                        }
                        _ => {}
                    }
                }

                // Second pass: type check all statements
                for stmt in statements {
                    self.check_node(stmt)?;
                }
            }
            AstNode::LetStatement { variable, value } => {
                let value_type = self.infer_type(value)?;
                self.variables.insert(variable.clone(), value_type);
            }
            AstNode::SetStatement { variable, value } => {
                let value_type = self.infer_type(value)?;
                if let Some(existing_type) = self.variables.get(variable) {
                    if *existing_type != value_type {
                        return Err(format!(
                            "Type mismatch: variable '{}' is {:?}, but trying to assign {:?}",
                            variable, existing_type, value_type
                        ));
                    }
                } else {
                    return Err(format!("Undefined variable: {}", variable));
                }
            }
            AstNode::DisplayStatement { value } => {
                // Display accepts any type for now
                self.infer_type(value)?;
            }
            AstNode::ReturnStatement { value } => {
                let return_type = if let Some(value) = value {
                    self.infer_type(value)?
                } else {
                    Type::Void
                };

                if let Some(expected_type) = &self.current_function_return_type {
                    if *expected_type != return_type {
                        return Err(format!(
                            "Return type mismatch: expected {:?}, got {:?}",
                            expected_type, return_type
                        ));
                    }
                }
            }
            AstNode::ProcessDefinition { name: _, parameters, return_type, body } => {
                // Save current function context
                let old_return_type = self.current_function_return_type.clone();
                let old_variables = self.variables.clone();

                // Set new function context
                self.current_function_return_type = if let Some(type_str) = return_type {
                    Some(self.parse_type(type_str))
                } else {
                    Some(Type::Void)
                };

                // Add parameters to variable scope
                for param in parameters {
                    let param_type = self.parse_type(&param.param_type);
                    self.variables.insert(param.name.clone(), param_type);
                }

                // Type check function body
                for stmt in body {
                    self.check_node(stmt)?;
                }

                // Restore previous context
                self.current_function_return_type = old_return_type;
                self.variables = old_variables;
            }
            AstNode::IfStatement { condition, then_block, else_block } => {
                // Condition should be a boolean-like expression (we'll be lenient for now)
                self.infer_type(condition)?;

                for stmt in then_block {
                    self.check_node(stmt)?;
                }

                if let Some(else_stmts) = else_block {
                    for stmt in else_stmts {
                        self.check_node(stmt)?;
                    }
                }
            }
            AstNode::WhileStatement { condition, body } => {
                // Condition should be a boolean-like expression
                self.infer_type(condition)?;

                for stmt in body {
                    self.check_node(stmt)?;
                }
            }
            AstNode::TypeDefinition { .. } => {
                // Type definitions are handled in the first pass
            }
            AstNode::StructCreation { type_name, field_values } => {
                // Check that the struct type exists
                if !self.structs.contains_key(type_name) {
                    return Err(format!("Unknown struct type: {}", type_name));
                }

                // Type check field assignments
                let struct_def = self.structs.get(type_name).cloned();
                if let Some(struct_def) = struct_def {
                    for (field_name, value) in field_values {
                        let value_type = self.infer_type(value)?;

                        // Check if field exists in struct definition
                        let mut field_found = false;
                        for field_def in &struct_def.fields {
                            if field_def.name == *field_name {
                                field_found = true;

                                // Check if value type matches expected field type
                                let expected_type = self.parse_type(&field_def.field_type);
                                if value_type != expected_type {
                                    return Err(format!(
                                        "Type mismatch for field '{}' in struct '{}': expected {:?}, got {:?}",
                                        field_name, type_name, expected_type, value_type
                                    ));
                                }
                                break;
                            }
                        }

                        if !field_found {
                            return Err(format!(
                                "Field '{}' does not exist in struct '{}'",
                                field_name, type_name
                            ));
                        }
                    }
                }
            }
            AstNode::FieldAccess { object, field } => {
                let object_type = self.infer_type(object)?;

                // Validate field access based on object type
                if let Type::Custom(struct_name) = object_type {
                    if let Some(struct_def) = self.structs.get(&struct_name) {
                        // Check if field exists in struct definition
                        let mut field_found = false;
                        for field_def in &struct_def.fields {
                            if field_def.name == *field {
                                field_found = true;
                                break;
                            }
                        }

                        if !field_found {
                            return Err(format!(
                                "Field '{}' does not exist in struct '{}'",
                                field, struct_name
                            ));
                        }
                    } else {
                        return Err(format!("Unknown struct type: {}", struct_name));
                    }
                } else {
                    return Err(format!(
                        "Cannot access field '{}' on non-struct type {:?}",
                        field, object_type
                    ));
                }
            }
            AstNode::IndexAccess { object, index } => {
                let _object_type = self.infer_type(object)?;
                let _index_type = self.infer_type(index)?;
                // Type checking for index access is handled in infer_type
            }
            _ => {
                // For expressions, just infer their type
                self.infer_type(node)?;
            }
        }
        Ok(())
    }

    fn infer_type(&mut self, node: &AstNode) -> Result<Type, String> {
        match node {
            AstNode::IntegerLiteral(_) => Ok(Type::Integer),
            AstNode::StringLiteral(_) => Ok(Type::String),
            AstNode::Identifier(name) => {
                if let Some(var_type) = self.variables.get(name) {
                    Ok(var_type.clone())
                } else {
                    Err(format!("Undefined variable: {}", name))
                }
            }
            AstNode::BinaryExpression { left, right, .. } => {
                let left_type = self.infer_type(left)?;
                let right_type = self.infer_type(right)?;

                // For arithmetic operations, both sides should be the same type
                if left_type != right_type {
                    return Err(format!(
                        "Type mismatch in binary expression: {:?} and {:?}",
                        left_type, right_type
                    ));
                }

                Ok(left_type)
            }
            AstNode::FunctionCall { name, arguments } => {
                // Clone the signature to avoid borrowing issues
                if let Some(signature) = self.functions.get(name).cloned() {
                    // Check argument count
                    if arguments.len() != signature.parameters.len() {
                        return Err(format!(
                            "Function '{}' expects {} arguments, got {}",
                            name, signature.parameters.len(), arguments.len()
                        ));
                    }

                    // Check argument types
                    for (i, (arg, expected_type)) in arguments.iter().zip(&signature.parameters).enumerate() {
                        let arg_type = self.infer_type(arg)?;
                        if arg_type != *expected_type {
                            return Err(format!(
                                "Function '{}' argument {} type mismatch: expected {:?}, got {:?}",
                                name, i, expected_type, arg_type
                            ));
                        }
                    }

                    Ok(signature.return_type)
                } else {
                    Err(format!("Unknown function: {}", name))
                }
            }
            AstNode::ListLiteral { elements } => {
                if elements.is_empty() {
                    // Empty list - infer as List of Unknown for now
                    Ok(Type::List(Box::new(Type::Unknown)))
                } else {
                    // Infer element type from first element
                    let first_element_type = self.infer_type(&elements[0])?;

                    // Check that all elements have the same type
                    for element in &elements[1..] {
                        let element_type = self.infer_type(element)?;
                        if element_type != first_element_type {
                            return Err(format!(
                                "List elements must have the same type. Found {:?} and {:?}",
                                first_element_type, element_type
                            ));
                        }
                    }

                    Ok(Type::List(Box::new(first_element_type)))
                }
            }
            AstNode::StructCreation { type_name, .. } => {
                // Return the custom type
                Ok(Type::Custom(type_name.clone()))
            }
            AstNode::FieldAccess { object, field } => {
                let object_type = self.infer_type(object)?;
                if let Type::Custom(struct_name) = object_type {
                    if let Some(struct_def) = self.structs.get(&struct_name) {
                        // Find the field and return its type
                        for field_def in &struct_def.fields {
                            if field_def.name == *field {
                                return Ok(self.parse_type(&field_def.field_type));
                            }
                        }
                        Err(format!("Field '{}' not found in struct '{}'", field, struct_name))
                    } else {
                        Err(format!("Unknown struct type: {}", struct_name))
                    }
                } else {
                    Err(format!("Cannot access field '{}' on non-struct type {:?}", field, object_type))
                }
            }
            AstNode::IndexAccess { object, index } => {
                let object_type = self.infer_type(object)?;
                let index_type = self.infer_type(index)?;

                // Index must be an integer
                if !matches!(index_type, Type::Integer) {
                    return Err(format!("List index must be Integer, got {:?}", index_type));
                }

                // Check what type of object we're indexing
                match object_type {
                    Type::List(element_type) => {
                        // Return the element type of the list
                        Ok(*element_type)
                    }
                    Type::String => {
                        // String indexing returns character (as Integer for simplicity)
                        Ok(Type::Integer)
                    }
                    Type::Integer => Err(format!("Cannot index into Integer")),
                    Type::Void => Err(format!("Cannot index into Void")),
                    Type::Unknown => Err(format!("Cannot index into Unknown type")),
                    Type::Custom(type_name) => Err(format!("Cannot index into custom type '{}'", type_name)),
                }
            }
            _ => Ok(Type::Unknown),
        }
    }

    fn parse_type(&self, type_str: &str) -> Type {
        match type_str {
            "Integer" => Type::Integer,
            "String" => Type::String,
            "Void" => Type::Void,
            _ => {
                // Check if it's a custom type
                if self.structs.contains_key(type_str) {
                    Type::Custom(type_str.to_string())
                } else {
                    Type::Unknown
                }
            }
        }
    }
}