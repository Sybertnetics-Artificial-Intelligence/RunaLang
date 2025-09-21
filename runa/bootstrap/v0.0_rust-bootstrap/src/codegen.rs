// Minimal Viable Codegen for Runa Bootstrap
// Generates x86-64 assembly using libc for simplicity

use crate::parser::{AstNode, ComparisonOp};
use std::collections::HashMap;

pub struct CodeGenerator {
    output: String,
    stack_offset: i32,
    variables: HashMap<String, i32>, // name -> stack offset
    structs: HashMap<String, Vec<(String, String)>>, // struct name -> fields
    functions: HashMap<String, (Vec<(String, String)>, String)>, // func name -> (params, return_type)
    label_counter: i32,
    string_literals: Vec<String>,
    in_function: bool,
}

impl CodeGenerator {
    pub fn new() -> Self {
        CodeGenerator {
            output: String::new(),
            stack_offset: 0,
            variables: HashMap::new(),
            structs: HashMap::new(),
            functions: HashMap::new(),
            label_counter: 0,
            string_literals: Vec::new(),
            in_function: false,
        }
    }

    fn emit(&mut self, line: &str) {
        self.output.push_str(line);
        self.output.push('\n');
    }

    fn new_label(&mut self) -> String {
        self.label_counter += 1;
        format!(".L{}", self.label_counter)
    }

    fn add_string_literal(&mut self, s: &str) -> String {
        let label = format!(".LC{}", self.string_literals.len());
        self.string_literals.push(s.to_string());
        label
    }

    pub fn generate(&mut self, ast: AstNode) -> String {
        // Generate assembly header
        self.emit("    .intel_syntax noprefix");
        self.emit("    .text");
        self.emit("");

        // Process the AST
        match ast {
            AstNode::Program(items) => {
                for item in items {
                    self.generate_item(item);
                }
            }
            _ => panic!("Expected Program node at root"),
        }

        // Add string literals at the end
        if !self.string_literals.is_empty() {
            self.output.push_str("\n");
            self.output.push_str("    .section .rodata\n");
            for (i, s) in self.string_literals.iter().enumerate() {
                self.output.push_str(&format!(".LC{}:\n", i));
                self.output.push_str(&format!("    .string \"{}\"\n", escape_string(s)));
            }
        }

        self.output.clone()
    }

    fn generate_item(&mut self, node: AstNode) {
        match node {
            AstNode::StructDef { name, fields } => {
                // Store struct definition for later use
                self.structs.insert(name, fields);
            }
            AstNode::FunctionDef { name, params, return_type, body } => {
                self.functions.insert(name.clone(), (params.clone(), return_type));
                self.generate_function(&name, params, body);
            }
            _ => {} // Top-level statements ignored for now
        }
    }

    fn generate_function(&mut self, name: &str, params: Vec<(String, String)>, body: Vec<AstNode>) {
        // Reset function context
        self.variables.clear();
        self.stack_offset = 0;
        self.in_function = true;

        // Function entry
        self.emit("");
        self.emit(&format!("    .global {}", name));
        self.emit(&format!("{}:", name));
        self.emit("    push rbp");
        self.emit("    mov rbp, rsp");

        // Allocate space for local variables (we'll adjust this later)
        let locals_space = 256; // Reserve 256 bytes for now
        self.emit(&format!("    sub rsp, {}", locals_space));

        // Store parameters
        let param_regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"];
        for (i, (param_name, _param_type)) in params.iter().enumerate() {
            if i < param_regs.len() {
                self.stack_offset -= 8;
                self.variables.insert(param_name.clone(), self.stack_offset);
                self.emit(&format!("    mov QWORD PTR [rbp{}], {}",
                    self.stack_offset, param_regs[i]));
            }
        }

        // Generate function body
        for stmt in body {
            self.generate_statement(stmt);
        }

        // Function exit (if no explicit return)
        if name == "main" && !self.output.ends_with("ret\n") {
            self.emit("    mov eax, 0");
        }

        self.emit("    leave");
        self.emit("    ret");

        self.in_function = false;
    }

    fn generate_statement(&mut self, node: AstNode) {
        match node {
            AstNode::LetStatement { name, value } => {
                self.generate_expression(*value);
                // Store in local variable
                self.stack_offset -= 8;
                self.variables.insert(name.clone(), self.stack_offset);
                self.emit(&format!("    mov QWORD PTR [rbp{}], rax", self.stack_offset));
            }
            AstNode::IfStatement { condition, then_branch, else_branch } => {
                let else_label = self.new_label();
                let end_label = self.new_label();

                // Generate condition
                self.generate_condition(*condition, &else_label);

                // Then branch
                for stmt in then_branch {
                    self.generate_statement(stmt);
                }
                self.emit(&format!("    jmp {}", end_label));

                // Else branch
                self.emit(&format!("{}:", else_label));
                if let Some(else_stmts) = else_branch {
                    for stmt in else_stmts {
                        self.generate_statement(stmt);
                    }
                }

                self.emit(&format!("{}:", end_label));
            }
            AstNode::WhileStatement { condition, body } => {
                let loop_start = self.new_label();
                let loop_end = self.new_label();

                self.emit(&format!("{}:", loop_start));

                // Generate condition
                self.generate_condition(*condition, &loop_end);

                // Loop body
                for stmt in body {
                    self.generate_statement(stmt);
                }

                self.emit(&format!("    jmp {}", loop_start));
                self.emit(&format!("{}:", loop_end));
            }
            AstNode::ReturnStatement { value } => {
                self.generate_expression(*value);
                self.emit("    leave");
                self.emit("    ret");
            }
            AstNode::ExpressionStatement { expr } => {
                self.generate_expression(*expr);
            }
            _ => {} // Ignore other statements for now
        }
    }

    fn generate_condition(&mut self, node: AstNode, false_label: &str) {
        match node {
            AstNode::Comparison { left, op, right } => {
                self.generate_expression(*left);
                self.emit("    push rax");
                self.generate_expression(*right);
                self.emit("    mov rbx, rax");
                self.emit("    pop rax");
                self.emit("    cmp rax, rbx");

                match op {
                    ComparisonOp::Equal => self.emit(&format!("    jne {}", false_label)),
                    ComparisonOp::LessThan => self.emit(&format!("    jge {}", false_label)),
                    ComparisonOp::GreaterThan => self.emit(&format!("    jle {}", false_label)),
                }
            }
            _ => {
                // Simple expression as condition
                self.generate_expression(node);
                self.emit("    test rax, rax");
                self.emit(&format!("    je {}", false_label));
            }
        }
    }

    fn generate_expression(&mut self, node: AstNode) {
        match node {
            AstNode::IntegerLiteral(n) => {
                self.emit(&format!("    mov rax, {}", n));
            }
            AstNode::StringLiteral(s) => {
                let label = self.add_string_literal(&s);
                self.emit(&format!("    lea rax, [rip + {}]", label));
            }
            AstNode::Identifier(name) => {
                if let Some(&offset) = self.variables.get(&name) {
                    self.emit(&format!("    mov rax, QWORD PTR [rbp{}]", offset));
                } else {
                    // Assume it's a builtin or external function
                    self.emit(&format!("    lea rax, [rip + {}]", name));
                }
            }
            AstNode::FunctionCall { name, args } => {
                self.generate_function_call(&name, args);
            }
            AstNode::FieldAccess { object, field: _ } => {
                // Simple field access (assuming structs are pointers)
                self.generate_expression(*object);

                // Calculate field offset (simple: assume 8 bytes per field)
                // In real implementation, we'd look up the struct type
                let field_index = 0; // Simplified - would need proper lookup
                let offset = field_index * 8;

                self.emit(&format!("    mov rax, QWORD PTR [rax + {}]", offset));
            }
            AstNode::ListLiteral { elements } => {
                // Allocate list on heap using malloc
                let size = (elements.len() + 1) * 8; // +1 for length field
                self.emit(&format!("    mov rdi, {}", size));
                self.emit("    call malloc");
                self.emit("    push rax"); // Save list pointer

                // Store length
                self.emit(&format!("    mov QWORD PTR [rax], {}", elements.len()));

                // Store elements
                for (i, elem) in elements.iter().enumerate() {
                    self.generate_expression(elem.clone());
                    self.emit(&format!("    mov rbx, QWORD PTR [rsp]")); // Get list pointer
                    self.emit(&format!("    mov QWORD PTR [rbx + {}], rax", (i + 1) * 8));
                }

                self.emit("    pop rax"); // Return list pointer
            }
            _ => {} // Ignore other expressions for now
        }
    }

    fn generate_function_call(&mut self, name: &str, args: Vec<AstNode>) {
        // Save caller-saved registers if needed

        // Evaluate arguments
        let param_regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"];

        // Special handling for builtin functions
        match name {
            "read_file" => {
                // read_file(path) -> string
                if args.len() == 1 {
                    self.generate_expression(args[0].clone());
                    self.emit("    mov rdi, rax");
                    self.emit("    call read_file_impl");
                }
            }
            "write_file" => {
                // write_file(path, content)
                if args.len() == 2 {
                    self.generate_expression(args[0].clone());
                    self.emit("    push rax");
                    self.generate_expression(args[1].clone());
                    self.emit("    mov rsi, rax");
                    self.emit("    pop rdi");
                    self.emit("    call write_file_impl");
                }
            }
            "length_of" => {
                // length_of(string) -> integer
                if args.len() == 1 {
                    self.generate_expression(args[0].clone());
                    self.emit("    mov rdi, rax");
                    self.emit("    call strlen");
                }
            }
            "char_at" => {
                // char_at(string, index) -> char
                if args.len() == 2 {
                    self.generate_expression(args[0].clone());
                    self.emit("    push rax");
                    self.generate_expression(args[1].clone());
                    self.emit("    pop rbx");
                    self.emit("    movzx rax, BYTE PTR [rbx + rax]");
                }
            }
            "is_digit" => {
                // is_digit(char) -> bool
                if args.len() == 1 {
                    self.generate_expression(args[0].clone());
                    self.emit("    sub rax, '0'");
                    self.emit("    cmp rax, 9");
                    self.emit("    setbe al");
                    self.emit("    movzx rax, al");
                }
            }
            "is_alpha" => {
                // is_alpha(char) -> bool
                if args.len() == 1 {
                    self.generate_expression(args[0].clone());
                    self.emit("    mov rbx, rax");
                    // Check if A-Z
                    self.emit("    sub rbx, 'A'");
                    self.emit("    cmp rbx, 25");
                    self.emit("    setbe cl");
                    // Check if a-z
                    self.emit("    mov rbx, rax");
                    self.emit("    sub rbx, 'a'");
                    self.emit("    cmp rbx, 25");
                    self.emit("    setbe dl");
                    // OR the results
                    self.emit("    or cl, dl");
                    self.emit("    movzx rax, cl");
                }
            }
            "add_to_list" => {
                // add_to_list(list, item)
                if args.len() == 2 {
                    self.generate_expression(args[0].clone());
                    self.emit("    push rax");
                    self.generate_expression(args[1].clone());
                    self.emit("    mov rsi, rax");
                    self.emit("    pop rdi");
                    self.emit("    call add_to_list_impl");
                }
            }
            "system_call" => {
                // system_call(command)
                if args.len() == 1 {
                    self.generate_expression(args[0].clone());
                    self.emit("    mov rdi, rax");
                    self.emit("    call system");
                }
            }
            _ => {
                // Regular function call
                for (i, arg) in args.iter().enumerate() {
                    if i < param_regs.len() {
                        self.generate_expression(arg.clone());
                        if i == 0 {
                            self.emit(&format!("    mov {}, rax", param_regs[i]));
                        } else {
                            self.emit(&format!("    push rax"));
                        }
                    }
                }

                // Pop arguments into registers (reverse order)
                for i in (1..args.len().min(param_regs.len())).rev() {
                    self.emit(&format!("    pop {}", param_regs[i]));
                }

                self.emit(&format!("    call {}", name));
            }
        }
    }
}

fn escape_string(s: &str) -> String {
    s.replace('\\', "\\\\")
        .replace('"', "\\\"")
        .replace('\n', "\\n")
        .replace('\t', "\\t")
        .replace('\r', "\\r")
}

// Helper implementations that would be linked
pub fn generate_runtime_helpers() -> String {
    let mut output = String::new();

    // read_file implementation
    output.push_str("
read_file_impl:
    push rbp
    mov rbp, rsp
    sub rsp, 16

    # Open file
    mov rsi, 0  # O_RDONLY
    mov rax, 2  # open syscall
    syscall

    test rax, rax
    js .read_error
    mov r12, rax  # Save fd

    # Get file size
    mov rdi, r12
    mov rsi, 0
    mov rdx, 2  # SEEK_END
    mov rax, 8  # lseek
    syscall
    mov r13, rax  # Save size

    # Allocate buffer
    mov rdi, r13
    inc rdi
    call malloc
    mov r14, rax  # Save buffer

    # Reset to beginning
    mov rdi, r12
    mov rsi, 0
    mov rdx, 0  # SEEK_SET
    mov rax, 8
    syscall

    # Read file
    mov rdi, r12
    mov rsi, r14
    mov rdx, r13
    mov rax, 0  # read
    syscall

    # Null terminate
    mov byte ptr [r14 + r13], 0

    # Close file
    mov rdi, r12
    mov rax, 3  # close
    syscall

    mov rax, r14
    leave
    ret

.read_error:
    xor rax, rax
    leave
    ret

write_file_impl:
    push rbp
    mov rbp, rsp
    push r12
    push r13

    mov r12, rdi  # path
    mov r13, rsi  # content

    # Open/create file
    mov rdi, r12
    mov rsi, 0x241  # O_CREAT | O_WRONLY | O_TRUNC
    mov rdx, 0644
    mov rax, 2  # open
    syscall

    test rax, rax
    js .write_error
    mov r12, rax  # fd

    # Get string length
    mov rdi, r13
    call strlen
    mov rdx, rax  # length

    # Write
    mov rdi, r12
    mov rsi, r13
    mov rax, 1  # write
    syscall

    # Close
    mov rdi, r12
    mov rax, 3  # close
    syscall

    xor rax, rax
    pop r13
    pop r12
    leave
    ret

.write_error:
    mov rax, -1
    pop r13
    pop r12
    leave
    ret

add_to_list_impl:
    # Simple implementation - reallocate with more space
    push rbp
    mov rbp, rsp
    push rbx

    mov rbx, rdi  # list pointer
    mov rcx, rsi  # new item

    # Get current length
    mov rdx, [rbx]

    # Allocate new list with size+1
    lea rdi, [rdx + 2]
    shl rdi, 3
    call malloc

    # Copy old data
    mov rdi, rax
    mov rsi, rbx
    mov rdx, [rbx]
    inc rdx
    shl rdx, 3
    call memcpy

    # Add new item
    mov rbx, rax
    mov rdx, [rbx]
    inc rdx
    mov [rbx], rdx
    mov [rbx + rdx*8], rcx

    mov rax, rbx
    pop rbx
    leave
    ret
");

    output
}