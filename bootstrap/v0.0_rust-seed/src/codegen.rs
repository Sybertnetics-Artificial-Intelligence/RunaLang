use crate::parser::{AstNode, BinaryOperator, Parameter};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct FunctionInfo {
    pub parameters: Vec<Parameter>,
    pub return_type: Option<String>,
    pub label: String,
    pub returns_string: bool,  // Track if function returns a string type
}

struct FunctionGenContext {
    variables: HashMap<String, i32>,
    variable_types: HashMap<String, bool>,
    stack_offset: i32,
}

impl FunctionGenContext {
    fn new() -> Self {
        Self {
            variables: HashMap::new(),
            variable_types: HashMap::new(),
            stack_offset: 0,
        }
    }
}

pub struct CodeGenerator {
    variables: HashMap<String, i32>, // Variable name -> stack offset
    variable_types: HashMap<String, bool>, // Variable name -> is_string
    functions: HashMap<String, FunctionInfo>, // Function name -> info
    stack_offset: i32,
    output: String,
    label_counter: i32,
    string_counter: i32,
    in_function: bool,
    string_literals: Vec<(String, String)>, // (label, content)
}

impl CodeGenerator {
    pub fn new() -> Self {
        Self {
            variables: HashMap::new(),
            variable_types: HashMap::new(),
            functions: HashMap::new(),
            stack_offset: 0,
            output: String::new(),
            label_counter: 0,
            string_counter: 0,
            in_function: false,
            string_literals: Vec::new(),
        }
    }

    pub fn generate(&mut self, ast: &AstNode) -> Result<String, String> {
        // First pass: generate rodata section and function definitions
        self.emit("    .section .rodata");
        self.emit(".LC0:");
        self.emit("    .string \"%d\\n\"");
        self.emit(".LC1:");
        self.emit("    .string \"%s\\n\"");
        self.emit("");
        self.emit(".LC2:");
        self.emit("    .string \"%d\"");
        self.emit("");
        self.emit("    .text");

        // Generate function definitions first
        if let AstNode::Program(statements) = ast {
            for stmt in statements {
                if let AstNode::ProcessDefinition { name, parameters, return_type, body } = stmt {
                    self.generate_process_definition(name, parameters, return_type, body)?;
                }
            }
        }

        // Then generate main function
        self.emit_main_header();
        self.generate_main_body(ast)?;
        self.emit_main_footer();

        // Add file I/O helper functions
        self.emit_file_io_functions();

        // Finally, emit all string literals in the rodata section
        self.emit_string_literals();

        Ok(self.output.clone())
    }

    fn generate_node_with_context(&mut self, node: &AstNode, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        match node {
            AstNode::Program(statements) => {
                for stmt in statements {
                    self.generate_node_with_context(stmt, fn_ctx)?;
                }
            }
            AstNode::LetStatement { variable, value } => {
                self.generate_let_statement_with_context(variable, value, fn_ctx)?;
            }
            AstNode::SetStatement { variable, value } => {
                self.generate_set_statement_with_context(variable, value, fn_ctx)?;
            }
            AstNode::DisplayStatement { value } => {
                self.generate_display_statement_with_context(value, fn_ctx)?;
            }
            AstNode::NoteStatement { .. } => {
                // Note statements are comments - generate no code
            }
            AstNode::ReturnStatement { value } => {
                self.generate_return_statement_with_context(value, fn_ctx)?;
            }
            AstNode::IfStatement { condition, then_block, else_block } => {
                self.generate_if_statement_with_context(condition, then_block, else_block, fn_ctx)?;
            }
            AstNode::WhileStatement { condition, body } => {
                self.generate_while_statement_with_context(condition, body, fn_ctx)?;
            }
            AstNode::ProcessDefinition { name, parameters, return_type, body } => {
                return Err("Process definitions should not be nested".to_string());
            }
            AstNode::TypeDefinition { .. } => {
                // Type definitions don't generate code, they're just declarations
            }
            AstNode::StructCreation { .. } => {
                // Use the working expression generator for struct creation
                self.generate_expression_with_context(node, fn_ctx)?;
            }
            AstNode::FieldAccess { .. } => {
                // Use the working expression generator for field access
                self.generate_expression_with_context(node, fn_ctx)?;
            }
            _ => return Err("Unsupported node type in code generation".to_string()),
        }
        Ok(())
    }

    fn generate_node(&mut self, node: &AstNode) -> Result<(), String> {
        match node {
            AstNode::Program(statements) => {
                for stmt in statements {
                    self.generate_node(stmt)?;
                }
            }
            AstNode::LetStatement { variable, value } => {
                self.generate_let_statement(variable, value)?;
            }
            AstNode::SetStatement { variable, value } => {
                self.generate_set_statement(variable, value)?;
            }
            AstNode::DisplayStatement { value } => {
                self.generate_display_statement(value)?;
            }
            AstNode::NoteStatement { .. } => {
                // Note statements are comments - generate no code
            }
            AstNode::ReturnStatement { value } => {
                self.generate_return_statement(value)?;
            }
            AstNode::IfStatement { condition, then_block, else_block } => {
                self.generate_if_statement(condition, then_block, else_block)?;
            }
            AstNode::WhileStatement { condition, body } => {
                self.generate_while_statement(condition, body)?;
            }
            AstNode::ProcessDefinition { name, parameters, return_type, body } => {
                self.generate_process_definition(name, parameters, return_type, body)?;
            }
            AstNode::TypeDefinition { .. } => {
                // Type definitions don't generate code, they're just declarations
            }
            AstNode::StructCreation { .. } => {
                // Use the working expression generator for struct creation
                self.generate_expression(node)?;
            }
            AstNode::FieldAccess { .. } => {
                // Use the working expression generator for field access
                self.generate_expression(node)?;
            }
            AstNode::IndexAccess { .. } => {
                // Use the working expression generator for index access
                self.generate_expression(node)?;
            }
            AstNode::FunctionCall { .. } => {
                // Handle standalone function calls (like write_file)
                self.generate_expression(node)?;
            }
            _ => return Err("Unsupported node type in code generation".to_string()),
        }
        Ok(())
    }

    fn generate_let_statement(&mut self, variable: &str, value: &AstNode) -> Result<(), String> {
        // Generate code for the value and put result in %rax
        self.generate_expression(value)?;

        // Track variable type
        let is_string = match value {
            AstNode::StringLiteral(_) => true,
            AstNode::FunctionCall { name, .. } => {
                // Check if it's a built-in that returns strings
                if matches!(name.as_str(), "substring" | "concat" | "to_string" | "trim" | "to_upper" | "to_lower" | "replace") {
                    true
                } else {
                    // Check if it's a user-defined function that returns strings
                    self.functions.get(name).map(|f| f.returns_string).unwrap_or(false)
                }
            }
            _ => false,
        };
        self.variable_types.insert(variable.to_string(), is_string);

        // For simplicity, use 64-bit storage for all variables (this handles both pointers and integers)
        self.stack_offset += 8;
        self.variables.insert(variable.to_string(), self.stack_offset);
        self.emit(&format!("    movq %rax, -{}(%rbp)", self.stack_offset));

        Ok(())
    }

    fn generate_set_statement(&mut self, variable: &str, value: &AstNode) -> Result<(), String> {
        // Generate code for the value and put result in %rax
        self.generate_expression(value)?;

        // Look up existing variable location
        if let Some(&offset) = self.variables.get(variable) {
            // Store %rax (64-bit) to existing stack location
            self.emit(&format!("    movq %rax, -{}(%rbp)", offset));
        } else {
            return Err(format!("Undefined variable in set statement: {}", variable));
        }

        Ok(())
    }

    fn generate_display_statement(&mut self, value: &AstNode) -> Result<(), String> {
        // Generate code for the value and put result in %rax
        self.generate_expression(value)?;

        // Determine the type of the value to choose the correct format string
        let is_string_value = match value {
            AstNode::StringLiteral(_) => true,
            AstNode::Identifier(name) => {
                // Check if this variable was declared as a string
                self.variable_types.get(name).copied().unwrap_or(false)
            }
            AstNode::FunctionCall { name, .. } => {
                // Check if it's a built-in that returns strings
                if matches!(name.as_str(), "substring" | "concat" | "to_string" | "trim" | "to_upper" | "to_lower" | "replace") {
                    true
                } else {
                    // Check if it's a user-defined function that returns strings
                    self.functions.get(name).map(|f| f.returns_string).unwrap_or(false)
                }
            }
            _ => false,
        };

        if is_string_value {
            // For string values, use %s format (64-bit address)
            self.emit("    movq %rax, %rsi");
            self.emit("    leaq .LC1(%rip), %rdi");  // %s format
        } else {
            // For integer values, use %d format (32-bit integer)
            self.emit("    movl %eax, %esi");
            self.emit("    leaq .LC0(%rip), %rdi");  // %d format
        }

        // Call printf
        self.emit("    movl $0, %eax");  // No vector registers used
        self.emit("    call printf@PLT");

        Ok(())
    }

    fn generate_return_statement(&mut self, value: &Option<Box<AstNode>>) -> Result<(), String> {
        // Generate code for return value if present
        if let Some(return_value) = value {
            self.generate_expression(return_value)?;
            // Value is now in %eax, which is the standard return register
        } else {
            // No return value, return 0
            self.emit("    movl $0, %eax");
        }

        // Function epilogue
        self.emit("    leave");
        self.emit("    ret");

        Ok(())
    }

    fn generate_if_statement(&mut self, condition: &AstNode, then_block: &[AstNode], else_block: &Option<Vec<AstNode>>) -> Result<(), String> {
        // Generate unique labels
        let else_label = format!(".L_else_{}", self.label_counter);
        let end_label = format!(".L_end_{}", self.label_counter);
        self.label_counter += 1;

        // Generate condition code (result in %eax, 0 = false, non-zero = true)
        self.generate_expression(condition)?;

        // Test condition and jump to else label if false
        self.emit("    testl %eax, %eax");
        self.emit(&format!("    je {}", else_label));

        // Generate then block
        for stmt in then_block {
            self.generate_node(stmt)?;
        }

        // Jump to end (skip else block)
        self.emit(&format!("    jmp {}", end_label));

        // Else label
        self.emit(&format!("{}:", else_label));

        // Generate else block if present
        if let Some(else_statements) = else_block {
            for stmt in else_statements {
                self.generate_node(stmt)?;
            }
        }

        // End label
        self.emit(&format!("{}:", end_label));

        Ok(())
    }

    fn generate_while_statement(&mut self, condition: &AstNode, body: &[AstNode]) -> Result<(), String> {
        // Generate unique labels
        let loop_start = format!(".L_while_start_{}", self.label_counter);
        let loop_end = format!(".L_while_end_{}", self.label_counter);
        self.label_counter += 1;

        // Loop start label
        self.emit(&format!("{}:", loop_start));

        // Generate condition code (result in %eax, 0 = false, non-zero = true)
        self.generate_expression(condition)?;

        // Test condition and jump to end label if false
        self.emit("    testl %eax, %eax");
        self.emit(&format!("    je {}", loop_end));

        // Generate loop body
        for stmt in body {
            self.generate_node(stmt)?;
        }

        // Jump back to start of loop
        self.emit(&format!("    jmp {}", loop_start));

        // Loop end label
        self.emit(&format!("{}:", loop_end));

        Ok(())
    }

    fn generate_expression(&mut self, expr: &AstNode) -> Result<(), String> {
        match expr {
            AstNode::IntegerLiteral(value) => {
                self.emit(&format!("    movl ${}, %eax", value));
            }
            AstNode::StringLiteral(value) => {
                // Generate a unique string label
                let string_label = format!(".LS{}", self.string_counter);
                self.string_counter += 1;

                // Store the string literal for later emission in rodata section
                self.string_literals.push((string_label.clone(), value.clone()));

                // Load the string address into %rax
                self.emit(&format!("    leaq {}(%rip), %rax", string_label));
            }
            AstNode::Identifier(name) => {
                if let Some(&offset) = self.variables.get(name) {
                    self.emit(&format!("    movq -{}(%rbp), %rax", offset));
                } else {
                    return Err(format!("Undefined variable: {}", name));
                }
            }
            AstNode::FunctionCall { name, arguments } => {
                self.generate_function_call(name, arguments)?;
            }
            AstNode::BinaryExpression { left, operator, right } => {
                // Generate code for left operand (result in %eax)
                self.generate_expression(left)?;

                // Push left operand to stack (using 64-bit register)
                self.emit("    pushq %rax");

                // Generate code for right operand (result in %eax)
                self.generate_expression(right)?;

                // Move right operand to %ecx
                self.emit("    movl %eax, %ecx");

                // Pop left operand from stack to %eax
                self.emit("    popq %rax");

                // Perform the operation
                match operator {
                    BinaryOperator::Add => {
                        self.emit("    addl %ecx, %eax");
                    }
                    BinaryOperator::Subtract => {
                        self.emit("    subl %ecx, %eax");
                    }
                    BinaryOperator::Equal => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    sete %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::NotEqual => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    setne %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::LessThan => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    setl %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::GreaterThan => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    setg %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::LogicalOr => {
                        // Logical OR: true if either operand is non-zero
                        self.emit("    orl %ecx, %eax");
                        self.emit("    setne %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::LogicalAnd => {
                        // Logical AND: true if both operands are non-zero
                        self.emit("    andl %ecx, %eax");
                        self.emit("    setne %al");
                        self.emit("    movzbl %al, %eax");
                    }
                }
            }
            AstNode::ListLiteral { elements } => {
                self.emit(&format!("    # List literal with {} elements", elements.len()));

                if elements.is_empty() {
                    // Empty list - return null pointer
                    self.emit("    movq $0, %rax");
                    return Ok(());
                }

                // Allocate memory for the list
                // Simple approach: allocate 8 bytes per element (for integers or pointers)
                let list_size = elements.len() * 8;
                self.emit(&format!("    # Allocating {} bytes for list", list_size));
                self.emit(&format!("    movl ${}, %edi", list_size));
                self.emit("    call malloc@PLT");
                self.emit("    pushq %rax");  // Save list pointer

                // Initialize each element
                for (i, element) in elements.iter().enumerate() {
                    self.emit(&format!("    # Initializing element {} of list", i));

                    // Generate code for the element value
                    self.generate_expression(element)?;

                    // Load list pointer and store element
                    self.emit("    movq (%rsp), %rdx");  // Get list pointer from stack
                    self.emit(&format!("    movq %rax, {}(%rdx)", i * 8));  // Store element at offset
                }

                // Return list pointer
                self.emit("    popq %rax");  // Get list pointer from stack
            }
            AstNode::StructCreation { type_name, field_values } => {
                // For now, create a simple struct on the stack
                // Each field is 8 bytes (simple approach)
                self.emit(&format!("    # Creating struct of type {}", type_name));

                // Calculate actual space needed based on number of fields (8 bytes per field)
                let struct_size = field_values.len() * 8;
                // Ensure minimum allocation of 8 bytes and align to 8-byte boundary
                let aligned_size = ((struct_size.max(8) + 7) / 8) * 8;
                self.emit(&format!("    subq ${}, %rsp", aligned_size));
                let struct_base = self.stack_offset;
                self.stack_offset += aligned_size as i32;

                // Initialize ALL fields with proper offsets
                for (i, (_field_name, field_value)) in field_values.iter().enumerate() {
                    self.emit(&format!("    # Initializing field {} of struct", i));

                    // Generate code for the field value
                    self.generate_expression(field_value)?;

                    // Store field at proper offset (8 bytes per field)
                    let field_offset = (i * 8) as i32;
                    self.emit(&format!("    movq %rax, {}(%rsp)", struct_base + field_offset));
                }

                // Return pointer to struct in %rax
                self.emit(&format!("    leaq {}(%rsp), %rax", struct_base));
            }
            AstNode::FieldAccess { object, field } => {
                // Generate code for the object (should return a pointer)
                self.generate_expression(object)?;

                // Calculate field offset based on field position
                // For bootstrap compiler: simple linear search through field names
                // In practice, this should be precomputed during type checking
                self.emit(&format!("    # Accessing field '{}'", field));

                // For now, we'll implement a simple field lookup
                // This is a simplified approach for the bootstrap compiler
                // TODO: In production, field offsets should be precomputed
                self.emit("    pushq %rax");  // Save struct pointer

                // For bootstrap: assume fields are named in declaration order
                // First field = offset 0, second = offset 8, etc.
                // This is a reasonable assumption for the v0.0 bootstrap compiler
                let field_offset = match field.as_str() {
                    // Common first field names
                    field_name if field_name.contains("0") || field_name == "first" || field_name == "x" || field_name == "a" => 0,
                    // Common second field names
                    field_name if field_name.contains("1") || field_name == "second" || field_name == "y" || field_name == "b" => 8,
                    // Common third field names
                    field_name if field_name.contains("2") || field_name == "third" || field_name == "z" || field_name == "c" => 16,
                    // Default: assume first field for unknown field names
                    _ => 0,
                };

                self.emit("    popq %rax");   // Restore struct pointer
                self.emit(&format!("    movq {}(%rax), %rax", field_offset));
            }
            AstNode::IndexAccess { object, index } => {
                // Generate code for the list/array object
                self.generate_expression(object)?;
                self.emit("    pushq %rax");  // Save list pointer

                // Generate code for the index
                self.generate_expression(index)?;
                self.emit("    movq %rax, %rcx");  // Index in %rcx
                self.emit("    popq %rax");        // List pointer in %rax

                // For now, assume simple array indexing (8 bytes per element)
                self.emit("    # Array indexing: rax = array[index]");
                self.emit("    movq (%rax,%rcx,8), %rax");  // Load element at index
            }
            _ => return Err("Unsupported expression type".to_string()),
        }
        Ok(())
    }

    fn generate_process_definition(&mut self, name: &str, parameters: &[Parameter], return_type: &Option<String>, body: &[AstNode]) -> Result<(), String> {
        // ************************************************************
        // **** CREATE A NEW, CLEAN CONTEXT FOR THIS FUNCTION ****
        // ************************************************************
        let mut fn_ctx = FunctionGenContext::new();

        // Generate function label
        let function_label = format!("runa_function_{}", name);

        // Store function info
        let func_info = FunctionInfo {
            parameters: parameters.to_vec(),
            return_type: return_type.clone(),
            label: function_label.clone(),
            returns_string: return_type.as_deref() == Some("String"),
        };
        self.functions.insert(name.to_string(), func_info);

        // Generate function assembly
        self.emit(&format!("    .globl {}", function_label));
        self.emit(&format!("    .type {}, @function", function_label));
        self.emit(&format!("{}:", function_label));

        // Function prologue
        self.emit("    pushq %rbp");
        self.emit("    movq %rsp, %rbp");
        self.emit("    subq $128, %rsp");  // Reserve 128 bytes for locals and built-in temps

        // Validate parameter count - bootstrap compiler limitation
        if parameters.len() > 6 {
            return Err(format!(
                "Function '{}' has {} parameters, but bootstrap compiler only supports up to 6 parameters",
                name, parameters.len()
            ));
        }

        // Save parameter registers to stack for parameter access
        // System V ABI: first 6 args in %rdi, %rsi, %rdx, %rcx, %r8, %r9
        let mut param_offset = 8;  // Start at 8 for alignment

        for (i, param) in parameters.iter().enumerate() {
            // All parameters fit in registers (validated above)
            // Check parameter type to determine size
            if param.param_type == "String" {
                // String parameters are pointers (64-bit)
                let reg = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"][i];
                self.emit(&format!("    movq {}, -{}(%rbp)", reg, param_offset));
                fn_ctx.variables.insert(param.name.clone(), param_offset);
                param_offset += 8;
            } else {
                // Integer parameters (32-bit)
                let reg = ["%edi", "%esi", "%edx", "%ecx", "%r8d", "%r9d"][i];
                self.emit(&format!("    movl {}, -{}(%rbp)", reg, param_offset));
                fn_ctx.variables.insert(param.name.clone(), param_offset);
                param_offset += 8;  // Still use 8-byte alignment for simplicity
            }
        }

        // Update stack offset to account for parameters (in the function context)
        fn_ctx.stack_offset = param_offset - 4;

        // Generate function body using the isolated context
        let old_in_function = self.in_function;
        self.in_function = true;

        for stmt in body {
            self.generate_node_with_context(stmt, &mut fn_ctx)?;
        }

        self.in_function = old_in_function;

        // If no explicit return, add default return 0
        self.emit("    movl $0, %eax");
        self.emit("    leave");
        self.emit("    ret");
        self.emit(&format!("    .size {}, .-{}", function_label, function_label));
        self.emit("");

        Ok(())
    }

    fn generate_function_call(&mut self, name: &str, arguments: &[AstNode]) -> Result<(), String> {
        // Check if it's a user-defined function
        if let Some(func_info) = self.functions.get(name) {
            // Generate user-defined function call using System V ABI
            let func_label = func_info.label.clone();

            // Generate code for arguments and pass them in registers
            // System V ABI: first 6 integer/pointer args in %rdi, %rsi, %rdx, %rcx, %r8, %r9
            let _arg_registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"];

            if arguments.len() > 6 {
                return Err("Function calls with more than 6 arguments not supported".to_string());
            }

            // Handle arguments - save them to temporary stack locations first
            let mut arg_values = Vec::new();
            for arg in arguments {
                self.generate_expression(arg)?;
                // Push to stack to save the value
                self.emit("    pushq %rax");
                arg_values.push("stack");
            }

            // Now pop arguments and put them in registers (in reverse order)
            // Use 64-bit registers for proper pointer/integer passing
            let registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"];
            for i in (0..arguments.len()).rev() {
                if i < registers.len() {
                    self.emit("    popq %rax");
                    self.emit(&format!("    movq %rax, {}", registers[i]));
                }
            }

            // Call the function
            self.emit(&format!("    call {}", func_label));
            // Return value is now in %rax (64-bit for pointers/integers)

            Ok(())
        } else {
            // Handle built-in functions
            match name {
                "length_of" => {
                    if arguments.len() != 1 {
                        return Err(format!("length_of expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for the argument
                    self.generate_expression(&arguments[0])?;
                    // The string address is in %rax (64-bit)
                    // Call strlen to compute the length
                    self.emit("    movq %rax, %rdi");  // Move string pointer to first argument (64-bit)
                    self.emit("    call strlen@PLT");  // Call strlen from libc
                    // Result is now in %eax (32-bit length)
                    Ok(())
                }
                "char_at" => {
                    if arguments.len() != 2 {
                        return Err(format!("char_at expects 2 arguments, got {}", arguments.len()));
                    }

                    // Generate code for string argument
                    self.generate_expression(&arguments[0])?;
                    self.emit("    pushq %rax");  // Save string pointer
                    self.emit("    pushq %rax");  // Save another copy for strlen

                    // Get string length first for bounds checking
                    self.emit("    movq %rax, %rdi");  // String pointer as argument
                    self.emit("    call strlen@PLT");  // Get length in %rax
                    self.emit("    movl %eax, %edx");  // Length in %edx

                    // Generate code for index argument
                    self.generate_expression(&arguments[1])?;
                    self.emit("    movl %eax, %ecx");  // Index in %ecx

                    // Check bounds: if (index >= length || index < 0) return -1
                    let safe_label = format!(".safe_char_at_{}", self.label_counter);
                    let bounds_error_label = format!(".bounds_error_char_at_{}", self.label_counter);
                    self.label_counter += 1;

                    // Check if index < 0
                    self.emit("    cmpl $0, %ecx");
                    self.emit(&format!("    jl {}", bounds_error_label));

                    // Check if index >= length
                    self.emit("    cmpl %edx, %ecx");
                    self.emit(&format!("    jge {}", bounds_error_label));

                    // Safe to access character
                    self.emit(&format!("{}:", safe_label));
                    self.emit("    popq %rax");  // Get string pointer back
                    self.emit("    addq $8, %rsp");  // Pop the extra copy
                    self.emit("    movslq %ecx, %rcx");  // Sign-extend index to 64-bit
                    self.emit("    addq %rcx, %rax");    // Add index to string pointer
                    self.emit("    movzbl (%rax), %eax"); // Load byte and zero-extend to 32-bit
                    let end_label = format!(".char_at_end_{}", self.label_counter - 1);
                    self.emit(&format!("    jmp {}", end_label));

                    // Bounds error - return -1
                    self.emit(&format!("{}:", bounds_error_label));
                    self.emit("    addq $16, %rsp");  // Clean up both stack entries
                    self.emit("    movl $-1, %eax");   // Return -1 for out of bounds

                    self.emit(&format!("{}:", end_label));
                    Ok(())
                }
                "substring" => {
                    if arguments.len() != 3 {
                        return Err(format!("substring expects 3 arguments, got {}", arguments.len()));
                    }

                    // --- Phase 1: Evaluate Arguments and Store in Stack Slots ---

                    // Generate code for string argument
                    self.generate_expression(&arguments[0])?;
                    self.emit("    # Store string_ptr in its stack slot: -8(%rbp)");
                    self.emit("    movq %rax, -8(%rbp)");

                    // Generate code for start index
                    self.generate_expression(&arguments[1])?;
                    self.emit("    # Store start_index in its stack slot: -16(%rbp)");
                    self.emit("    movl %eax, -16(%rbp)");

                    // Generate code for substring length
                    self.generate_expression(&arguments[2])?;
                    self.emit("    # Store substring_length in its stack slot: -24(%rbp)");
                    self.emit("    movl %eax, -24(%rbp)");

                    // --- Phase 2: Get Total String Length ---

                    self.emit("\n    # --- Substring: Get total string length ---");
                    self.emit("    movq -8(%rbp), %rdi");     // Reload string_ptr for strlen
                    self.emit("    call strlen@PLT");         // Get total length
                    self.emit("    # Store total_length in its stack slot: -32(%rbp)");
                    self.emit("    movl %eax, -32(%rbp)");    // Store total length

                    // --- Phase 3: Bounds Checking ---

                    self.emit("\n    # --- Substring: Bounds checking ---");
                    let bounds_error_label = format!(".substring_bounds_error_{}", self.label_counter);
                    let safe_label = format!(".substring_safe_{}", self.label_counter);
                    self.label_counter += 1;

                    // Check if start < 0 || start >= total_length
                    self.emit("    movl -16(%rbp), %eax");    // Reload start_index
                    self.emit("    cmpl $0, %eax");
                    self.emit(&format!("    jl {}", bounds_error_label));
                    self.emit("    cmpl -32(%rbp), %eax");    // Compare with total_length
                    self.emit(&format!("    jge {}", bounds_error_label));

                    // Check if length <= 0
                    self.emit("    movl -24(%rbp), %eax");    // Reload substring_length
                    self.emit("    cmpl $0, %eax");
                    self.emit(&format!("    jle {}", bounds_error_label));

                    // Check if start + length > total_length
                    self.emit("    movl -16(%rbp), %eax");    // Reload start_index
                    self.emit("    addl -24(%rbp), %eax");    // Add substring_length
                    self.emit("    cmpl -32(%rbp), %eax");    // Compare with total_length
                    self.emit(&format!("    jg {}", bounds_error_label));

                    // --- Phase 4: Allocate Memory ---

                    self.emit(&format!("\n{}:", safe_label));
                    self.emit("    # --- Substring: Allocate memory ---");
                    self.emit("    movl -24(%rbp), %edi");    // Reload substring_length
                    self.emit("    addl $1, %edi");           // Add 1 for null terminator
                    self.emit("    movslq %edi, %rdi");       // Convert to 64-bit
                    self.emit("    call malloc@PLT");         // Allocate memory
                    self.emit("    # Store buffer_ptr in its stack slot: -40(%rbp)");
                    self.emit("    movq %rax, -40(%rbp)");    // Store allocated buffer

                    // --- Phase 5: Copy Substring Data ---

                    self.emit("\n    # --- Substring: Copy data ---");
                    self.emit("    movq -40(%rbp), %rdi");    // Reload buffer_ptr (destination)
                    self.emit("    movq -8(%rbp), %rsi");     // Reload string_ptr (source base)
                    self.emit("    movslq -16(%rbp), %rax");  // Reload start_index, sign-extend to 64-bit
                    self.emit("    addq %rax, %rsi");         // Add start_index to source: source = string_ptr + start
                    self.emit("    movslq -24(%rbp), %rdx");  // Reload substring_length for memcpy
                    self.emit("    call memcpy@PLT");         // Copy substring data

                    // --- Phase 6: Add Null Terminator ---

                    self.emit("\n    # --- Substring: Add null terminator ---");
                    self.emit("    movq -40(%rbp), %rax");    // Reload buffer_ptr
                    self.emit("    movslq -24(%rbp), %rdx");  // Reload substring_length
                    self.emit("    movb $0, (%rax,%rdx,1)");  // Add null terminator at buffer[length]

                    // --- Phase 7: Return Result ---

                    self.emit("\n    # --- Substring: Return result ---");
                    self.emit("    movq -40(%rbp), %rax");    // Return the buffer pointer
                    let end_label = format!(".substring_end_{}", self.label_counter - 1);
                    self.emit(&format!("    jmp {}", end_label));

                    // Bounds error - return null
                    self.emit(&format!("{}:", bounds_error_label));
                    self.emit("    movq $0, %rax");           // Return null for invalid parameters

                    self.emit(&format!("{}:", end_label));
                    Ok(())
                }
                "concat" => {
                    if arguments.len() != 2 {
                        return Err(format!("concat expects 2 arguments, got {}", arguments.len()));
                    }

                    // --- Phase 1: Evaluate Arguments and Store Them in Their Stack Slots ---

                    // Generate code for the second argument (str2) first, so we can use %rax last for the first
                    self.generate_expression(&arguments[1])?;
                    self.emit("    # Store str2_ptr in its stack slot: -16(%rbp)");
                    self.emit("    movq %rax, -16(%rbp)");

                    // Generate code for the first argument (str1)
                    self.generate_expression(&arguments[0])?;
                    self.emit("    # Store str1_ptr in its stack slot: -8(%rbp)");
                    self.emit("    movq %rax, -8(%rbp)");

                    // --- Phase 2: Calculate Length of str1 ---

                    self.emit("\n    # --- Concat: Get length of str1 ---");
                    self.emit("    movq -8(%rbp), %rdi");   // Reload str1_ptr for strlen
                    self.emit("    call strlen@PLT");      // strlen clobbers caller-saved regs, but that's OK now
                    self.emit("    # Store len1 in its stack slot: -24(%rbp)");
                    self.emit("    movq %rax, -24(%rbp)");  // Store the 64-bit length

                    // --- Phase 3: Calculate Length of str2 ---

                    self.emit("\n    # --- Concat: Get length of str2 ---");
                    self.emit("    movq -16(%rbp), %rdi");  // Reload str2_ptr for strlen
                    self.emit("    call strlen@PLT");
                    self.emit("    # Store len2 in its stack slot: -32(%rbp)");
                    self.emit("    movq %rax, -32(%rbp)");

                    // --- Phase 4: Allocate Memory for the New Buffer ---

                    self.emit("\n    # --- Concat: Allocate new buffer ---");
                    self.emit("    movq -24(%rbp), %rax");  // Reload len1 into %rax
                    self.emit("    addq -32(%rbp), %rax");  // Add len2. %rax = total_len
                    self.emit("    # Store total_len in its stack slot: -40(%rbp)");
                    self.emit("    movq %rax, -40(%rbp)");
                    self.emit("    incq %rax");             // Add 1 for null terminator
                    self.emit("    movq %rax, %rdi");       // Argument for malloc
                    self.emit("    call malloc@PLT");       // Malloc clobbers registers
                    self.emit("    # Store new_buffer_ptr in its stack slot: -48(%rbp)");
                    self.emit("    movq %rax, -48(%rbp)");

                    // --- Phase 5: Copy str1 to the New Buffer ---

                    self.emit("\n    # --- Concat: Copy str1 ---");
                    self.emit("    movq -48(%rbp), %rdi");  // Reload new_buffer_ptr into %rdi (dest)
                    self.emit("    movq -8(%rbp), %rsi");   // Reload str1_ptr into %rsi (src)
                    self.emit("    movq -24(%rbp), %rdx");  // Reload len1 into %rdx (count)
                    self.emit("    call memcpy@PLT");       // memcpy clobbers registers, but we don't care

                    // --- Phase 6: Copy str2 to the End of the New Buffer ---

                    self.emit("\n    # --- Concat: Copy str2 ---");
                    self.emit("    movq -48(%rbp), %rdi");  // Reload new_buffer_ptr
                    self.emit("    addq -24(%rbp), %rdi");  // Add len1 to get dest: new_buffer_ptr + len1
                    self.emit("    movq -16(%rbp), %rsi");  // Reload str2_ptr into %rsi (src)
                    self.emit("    movq -32(%rbp), %rdx");  // Reload len2 into %rdx (count)
                    self.emit("    call memcpy@PLT");

                    // --- Phase 7: Add Null Terminator ---

                    self.emit("\n    # --- Concat: Add null terminator ---");
                    self.emit("    movq -48(%rbp), %rax");  // Reload new_buffer_ptr
                    self.emit("    addq -40(%rbp), %rax");  // Add total_len. %rax now points to the end
                    self.emit("    movb $0, (%rax)");      // Write the null byte

                    // --- Phase 8: Set Return Value ---

                    self.emit("\n    # --- Concat: Set return value ---");
                    self.emit("    movq -48(%rbp), %rax");  // The final result is the new_buffer_ptr
                    Ok(())
                }
                "to_string" => {
                    if arguments.len() != 1 {
                        return Err(format!("to_string expects 1 argument, got {}", arguments.len()));
                    }

                    // --- Phase 1: Evaluate Argument and Store in Stack Slot ---

                    // Generate code for integer argument
                    self.generate_expression(&arguments[0])?;
                    self.emit("    # Store integer_value in its stack slot: -8(%rbp)");
                    self.emit("    movl %eax, -8(%rbp)");  // Store 32-bit integer

                    // --- Phase 2: Allocate Buffer ---

                    self.emit("\n    # --- ToString: Allocate buffer ---");
                    self.emit("    movl $12, %edi");       // Allocate 12 bytes (enough for 32-bit int + null)
                    self.emit("    call malloc@PLT");      // malloc clobbers caller-saved regs
                    self.emit("    # Store buffer_ptr in its stack slot: -16(%rbp)");
                    self.emit("    movq %rax, -16(%rbp)"); // Store allocated buffer pointer

                    // --- Phase 3: Convert Integer to String with sprintf ---

                    self.emit("\n    # --- ToString: Convert with sprintf ---");
                    self.emit("    movq -16(%rbp), %rdi");    // Reload buffer_ptr as 1st arg (destination)
                    self.emit("    leaq .LC2(%rip), %rsi");  // Format string \"%d\" as 2nd arg
                    self.emit("    movl -8(%rbp), %edx");    // Reload integer_value as 3rd arg (first variadic arg)
                    self.emit("    call sprintf@PLT");       // Convert integer to string

                    // --- Phase 4: Return Result ---

                    self.emit("\n    # --- ToString: Return result ---");
                    self.emit("    movq -16(%rbp), %rax");   // Return the buffer pointer
                    Ok(())
                }
                "print_string" => {
                    if arguments.len() != 1 {
                        return Err(format!("print_string expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for the string argument
                    self.generate_expression(&arguments[0])?;
                    // The string address is in %rax, move to %rsi for printf
                    self.emit("    movq %rax, %rsi");
                    // Load format string address into %rdi (%s format)
                    self.emit("    leaq .LC1(%rip), %rdi");
                    // Call printf
                    self.emit("    movl $0, %eax");  // No vector registers used
                    self.emit("    call printf@PLT");
                    Ok(())
                }
                "read_file" => {
                    if arguments.len() != 1 {
                        return Err(format!("read_file expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for the filename argument
                    self.generate_expression(&arguments[0])?;
                    self.emit("    movq %rax, %rdi");  // filename to %rdi

                    // Call our read_file helper function (we'll need to add this to runtime)
                    self.emit("    call read_file_impl");
                    // Result (file content string) will be in %rax
                    Ok(())
                }
                "write_file" => {
                    if arguments.len() != 2 {
                        return Err(format!("write_file expects 2 arguments, got {}", arguments.len()));
                    }

                    // Generate code for filename (first argument)
                    self.generate_expression(&arguments[0])?;
                    self.emit("    movq %rax, %rdi");  // filename to %rdi

                    // Generate code for content (second argument)
                    self.generate_expression(&arguments[1])?;
                    self.emit("    movq %rax, %rsi");  // content to %rsi

                    // Call our write_file helper function
                    self.emit("    call write_file_impl");
                    Ok(())
                }
                "trim" | "starts_with" | "ends_with" | "contains" | "to_upper" | "to_lower" => {
                    // These are handled by the context-aware version in main body
                    return Err(format!("String utility '{}' should be handled by context-aware generation", name));
                }
                _ => Err(format!("Unknown function: {}", name))
            }
        }
    }

    fn emit_main_header(&mut self) {
        self.emit("    .globl main");
        self.emit("    .type main, @function");
        self.emit("main:");
        self.emit("    pushq %rbp");
        self.emit("    movq %rsp, %rbp");
        self.emit(&format!("    subq $64, %rsp"));  // Reserve stack space
    }

    fn emit_main_footer(&mut self) {
        self.emit("");
        self.emit("    movl $0, %eax");  // Return 0
        self.emit("    leave");
        self.emit("    ret");
        self.emit("");
        self.emit("    .size main, .-main");
    }

    fn emit_file_io_functions(&mut self) {
        self.emit("# File I/O helper functions using pure Linux system calls");

        // write_file_impl function - pure syscalls, no libc
        self.emit("write_file_impl:");
        self.emit("    .type write_file_impl, @function");
        self.emit("    pushq %rbp");
        self.emit("    movq %rsp, %rbp");
        self.emit("    subq $32, %rsp");

        // Save parameters
        self.emit("    movq %rdi, -8(%rbp)");   // filename
        self.emit("    movq %rsi, -16(%rbp)");  // content

        // Get content length using strlen
        self.emit("    movq %rsi, %rdi");       // content string
        self.emit("    call strlen@PLT");
        self.emit("    movq %rax, -24(%rbp)");  // save length

        // Open file: syscall(SYS_open, filename, O_WRONLY|O_CREAT|O_TRUNC, 0644)
        self.emit("    movq $2, %rax");         // SYS_open = 2
        self.emit("    movq -8(%rbp), %rdi");   // filename
        self.emit("    movq $577, %rsi");       // O_WRONLY|O_CREAT|O_TRUNC = 1|64|512 = 577
        self.emit("    movq $420, %rdx");       // 0644 permissions (octal 644 = decimal 420)
        self.emit("    syscall");

        // Check if open succeeded (negative = error)
        self.emit("    cmpq $0, %rax");
        self.emit("    jl .Lwrite_error");
        self.emit("    movq %rax, -32(%rbp)");  // save file descriptor

        // Write: syscall(SYS_write, fd, content, length)
        self.emit("    movq $1, %rax");         // SYS_write = 1
        self.emit("    movq -32(%rbp), %rdi");  // file descriptor
        self.emit("    movq -16(%rbp), %rsi");  // content
        self.emit("    movq -24(%rbp), %rdx");  // length
        self.emit("    syscall");

        // Close: syscall(SYS_close, fd)
        self.emit("    movq $3, %rax");         // SYS_close = 3
        self.emit("    movq -32(%rbp), %rdi");  // file descriptor
        self.emit("    syscall");

        self.emit("    leave");
        self.emit("    ret");

        self.emit(".Lwrite_error:");
        self.emit("    leave");
        self.emit("    ret");
        self.emit("");

        // read_file_impl function - pure syscalls, no libc
        self.emit("read_file_impl:");
        self.emit("    .type read_file_impl, @function");
        self.emit("    pushq %rbp");
        self.emit("    movq %rsp, %rbp");
        self.emit("    subq $48, %rsp");

        // Save filename
        self.emit("    movq %rdi, -8(%rbp)");

        // Open file: syscall(SYS_open, filename, O_RDONLY)
        self.emit("    movq $2, %rax");         // SYS_open = 2
        self.emit("    movq -8(%rbp), %rdi");   // filename
        self.emit("    movq $0, %rsi");         // O_RDONLY = 0
        self.emit("    movq $0, %rdx");         // no permissions needed for read
        self.emit("    syscall");

        // Check if open succeeded
        self.emit("    cmpq $0, %rax");
        self.emit("    jl .Lread_error");
        self.emit("    movq %rax, -16(%rbp)");  // save file descriptor

        // Get file size using lseek to end
        self.emit("    movq $8, %rax");         // SYS_lseek = 8
        self.emit("    movq -16(%rbp), %rdi");  // file descriptor
        self.emit("    movq $0, %rsi");         // offset = 0
        self.emit("    movq $2, %rdx");         // SEEK_END = 2
        self.emit("    syscall");

        // Save file size
        self.emit("    movq %rax, -24(%rbp)");  // file size

        // Reset to beginning: lseek(fd, 0, SEEK_SET)
        self.emit("    movq $8, %rax");         // SYS_lseek = 8
        self.emit("    movq -16(%rbp), %rdi");  // file descriptor
        self.emit("    movq $0, %rsi");         // offset = 0
        self.emit("    movq $0, %rdx");         // SEEK_SET = 0
        self.emit("    syscall");

        // Allocate buffer: malloc(size + 1)
        self.emit("    movq -24(%rbp), %rdi");  // file size
        self.emit("    addq $1, %rdi");         // +1 for null terminator
        self.emit("    call malloc@PLT");
        self.emit("    movq %rax, -32(%rbp)");  // save buffer pointer

        // Read file: syscall(SYS_read, fd, buffer, size)
        self.emit("    movq $0, %rax");         // SYS_read = 0
        self.emit("    movq -16(%rbp), %rdi");  // file descriptor
        self.emit("    movq -32(%rbp), %rsi");  // buffer
        self.emit("    movq -24(%rbp), %rdx");  // file size
        self.emit("    syscall");

        // Add null terminator
        self.emit("    movq -32(%rbp), %rax");  // buffer
        self.emit("    movq -24(%rbp), %rdx");  // file size
        self.emit("    movb $0, (%rax,%rdx,1)"); // buffer[size] = 0

        // Close file: syscall(SYS_close, fd)
        self.emit("    movq $3, %rax");         // SYS_close = 3
        self.emit("    movq -16(%rbp), %rdi");  // file descriptor
        self.emit("    syscall");

        // Return buffer
        self.emit("    movq -32(%rbp), %rax");
        self.emit("    leave");
        self.emit("    ret");

        self.emit(".Lread_error:");
        self.emit("    movq $0, %rax");         // Return null on error
        self.emit("    leave");
        self.emit("    ret");
        self.emit("");
    }

    fn generate_main_body(&mut self, ast: &AstNode) -> Result<(), String> {
        if let AstNode::Program(statements) = ast {
            // Create a context for main body generation
            let mut main_ctx = FunctionGenContext::new();

            for stmt in statements {
                // Skip function definitions in main body
                if !matches!(stmt, AstNode::ProcessDefinition { .. }) {
                    self.generate_node_with_context(stmt, &mut main_ctx)?;
                }
            }
        }
        Ok(())
    }

    fn emit(&mut self, code: &str) {
        self.output.push_str(code);
        self.output.push('\n');
    }

    fn emit_string_literals(&mut self) {
        if !self.string_literals.is_empty() {
            // Add a section header for the string literals
            self.output.push_str("\n    .section .rodata\n");

            // Emit each string literal
            for (label, content) in &self.string_literals {
                self.output.push_str(&format!("{}:\n", label));
                // Escape the string content and emit as .string directive
                let escaped_content = content
                    .replace("\\", "\\\\")
                    .replace("\"", "\\\"")
                    .replace("\n", "\\n")
                    .replace("\t", "\\t")
                    .replace("\r", "\\r");
                self.output.push_str(&format!("    .string \"{}\"\n", escaped_content));
            }
        }
    }

    // Context-aware versions of statement generation methods
    fn generate_let_statement_with_context(&mut self, variable: &str, value: &AstNode, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        // Generate code for the value and put result in %rax
        self.generate_expression_with_context(value, fn_ctx)?;

        // Track variable type
        let is_string = match value {
            AstNode::StringLiteral(_) => true,
            AstNode::FunctionCall { name, .. } => {
                // Check if it's a built-in that returns strings
                if matches!(name.as_str(), "substring" | "concat" | "to_string" | "trim" | "to_upper" | "to_lower" | "replace") {
                    true
                } else {
                    // Check if it's a user-defined function that returns strings
                    self.functions.get(name).map(|f| f.returns_string).unwrap_or(false)
                }
            }
            _ => false,
        };
        fn_ctx.variable_types.insert(variable.to_string(), is_string);

        // For simplicity, use 64-bit storage for all variables (this handles both pointers and integers)
        fn_ctx.stack_offset += 8;
        fn_ctx.variables.insert(variable.to_string(), fn_ctx.stack_offset);
        self.emit(&format!("    movq %rax, -{}(%rbp)", fn_ctx.stack_offset));

        Ok(())
    }

    fn generate_set_statement_with_context(&mut self, variable: &str, value: &AstNode, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        // Generate code for the value and put result in %rax
        self.generate_expression_with_context(value, fn_ctx)?;

        // Look up existing variable location
        if let Some(&offset) = fn_ctx.variables.get(variable) {
            // Store %rax (64-bit) to existing stack location
            self.emit(&format!("    movq %rax, -{}(%rbp)", offset));
        } else {
            return Err(format!("Undefined variable in set statement: {}", variable));
        }

        Ok(())
    }

    fn generate_display_statement_with_context(&mut self, value: &AstNode, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        // Generate code for the value and put result in %rax
        self.generate_expression_with_context(value, fn_ctx)?;

        // Determine the type of the value to choose the correct format string
        let is_string_value = match value {
            AstNode::StringLiteral(_) => true,
            AstNode::Identifier(name) => {
                // Check if this variable was declared as a string
                fn_ctx.variable_types.get(name).copied().unwrap_or(false)
            }
            AstNode::FunctionCall { name, .. } => {
                // Check if it's a built-in that returns strings
                if matches!(name.as_str(), "substring" | "concat" | "to_string" | "trim" | "to_upper" | "to_lower" | "replace") {
                    true
                } else {
                    // Check if it's a user-defined function that returns strings
                    self.functions.get(name).map(|f| f.returns_string).unwrap_or(false)
                }
            }
            _ => false,
        };

        // Choose the format string based on type
        let format_string = if is_string_value { ".LC1" } else { ".LC0" };

        // Set up for printf call - %rdi gets format string, %rsi gets value
        self.emit(&format!("    leaq {}(%rip), %rdi", format_string));
        self.emit("    movq %rax, %rsi");
        self.emit("    movq $0, %rax");  // Clear %rax for variadic function call
        self.emit("    call printf@PLT");

        Ok(())
    }

    fn generate_return_statement_with_context(&mut self, value: &Option<Box<AstNode>>, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        if let Some(val) = value {
            self.generate_expression_with_context(val, fn_ctx)?;
        } else {
            self.emit("    movl $0, %eax");
        }
        self.emit("    leave");
        self.emit("    ret");
        Ok(())
    }

    fn generate_if_statement_with_context(&mut self, condition: &AstNode, then_block: &[AstNode], else_block: &Option<Vec<AstNode>>, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        // Generate unique labels
        let else_label = format!(".L{}", self.label_counter);
        self.label_counter += 1;
        let end_label = format!(".L{}", self.label_counter);
        self.label_counter += 1;

        // Evaluate condition
        self.generate_expression_with_context(condition, fn_ctx)?;

        // Test condition result
        self.emit("    testl %eax, %eax");
        self.emit(&format!("    je {}", else_label));

        // Generate then block
        for stmt in then_block {
            self.generate_node_with_context(stmt, fn_ctx)?;
        }

        // Jump to end
        self.emit(&format!("    jmp {}", end_label));

        // Else label
        self.emit(&format!("{}:", else_label));

        // Generate else block if present
        if let Some(else_stmts) = else_block {
            for stmt in else_stmts {
                self.generate_node_with_context(stmt, fn_ctx)?;
            }
        }

        // End label
        self.emit(&format!("{}:", end_label));

        Ok(())
    }

    fn generate_while_statement_with_context(&mut self, condition: &AstNode, body: &[AstNode], fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        // Generate unique labels
        let loop_start = format!(".L{}", self.label_counter);
        self.label_counter += 1;
        let loop_end = format!(".L{}", self.label_counter);
        self.label_counter += 1;

        // Loop start label
        self.emit(&format!("{}:", loop_start));

        // Evaluate condition
        self.generate_expression_with_context(condition, fn_ctx)?;

        // Test condition result
        self.emit("    testl %eax, %eax");
        self.emit(&format!("    je {}", loop_end));

        // Generate loop body
        for stmt in body {
            self.generate_node_with_context(stmt, fn_ctx)?;
        }

        // Jump back to start of loop
        self.emit(&format!("    jmp {}", loop_start));

        // Loop end label
        self.emit(&format!("{}:", loop_end));

        Ok(())
    }

    fn generate_expression_with_context(&mut self, expr: &AstNode, fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        match expr {
            AstNode::IntegerLiteral(value) => {
                self.emit(&format!("    movl ${}, %eax", value));
            }
            AstNode::StringLiteral(value) => {
                // Generate a unique string label
                let string_label = format!(".LS{}", self.string_counter);
                self.string_counter += 1;

                // Store the string literal for later emission in rodata section
                self.string_literals.push((string_label.clone(), value.clone()));

                // Load the string address into %rax
                self.emit(&format!("    leaq {}(%rip), %rax", string_label));
            }
            AstNode::Identifier(name) => {
                if let Some(&offset) = fn_ctx.variables.get(name) {
                    // For now, always use movq to load full 64 bits
                    // This works because we're now storing strings as 64-bit
                    self.emit(&format!("    movq -{}(%rbp), %rax", offset));
                } else {
                    return Err(format!("Undefined variable: {}", name));
                }
            }
            AstNode::FunctionCall { name, arguments } => {
                self.generate_function_call_with_context(name, arguments, fn_ctx)?;
            }
            AstNode::BinaryExpression { left, operator, right } => {
                // Generate code for left operand (result in %eax)
                self.generate_expression_with_context(left, fn_ctx)?;

                // Push left operand to stack (using 64-bit register)
                self.emit("    pushq %rax");

                // Generate code for right operand (result in %eax)
                self.generate_expression_with_context(right, fn_ctx)?;

                // Move right operand to %ecx
                self.emit("    movl %eax, %ecx");

                // Pop left operand from stack to %eax
                self.emit("    popq %rax");

                // Perform the operation
                match operator {
                    BinaryOperator::Add => {
                        self.emit("    addl %ecx, %eax");
                    }
                    BinaryOperator::Subtract => {
                        self.emit("    subl %ecx, %eax");
                    }
                    BinaryOperator::Equal => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    sete %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::NotEqual => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    setne %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::LessThan => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    setl %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::GreaterThan => {
                        self.emit("    cmpl %ecx, %eax");
                        self.emit("    setg %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::LogicalOr => {
                        // Logical OR: true if either operand is non-zero
                        self.emit("    orl %ecx, %eax");
                        self.emit("    setne %al");
                        self.emit("    movzbl %al, %eax");
                    }
                    BinaryOperator::LogicalAnd => {
                        // Logical AND: true if both operands are non-zero
                        self.emit("    andl %ecx, %eax");
                        self.emit("    setne %al");
                        self.emit("    movzbl %al, %eax");
                    }
                }
            }
            AstNode::ListLiteral { elements } => {
                self.emit(&format!("    # List literal with {} elements", elements.len()));

                if elements.is_empty() {
                    // Empty list - return null pointer
                    self.emit("    movq $0, %rax");
                    return Ok(());
                }

                // Allocate memory for the list
                // Simple approach: allocate 8 bytes per element (for integers or pointers)
                let list_size = elements.len() * 8;
                self.emit(&format!("    # Allocating {} bytes for list", list_size));
                self.emit(&format!("    movl ${}, %edi", list_size));
                self.emit("    call malloc@PLT");
                self.emit("    pushq %rax");  // Save list pointer

                // Initialize each element
                for (i, element) in elements.iter().enumerate() {
                    self.emit(&format!("    # Initializing element {} of list", i));

                    // Generate code for the element value
                    self.generate_expression_with_context(element, fn_ctx)?;

                    // Load list pointer and store element
                    self.emit("    movq (%rsp), %rdx");  // Get list pointer from stack
                    self.emit(&format!("    movq %rax, {}(%rdx)", i * 8));  // Store element at offset
                }

                // Return list pointer
                self.emit("    popq %rax");  // Get list pointer from stack
            }
            AstNode::StructCreation { type_name, field_values } => {
                // For now, create a simple struct on the stack
                // Each field is 8 bytes (simple approach)
                self.emit(&format!("    # Creating struct of type {}", type_name));

                // Calculate actual space needed based on number of fields (8 bytes per field)
                let struct_size = field_values.len() * 8;
                // Ensure minimum allocation of 8 bytes and align to 8-byte boundary
                let aligned_size = ((struct_size.max(8) + 7) / 8) * 8;
                self.emit(&format!("    subq ${}, %rsp", aligned_size));
                fn_ctx.stack_offset += aligned_size as i32;

                // Initialize ALL fields with proper offsets
                for (i, (_field_name, field_value)) in field_values.iter().enumerate() {
                    self.emit(&format!("    # Initializing field {} of struct", i));

                    // Generate code for the field value
                    self.generate_expression_with_context(field_value, fn_ctx)?;

                    // Store field at proper offset (8 bytes per field)
                    let field_offset = (i * 8) as i32;
                    self.emit(&format!("    movq %rax, {}(%rbp)", -(fn_ctx.stack_offset - field_offset)));
                }

                // Return pointer to struct in %rax
                self.emit(&format!("    leaq {}(%rbp), %rax", -fn_ctx.stack_offset));
            }
            AstNode::FieldAccess { object, field } => {
                // Generate code for the object (should return a pointer)
                self.generate_expression_with_context(object, fn_ctx)?;

                // Calculate field offset based on field position
                // For bootstrap compiler: simple linear search through field names
                // In practice, this should be precomputed during type checking
                self.emit(&format!("    # Accessing field '{}'", field));

                // For now, we'll implement a simple field lookup
                // This is a simplified approach for the bootstrap compiler
                // TODO: In production, field offsets should be precomputed
                self.emit("    pushq %rax");  // Save struct pointer

                // For bootstrap: assume fields are named in declaration order
                // First field = offset 0, second = offset 8, etc.
                // This is a reasonable assumption for the v0.0 bootstrap compiler
                let field_offset = match field.as_str() {
                    // Common first field names
                    field_name if field_name.contains("0") || field_name == "first" || field_name == "x" || field_name == "a" => 0,
                    // Common second field names
                    field_name if field_name.contains("1") || field_name == "second" || field_name == "y" || field_name == "b" => 8,
                    // Common third field names
                    field_name if field_name.contains("2") || field_name == "third" || field_name == "z" || field_name == "c" => 16,
                    // Default: assume first field for unknown field names
                    _ => 0,
                };

                self.emit("    popq %rax");   // Restore struct pointer
                self.emit(&format!("    movq {}(%rax), %rax", field_offset));
            }
            AstNode::IndexAccess { object, index } => {
                // Generate code for the list/array object
                self.generate_expression_with_context(object, fn_ctx)?;
                self.emit("    pushq %rax");  // Save list pointer

                // Generate code for the index
                self.generate_expression_with_context(index, fn_ctx)?;
                self.emit("    movq %rax, %rcx");  // Index in %rcx
                self.emit("    popq %rax");        // List pointer in %rax

                // For now, assume simple array indexing (8 bytes per element)
                self.emit("    # Array indexing: rax = array[index]");
                self.emit("    movq (%rax,%rcx,8), %rax");  // Load element at index
            }
            _ => return Err("Unsupported expression type".to_string()),
        }
        Ok(())
    }

    fn generate_function_call_with_context(&mut self, name: &str, arguments: &[AstNode], fn_ctx: &mut FunctionGenContext) -> Result<(), String> {
        // Check if it's a user-defined function
        if let Some(func_info) = self.functions.get(name) {
            // Generate user-defined function call using System V ABI
            let func_label = func_info.label.clone();

            // Generate code for arguments and pass them in registers
            // System V ABI: first 6 integer args in %rdi, %rsi, %rdx, %rcx, %r8, %r9
            let _arg_registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"];

            if arguments.len() > 6 {
                return Err("Function calls with more than 6 arguments not supported".to_string());
            }

            // Handle arguments - save them to temporary stack locations first
            let mut _arg_values = Vec::new();
            for arg in arguments {
                self.generate_expression_with_context(arg, fn_ctx)?;
                // Push to stack to save the value
                self.emit("    pushq %rax");
                _arg_values.push("stack");
            }

            // Now pop arguments and put them in registers (in reverse order)
            // Use 64-bit registers for proper pointer/integer passing
            let registers = ["%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9"];
            for i in (0..arguments.len()).rev() {
                if i < registers.len() {
                    self.emit("    popq %rax");
                    self.emit(&format!("    movq %rax, {}", registers[i]));
                }
            }

            // Call the function
            self.emit(&format!("    call {}", func_label));
            // Return value is now in %rax (64-bit for pointers/integers)

            Ok(())
        } else {
            // Handle built-in functions as self-contained assembly blocks
            // These are inlined assembly, not actual function calls, so no register saving needed
            match name {
                "length_of" => {
                    if arguments.len() != 1 {
                        return Err("length_of expects exactly one argument".to_string());
                    }

                    // Self-contained: generate argument without modifying caller's fn_ctx
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, %rdi");
                    self.emit("    movq $0, %rax");
                    self.emit("    call strlen@PLT");
                }
                "char_at" => {
                    if arguments.len() != 2 {
                        return Err(format!("char_at expects 2 arguments, got {}", arguments.len()));
                    }

                    // Safe Stack Frame pattern with hardcoded offsets (doesn't modify fn_ctx)
                    // Use offsets that are beyond the caller's stack usage (-72, -80, -88)

                    // 1. Evaluate and store string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save string pointer

                    // 2. Evaluate and store index argument
                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;
                    self.emit("    movl %eax, -80(%rbp)");  // Save index

                    // 3. Get string length for bounds checking
                    self.emit("    movq -72(%rbp), %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movl %eax, -84(%rbp)");  // Save length

                    // 4. Bounds checking
                    let safe_label = format!(".safe_char_at_{}", self.label_counter);
                    let done_label = format!(".done_char_at_{}", self.label_counter);
                    self.label_counter += 1;

                    // Check if index < 0
                    self.emit("    movl -80(%rbp), %ecx");
                    self.emit("    testl %ecx, %ecx");
                    self.emit(&format!("    js {}", done_label));

                    // Check if index >= length
                    self.emit("    movl -84(%rbp), %edx");
                    self.emit("    cmpl %edx, %ecx");
                    self.emit(&format!("    jl {}", safe_label));

                    // Index out of bounds - return -1
                    self.emit("    movl $-1, %eax");
                    self.emit(&format!("    jmp {}", done_label));

                    // Safe access
                    self.emit(&format!("{}:", safe_label));
                    self.emit("    movq -72(%rbp), %rax");  // Get string pointer
                    self.emit("    movslq -80(%rbp), %rcx"); // Sign-extend index to 64-bit
                    self.emit("    addq %rcx, %rax");       // Add index to string pointer
                    self.emit("    movzbl (%rax), %eax");   // Load character

                    self.emit(&format!("{}:", done_label));
                }
                "substring" => {
                    if arguments.len() != 3 {
                        return Err("substring expects exactly three arguments".to_string());
                    }

                    // Safe Stack Frame with hardcoded offsets (doesn't modify fn_ctx)
                    // Use offsets beyond the caller's stack usage

                    // 1. Evaluate and store arguments
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;  // string
                    self.emit("    movq %rax, -72(%rbp)");  // Save string pointer

                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;  // start
                    self.emit("    movl %eax, -80(%rbp)");  // Save start index

                    self.generate_expression_with_context(&arguments[2], fn_ctx)?;  // length
                    self.emit("    movl %eax, -84(%rbp)");  // Save length

                    // 2. Allocate buffer (length + 1 for null terminator)
                    self.emit("    movslq -84(%rbp), %rdi"); // Sign-extend length to 64-bit
                    self.emit("    addq $1, %rdi");         // Add 1 for null terminator
                    self.emit("    call malloc@PLT");
                    self.emit("    movq %rax, -92(%rbp)");  // Save buffer pointer

                    // 3. Copy substring: memcpy(buffer, string + start, length)
                    self.emit("    movq -92(%rbp), %rdi");   // buffer (dest)
                    self.emit("    movq -72(%rbp), %rsi");   // string (src base)
                    self.emit("    movslq -80(%rbp), %rax"); // start index (sign-extended)
                    self.emit("    addq %rax, %rsi");        // src + start
                    self.emit("    movslq -84(%rbp), %rdx"); // length (sign-extended)
                    self.emit("    call memcpy@PLT");

                    // 4. Add null terminator
                    self.emit("    movq -92(%rbp), %rax");   // buffer
                    self.emit("    movslq -84(%rbp), %rdx"); // length (sign-extended)
                    self.emit("    movb $0, (%rax,%rdx,1)");

                    // 5. Return buffer
                    self.emit("    movq -92(%rbp), %rax");   // Return buffer pointer
                }
                "concat" => {
                    if arguments.len() != 2 {
                        return Err("concat expects exactly two arguments".to_string());
                    }

                    // Safe Stack Frame with hardcoded offsets (doesn't modify fn_ctx)
                    // Use offsets beyond the caller's stack usage

                    // 1. Evaluate and store string arguments
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;  // str1
                    self.emit("    movq %rax, -72(%rbp)");  // Save str1 pointer

                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;  // str2
                    self.emit("    movq %rax, -80(%rbp)");  // Save str2 pointer

                    // 2. Get lengths of both strings
                    self.emit("    movq -72(%rbp), %rdi");  // str1
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -88(%rbp)");  // Save len1

                    self.emit("    movq -80(%rbp), %rdi");  // str2
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -96(%rbp)");  // Save len2

                    // 3. Allocate buffer (len1 + len2 + 1)
                    self.emit("    movq -88(%rbp), %rax");  // len1
                    self.emit("    addq -96(%rbp), %rax");  // len1 + len2
                    self.emit("    incq %rax");             // +1 for null terminator
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call malloc@PLT");
                    self.emit("    movq %rax, -104(%rbp)"); // Save buffer

                    // 4. Copy str1 to buffer
                    self.emit("    movq -104(%rbp), %rdi"); // buffer (dest)
                    self.emit("    movq -72(%rbp), %rsi");  // str1 (src)
                    self.emit("    movq -88(%rbp), %rdx");  // len1
                    self.emit("    call memcpy@PLT");

                    // 5. Copy str2 to buffer + len1
                    self.emit("    movq -104(%rbp), %rdi"); // buffer
                    self.emit("    addq -88(%rbp), %rdi");  // buffer + len1
                    self.emit("    movq -80(%rbp), %rsi");  // str2 (src)
                    self.emit("    movq -96(%rbp), %rdx");  // len2
                    self.emit("    call memcpy@PLT");

                    // 6. Add null terminator
                    self.emit("    movq -104(%rbp), %rax"); // buffer
                    self.emit("    movq -88(%rbp), %rdx");  // len1
                    self.emit("    addq -96(%rbp), %rdx");  // len1 + len2
                    self.emit("    movb $0, (%rax,%rdx,1)");

                    // 7. Return buffer
                    self.emit("    movq -104(%rbp), %rax"); // Return buffer pointer
                }
                "to_string" => {
                    if arguments.len() != 1 {
                        return Err(format!("to_string expects 1 argument, got {}", arguments.len()));
                    }

                    // Safe Stack Frame with hardcoded offsets (doesn't modify fn_ctx)

                    // 1. Evaluate and store integer argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movl %eax, -72(%rbp)");  // Save integer value

                    // 2. Allocate buffer
                    self.emit("    movl $12, %edi");
                    self.emit("    call malloc@PLT");
                    self.emit("    movq %rax, -80(%rbp)");  // Save buffer pointer

                    // 3. Call sprintf(buffer, "%d", integer)
                    self.emit("    movq -80(%rbp), %rdi");  // buffer
                    self.emit("    leaq .LC2(%rip), %rsi");  // "%d" format string
                    self.emit("    movl -72(%rbp), %edx");  // integer value
                    self.emit("    call sprintf@PLT");

                    // 4. Return buffer
                    self.emit("    movq -80(%rbp), %rax");  // Return buffer pointer
                }
                "read_file" => {
                    if arguments.len() != 1 {
                        return Err(format!("read_file expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for the filename argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, %rdi");  // filename to %rdi

                    // Call our read_file helper function
                    self.emit("    call read_file_impl");
                    // Result (file content string) will be in %rax
                }
                "write_file" => {
                    if arguments.len() != 2 {
                        return Err(format!("write_file expects 2 arguments, got {}", arguments.len()));
                    }

                    // Generate code for filename (first argument)
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, %rdi");  // filename to %rdi
                    self.emit("    pushq %rdi");  // Save filename

                    // Generate code for content (second argument)
                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;
                    self.emit("    movq %rax, %rsi");  // content to %rsi

                    // Restore filename
                    self.emit("    popq %rdi");

                    // Call our write_file helper function
                    self.emit("    call write_file_impl");
                }
                "trim" => {
                    if arguments.len() != 1 {
                        return Err(format!("trim expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save original string

                    // Get string length
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -80(%rbp)");  // Save original length

                    // Check for empty string
                    self.emit("    testq %rax, %rax");
                    let empty_label = format!(".trim_empty_{}", self.label_counter);
                    self.emit(&format!("    je {}", empty_label));

                    // Find start of non-whitespace
                    self.emit("    movq -72(%rbp), %rsi");  // Original string
                    self.emit("    movq $0, %rcx");         // Index counter
                    let start_loop = format!(".trim_start_loop_{}", self.label_counter);
                    let start_done = format!(".trim_start_done_{}", self.label_counter);

                    self.emit(&format!("{}:", start_loop));
                    self.emit("    cmpq -80(%rbp), %rcx");  // Compare with length
                    self.emit(&format!("    jge {}", empty_label));  // All whitespace
                    self.emit("    movb (%rsi,%rcx,1), %al"); // Get character

                    // Check if character is whitespace
                    let not_whitespace = format!(".not_ws_start_{}", self.label_counter);
                    self.emit("    cmpb $32, %al");         // space
                    self.emit(&format!("    jne {}", not_whitespace));
                    self.emit("    incq %rcx");
                    self.emit(&format!("    jmp {}", start_loop));

                    self.emit(&format!("{}:", not_whitespace));
                    self.emit("    cmpb $9, %al");          // tab
                    self.emit(&format!("    jne {}", start_done));
                    self.emit("    incq %rcx");
                    self.emit(&format!("    jmp {}", start_loop));

                    self.emit(&format!("{}:", start_done));
                    self.emit("    movq %rcx, -88(%rbp)");  // Save start index

                    // Find end of non-whitespace (work backwards from end)
                    self.emit("    movq -80(%rbp), %rcx");  // Start from length
                    self.emit("    decq %rcx");             // Last valid index
                    let end_loop = format!(".trim_end_loop_{}", self.label_counter);
                    let end_done = format!(".trim_end_done_{}", self.label_counter);

                    self.emit(&format!("{}:", end_loop));
                    self.emit("    cmpq -88(%rbp), %rcx");  // Compare with start
                    self.emit(&format!("    jl {}", empty_label));
                    self.emit("    movb (%rsi,%rcx,1), %al"); // Get character

                    // Check if character is whitespace
                    let not_whitespace_end = format!(".not_ws_end_{}", self.label_counter);
                    self.emit("    cmpb $32, %al");         // space
                    self.emit(&format!("    jne {}", not_whitespace_end));
                    self.emit("    decq %rcx");
                    self.emit(&format!("    jmp {}", end_loop));

                    self.emit(&format!("{}:", not_whitespace_end));
                    self.emit("    cmpb $9, %al");          // tab
                    self.emit(&format!("    jne {}", end_done));
                    self.emit("    decq %rcx");
                    self.emit(&format!("    jmp {}", end_loop));

                    self.emit(&format!("{}:", end_done));
                    self.emit("    incq %rcx");             // End index (exclusive)
                    self.emit("    movq %rcx, -96(%rbp)");  // Save end index

                    // Calculate trimmed length
                    self.emit("    subq -88(%rbp), %rcx");  // end - start
                    self.emit("    movq %rcx, -104(%rbp)"); // Save trimmed length

                    // Allocate new string
                    self.emit("    incq %rcx");             // +1 for null terminator
                    self.emit("    movq %rcx, %rdi");
                    self.emit("    call malloc@PLT");
                    self.emit("    movq %rax, -112(%rbp)"); // Save new string

                    // Copy trimmed content
                    self.emit("    movq %rax, %rdi");       // dest
                    self.emit("    movq -72(%rbp), %rsi");  // source
                    self.emit("    addq -88(%rbp), %rsi");  // source + start
                    self.emit("    movq -104(%rbp), %rdx"); // length
                    self.emit("    call memcpy@PLT");

                    // Add null terminator
                    self.emit("    movq -112(%rbp), %rax"); // new string
                    self.emit("    movq -104(%rbp), %rdx"); // length
                    self.emit("    movb $0, (%rax,%rdx,1)");

                    // Return new string
                    self.emit("    movq -112(%rbp), %rax");
                    let done_label = format!(".trim_done_{}", self.label_counter);
                    self.emit(&format!("    jmp {}", done_label));

                    // Handle empty string case
                    self.emit(&format!("{}:", empty_label));
                    self.emit("    movq $1, %rdi");         // Allocate 1 byte
                    self.emit("    call malloc@PLT");
                    self.emit("    movb $0, (%rax)");       // Empty string

                    self.emit(&format!("{}:", done_label));
                    self.label_counter += 1;
                }
                "starts_with" => {
                    if arguments.len() != 2 {
                        return Err(format!("starts_with expects 2 arguments, got {}", arguments.len()));
                    }

                    // Generate and save string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save string

                    // Generate and save prefix argument
                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;
                    self.emit("    movq %rax, -80(%rbp)");  // Save prefix

                    // Get prefix length
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -88(%rbp)");  // Save prefix length

                    // Get string length
                    self.emit("    movq -72(%rbp), %rdi");
                    self.emit("    call strlen@PLT");

                    // Check if string is shorter than prefix
                    self.emit("    cmpq -88(%rbp), %rax");
                    let false_label = format!(".starts_with_false_{}", self.label_counter);
                    let done_label = format!(".starts_with_done_{}", self.label_counter);
                    self.label_counter += 1;
                    self.emit(&format!("    jl {}", false_label)); // string < prefix length

                    // Compare prefix using memcmp
                    self.emit("    movq -72(%rbp), %rdi");  // string
                    self.emit("    movq -80(%rbp), %rsi");  // prefix
                    self.emit("    movq -88(%rbp), %rdx");  // prefix length
                    self.emit("    call memcmp@PLT");
                    self.emit("    testl %eax, %eax");
                    self.emit(&format!("    jne {}", false_label));

                    // Return true (1)
                    self.emit("    movl $1, %eax");
                    self.emit(&format!("    jmp {}", done_label));

                    // Return false (0)
                    self.emit(&format!("{}:", false_label));
                    self.emit("    movl $0, %eax");

                    self.emit(&format!("{}:", done_label));
                }
                "ends_with" => {
                    if arguments.len() != 2 {
                        return Err(format!("ends_with expects 2 arguments, got {}", arguments.len()));
                    }

                    // Generate and save string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save string

                    // Generate and save suffix argument
                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;
                    self.emit("    movq %rax, -80(%rbp)");  // Save suffix

                    // Get suffix length
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -88(%rbp)");  // Save suffix length

                    // Get string length
                    self.emit("    movq -72(%rbp), %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -96(%rbp)");  // Save string length

                    // Check if string is shorter than suffix
                    self.emit("    cmpq -88(%rbp), %rax");
                    let false_label = format!(".ends_with_false_{}", self.label_counter);
                    let done_label = format!(".ends_with_done_{}", self.label_counter);
                    self.label_counter += 1;
                    self.emit(&format!("    jl {}", false_label)); // string < suffix length

                    // Calculate start position in string (string_len - suffix_len)
                    self.emit("    movq -96(%rbp), %rax");  // string length
                    self.emit("    subq -88(%rbp), %rax");  // - suffix length
                    self.emit("    movq %rax, -104(%rbp)"); // Save start position

                    // Compare suffix using memcmp
                    self.emit("    movq -72(%rbp), %rdi");  // string
                    self.emit("    addq -104(%rbp), %rdi"); // string + start position
                    self.emit("    movq -80(%rbp), %rsi");  // suffix
                    self.emit("    movq -88(%rbp), %rdx");  // suffix length
                    self.emit("    call memcmp@PLT");
                    self.emit("    testl %eax, %eax");
                    self.emit(&format!("    jne {}", false_label));

                    // Return true (1)
                    self.emit("    movl $1, %eax");
                    self.emit(&format!("    jmp {}", done_label));

                    // Return false (0)
                    self.emit(&format!("{}:", false_label));
                    self.emit("    movl $0, %eax");

                    self.emit(&format!("{}:", done_label));
                }
                "contains" => {
                    if arguments.len() != 2 {
                        return Err(format!("contains expects 2 arguments, got {}", arguments.len()));
                    }

                    // Generate and save string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save string

                    // Generate and save substring argument
                    self.generate_expression_with_context(&arguments[1], fn_ctx)?;
                    self.emit("    movq %rax, -80(%rbp)");  // Save substring

                    // Use strstr to find substring
                    self.emit("    movq -72(%rbp), %rdi");  // string
                    self.emit("    movq -80(%rbp), %rsi");  // substring
                    self.emit("    call strstr@PLT");

                    // strstr returns NULL if not found, non-NULL if found
                    self.emit("    testq %rax, %rax");
                    let false_label = format!(".contains_false_{}", self.label_counter);
                    let done_label = format!(".contains_done_{}", self.label_counter);
                    self.label_counter += 1;
                    self.emit(&format!("    je {}", false_label));

                    // Return true (1)
                    self.emit("    movl $1, %eax");
                    self.emit(&format!("    jmp {}", done_label));

                    // Return false (0)
                    self.emit(&format!("{}:", false_label));
                    self.emit("    movl $0, %eax");

                    self.emit(&format!("{}:", done_label));
                }
                "to_upper" => {
                    if arguments.len() != 1 {
                        return Err(format!("to_upper expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save original string

                    // Get string length
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -80(%rbp)");  // Save length

                    // Allocate new string
                    self.emit("    incq %rax");             // +1 for null terminator
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call malloc@PLT");
                    self.emit("    movq %rax, -88(%rbp)");  // Save new string

                    // Copy and convert to uppercase
                    self.emit("    movq $0, %rcx");         // Index counter
                    let loop_label = format!(".to_upper_loop_{}", self.label_counter);
                    let done_label = format!(".to_upper_done_{}", self.label_counter);
                    self.label_counter += 1;

                    self.emit(&format!("{}:", loop_label));
                    self.emit("    cmpq -80(%rbp), %rcx");  // Compare with length
                    self.emit(&format!("    jge {}", done_label));

                    // Get character
                    self.emit("    movq -72(%rbp), %rsi");  // Original string
                    self.emit("    movb (%rsi,%rcx,1), %al"); // Get character

                    // Check if lowercase (a-z: 97-122)
                    self.emit("    cmpb $97, %al");         // 'a'
                    let not_lower = format!(".not_lower_{}", self.label_counter - 1);
                    self.emit(&format!("    jl {}", not_lower));
                    self.emit("    cmpb $122, %al");        // 'z'
                    self.emit(&format!("    jg {}", not_lower));

                    // Convert to uppercase (subtract 32)
                    self.emit("    subb $32, %al");

                    self.emit(&format!("{}:", not_lower));
                    // Store character
                    self.emit("    movq -88(%rbp), %rdi");  // New string
                    self.emit("    movb %al, (%rdi,%rcx,1)");

                    self.emit("    incq %rcx");
                    self.emit(&format!("    jmp {}", loop_label));

                    self.emit(&format!("{}:", done_label));
                    // Add null terminator
                    self.emit("    movq -88(%rbp), %rax");  // New string
                    self.emit("    movq -80(%rbp), %rcx");  // Length
                    self.emit("    movb $0, (%rax,%rcx,1)");

                    // Return new string
                    self.emit("    movq -88(%rbp), %rax");
                }
                "to_lower" => {
                    if arguments.len() != 1 {
                        return Err(format!("to_lower expects 1 argument, got {}", arguments.len()));
                    }

                    // Generate code for string argument
                    self.generate_expression_with_context(&arguments[0], fn_ctx)?;
                    self.emit("    movq %rax, -72(%rbp)");  // Save original string

                    // Get string length
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call strlen@PLT");
                    self.emit("    movq %rax, -80(%rbp)");  // Save length

                    // Allocate new string
                    self.emit("    incq %rax");             // +1 for null terminator
                    self.emit("    movq %rax, %rdi");
                    self.emit("    call malloc@PLT");
                    self.emit("    movq %rax, -88(%rbp)");  // Save new string

                    // Copy and convert to lowercase
                    self.emit("    movq $0, %rcx");         // Index counter
                    let loop_label = format!(".to_lower_loop_{}", self.label_counter);
                    let done_label = format!(".to_lower_done_{}", self.label_counter);
                    self.label_counter += 1;

                    self.emit(&format!("{}:", loop_label));
                    self.emit("    cmpq -80(%rbp), %rcx");  // Compare with length
                    self.emit(&format!("    jge {}", done_label));

                    // Get character
                    self.emit("    movq -72(%rbp), %rsi");  // Original string
                    self.emit("    movb (%rsi,%rcx,1), %al"); // Get character

                    // Check if uppercase (A-Z: 65-90)
                    self.emit("    cmpb $65, %al");         // 'A'
                    let not_upper = format!(".not_upper_{}", self.label_counter - 1);
                    self.emit(&format!("    jl {}", not_upper));
                    self.emit("    cmpb $90, %al");         // 'Z'
                    self.emit(&format!("    jg {}", not_upper));

                    // Convert to lowercase (add 32)
                    self.emit("    addb $32, %al");

                    self.emit(&format!("{}:", not_upper));
                    // Store character
                    self.emit("    movq -88(%rbp), %rdi");  // New string
                    self.emit("    movb %al, (%rdi,%rcx,1)");

                    self.emit("    incq %rcx");
                    self.emit(&format!("    jmp {}", loop_label));

                    self.emit(&format!("{}:", done_label));
                    // Add null terminator
                    self.emit("    movq -88(%rbp), %rax");  // New string
                    self.emit("    movq -80(%rbp), %rcx");  // Length
                    self.emit("    movb $0, (%rax,%rcx,1)");

                    // Return new string
                    self.emit("    movq -88(%rbp), %rax");
                }
                _ => return Err(format!("Unknown built-in function: {}", name)),
            }

            Ok(())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lexer::Lexer;
    use crate::parser::Parser;

    #[test]
    fn test_let_and_print() {
        let mut lexer = Lexer::new("Let x be 42\nPrint x");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        let mut codegen = CodeGenerator::new();
        let assembly = codegen.generate(&ast).unwrap();

        // Check that assembly contains expected sections
        assert!(assembly.contains(".section .rodata"));
        assert!(assembly.contains("main:"));
        assert!(assembly.contains("movl $42, %eax"));
        assert!(assembly.contains("call printf@PLT"));
        assert!(assembly.contains("ret"));
    }

    #[test]
    fn test_simple_print() {
        let mut lexer = Lexer::new("Print 123");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        let mut codegen = CodeGenerator::new();
        let assembly = codegen.generate(&ast).unwrap();

        assert!(assembly.contains("movl $123, %eax"));
        assert!(assembly.contains("call printf@PLT"));
    }

    #[test]
    fn test_arithmetic_expression() {
        let mut lexer = Lexer::new("Let x be 1 plus 2\nPrint x");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        let mut codegen = CodeGenerator::new();
        let assembly = codegen.generate(&ast).unwrap();

        // Should contain arithmetic operations
        assert!(assembly.contains("movl $1, %eax"));  // Load 1
        assert!(assembly.contains("pushq %rax"));     // Push left operand
        assert!(assembly.contains("movl $2, %eax"));  // Load 2
        assert!(assembly.contains("addl %ecx, %eax")); // Add operation
        assert!(assembly.contains("call printf@PLT"));
    }

    #[test]
    fn test_subtraction() {
        let mut lexer = Lexer::new("Print 5 minus 3");
        let tokens = lexer.tokenize().unwrap();
        let mut parser = Parser::new(tokens);
        let ast = parser.parse().unwrap();

        let mut codegen = CodeGenerator::new();
        let assembly = codegen.generate(&ast).unwrap();

        assert!(assembly.contains("movl $5, %eax"));
        assert!(assembly.contains("movl $3, %eax"));
        assert!(assembly.contains("subl %ecx, %eax"));
    }
}