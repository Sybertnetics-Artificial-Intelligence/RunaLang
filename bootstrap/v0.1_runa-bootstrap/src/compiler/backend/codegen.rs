use anyhow::Result;
use std::path::Path;
use std::collections::HashMap;
use llvm_sys::prelude::*;

use crate::compiler::frontend::ast::*;
use crate::compiler::backend::llvm::LLVMBackend;

pub struct CodeGenerator {
    backend: LLVMBackend,
    variables: HashMap<String, LLVMValueRef>,
    functions: HashMap<String, LLVMValueRef>,
    current_function: Option<LLVMValueRef>,
}

impl CodeGenerator {
    pub fn new(backend: LLVMBackend) -> Self {
        Self {
            backend,
            variables: HashMap::new(),
            functions: HashMap::new(),
            current_function: None,
        }
    }
    
    pub fn generate(&mut self, program: Program, output_path: &Path) -> Result<()> {
        // Generate all functions
        for function in &program.functions {
            self.generate_function_declaration(function)?;
        }
        
        // Generate function bodies
        for function in program.functions {
            self.generate_function_body(function)?;
        }
        
        // Emit to object file
        let output_str = output_path.to_string_lossy();
        self.backend.emit_to_file(&output_str)?;
        
        Ok(())
    }
    
    fn generate_function_declaration(&mut self, function: &Function) -> Result<()> {
        let mut param_types = Vec::new();
        
        for param in &function.parameters {
            param_types.push(self.get_llvm_type(&param.param_type)?);
        }
        
        let return_type = self.get_llvm_type(&function.return_type)?;
        let llvm_function = self.backend.create_function(&function.name, &param_types, return_type)?;
        
        self.functions.insert(function.name.clone(), llvm_function);
        
        Ok(())
    }
    
    fn generate_function_body(&mut self, function: Function) -> Result<()> {
        let llvm_function = self.functions[&function.name];
        self.current_function = Some(llvm_function);
        
        let entry_block = self.backend.create_basic_block(llvm_function, "entry")?;
        self.backend.position_builder_at_end(entry_block);
        
        // Clear variable scope
        self.variables.clear();
        
        // Create allocas for parameters
        for (i, param) in function.parameters.iter().enumerate() {
            let param_type = self.get_llvm_type(&param.param_type)?;
            let alloca = self.backend.build_alloca(param_type, &param.name);
            
            // Get function parameter and store it
            let param_value = unsafe {
                llvm_sys::core::LLVMGetParam(llvm_function, i as u32)
            };
            self.backend.build_store(param_value, alloca);
            
            self.variables.insert(param.name.clone(), alloca);
        }
        
        // Generate function body
        for statement in function.body {
            self.generate_statement(statement)?;
        }
        
        // If no return statement, add void return
        if matches!(function.return_type, Type::Void) {
            self.backend.build_return(None);
        }
        
        self.current_function = None;
        
        Ok(())
    }
    
    fn generate_statement(&mut self, statement: Statement) -> Result<()> {
        match statement {
            Statement::VariableDeclaration { name, var_type, initializer } => {
                let value = self.generate_expression(initializer)?;
                
                let var_type = var_type.unwrap_or_else(|| {
                    // Type inference would go here
                    Type::Integer
                });
                
                let llvm_type = self.get_llvm_type(&var_type)?;
                let alloca = self.backend.build_alloca(llvm_type, &name);
                self.backend.build_store(value, alloca);
                
                self.variables.insert(name, alloca);
            }
            Statement::Assignment { target, value } => {
                let rvalue = self.generate_expression(value)?;
                
                if let Some(&ptr) = self.variables.get(&target) {
                    self.backend.build_store(rvalue, ptr);
                } else {
                    return Err(anyhow::anyhow!("Undefined variable: {}", target));
                }
            }
            Statement::FunctionCall { name, args } => {
                self.generate_function_call(name, args)?;
            }
            Statement::Return { value } => {
                if let Some(expr) = value {
                    let return_value = self.generate_expression(expr)?;
                    self.backend.build_return(Some(return_value));
                } else {
                    self.backend.build_return(None);
                }
            }
            Statement::Expression(expr) => {
                self.generate_expression(expr)?;
            }
            Statement::If { condition, then_branch, else_branch } => {
                self.generate_if_statement(condition, then_branch, else_branch)?;
            }
            Statement::While { condition, body } => {
                self.generate_while_statement(condition, body)?;
            }
            Statement::For { variable: _, iterable: _, body: _ } => {
                // TODO: Implement for loops
                return Err(anyhow::anyhow!("For loops not yet implemented"));
            }
            Statement::FieldAssignment { object: _, field: _, value: _ } => {
                // TODO: Implement field assignment
                return Err(anyhow::anyhow!("Field assignment not yet implemented"));
            }
        }
        
        Ok(())
    }
    
    fn generate_expression(&mut self, expression: Expression) -> Result<LLVMValueRef> {
        match expression {
            Expression::Literal { value } => {
                match value {
                    LiteralValue::Integer(i) => {
                        let int_type = self.backend.get_int64_type();
                        Ok(self.backend.const_int(int_type, i as u64))
                    }
                    LiteralValue::Float(f) => {
                        let float_type = self.backend.get_double_type();
                        Ok(self.backend.const_real(float_type, f))
                    }
                    LiteralValue::Boolean(b) => {
                        let bool_type = self.backend.get_int32_type();
                        Ok(self.backend.const_int(bool_type, if b { 1 } else { 0 }))
                    }
                    LiteralValue::String(_s) => {
                        // TODO: Implement string literals
                        Err(anyhow::anyhow!("String literals not yet implemented"))
                    }
                }
            }
            Expression::Variable { name } => {
                if let Some(&ptr) = self.variables.get(&name) {
                    Ok(self.backend.build_load(ptr, &format!("{}_load", name)))
                } else {
                    Err(anyhow::anyhow!("Undefined variable: {}", name))
                }
            }
            Expression::BinaryOperation { left, operator, right } => {
                self.generate_binary_operation(*left, operator, *right)
            }
            Expression::UnaryOperation { operator, operand } => {
                self.generate_unary_operation(operator, *operand)
            }
            Expression::FunctionCall { name, args } => {
                self.generate_function_call(name, args)
            }
            Expression::FieldAccess { object: _, field: _ } => {
                // TODO: Implement field access
                Err(anyhow::anyhow!("Field access not yet implemented"))
            }
            Expression::Constructor { type_name: _, fields: _ } => {
                // TODO: Implement constructors
                Err(anyhow::anyhow!("Constructors not yet implemented"))
            }
        }
    }
    
    fn generate_binary_operation(&mut self, left: Expression, operator: BinaryOperator, right: Expression) -> Result<LLVMValueRef> {
        let lhs = self.generate_expression(left)?;
        let rhs = self.generate_expression(right)?;
        
        unsafe {
            use llvm_sys::core::*;
            
            let result = match operator {
                BinaryOperator::Add => LLVMBuildAdd(self.backend.get_builder(), lhs, rhs, b"add\0".as_ptr() as *const i8),
                BinaryOperator::Subtract => LLVMBuildSub(self.backend.get_builder(), lhs, rhs, b"sub\0".as_ptr() as *const i8),
                BinaryOperator::Multiply => LLVMBuildMul(self.backend.get_builder(), lhs, rhs, b"mul\0".as_ptr() as *const i8),
                BinaryOperator::Divide => LLVMBuildSDiv(self.backend.get_builder(), lhs, rhs, b"div\0".as_ptr() as *const i8),
                BinaryOperator::Modulo => LLVMBuildSRem(self.backend.get_builder(), lhs, rhs, b"rem\0".as_ptr() as *const i8),
                BinaryOperator::Equal => LLVMBuildICmp(self.backend.get_builder(), llvm_sys::LLVMIntPredicate::LLVMIntEQ, lhs, rhs, b"eq\0".as_ptr() as *const i8),
                BinaryOperator::NotEqual => LLVMBuildICmp(self.backend.get_builder(), llvm_sys::LLVMIntPredicate::LLVMIntNE, lhs, rhs, b"ne\0".as_ptr() as *const i8),
                BinaryOperator::LessThan => LLVMBuildICmp(self.backend.get_builder(), llvm_sys::LLVMIntPredicate::LLVMIntSLT, lhs, rhs, b"lt\0".as_ptr() as *const i8),
                BinaryOperator::LessThanEqual => LLVMBuildICmp(self.backend.get_builder(), llvm_sys::LLVMIntPredicate::LLVMIntSLE, lhs, rhs, b"le\0".as_ptr() as *const i8),
                BinaryOperator::GreaterThan => LLVMBuildICmp(self.backend.get_builder(), llvm_sys::LLVMIntPredicate::LLVMIntSGT, lhs, rhs, b"gt\0".as_ptr() as *const i8),
                BinaryOperator::GreaterThanEqual => LLVMBuildICmp(self.backend.get_builder(), llvm_sys::LLVMIntPredicate::LLVMIntSGE, lhs, rhs, b"ge\0".as_ptr() as *const i8),
                BinaryOperator::And => LLVMBuildAnd(self.backend.get_builder(), lhs, rhs, b"and\0".as_ptr() as *const i8),
                BinaryOperator::Or => LLVMBuildOr(self.backend.get_builder(), lhs, rhs, b"or\0".as_ptr() as *const i8),
            };
            
            Ok(result)
        }
    }
    
    fn generate_unary_operation(&mut self, operator: UnaryOperator, operand: Expression) -> Result<LLVMValueRef> {
        let operand_value = self.generate_expression(operand)?;
        
        unsafe {
            use llvm_sys::core::*;
            
            let result = match operator {
                UnaryOperator::Negate => {
                    let zero = self.backend.const_int(self.backend.get_int64_type(), 0);
                    LLVMBuildSub(self.backend.get_builder(), zero, operand_value, b"neg\0".as_ptr() as *const i8)
                }
                UnaryOperator::Not => {
                    LLVMBuildNot(self.backend.get_builder(), operand_value, b"not\0".as_ptr() as *const i8)
                }
            };
            
            Ok(result)
        }
    }
    
    fn generate_function_call(&mut self, name: String, args: Vec<Expression>) -> Result<LLVMValueRef> {
        if let Some(&function) = self.functions.get(&name) {
            let mut arg_values = Vec::new();
            
            for arg in args {
                arg_values.push(self.generate_expression(arg)?);
            }
            
            unsafe {
                use llvm_sys::core::*;
                let call_result = LLVMBuildCall2(
                    self.backend.get_builder(),
                    LLVMGlobalGetValueType(function),
                    function,
                    arg_values.as_mut_ptr(),
                    arg_values.len() as u32,
                    b"call\0".as_ptr() as *const i8
                );
                
                Ok(call_result)
            }
        } else {
            Err(anyhow::anyhow!("Undefined function: {}", name))
        }
    }
    
    fn generate_if_statement(&mut self, condition: Expression, then_branch: Vec<Statement>, else_branch: Option<Vec<Statement>>) -> Result<()> {
        let condition_value = self.generate_expression(condition)?;
        
        let function = self.current_function.unwrap();
        let then_block = self.backend.create_basic_block(function, "if_then")?;
        let else_block = self.backend.create_basic_block(function, "if_else")?;
        let merge_block = self.backend.create_basic_block(function, "if_merge")?;
        
        // Branch based on condition
        unsafe {
            use llvm_sys::core::*;
            LLVMBuildCondBr(self.backend.get_builder(), condition_value, then_block, else_block);
        }
        
        // Generate then branch
        self.backend.position_builder_at_end(then_block);
        for statement in then_branch {
            self.generate_statement(statement)?;
        }
        unsafe {
            use llvm_sys::core::*;
            LLVMBuildBr(self.backend.get_builder(), merge_block);
        }
        
        // Generate else branch
        self.backend.position_builder_at_end(else_block);
        if let Some(else_statements) = else_branch {
            for statement in else_statements {
                self.generate_statement(statement)?;
            }
        }
        unsafe {
            use llvm_sys::core::*;
            LLVMBuildBr(self.backend.get_builder(), merge_block);
        }
        
        // Continue with merge block
        self.backend.position_builder_at_end(merge_block);
        
        Ok(())
    }
    
    fn generate_while_statement(&mut self, condition: Expression, body: Vec<Statement>) -> Result<()> {
        let function = self.current_function.unwrap();
        let loop_condition = self.backend.create_basic_block(function, "while_cond")?;
        let loop_body = self.backend.create_basic_block(function, "while_body")?;
        let loop_exit = self.backend.create_basic_block(function, "while_exit")?;
        
        // Jump to condition check
        unsafe {
            use llvm_sys::core::*;
            LLVMBuildBr(self.backend.get_builder(), loop_condition);
        }
        
        // Generate condition check
        self.backend.position_builder_at_end(loop_condition);
        let condition_value = self.generate_expression(condition)?;
        unsafe {
            use llvm_sys::core::*;
            LLVMBuildCondBr(self.backend.get_builder(), condition_value, loop_body, loop_exit);
        }
        
        // Generate loop body
        self.backend.position_builder_at_end(loop_body);
        for statement in body {
            self.generate_statement(statement)?;
        }
        unsafe {
            use llvm_sys::core::*;
            LLVMBuildBr(self.backend.get_builder(), loop_condition);
        }
        
        // Continue with exit block
        self.backend.position_builder_at_end(loop_exit);
        
        Ok(())
    }
    
    fn get_llvm_type(&self, runa_type: &Type) -> Result<LLVMTypeRef> {
        match runa_type {
            Type::Integer => Ok(self.backend.get_int64_type()),
            Type::Float => Ok(self.backend.get_double_type()),
            Type::Boolean => Ok(self.backend.get_int32_type()),
            Type::String => {
                // String as i8 pointer for now
                let char_type = unsafe { llvm_sys::core::LLVMInt8TypeInContext(self.backend.get_context()) };
                Ok(self.backend.get_pointer_type(char_type))
            }
            Type::Void => Ok(self.backend.get_void_type()),
            Type::Named(_) => {
                // TODO: Look up named types
                Err(anyhow::anyhow!("Named types not yet implemented"))
            }
            Type::Array(_) => {
                // TODO: Implement array types
                Err(anyhow::anyhow!("Array types not yet implemented"))
            }
            Type::Dictionary(_, _) => {
                // TODO: Implement dictionary types
                Err(anyhow::anyhow!("Dictionary types not yet implemented"))
            }
            Type::Function { .. } => {
                // TODO: Implement function pointer types
                Err(anyhow::anyhow!("Function types not yet implemented"))
            }
        }
    }
}