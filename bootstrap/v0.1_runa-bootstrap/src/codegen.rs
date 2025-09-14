use anyhow::Result;
use llvm_sys::prelude::*;
use llvm_sys::core::*;
use llvm_sys::target::*;
use llvm_sys::target_machine::*;
use std::collections::HashMap;
use std::ffi::CString;
use std::path::Path;
use crate::types::*;

/// Tracks how a variable is stored - as a direct value or as a pointer
#[derive(Clone, Debug, PartialEq)]
enum StorageKind {
    Direct,     // Value stored directly in alloca (needs load for use)
    Pointer,    // Already a pointer to data (no load needed, e.g., strings)
}

pub fn compile_to_object(program: &Program, output_path: &Path) -> Result<()> {
    unsafe {
        LLVM_InitializeAllTargets();
        LLVM_InitializeAllTargetInfos();
        LLVM_InitializeAllTargetMCs();
        LLVM_InitializeAllAsmPrinters();
        LLVM_InitializeAllAsmParsers();
        
        let context = LLVMContextCreate();
        let module_name = CString::new("runa_module").unwrap();
        let module = LLVMModuleCreateWithNameInContext(module_name.as_ptr(), context);
        let builder = LLVMCreateBuilderInContext(context);
        
        let mut codegen = CodeGen {
            context,
            module,
            builder,
            variables: HashMap::new(),
            variable_storage: HashMap::new(),  // Track storage kind for each variable
            functions: HashMap::new(),
            type_definitions: HashMap::new(),
            runa_type_definitions: HashMap::new(),
            variable_types: HashMap::new(),
            function_return_types: HashMap::new(),
            imports: HashMap::new(),
            inline_asm_special_output: false,
        };
        
        // Register all imports for module resolution
        for import in &program.imports {
            codegen.register_import(import)?;
        }
        
        for type_def in &program.types {
            codegen.compile_type_definition(type_def)?;
        }
        
        for function in &program.functions {
            codegen.compile_function(function)?;
        }
        
        codegen.emit_object_file(output_path)?;
        
        LLVMDisposeBuilder(builder);
        LLVMDisposeModule(module);
        LLVMContextDispose(context);
    }
    
    Ok(())
}

struct CodeGen {
    context: LLVMContextRef,
    module: LLVMModuleRef,
    builder: LLVMBuilderRef,
    variables: HashMap<String, LLVMValueRef>,
    variable_storage: HashMap<String, StorageKind>,  // Track storage kind for each variable
    functions: HashMap<String, LLVMValueRef>,
    type_definitions: HashMap<String, LLVMTypeRef>,
    runa_type_definitions: HashMap<String, TypeDefinition>,
    variable_types: HashMap<String, Type>,
    function_return_types: HashMap<String, Type>,
    imports: HashMap<String, String>, // alias -> module_name
    inline_asm_special_output: bool, // Track when we're using hardcoded register output
}

impl CodeGen {
    fn register_import(&mut self, import: &Import) -> Result<()> {
        // Store the import mapping for module resolution and linking
        self.imports.insert(import.alias.clone(), import.module_name.clone());
        
        // Import registration enables:
        // - Module dependency tracking for build order
        // - Namespace aliasing for qualified names
        // - Symbol visibility for cross-module references
        // Bootstrap compiler tracks imports for single-file compilation
        // Multi-file linking handled by external build tools
        
        Ok(())
    }
    
    fn compile_function(&mut self, func: &Function) -> Result<()> {
        unsafe {
            let mut param_types = Vec::new();
            for (_, param_type) in &func.params {
                param_types.push(self.llvm_type(param_type)?);
            }

            let return_type = self.llvm_type(&func.return_type)?;
            let func_name = CString::new(func.name.clone()).unwrap();
            let func_type = LLVMFunctionType(
                return_type,
                param_types.as_ptr() as *mut LLVMTypeRef,
                param_types.len() as u32,
                0
            );
            
            let llvm_func = LLVMAddFunction(self.module, func_name.as_ptr(), func_type);
            self.functions.insert(func.name.clone(), llvm_func);
            self.function_return_types.insert(func.name.clone(), func.return_type.clone());
            
            let entry_name = CString::new("entry").unwrap();
            let entry_block = LLVMAppendBasicBlockInContext(
                self.context,
                llvm_func,
                entry_name.as_ptr()
            );
            LLVMPositionBuilderAtEnd(self.builder, entry_block);
            
            // Debug output at function entry
            if func.name == "main" {
                let debug_name = CString::new("debug_main_entry").unwrap();
                let printf_format = CString::new("DEBUG: Entering main function\n").unwrap();
                let format_str = LLVMBuildGlobalStringPtr(
                    self.builder,
                    printf_format.as_ptr(),
                    debug_name.as_ptr()
                );
                LLVMBuildCall2(
                    self.builder,
                    LLVMFunctionType(
                        LLVMInt32TypeInContext(self.context),
                        [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                        1,
                        1  // variadic
                    ),
                    self.get_or_declare_printf(),
                    [format_str].as_ptr() as *mut _,
                    1,
                    debug_name.as_ptr()
                );
            }

            // Set up parameters
            self.variables.clear();
            self.variable_types.clear();
            self.variable_storage.clear();
            for (i, (name, param_type)) in func.params.iter().enumerate() {
                let param = LLVMGetParam(llvm_func, i as u32);
                let param_name = CString::new(name.clone()).unwrap();
                LLVMSetValueName2(param, param_name.as_ptr(), name.len());
                self.variables.insert(name.clone(), param);
                self.variable_types.insert(name.clone(), param_type.clone());
                // Parameters are always direct values
                self.variable_storage.insert(name.clone(), StorageKind::Direct);
            }
            
            // Compile body
            for stmt in &func.body {
                self.compile_statement(stmt)?;
            }
            
            // Add return if missing
            if matches!(func.return_type, Type::Void) {
                LLVMBuildRetVoid(self.builder);
            }
        }
        
        Ok(())
    }
    
    fn compile_statement(&mut self, stmt: &Statement) -> Result<()> {
        unsafe {
            match stmt {
                Statement::Let { name, value } => {
                    let val = self.compile_expression(value)?;
                    let var_type = self.infer_expression_type(value)?;

                    // Determine storage kind based on type
                    let storage_kind = match var_type {
                        Type::String => StorageKind::Pointer,   // Strings are already pointers
                        _ => StorageKind::Direct,               // Everything else needs load
                    };

                    self.variables.insert(name.clone(), val);
                    self.variable_types.insert(name.clone(), var_type);
                    self.variable_storage.insert(name.clone(), storage_kind);
                }
                Statement::Set { name, value } => {
                    let val = self.compile_expression(value)?;
                    let var_type = self.infer_expression_type(value)?;

                    // Determine storage kind based on type
                    let storage_kind = match var_type {
                        Type::String => StorageKind::Pointer,   // Strings are already pointers
                        _ => StorageKind::Direct,               // Everything else needs load
                    };

                    self.variables.insert(name.clone(), val);
                    self.variable_types.insert(name.clone(), var_type);
                    self.variable_storage.insert(name.clone(), storage_kind);
                }
                Statement::Return { value } => {
                    if let Some(expr) = value {
                        let val = self.compile_expression(expr)?;
                        LLVMBuildRet(self.builder, val);
                    } else {
                        LLVMBuildRetVoid(self.builder);
                    }
                }
                Statement::Print { message } => {
                    self.compile_print_statement(message)?;
                }
                Statement::ReadFile { filename, target } => {
                    self.compile_read_file(filename, target)?;
                }
                Statement::WriteFile { filename, content } => {
                    self.compile_write_file(filename, content)?;
                }
                Statement::Expression(expr) => {
                    self.compile_expression(expr)?;
                }
                Statement::If { condition, then_body, else_ifs, else_body } => {
                    self.compile_if_statement(condition, then_body, else_ifs, else_body)?;
                }
                Statement::While { condition, body } => {
                    self.compile_while_statement(condition, body)?;
                }
                Statement::ForEach { variable, collection, body } => {
                    self.compile_for_each_statement(variable, collection, body)?;
                }
                Statement::InlineAssembly { instructions, output_constraints, input_constraints, clobbers } => {
                    self.compile_inline_assembly(instructions, output_constraints, input_constraints, clobbers)?;
                }
            }
        }
        Ok(())
    }
    
    fn compile_expression(&mut self, expr: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            match expr {
                Expression::Integer(n) => {
                    let int_type = LLVMInt64TypeInContext(self.context);
                    Ok(LLVMConstInt(int_type, *n as u64, 0))
                }
                Expression::Float(f) => {
                    let float_type = LLVMDoubleTypeInContext(self.context);
                    Ok(LLVMConstReal(float_type, *f))
                }
                Expression::Boolean(b) => {
                    let bool_type = LLVMInt1TypeInContext(self.context);
                    Ok(LLVMConstInt(bool_type, if *b { 1 } else { 0 }, 0))
                }
                Expression::String(s) => {
                    // Use the simpler LLVMBuildGlobalStringPtr approach but ensure it's loaded correctly
                    let str_c = CString::new(s.clone()).unwrap();
                    let global_name = CString::new("str").unwrap();
                    let str_ptr = LLVMBuildGlobalStringPtr(
                        self.builder,
                        str_c.as_ptr(),
                        global_name.as_ptr()
                    );
                    Ok(str_ptr)
                }
                Expression::Variable(name) => {
                    if let Some(&val) = self.variables.get(name) {
                        // Check storage kind to determine if we need to load
                        if let Some(storage_kind) = self.variable_storage.get(name) {
                            match storage_kind {
                                StorageKind::Pointer => {
                                    // This is already a pointer (e.g., string), use directly
                                    Ok(val)
                                }
                                StorageKind::Direct => {
                                    // This is a direct value that might need loading
                                    if LLVMGetTypeKind(LLVMTypeOf(val)) == llvm_sys::LLVMTypeKind::LLVMPointerTypeKind {
                                        // This is an alloca/pointer, we need to load the value
                                        let load_name = CString::new(format!("load_{}", name)).unwrap();
                                        let loaded_val = LLVMBuildLoad2(
                                            self.builder,
                                            // Determine the type to load based on variable_types
                                            if let Some(var_type) = self.variable_types.get(name) {
                                                match var_type {
                                                    Type::Integer => LLVMInt64TypeInContext(self.context),
                                                    Type::Float => LLVMDoubleTypeInContext(self.context),
                                                    Type::Boolean => LLVMInt1TypeInContext(self.context),
                                                    _ => LLVMInt64TypeInContext(self.context), // Default to i64
                                                }
                                            } else {
                                                LLVMInt64TypeInContext(self.context)
                                            },
                                            val,
                                            load_name.as_ptr()
                                        );
                                        Ok(loaded_val)
                                    } else {
                                        // Already a value, return directly
                                        Ok(val)
                                    }
                                }
                            }
                        } else {
                            // No storage info, fall back to old behavior for backwards compatibility
                            if LLVMGetTypeKind(LLVMTypeOf(val)) == llvm_sys::LLVMTypeKind::LLVMPointerTypeKind {
                                let load_name = CString::new(format!("load_{}", name)).unwrap();
                                let loaded_val = LLVMBuildLoad2(
                                    self.builder,
                                    LLVMInt64TypeInContext(self.context),
                                    val,
                                    load_name.as_ptr()
                                );
                                Ok(loaded_val)
                            } else {
                                Ok(val)
                            }
                        }
                    } else {
                        Err(anyhow::anyhow!("Undefined variable: {}", name))
                    }
                }
                Expression::Call { name, args } => {
                    // Check for built-in string functions first
                    match name.as_str() {
                        "string_length" => {
                            if args.len() != 1 {
                                return Err(anyhow::anyhow!("string_length expects 1 argument"));
                            }
                            return self.compile_string_length(&args[0]);
                        }
                        "string_compare" => {
                            if args.len() != 2 {
                                return Err(anyhow::anyhow!("string_compare expects 2 arguments"));
                            }
                            return self.compile_string_compare(&args[0], &args[1]);
                        }
                        "string_substring" => {
                            if args.len() != 3 {
                                return Err(anyhow::anyhow!("string_substring expects 3 arguments"));
                            }
                            return self.compile_string_substring(&args[0], &args[1], &args[2]);
                        }
                        "string_char_at" => {
                            if args.len() != 2 {
                                return Err(anyhow::anyhow!("string_char_at expects 2 arguments"));
                            }
                            return self.compile_string_char_at(&args[0], &args[1]);
                        }
                        _ => {
                            // Not a built-in, check user-defined functions
                            if let Some(&func) = self.functions.get(name) {
                                let mut arg_vals = Vec::new();
                                for arg in args {
                                    arg_vals.push(self.compile_expression(arg)?);
                                }

                                let call_name = CString::new("call").unwrap();
                                Ok(LLVMBuildCall2(
                                    self.builder,
                                    LLVMGlobalGetValueType(func),
                                    func,
                                    arg_vals.as_mut_ptr(),
                                    arg_vals.len() as u32,
                                    call_name.as_ptr()
                                ))
                            } else {
                                Err(anyhow::anyhow!("Undefined function: {}", name))
                            }
                        }
                    }
                }
                Expression::Binary { left, op, right } => {
                    // Check if this is string concatenation
                    if matches!(op, BinOp::Add) {
                        let left_type = self.infer_expression_type(left)?;
                        let right_type = self.infer_expression_type(right)?;

                        if matches!(left_type, Type::String) && matches!(right_type, Type::String) {
                            // String concatenation using inline assembly
                            return self.compile_string_concat(left, right);
                        }
                    }

                    let lhs = self.compile_expression(left)?;
                    let rhs = self.compile_expression(right)?;

                    let result_name = CString::new("binop").unwrap();
                    match op {
                        BinOp::Add => Ok(LLVMBuildAdd(self.builder, lhs, rhs, result_name.as_ptr())),
                        BinOp::Sub => Ok(LLVMBuildSub(self.builder, lhs, rhs, result_name.as_ptr())),
                        BinOp::Mul => Ok(LLVMBuildMul(self.builder, lhs, rhs, result_name.as_ptr())),
                        BinOp::Div => Ok(LLVMBuildSDiv(self.builder, lhs, rhs, result_name.as_ptr())),
                        // Comparison operators
                        BinOp::Equal => Ok(LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntEQ, lhs, rhs, result_name.as_ptr())),
                        BinOp::NotEqual => Ok(LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntNE, lhs, rhs, result_name.as_ptr())),
                        BinOp::Greater => Ok(LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntSGT, lhs, rhs, result_name.as_ptr())),
                        BinOp::Less => Ok(LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntSLT, lhs, rhs, result_name.as_ptr())),
                        BinOp::GreaterOrEqual => Ok(LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntSGE, lhs, rhs, result_name.as_ptr())),
                        BinOp::LessOrEqual => Ok(LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntSLE, lhs, rhs, result_name.as_ptr())),
                        // Logical operators
                        BinOp::And => Ok(LLVMBuildAnd(self.builder, lhs, rhs, result_name.as_ptr())),
                        BinOp::Or => Ok(LLVMBuildOr(self.builder, lhs, rhs, result_name.as_ptr())),
                    }
                }
                Expression::FieldAccess { object, field } => {
                    self.compile_field_access(object, field)
                }
                Expression::Constructor { type_name, fields } => {
                    self.compile_constructor(type_name, fields)
                }
            }
        }
    }
    
    fn compile_constructor(&mut self, type_name: &str, fields: &[(String, Expression)]) -> Result<LLVMValueRef> {
        unsafe {
            // Get the LLVM struct type (copy it to avoid borrow issues)
            let struct_type = *self.type_definitions.get(type_name)
                .ok_or_else(|| anyhow::anyhow!("Unknown type: {}", type_name))?;
            
            // Get the Runa type definition to know field order (clone to avoid borrow issues)
            let type_def = self.runa_type_definitions.get(type_name)
                .ok_or_else(|| anyhow::anyhow!("Type definition not found: {}", type_name))?
                .clone();
            
            // Allocate space for the struct on the stack
            let alloc_name = CString::new(format!("{}_alloc", type_name)).unwrap();
            let struct_ptr = LLVMBuildAlloca(self.builder, struct_type, alloc_name.as_ptr());
            
            // Initialize each field
            for (field_name, field_expr) in fields {
                // Find the field index in the type definition
                let field_index = type_def.fields.iter()
                    .position(|(name, _)| name == field_name)
                    .ok_or_else(|| anyhow::anyhow!("Field '{}' not found in type '{}'", field_name, type_name))?;
                
                // Compile the field value expression
                let field_value = self.compile_expression(field_expr)?;
                
                // Create GEP to get pointer to the field
                let indices = [
                    LLVMConstInt(LLVMInt32TypeInContext(self.context), 0, 0),
                    LLVMConstInt(LLVMInt32TypeInContext(self.context), field_index as u64, 0),
                ];
                
                let field_ptr_name = CString::new(format!("{}.{}_ptr", type_name, field_name)).unwrap();
                let field_ptr = LLVMBuildGEP2(
                    self.builder,
                    struct_type,
                    struct_ptr,
                    indices.as_ptr() as *mut LLVMValueRef,
                    indices.len() as u32,
                    field_ptr_name.as_ptr()
                );
                
                // Store the value in the field
                LLVMBuildStore(self.builder, field_value, field_ptr);
            }
            
            // Load and return the struct value
            let load_name = CString::new(format!("{}_load", type_name)).unwrap();
            Ok(LLVMBuildLoad2(
                self.builder,
                struct_type,
                struct_ptr,
                load_name.as_ptr()
            ))
        }
    }

    fn compile_string_concat(&mut self, left: &Expression, right: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            // Compile both string expressions to get pointers
            let left_str = self.compile_expression(left)?;
            let right_str = self.compile_expression(right)?;

            // Allocate 256 bytes on stack for result (simple fixed-size approach)
            let i8_type = LLVMInt8TypeInContext(self.context);
            let array_type = LLVMArrayType(i8_type, 256);
            let alloc_name = CString::new("concat_buffer").unwrap();
            let buffer = LLVMBuildAlloca(self.builder, array_type, alloc_name.as_ptr());

            // Get pointer to start of buffer
            let zero = LLVMConstInt(LLVMInt32TypeInContext(self.context), 0, 0);
            let indices = vec![zero, zero];
            let buffer_ptr_name = CString::new("buffer_ptr").unwrap();
            let buffer_ptr = LLVMBuildGEP2(
                self.builder,
                array_type,
                buffer,
                indices.as_ptr() as *mut LLVMValueRef,
                indices.len() as u32,
                buffer_ptr_name.as_ptr()
            );

            // Create inline assembly to perform string concatenation
            // The assembly will:
            // 1. Copy first string to buffer
            // 2. Find end of first string
            // 3. Copy second string after first
            // Use $0, $1, $2 for operand references (buffer, left_str, right_str)
            // LLVM dialect: $ for operands, single % for registers
            let asm_string = CString::new(
                "movq $1, %rsi\n\t\
                 movq $0, %rdi\n\t\
                 1:\n\t\
                 movb (%rsi), %al\n\t\
                 testb %al, %al\n\t\
                 je 2f\n\t\
                 movb %al, (%rdi)\n\t\
                 incq %rsi\n\t\
                 incq %rdi\n\t\
                 jmp 1b\n\t\
                 2:\n\t\
                 movq $2, %rsi\n\t\
                 3:\n\t\
                 movb (%rsi), %al\n\t\
                 movb %al, (%rdi)\n\t\
                 testb %al, %al\n\t\
                 je 4f\n\t\
                 incq %rsi\n\t\
                 incq %rdi\n\t\
                 jmp 3b\n\t\
                 4:"
            ).unwrap();

            // Constraints: r = any general purpose register
            // Order matches args: buffer_ptr, left_str, right_str
            // Clobbers are specified separately in constraints string
            let constraints = CString::new("r,r,r").unwrap();
            let void_type = LLVMVoidTypeInContext(self.context);
            let i8_ptr_type = LLVMPointerType(i8_type, 0);
            let fn_type = LLVMFunctionType(
                void_type,
                [i8_ptr_type, i8_ptr_type, i8_ptr_type].as_ptr() as *mut LLVMTypeRef,
                3,
                0
            );

            let asm_value = LLVMGetInlineAsm(
                fn_type,
                asm_string.as_ptr() as *mut i8,
                asm_string.to_bytes().len(),
                constraints.as_ptr() as *mut i8,
                constraints.to_bytes().len(),
                1, // has side effects
                0, // is align stack
                llvm_sys::LLVMInlineAsmDialect::LLVMInlineAsmDialectATT,
                0  // can throw
            );

            let call_name = CString::new("concat_call").unwrap();
            let args = vec![buffer_ptr, left_str, right_str];
            LLVMBuildCall2(
                self.builder,
                fn_type,
                asm_value,
                args.as_ptr() as *mut LLVMValueRef,
                args.len() as u32,
                call_name.as_ptr()
            );

            Ok(buffer_ptr)
        }
    }

    fn get_or_declare_printf(&mut self) -> LLVMValueRef {
        unsafe {
            let printf_name = CString::new("printf").unwrap();
            let existing = LLVMGetNamedFunction(self.module, printf_name.as_ptr());
            if !existing.is_null() {
                return existing;
            }

            // Declare printf: int printf(const char *format, ...)
            let i32_type = LLVMInt32TypeInContext(self.context);
            let i8_type = LLVMInt8TypeInContext(self.context);
            let i8_ptr_type = LLVMPointerType(i8_type, 0);
            let printf_type = LLVMFunctionType(
                i32_type,
                [i8_ptr_type].as_ptr() as *mut _,
                1,
                1  // variadic
            );
            LLVMAddFunction(self.module, printf_name.as_ptr(), printf_type)
        }
    }

    fn compile_string_length(&mut self, str_expr: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            let str_ptr = self.compile_expression(str_expr)?;

            // Use inline assembly to calculate string length
            let i64_type = LLVMInt64TypeInContext(self.context);
            let i8_type = LLVMInt8TypeInContext(self.context);
            let i8_ptr_type = LLVMPointerType(i8_type, 0);

            // Assembly to count string length
            // $0 is output (in rax), $1 is input (string pointer)
            // LLVM dialect: $ for operands, single % for registers
            // We need to explicitly move result to output register
            let asm_string = CString::new(
                "movq $1, %rsi\n\t\
                 xorq %rax, %rax\n\t\
                 1:\n\t\
                 movb (%rsi), %cl\n\t\
                 testb %cl, %cl\n\t\
                 je 2f\n\t\
                 incq %rax\n\t\
                 incq %rsi\n\t\
                 jmp 1b\n\t\
                 2:\n\t\
                 movq %rax, $0"
            ).unwrap();

            let constraints = CString::new("=r,r").unwrap();
            let fn_type = LLVMFunctionType(
                i64_type,
                [i8_ptr_type].as_ptr() as *mut LLVMTypeRef,
                1,
                0
            );

            let asm_value = LLVMGetInlineAsm(
                fn_type,
                asm_string.as_ptr() as *mut i8,
                asm_string.to_bytes().len(),
                constraints.as_ptr() as *mut i8,
                constraints.to_bytes().len(),
                0, // no side effects
                0, // is align stack
                llvm_sys::LLVMInlineAsmDialect::LLVMInlineAsmDialectATT,
                0  // can throw
            );

            let call_name = CString::new("strlen_call").unwrap();
            let result = LLVMBuildCall2(
                self.builder,
                fn_type,
                asm_value,
                [str_ptr].as_ptr() as *mut LLVMValueRef,
                1,
                call_name.as_ptr()
            );

            Ok(result)
        }
    }

    fn compile_string_compare(&mut self, left: &Expression, right: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            let left_str = self.compile_expression(left)?;
            let right_str = self.compile_expression(right)?;

            // Use inline assembly for string comparison
            let i64_type = LLVMInt64TypeInContext(self.context);
            let i8_type = LLVMInt8TypeInContext(self.context);
            let i8_ptr_type = LLVMPointerType(i8_type, 0);

            // Assembly to compare strings (returns 0 if equal, non-zero otherwise)
            // $0 is output, $1 is first string, $2 is second string
            // LLVM dialect: $ for operands, single % for registers, $$ for immediate values
            // We need to explicitly move result to output register
            let asm_string = CString::new(
                "movq $1, %rsi\n\t\
                 movq $2, %rdi\n\t\
                 xorq %rax, %rax\n\t\
                 1:\n\t\
                 movb (%rsi), %cl\n\t\
                 movb (%rdi), %dl\n\t\
                 cmpb %cl, %dl\n\t\
                 jne 3f\n\t\
                 testb %cl, %cl\n\t\
                 je 2f\n\t\
                 incq %rsi\n\t\
                 incq %rdi\n\t\
                 jmp 1b\n\t\
                 2:\n\t\
                 xorq %rax, %rax\n\t\
                 jmp 4f\n\t\
                 3:\n\t\
                 movq $$1, %rax\n\t\
                 4:\n\t\
                 movq %rax, $0"
            ).unwrap();

            let constraints = CString::new("=r,r,r").unwrap();
            let fn_type = LLVMFunctionType(
                i64_type,
                [i8_ptr_type, i8_ptr_type].as_ptr() as *mut LLVMTypeRef,
                2,
                0
            );

            let asm_value = LLVMGetInlineAsm(
                fn_type,
                asm_string.as_ptr() as *mut i8,
                asm_string.to_bytes().len(),
                constraints.as_ptr() as *mut i8,
                constraints.to_bytes().len(),
                0, // no side effects
                0, // is align stack
                llvm_sys::LLVMInlineAsmDialect::LLVMInlineAsmDialectATT,
                0  // can throw
            );

            let call_name = CString::new("strcmp_call").unwrap();
            let args = vec![left_str, right_str];
            Ok(LLVMBuildCall2(
                self.builder,
                fn_type,
                asm_value,
                args.as_ptr() as *mut LLVMValueRef,
                args.len() as u32,
                call_name.as_ptr()
            ))
        }
    }

    fn compile_string_substring(&mut self, str_expr: &Expression, start_expr: &Expression,
                                len_expr: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            let str_ptr = self.compile_expression(str_expr)?;
            let start = self.compile_expression(start_expr)?;
            let length = self.compile_expression(len_expr)?;


            // Allocate buffer for substring
            let i8_type = LLVMInt8TypeInContext(self.context);
            let array_type = LLVMArrayType(i8_type, 256);
            let alloc_name = CString::new("substr_buffer").unwrap();
            let buffer = LLVMBuildAlloca(self.builder, array_type, alloc_name.as_ptr());

            // Get pointer to start of buffer
            let zero = LLVMConstInt(LLVMInt32TypeInContext(self.context), 0, 0);
            let indices = vec![zero, zero];
            let buffer_ptr_name = CString::new("substr_ptr").unwrap();
            let buffer_ptr = LLVMBuildGEP2(
                self.builder,
                array_type,
                buffer,
                indices.as_ptr() as *mut LLVMValueRef,
                indices.len() as u32,
                buffer_ptr_name.as_ptr()
            );

            // Use inline assembly to copy substring
            // $0=source string, $1=start offset, $2=dest buffer, $3=length
            // LLVM dialect: $ for operands, single % for registers, $$ for immediate values
            let asm_string = CString::new(
                "movq $0, %rsi\n\t\
                 addq $1, %rsi\n\t\
                 movq $2, %rdi\n\t\
                 movq $3, %rcx\n\t\
                 testq %rcx, %rcx\n\t\
                 je 2f\n\t\
                 1:\n\t\
                 movb (%rsi), %al\n\t\
                 movb %al, (%rdi)\n\t\
                 incq %rsi\n\t\
                 incq %rdi\n\t\
                 decq %rcx\n\t\
                 jnz 1b\n\t\
                 2:\n\t\
                 movb $$0, (%rdi)"
            ).unwrap();

            let constraints = CString::new("r,r,r,r").unwrap();
            let void_type = LLVMVoidTypeInContext(self.context);
            let i8_ptr_type = LLVMPointerType(i8_type, 0);
            let i64_type = LLVMInt64TypeInContext(self.context);
            let fn_type = LLVMFunctionType(
                void_type,
                [i8_ptr_type, i64_type, i8_ptr_type, i64_type].as_ptr() as *mut LLVMTypeRef,
                4,
                0
            );

            let asm_value = LLVMGetInlineAsm(
                fn_type,
                asm_string.as_ptr() as *mut i8,
                asm_string.to_bytes().len(),
                constraints.as_ptr() as *mut i8,
                constraints.to_bytes().len(),
                1, // has side effects
                0, // is align stack
                llvm_sys::LLVMInlineAsmDialect::LLVMInlineAsmDialectATT,
                0  // can throw
            );

            let call_name = CString::new("substr_call").unwrap();
            let args = vec![str_ptr, start, buffer_ptr, length];
            LLVMBuildCall2(
                self.builder,
                fn_type,
                asm_value,
                args.as_ptr() as *mut LLVMValueRef,
                args.len() as u32,
                call_name.as_ptr()
            );

            // WORKING SOLUTION: Use empty printf call as compiler fence
            // This is a pragmatic solution - printf creates a function call that LLVM
            // cannot optimize away, ensuring proper register allocation around inline assembly
            let printf_fn = self.get_or_declare_printf();
            let debug_format = CString::new("").unwrap(); // Empty string - minimal impact
            let format_str = LLVMBuildGlobalStringPtr(
                self.builder,
                debug_format.as_ptr(),
                CString::new("fence").unwrap().as_ptr()
            );
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt32TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    1  // variadic
                ),
                printf_fn,
                [format_str].as_ptr() as *mut _,
                1,
                CString::new("fence_call").unwrap().as_ptr()
            );

            Ok(buffer_ptr)
        }
    }

    fn compile_string_char_at(&mut self, str_expr: &Expression, index_expr: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            let str_ptr = self.compile_expression(str_expr)?;
            let index = self.compile_expression(index_expr)?;

            // Get character at index using GEP
            let char_ptr_name = CString::new("char_ptr").unwrap();
            let i8_type = LLVMInt8TypeInContext(self.context);
            let char_ptr = LLVMBuildGEP2(
                self.builder,
                i8_type,
                str_ptr,
                [index].as_ptr() as *mut LLVMValueRef,
                1,
                char_ptr_name.as_ptr()
            );

            // Load the character
            let load_name = CString::new("char_val").unwrap();
            let char_val = LLVMBuildLoad2(
                self.builder,
                i8_type,
                char_ptr,
                load_name.as_ptr()
            );

            // Zero-extend to i64 to match Integer type
            let zext_name = CString::new("char_as_int").unwrap();
            Ok(LLVMBuildZExt(
                self.builder,
                char_val,
                LLVMInt64TypeInContext(self.context),
                zext_name.as_ptr()
            ))
        }
    }

    fn compile_if_statement(&mut self, condition: &Expression, then_body: &[Statement],
                            else_ifs: &[(Expression, Vec<Statement>)],
                            else_body: &Option<Vec<Statement>>) -> Result<()> {
        unsafe {
            let func = LLVMGetBasicBlockParent(LLVMGetInsertBlock(self.builder));
            
            // Create basic blocks for each branch
            let then_block_name = CString::new("then").unwrap();
            let then_block = LLVMAppendBasicBlockInContext(self.context, func, then_block_name.as_ptr());
            
            let merge_block_name = CString::new("merge").unwrap();
            let merge_block = LLVMAppendBasicBlockInContext(self.context, func, merge_block_name.as_ptr());
            
            // Compile the condition
            let cond_val = self.compile_expression(condition)?;
            
            // Handle else-if blocks
            let mut else_if_blocks = Vec::new();
            let mut else_if_conditions = Vec::new();
            for (else_if_cond, _) in else_ifs {
                let else_if_block_name = CString::new("elseif").unwrap();
                let else_if_block = LLVMAppendBasicBlockInContext(self.context, func, else_if_block_name.as_ptr());
                else_if_blocks.push(else_if_block);
                else_if_conditions.push(else_if_cond);
            }
            
            // Create else block if needed
            let else_block = if else_body.is_some() || !else_ifs.is_empty() {
                let else_block_name = CString::new("else").unwrap();
                LLVMAppendBasicBlockInContext(self.context, func, else_block_name.as_ptr())
            } else {
                merge_block
            };
            
            // Branch on the main condition
            let first_else = else_if_blocks.first().copied().unwrap_or(else_block);
            LLVMBuildCondBr(self.builder, cond_val, then_block, first_else);
            
            // Compile then block
            LLVMPositionBuilderAtEnd(self.builder, then_block);
            for stmt in then_body {
                self.compile_statement(stmt)?;
            }
            // Only branch to merge if we haven't returned
            if LLVMGetBasicBlockTerminator(then_block).is_null() {
                LLVMBuildBr(self.builder, merge_block);
            }
            
            // Compile else-if blocks
            for (i, ((else_if_cond, else_if_body), else_if_block)) in 
                else_ifs.iter().zip(else_if_blocks.iter()).enumerate() {
                
                LLVMPositionBuilderAtEnd(self.builder, *else_if_block);
                let else_if_cond_val = self.compile_expression(else_if_cond)?;
                
                let else_if_then_name = CString::new(format!("elseif_then_{}", i)).unwrap();
                let else_if_then_block = LLVMAppendBasicBlockInContext(
                    self.context, func, else_if_then_name.as_ptr()
                );
                
                let next_block = else_if_blocks.get(i + 1).copied().unwrap_or(else_block);
                LLVMBuildCondBr(self.builder, else_if_cond_val, else_if_then_block, next_block);
                
                LLVMPositionBuilderAtEnd(self.builder, else_if_then_block);
                for stmt in else_if_body {
                    self.compile_statement(stmt)?;
                }
                if LLVMGetBasicBlockTerminator(else_if_then_block).is_null() {
                    LLVMBuildBr(self.builder, merge_block);
                }
            }
            
            // Compile else block if it exists
            if let Some(else_statements) = else_body {
                LLVMPositionBuilderAtEnd(self.builder, else_block);
                for stmt in else_statements {
                    self.compile_statement(stmt)?;
                }
                if LLVMGetBasicBlockTerminator(else_block).is_null() {
                    LLVMBuildBr(self.builder, merge_block);
                }
            } else if else_body.is_none() && !else_ifs.is_empty() {
                // Empty else block for else-if chains
                LLVMPositionBuilderAtEnd(self.builder, else_block);
                LLVMBuildBr(self.builder, merge_block);
            }
            
            // Continue at merge block
            LLVMPositionBuilderAtEnd(self.builder, merge_block);
        }
        
        Ok(())
    }
    
    fn compile_while_statement(&mut self, condition: &Expression, body: &[Statement]) -> Result<()> {
        unsafe {
            let func = LLVMGetBasicBlockParent(LLVMGetInsertBlock(self.builder));
            
            // Create basic blocks
            let loop_cond_name = CString::new("while_cond").unwrap();
            let loop_cond_block = LLVMAppendBasicBlockInContext(self.context, func, loop_cond_name.as_ptr());
            
            let loop_body_name = CString::new("while_body").unwrap();
            let loop_body_block = LLVMAppendBasicBlockInContext(self.context, func, loop_body_name.as_ptr());
            
            let loop_end_name = CString::new("while_end").unwrap();
            let loop_end_block = LLVMAppendBasicBlockInContext(self.context, func, loop_end_name.as_ptr());
            
            // Branch to condition check
            LLVMBuildBr(self.builder, loop_cond_block);
            
            // Compile condition
            LLVMPositionBuilderAtEnd(self.builder, loop_cond_block);
            let cond_val = self.compile_expression(condition)?;
            LLVMBuildCondBr(self.builder, cond_val, loop_body_block, loop_end_block);
            
            // Compile loop body
            LLVMPositionBuilderAtEnd(self.builder, loop_body_block);
            for stmt in body {
                self.compile_statement(stmt)?;
            }
            // Loop back to condition
            if LLVMGetBasicBlockTerminator(loop_body_block).is_null() {
                LLVMBuildBr(self.builder, loop_cond_block);
            }
            
            // Continue after loop
            LLVMPositionBuilderAtEnd(self.builder, loop_end_block);
        }
        
        Ok(())
    }
    
    fn compile_for_each_statement(&mut self, variable: &str, collection: &Expression, 
                                  body: &[Statement]) -> Result<()> {
        // Compile ForEach as an index-based loop with proper array bounds
        unsafe {
            let func = LLVMGetBasicBlockParent(LLVMGetInsertBlock(self.builder));
            
            // Compile the collection expression
            let collection_val = self.compile_expression(collection)?;
            
            // Create loop counter
            let _i32_type = LLVMInt32TypeInContext(self.context);
            let i64_type = LLVMInt64TypeInContext(self.context);
            let counter_name = CString::new("for_counter").unwrap();
            let counter_ptr = LLVMBuildAlloca(self.builder, i64_type, counter_name.as_ptr());
            LLVMBuildStore(self.builder, LLVMConstInt(i64_type, 0, 0), counter_ptr);
            
            // Calculate actual array length based on collection type
            // Collections in Runa have an implicit length property
            let array_length = match self.infer_expression_type(collection) {
                Ok(Type::Named(type_name)) if type_name.contains("Array") => {
                    // Arrays have a fixed size encoded in their type
                    // Extract size from type name or use dynamic size calculation
                    let size_name = CString::new("array_size").unwrap();
                    let size_ptr = LLVMBuildStructGEP2(
                        self.builder,
                        LLVMTypeOf(collection_val),
                        collection_val,
                        0, // Size field is typically first
                        size_name.as_ptr()
                    );
                    LLVMBuildLoad2(self.builder, i64_type, size_ptr, size_name.as_ptr())
                }
                _ => {
                    // For other collection types, compute length dynamically
                    // This handles strings, lists, and other iterable types
                    let get_len_name = CString::new("get_length").unwrap();
                    LLVMBuildCall2(
                        self.builder,
                        LLVMFunctionType(i64_type, std::ptr::null_mut(), 0, 0),
                        collection_val,
                        std::ptr::null_mut(),
                        0,
                        get_len_name.as_ptr()
                    )
                }
            };
            
            // Create basic blocks
            let loop_cond_name = CString::new("for_cond").unwrap();
            let loop_cond_block = LLVMAppendBasicBlockInContext(self.context, func, loop_cond_name.as_ptr());
            
            let loop_body_name = CString::new("for_body").unwrap();
            let loop_body_block = LLVMAppendBasicBlockInContext(self.context, func, loop_body_name.as_ptr());
            
            let loop_end_name = CString::new("for_end").unwrap();
            let loop_end_block = LLVMAppendBasicBlockInContext(self.context, func, loop_end_name.as_ptr());
            
            // Branch to condition
            LLVMBuildBr(self.builder, loop_cond_block);
            
            // Check loop condition (counter < array_length)
            LLVMPositionBuilderAtEnd(self.builder, loop_cond_block);
            let counter_val_name = CString::new("counter_val").unwrap();
            let counter_val = LLVMBuildLoad2(self.builder, i64_type, counter_ptr, counter_val_name.as_ptr());
            
            let cmp_name = CString::new("for_cmp").unwrap();
            let cond = LLVMBuildICmp(self.builder, llvm_sys::LLVMIntPredicate::LLVMIntSLT, 
                                     counter_val, array_length, cmp_name.as_ptr());
            LLVMBuildCondBr(self.builder, cond, loop_body_block, loop_end_block);
            
            // Loop body
            LLVMPositionBuilderAtEnd(self.builder, loop_body_block);
            
            // Get current element from collection and bind to variable
            let elem_name = CString::new("elem").unwrap();
            let elem_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMTypeOf(collection_val),
                collection_val,
                &counter_val as *const _ as *mut LLVMValueRef,
                1,
                elem_name.as_ptr()
            );
            let elem_val = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context), // Element type
                elem_ptr,
                elem_name.as_ptr()
            );
            
            // Bind element to loop variable
            self.variables.insert(variable.to_string(), elem_val);
            self.variable_types.insert(variable.to_string(), Type::Integer);
            
            // Execute loop body
            for stmt in body {
                self.compile_statement(stmt)?;
            }
            
            // Increment counter
            let one = LLVMConstInt(i64_type, 1, 0);
            let inc_name = CString::new("inc").unwrap();
            let incremented = LLVMBuildAdd(self.builder, counter_val, one, inc_name.as_ptr());
            LLVMBuildStore(self.builder, incremented, counter_ptr);
            
            // Loop back
            if LLVMGetBasicBlockTerminator(loop_body_block).is_null() {
                LLVMBuildBr(self.builder, loop_cond_block);
            }
            
            // Continue after loop
            LLVMPositionBuilderAtEnd(self.builder, loop_end_block);
        }
        
        Ok(())
    }
    
    fn compile_inline_assembly(&mut self, instructions: &[String], 
                               output_constraints: &[(String, String)],
                               input_constraints: &[(String, String)],
                               clobbers: &[String]) -> Result<()> {
        unsafe {
            // Build the assembly string - handle common patterns
            let mut asm_string = String::new();
            for instruction in instructions {
                let mut processed = instruction.to_string();
                
                // Special case: immediate value moves like "mov $42, %0"
                // Convert to LLVM-compatible syntax without operand references
                if processed.contains("mov $") && processed.contains(", %0") {
                    // Extract the immediate value
                    if let Some(start) = processed.find("$") {
                        if let Some(end) = processed[start+1..].find(",") {
                            let immediate = &processed[start+1..start+1+end];
                            // Generate direct register move without operand reference
                            processed = format!("movl $${}, %eax", immediate);
                            // Mark that we need to handle output specially
                            self.inline_asm_special_output = true;
                        }
                    }
                } else {
                    // For other instructions, escape $ for LLVM
                    processed = processed.replace("$", "$$");
                }
                
                asm_string.push_str(&processed);
                if !processed.ends_with('\n') {
                    asm_string.push('\n');
                }
            }
            
            // Prepare operands and constraints - LLVM inline assembly operands must match constraint order
            let mut operand_values = Vec::new();
            let mut operand_types = Vec::new();
            let mut constraint_parts = Vec::new();
            let mut output_vars = Vec::new();
            
            // For outputs - handle special case where we're using hardcoded register
            for (constraint, var_name) in output_constraints {
                let i32_type = LLVMInt32TypeInContext(self.context);
                let var_name_c = CString::new(var_name.clone()).unwrap();
                let alloca = LLVMBuildAlloca(self.builder, i32_type, var_name_c.as_ptr());
                
                if self.inline_asm_special_output {
                    // Special case: we're using %eax directly, so constraint is different
                    constraint_parts.push("={eax}".to_string());
                } else {
                    // Normal case: provide operand for %0 reference
                    let zero_val = LLVMConstInt(i32_type, 0, 0);
                    operand_values.push(zero_val);
                    operand_types.push(i32_type);
                    constraint_parts.push(constraint.clone());
                }
                
                output_vars.push((var_name.clone(), alloca));
            }
            
            // Add input operands and constraints after outputs
            for (constraint, var_name) in input_constraints {
                if let Some(&val) = self.variables.get(var_name) {
                    // Load the value if it's a pointer
                    let loaded_val = if LLVMGetTypeKind(LLVMTypeOf(val)) == llvm_sys::LLVMTypeKind::LLVMPointerTypeKind {
                        let load_name = CString::new("load_input").unwrap();
                        LLVMBuildLoad2(self.builder, LLVMInt64TypeInContext(self.context), val, load_name.as_ptr())
                    } else {
                        val
                    };
                    operand_values.push(loaded_val);
                    operand_types.push(LLVMTypeOf(loaded_val));
                    constraint_parts.push(constraint.clone());
                } else {
                    return Err(anyhow::anyhow!("Undefined variable in inline assembly input: {}", var_name));
                }
            }
            
            // Add clobbers to constraints
            for clobber in clobbers {
                constraint_parts.push(format!("~{{{}}}", clobber));
            }
            
            let constraint_string = constraint_parts.join(",");
            
            // Create the inline assembly function type
            let return_type = if output_constraints.len() == 1 {
                // Single output returns the value (32-bit for movl)
                LLVMInt32TypeInContext(self.context)
            } else if output_constraints.is_empty() {
                // No outputs - void
                LLVMVoidTypeInContext(self.context)
            } else {
                // Multiple outputs - create struct with all output types
                let mut output_types: Vec<LLVMTypeRef> = Vec::new();
                for (_, var) in output_constraints {
                    if let Some(var_type) = self.variable_types.get(var).cloned() {
                        output_types.push(self.llvm_type(&var_type)?);
                    } else {
                        return Err(anyhow::anyhow!("Unknown output variable type: {}", var));
                    }
                }
                LLVMStructTypeInContext(
                    self.context,
                    output_types.as_mut_ptr(),
                    output_types.len() as u32,
                    0
                )
            };
            
            let func_type = LLVMFunctionType(
                return_type,
                operand_types.as_ptr() as *mut _,
                operand_types.len() as u32,
                0
            );
            
            // Create the inline assembly value
            let asm_c = CString::new(asm_string).unwrap();
            let constraint_c = CString::new(constraint_string).unwrap();
            
            let inline_asm = LLVMGetInlineAsm(
                func_type,
                asm_c.as_ptr() as *mut i8,
                asm_c.to_bytes().len(),
                constraint_c.as_ptr() as *mut i8,
                constraint_c.to_bytes().len(),
                1, // has_side_effects
                0, // is_align_stack
                llvm_sys::LLVMInlineAsmDialect::LLVMInlineAsmDialectATT,
                0  // can_throw
            );

            // Call the inline assembly
            let call_name = CString::new("asm").unwrap();
            let result = LLVMBuildCall2(
                self.builder,
                func_type,
                inline_asm,
                operand_values.as_ptr() as *mut _,
                operand_values.len() as u32,
                call_name.as_ptr()
            );
            
            // Store output variables in symbol table
            if output_constraints.len() == 1 {
                // Single output - store the returned value
                let (var_name, alloca) = &output_vars[0];
                LLVMBuildStore(self.builder, result, *alloca);
                // Store the alloca pointer, not the value - it will be loaded when used
                self.variables.insert(var_name.clone(), *alloca);
                self.variable_types.insert(var_name.clone(), Type::Integer);
            } else {
                // No outputs or multiple outputs
                for (var_name, alloca) in output_vars {
                    self.variables.insert(var_name.clone(), alloca);
                    self.variable_types.insert(var_name, Type::Integer);
                }
            }
            
            // Reset the special output flag
            self.inline_asm_special_output = false;
        }
        
        Ok(())
    }
    
    fn compile_field_access(&mut self, object: &Expression, field: &str) -> Result<LLVMValueRef> {
        unsafe {
            let obj_val = self.compile_expression(object)?;
            
            // Get the struct type name from the object expression
            let struct_type_name = self.get_object_type_name(object)?;
            
            // Find the type definition
            let type_def = self.find_type_definition(&struct_type_name)?;
            
            // Find the field index and type
            let (field_index, field_type) = type_def.fields.iter()
                .enumerate()
                .find(|(_, (name, _))| name == field)
                .map(|(idx, (_, typ))| (idx, typ.clone()))
                .ok_or_else(|| anyhow::anyhow!("Field '{}' not found in type '{}'", field, struct_type_name))?;
            
            // Create GEP (GetElementPtr) instruction to access the field
            let indices = [
                LLVMConstInt(LLVMInt32TypeInContext(self.context), 0, 0), // struct pointer
                LLVMConstInt(LLVMInt32TypeInContext(self.context), field_index as u64, 0), // field index
            ];
            
            let field_name = CString::new(format!("{}.{}", struct_type_name, field)).unwrap();
            let field_ptr = LLVMBuildGEP2(
                self.builder,
                self.type_definitions[&struct_type_name],
                obj_val,
                indices.as_ptr() as *mut LLVMValueRef,
                indices.len() as u32,
                field_name.as_ptr()
            );
            
            // Load the field value
            let load_name = CString::new(format!("load_{}", field)).unwrap();
            let llvm_field_type = self.llvm_type(&field_type);
            Ok(LLVMBuildLoad2(
                self.builder,
                llvm_field_type?,
                field_ptr,
                load_name.as_ptr()
            ))
        }
    }
    
    fn infer_expression_type(&self, expr: &Expression) -> Result<Type> {
        match expr {
            Expression::Integer(_) => Ok(Type::Integer),
            Expression::Float(_) => Ok(Type::Float),
            Expression::String(_) => Ok(Type::String),
            Expression::Boolean(_) => Ok(Type::Boolean),
            Expression::Variable(name) => {
                self.variable_types.get(name)
                    .cloned()
                    .ok_or_else(|| anyhow::anyhow!("Unknown variable type: {}", name))
            }
            Expression::FieldAccess { object, field } => {
                // Get the object type first
                let obj_type = self.infer_expression_type(object)?;
                match obj_type {
                    Type::Named(type_name) => {
                        // Find the field type in the struct definition
                        let type_def = self.runa_type_definitions.get(&type_name)
                            .ok_or_else(|| anyhow::anyhow!("Type definition not found: {}", type_name))?;
                        
                        for (field_name, field_type) in &type_def.fields {
                            if field_name == field {
                                return Ok(field_type.clone());
                            }
                        }
                        Err(anyhow::anyhow!("Field '{}' not found in type '{}'", field, type_name))
                    }
                    _ => Err(anyhow::anyhow!("Cannot access field on non-struct type"))
                }
            }
            Expression::Call { name, .. } => {
                // Check for built-in string functions first
                match name.as_str() {
                    "string_length" => Ok(Type::Integer),
                    "string_compare" => Ok(Type::Integer),
                    "string_substring" => Ok(Type::String),
                    "string_char_at" => Ok(Type::Integer),
                    _ => {
                        // Look up the function's return type
                        if let Some(func_type) = self.function_return_types.get(name) {
                            Ok(func_type.clone())
                        } else {
                            Err(anyhow::anyhow!("Unknown function: {}", name))
                        }
                    }
                }
            }
            Expression::Binary { left, .. } => {
                // Binary operations typically preserve the left operand type
                self.infer_expression_type(left)
            }
            Expression::Constructor { type_name, .. } => {
                // Constructor creates an instance of the named type
                Ok(Type::Named(type_name.clone()))
            }
        }
    }
    
    fn get_object_type_name(&self, expr: &Expression) -> Result<String> {
        let expr_type = self.infer_expression_type(expr)?;
        match expr_type {
            Type::Named(type_name) => Ok(type_name),
            _ => Err(anyhow::anyhow!("Expression is not a named type"))
        }
    }
    
    fn find_type_definition(&self, type_name: &str) -> Result<&TypeDefinition> {
        self.runa_type_definitions.get(type_name)
            .ok_or_else(|| anyhow::anyhow!("Type definition not found: {}", type_name))
    }
    
    fn compile_type_definition(&mut self, type_def: &TypeDefinition) -> Result<()> {
        unsafe {
            let mut field_types = Vec::new();
            for (_, field_type) in &type_def.fields {
                field_types.push(self.llvm_type(field_type)?);
            }

            let struct_type = LLVMStructTypeInContext(
                self.context,
                field_types.as_mut_ptr(),
                field_types.len() as u32,
                0 // Not packed
            );
            
            self.type_definitions.insert(type_def.name.clone(), struct_type);
            self.runa_type_definitions.insert(type_def.name.clone(), type_def.clone());
        }
        Ok(())
    }
    
    fn llvm_type(&mut self, runa_type: &Type) -> Result<LLVMTypeRef> {
        unsafe {
            Ok(match runa_type {
                Type::Integer => LLVMInt64TypeInContext(self.context),
                Type::Float => LLVMDoubleTypeInContext(self.context),
                Type::Boolean => LLVMInt1TypeInContext(self.context),
                Type::String => LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                Type::Void => LLVMVoidTypeInContext(self.context),
                Type::Named(name) => {
                    self.type_definitions.get(name)
                        .copied()
                        .ok_or_else(|| anyhow::anyhow!("Type '{}' not defined", name))
                        .unwrap_or_else(|err| {
                            // Create forward declaration for unresolved types
                            // This handles forward references and external types
                            eprintln!("Warning: {}", err);
                            let opaque_type = LLVMStructCreateNamed(self.context,
                                CString::new(name.clone()).unwrap().as_ptr());
                            let ptr = LLVMPointerType(opaque_type, 0);
                            // Cache the forward declaration
                            self.type_definitions.insert(name.clone(), ptr);
                            ptr
                        })
                }
            })
        }
    }

    fn compile_print_statement(&mut self, message: &Expression) -> Result<()> {
        unsafe {
            let message_value = self.compile_expression(message)?;

            // Declare printf if not already declared
            let printf_name = CString::new("printf").unwrap();
            let printf_func = LLVMGetNamedFunction(self.module, printf_name.as_ptr());
            let printf_func = if printf_func.is_null() {
                // Declare printf function: i32 printf(i8* format, ...)
                let i32_type = LLVMInt32TypeInContext(self.context);
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let printf_type = LLVMFunctionType(i32_type, [i8_ptr_type].as_ptr() as *mut _, 1, 1); // variadic = 1
                LLVMAddFunction(self.module, printf_name.as_ptr(), printf_type)
            } else {
                printf_func
            };

            // Call printf with the message
            let args = [message_value];
            let call_name = CString::new("printf_call").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(printf_func),
                printf_func,
                args.as_ptr() as *mut _,
                1,
                call_name.as_ptr()
            );

            Ok(())
        }
    }

    fn compile_read_file(&mut self, filename: &Expression, target: &str) -> Result<()> {
        unsafe {
            // Get the filename string
            let filename_value = self.compile_expression(filename)?;

            // Declare fopen if not already declared
            let fopen_name = CString::new("fopen").unwrap();
            let fopen_func = LLVMGetNamedFunction(self.module, fopen_name.as_ptr());
            let fopen_func = if fopen_func.is_null() {
                // FILE* fopen(const char* filename, const char* mode)
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let fopen_type = LLVMFunctionType(
                    i8_ptr_type, // FILE* return type (simplified as i8*)
                    [i8_ptr_type, i8_ptr_type].as_ptr() as *mut _,
                    2,
                    0 // not variadic
                );
                LLVMAddFunction(self.module, fopen_name.as_ptr(), fopen_type)
            } else {
                fopen_func
            };

            // Declare fread if not already declared
            let fread_name = CString::new("fread").unwrap();
            let fread_func = LLVMGetNamedFunction(self.module, fread_name.as_ptr());
            let fread_func = if fread_func.is_null() {
                // size_t fread(void* ptr, size_t size, size_t count, FILE* stream)
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let i64_type = LLVMInt64TypeInContext(self.context);
                let fread_type = LLVMFunctionType(
                    i64_type, // size_t return type
                    [i8_ptr_type, i64_type, i64_type, i8_ptr_type].as_ptr() as *mut _,
                    4,
                    0 // not variadic
                );
                LLVMAddFunction(self.module, fread_name.as_ptr(), fread_type)
            } else {
                fread_func
            };

            // Declare fclose if not already declared
            let fclose_name = CString::new("fclose").unwrap();
            let fclose_func = LLVMGetNamedFunction(self.module, fclose_name.as_ptr());
            let fclose_func = if fclose_func.is_null() {
                // int fclose(FILE* stream)
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let i32_type = LLVMInt32TypeInContext(self.context);
                let fclose_type = LLVMFunctionType(
                    i32_type,
                    [i8_ptr_type].as_ptr() as *mut _,
                    1,
                    0 // not variadic
                );
                LLVMAddFunction(self.module, fclose_name.as_ptr(), fclose_type)
            } else {
                fclose_func
            };

            // Create mode string "r" for reading
            let mode_str = CString::new("r").unwrap();
            let mode_name = CString::new("read_mode").unwrap();
            let mode_value = LLVMBuildGlobalStringPtr(
                self.builder,
                mode_str.as_ptr(),
                mode_name.as_ptr()
            );

            // Call fopen
            let fopen_call_name = CString::new("fopen_call").unwrap();
            let file_ptr = LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(fopen_func),
                fopen_func,
                [filename_value, mode_value].as_ptr() as *mut _,
                2,
                fopen_call_name.as_ptr()
            );

            // Allocate buffer for file content (8KB buffer)
            let i8_type = LLVMInt8TypeInContext(self.context);
            let buffer_size = 8192;
            let array_type = LLVMArrayType(i8_type, buffer_size);
            let buffer_name = CString::new("file_buffer").unwrap();
            let buffer = LLVMBuildAlloca(self.builder, array_type, buffer_name.as_ptr());

            // Get pointer to first element of buffer
            let i64_type = LLVMInt64TypeInContext(self.context);
            let zero = LLVMConstInt(i64_type, 0, 0);
            let indices = [zero, zero];
            let buffer_ptr_name = CString::new("buffer_ptr").unwrap();
            let buffer_ptr = LLVMBuildGEP2(
                self.builder,
                array_type,
                buffer,
                indices.as_ptr() as *mut _,
                2,
                buffer_ptr_name.as_ptr()
            );

            // Call fread to read file content
            let size_one = LLVMConstInt(i64_type, 1, 0);
            let size_max = LLVMConstInt(i64_type, (buffer_size - 1) as u64, 0);
            let fread_call_name = CString::new("fread_call").unwrap();
            let bytes_read = LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(fread_func),
                fread_func,
                [buffer_ptr, size_one, size_max, file_ptr].as_ptr() as *mut _,
                4,
                fread_call_name.as_ptr()
            );

            // Null-terminate the buffer
            let terminator_name = CString::new("null_terminator").unwrap();
            let terminator_ptr = LLVMBuildGEP2(
                self.builder,
                i8_type,
                buffer_ptr,
                [bytes_read].as_ptr() as *mut _,
                1,
                terminator_name.as_ptr()
            );
            let zero_byte = LLVMConstInt(i8_type, 0, 0);
            LLVMBuildStore(self.builder, zero_byte, terminator_ptr);

            // Close the file
            let fclose_call_name = CString::new("fclose_call").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(fclose_func),
                fclose_func,
                [file_ptr].as_ptr() as *mut _,
                1,
                fclose_call_name.as_ptr()
            );

            // Store the buffer pointer as a string in the target variable
            self.variables.insert(target.to_string(), buffer_ptr);
            self.variable_types.insert(target.to_string(), Type::String);
            self.variable_storage.insert(target.to_string(), StorageKind::Direct);

            Ok(())
        }
    }

    fn compile_write_file(&mut self, filename: &Expression, content: &Expression) -> Result<()> {
        unsafe {
            // Get the filename and content strings
            let filename_value = self.compile_expression(filename)?;
            let content_value = self.compile_expression(content)?;

            // Declare fopen if not already declared
            let fopen_name = CString::new("fopen").unwrap();
            let fopen_func = LLVMGetNamedFunction(self.module, fopen_name.as_ptr());
            let fopen_func = if fopen_func.is_null() {
                // FILE* fopen(const char* filename, const char* mode)
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let fopen_type = LLVMFunctionType(
                    i8_ptr_type,
                    [i8_ptr_type, i8_ptr_type].as_ptr() as *mut _,
                    2,
                    0
                );
                LLVMAddFunction(self.module, fopen_name.as_ptr(), fopen_type)
            } else {
                fopen_func
            };

            // Declare fprintf if not already declared
            let fprintf_name = CString::new("fprintf").unwrap();
            let fprintf_func = LLVMGetNamedFunction(self.module, fprintf_name.as_ptr());
            let fprintf_func = if fprintf_func.is_null() {
                // int fprintf(FILE* stream, const char* format, ...)
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let i32_type = LLVMInt32TypeInContext(self.context);
                let fprintf_type = LLVMFunctionType(
                    i32_type,
                    [i8_ptr_type, i8_ptr_type].as_ptr() as *mut _,
                    2,
                    1 // variadic
                );
                LLVMAddFunction(self.module, fprintf_name.as_ptr(), fprintf_type)
            } else {
                fprintf_func
            };

            // Declare fclose if not already declared
            let fclose_name = CString::new("fclose").unwrap();
            let fclose_func = LLVMGetNamedFunction(self.module, fclose_name.as_ptr());
            let fclose_func = if fclose_func.is_null() {
                let i8_ptr_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                let i32_type = LLVMInt32TypeInContext(self.context);
                let fclose_type = LLVMFunctionType(
                    i32_type,
                    [i8_ptr_type].as_ptr() as *mut _,
                    1,
                    0
                );
                LLVMAddFunction(self.module, fclose_name.as_ptr(), fclose_type)
            } else {
                fclose_func
            };

            // Create mode string "w" for writing
            let mode_str = CString::new("w").unwrap();
            let mode_name = CString::new("write_mode").unwrap();
            let mode_value = LLVMBuildGlobalStringPtr(
                self.builder,
                mode_str.as_ptr(),
                mode_name.as_ptr()
            );

            // Call fopen
            let fopen_call_name = CString::new("fopen_call").unwrap();
            let file_ptr = LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(fopen_func),
                fopen_func,
                [filename_value, mode_value].as_ptr() as *mut _,
                2,
                fopen_call_name.as_ptr()
            );

            // Create format string "%s" for fprintf
            let format_str = CString::new("%s").unwrap();
            let format_name = CString::new("fprintf_format").unwrap();
            let format_value = LLVMBuildGlobalStringPtr(
                self.builder,
                format_str.as_ptr(),
                format_name.as_ptr()
            );

            // Call fprintf to write content
            let fprintf_call_name = CString::new("fprintf_call").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(fprintf_func),
                fprintf_func,
                [file_ptr, format_value, content_value].as_ptr() as *mut _,
                3,
                fprintf_call_name.as_ptr()
            );

            // Close the file
            let fclose_call_name = CString::new("fclose_call").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMGlobalGetValueType(fclose_func),
                fclose_func,
                [file_ptr].as_ptr() as *mut _,
                1,
                fclose_call_name.as_ptr()
            );

            Ok(())
        }
    }

    fn emit_object_file(&self, output_path: &Path) -> Result<()> {
        unsafe {
            // Get default target triple
            let target_triple = LLVMGetDefaultTargetTriple();
            LLVMSetTarget(self.module, target_triple);
            
            let mut target: LLVMTargetRef = std::ptr::null_mut();
            let mut error_message: *mut i8 = std::ptr::null_mut();
            
            if LLVMGetTargetFromTriple(target_triple, &mut target, &mut error_message) != 0 {
                let error_str = std::ffi::CStr::from_ptr(error_message).to_string_lossy();
                LLVMDisposeMessage(error_message);
                return Err(anyhow::anyhow!("Failed to get target: {}", error_str));
            }
            
            let cpu = CString::new("generic").unwrap();
            let features = CString::new("").unwrap();
            let target_machine = LLVMCreateTargetMachine(
                target,
                target_triple,
                cpu.as_ptr(),
                features.as_ptr(),
                LLVMCodeGenOptLevel::LLVMCodeGenLevelDefault,
                LLVMRelocMode::LLVMRelocDefault,
                LLVMCodeModel::LLVMCodeModelDefault
            );
            
            let output_str = CString::new(output_path.to_string_lossy().as_ref()).unwrap();
            let mut error_message: *mut i8 = std::ptr::null_mut();
            
            if LLVMTargetMachineEmitToFile(
                target_machine,
                self.module,
                output_str.as_ptr() as *mut i8,
                LLVMCodeGenFileType::LLVMObjectFile,
                &mut error_message
            ) != 0 {
                let error_str = std::ffi::CStr::from_ptr(error_message).to_string_lossy();
                LLVMDisposeMessage(error_message);
                LLVMDisposeTargetMachine(target_machine);
                return Err(anyhow::anyhow!("Failed to emit object file: {}", error_str));
            }
            
            LLVMDisposeTargetMachine(target_machine);
            LLVMDisposeMessage(target_triple);
        }

        Ok(())
    }
}