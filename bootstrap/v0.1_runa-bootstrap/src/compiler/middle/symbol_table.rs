use std::collections::HashMap;
use crate::compiler::frontend::ast::{Type, TypeDefinition, Parameter};

#[derive(Debug, Clone)]
pub struct Variable {
    pub name: String,
    pub var_type: Type,
    pub is_mutable: bool,
}

#[derive(Debug, Clone)]
pub struct FunctionSignature {
    pub name: String,
    pub parameters: Vec<Parameter>,
    pub return_type: Type,
}

pub struct Scope {
    variables: HashMap<String, Variable>,
    functions: HashMap<String, FunctionSignature>,
    types: HashMap<String, TypeDefinition>,
}

impl Scope {
    fn new() -> Self {
        Self {
            variables: HashMap::new(),
            functions: HashMap::new(),
            types: HashMap::new(),
        }
    }
    
    fn define_variable(&mut self, name: String, var_type: Type) {
        self.variables.insert(name.clone(), Variable {
            name,
            var_type,
            is_mutable: true, // Default to mutable for now
        });
    }
    
    fn lookup_variable(&self, name: &str) -> Option<&Variable> {
        self.variables.get(name)
    }
    
    fn define_function(&mut self, name: String, parameters: Vec<Parameter>, return_type: Type) {
        self.functions.insert(name.clone(), FunctionSignature {
            name,
            parameters,
            return_type,
        });
    }
    
    fn lookup_function(&self, name: &str) -> Option<&FunctionSignature> {
        self.functions.get(name)
    }
    
    fn define_type(&mut self, name: String, type_def: TypeDefinition) {
        self.types.insert(name, type_def);
    }
    
    fn lookup_type(&self, name: &str) -> Option<&TypeDefinition> {
        self.types.get(name)
    }
}

pub struct SymbolTable {
    scopes: Vec<Scope>,
    current_function: Option<String>,
}

impl SymbolTable {
    pub fn new() -> Self {
        let mut symbol_table = Self {
            scopes: Vec::new(),
            current_function: None,
        };
        
        // Push global scope
        symbol_table.push_scope();
        
        // Define built-in types
        symbol_table.define_builtin_types();
        
        symbol_table
    }
    
    fn define_builtin_types(&mut self) {
        // Built-in types are already handled by the Type enum
        // This is where we'd add any special built-in type definitions if needed
    }
    
    pub fn push_scope(&mut self) {
        self.scopes.push(Scope::new());
    }
    
    pub fn pop_scope(&mut self) {
        if self.scopes.len() > 1 {
            self.scopes.pop();
        }
    }
    
    pub fn define_variable(&mut self, name: String, var_type: Type) {
        if let Some(scope) = self.scopes.last_mut() {
            scope.define_variable(name, var_type);
        }
    }
    
    pub fn lookup_variable(&self, name: &str) -> bool {
        // Search from innermost to outermost scope
        for scope in self.scopes.iter().rev() {
            if scope.lookup_variable(name).is_some() {
                return true;
            }
        }
        false
    }
    
    pub fn get_variable(&self, name: &str) -> Option<&Variable> {
        // Search from innermost to outermost scope
        for scope in self.scopes.iter().rev() {
            if let Some(var) = scope.lookup_variable(name) {
                return Some(var);
            }
        }
        None
    }
    
    pub fn define_function(&mut self, name: String, parameters: Vec<Parameter>, return_type: Type) {
        if let Some(scope) = self.scopes.first_mut() {
            // Functions are always defined in global scope for now
            scope.define_function(name, parameters, return_type);
        }
    }
    
    pub fn lookup_function(&self, name: &str) -> bool {
        // Search all scopes for function (functions are global)
        for scope in &self.scopes {
            if scope.lookup_function(name).is_some() {
                return true;
            }
        }
        false
    }
    
    pub fn get_function(&self, name: &str) -> Option<&FunctionSignature> {
        // Search all scopes for function
        for scope in &self.scopes {
            if let Some(func) = scope.lookup_function(name) {
                return Some(func);
            }
        }
        None
    }
    
    pub fn define_type(&mut self, name: String, type_def: TypeDefinition) {
        if let Some(scope) = self.scopes.first_mut() {
            // Types are always defined in global scope
            scope.define_type(name, type_def);
        }
    }
    
    pub fn lookup_type(&self, name: &str) -> bool {
        // Search all scopes for type (types are global)
        for scope in &self.scopes {
            if scope.lookup_type(name).is_some() {
                return true;
            }
        }
        false
    }
    
    pub fn get_type(&self, name: &str) -> Option<&TypeDefinition> {
        // Search all scopes for type
        for scope in &self.scopes {
            if let Some(type_def) = scope.lookup_type(name) {
                return Some(type_def);
            }
        }
        None
    }
    
    pub fn enter_function(&mut self, function_name: String) {
        self.current_function = Some(function_name);
        self.push_scope();
    }
    
    pub fn exit_function(&mut self) {
        self.current_function = None;
        self.pop_scope();
    }
    
    pub fn current_function(&self) -> Option<&str> {
        self.current_function.as_deref()
    }
    
    pub fn is_in_function(&self) -> bool {
        self.current_function.is_some()
    }
    
    pub fn scope_depth(&self) -> usize {
        self.scopes.len()
    }
}