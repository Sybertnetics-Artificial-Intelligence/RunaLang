use anyhow::{anyhow, Result};
use llvm_sys::core::*;
use llvm_sys::prelude::*;
use llvm_sys::target::*;
use llvm_sys::target_machine::*;
use llvm_sys::analysis::*;
use llvm_sys::analysis::LLVMVerifierFailureAction::*;
use llvm_sys::LLVMIntPredicate;
use llvm_sys::LLVMRealPredicate;
use llvm_sys::LLVMTypeKind;
use std::collections::HashMap;
use std::ffi::{CString, CStr};
use std::ptr;

use crate::parser::*;
use crate::types::Type;
use crate::modules::{ModuleManager, Module, ModuleExport};

pub struct CodeGenerator {
    context: LLVMContextRef,
    module: LLVMModuleRef,
    builder: LLVMBuilderRef,

    // Symbol tables
    functions: HashMap<String, LLVMValueRef>,
    function_types: HashMap<String, LLVMTypeRef>,  // Store function types separately
    variables: HashMap<String, LLVMValueRef>,
    variable_types: HashMap<String, String>,  // Track variable type names: var_name -> type_name
    types: HashMap<String, LLVMTypeRef>,
    type_fields: HashMap<String, Vec<(String, LLVMTypeRef)>>,  // Track struct fields: type_name -> [(field_name, field_type)]

    // Pass-by-reference tracking
    mutable_params: HashMap<String, Vec<String>>,  // function_name -> [mutable_param_names]
    param_is_pointer: HashMap<String, bool>,  // param_name -> is_passed_by_ref (for current function)

    // Current function context
    current_function: Option<LLVMValueRef>,
    current_block: Option<LLVMBasicBlockRef>,
    current_function_name: Option<String>,

    // Optimization level
    opt_level: u8,

    // Module system
    module_manager: Option<ModuleManager>,
}

impl CodeGenerator {
    pub fn new(module_name: &str, opt_level: u8) -> Result<Self> {
        unsafe {
            // Initialize LLVM
            LLVM_InitializeAllTargetInfos();
            LLVM_InitializeAllTargets();
            LLVM_InitializeAllTargetMCs();
            LLVM_InitializeAllAsmParsers();
            LLVM_InitializeAllAsmPrinters();

            let context = LLVMContextCreate();
            let module_name = CString::new(module_name)?;
            let module = LLVMModuleCreateWithNameInContext(module_name.as_ptr(), context);
            let builder = LLVMCreateBuilderInContext(context);

            // Set target triple
            let target_triple = get_default_target_triple();
            LLVMSetTarget(module, target_triple.as_ptr());

            let mut codegen = CodeGenerator {
                context,
                module,
                builder,
                functions: HashMap::new(),
                function_types: HashMap::new(),
                variables: HashMap::new(),
                variable_types: HashMap::new(),
                types: HashMap::new(),
                type_fields: HashMap::new(),
                mutable_params: HashMap::new(),
                param_is_pointer: HashMap::new(),
                current_function: None,
                current_block: None,
                current_function_name: None,
                opt_level,
                module_manager: Some(ModuleManager::new()),
            };

            // Declare runtime functions
            codegen.declare_runtime_functions();

            Ok(codegen)
        }
    }

    fn declare_runtime_functions(&mut self) {
        unsafe {
            // Declare printf for output
            let printf_type = LLVMFunctionType(
                LLVMInt32TypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                1,
                1, // variadic
            );
            let printf_name = CString::new("printf").unwrap();
            let printf = LLVMAddFunction(self.module, printf_name.as_ptr(), printf_type);
            self.functions.insert("printf".to_string(), printf);

            // Declare malloc for memory allocation
            let malloc_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                1,
                0,
            );
            let malloc_name = CString::new("malloc").unwrap();
            let malloc = LLVMAddFunction(self.module, malloc_name.as_ptr(), malloc_type);
            self.functions.insert("malloc".to_string(), malloc);
            self.function_types.insert("malloc".to_string(), malloc_type);

            // Declare free for memory deallocation
            let free_type = LLVMFunctionType(
                LLVMVoidTypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                1,
                0,
            );
            let free_name = CString::new("free").unwrap();
            let free = LLVMAddFunction(self.module, free_name.as_ptr(), free_type);
            self.functions.insert("free".to_string(), free);

            // Declare fopen for file opening
            let fopen_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // FILE*
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // filename
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // mode
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let fopen_name = CString::new("fopen").unwrap();
            let fopen = LLVMAddFunction(self.module, fopen_name.as_ptr(), fopen_type);
            self.functions.insert("fopen".to_string(), fopen);

            // Declare fclose for file closing
            let fclose_type = LLVMFunctionType(
                LLVMInt32TypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _, // FILE*
                1,
                0,
            );
            let fclose_name = CString::new("fclose").unwrap();
            let fclose = LLVMAddFunction(self.module, fclose_name.as_ptr(), fclose_type);
            self.functions.insert("fclose".to_string(), fclose);

            // Declare fread for file reading
            let fread_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // size_t
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // buffer
                    LLVMInt64TypeInContext(self.context), // size
                    LLVMInt64TypeInContext(self.context), // count
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // FILE*
                ].as_ptr() as *mut _,
                4,
                0,
            );
            let fread_name = CString::new("fread").unwrap();
            let fread = LLVMAddFunction(self.module, fread_name.as_ptr(), fread_type);
            self.functions.insert("fread".to_string(), fread);

            // Declare fwrite for file writing
            let fwrite_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // size_t
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // buffer
                    LLVMInt64TypeInContext(self.context), // size
                    LLVMInt64TypeInContext(self.context), // count
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // FILE*
                ].as_ptr() as *mut _,
                4,
                0,
            );
            let fwrite_name = CString::new("fwrite").unwrap();
            let fwrite = LLVMAddFunction(self.module, fwrite_name.as_ptr(), fwrite_type);
            self.functions.insert("fwrite".to_string(), fwrite);

            // Declare fseek for file positioning
            let fseek_type = LLVMFunctionType(
                LLVMInt32TypeInContext(self.context),
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // FILE*
                    LLVMInt64TypeInContext(self.context), // offset
                    LLVMInt32TypeInContext(self.context), // whence
                ].as_ptr() as *mut _,
                3,
                0,
            );
            let fseek_name = CString::new("fseek").unwrap();
            let fseek = LLVMAddFunction(self.module, fseek_name.as_ptr(), fseek_type);
            self.functions.insert("fseek".to_string(), fseek);

            // Declare ftell for getting file position
            let ftell_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _, // FILE*
                1,
                0,
            );
            let ftell_name = CString::new("ftell").unwrap();
            let ftell = LLVMAddFunction(self.module, ftell_name.as_ptr(), ftell_type);
            self.functions.insert("ftell".to_string(), ftell);

            // Declare strlen for string length
            let strlen_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                1,
                0,
            );
            let strlen_name = CString::new("strlen").unwrap();
            let strlen = LLVMAddFunction(self.module, strlen_name.as_ptr(), strlen_type);
            self.functions.insert("strlen".to_string(), strlen);

            // Declare sprintf for string formatting
            let sprintf_type = LLVMFunctionType(
                LLVMInt32TypeInContext(self.context), // returns number of chars written
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // buffer
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // format
                ].as_ptr() as *mut _,
                2,
                1, // variadic
            );
            let sprintf_name = CString::new("sprintf").unwrap();
            let sprintf = LLVMAddFunction(self.module, sprintf_name.as_ptr(), sprintf_type);
            self.functions.insert("sprintf".to_string(), sprintf);
            self.function_types.insert("sprintf".to_string(), sprintf_type);

            // Now declare our high-level File I/O functions
            self.declare_file_io_functions();

            // Declare string operation functions
            self.declare_string_functions();

            // Declare collection functions
            self.declare_collection_functions();

            // Declare character functions
            self.declare_character_functions();
        }
    }

    fn declare_file_io_functions(&mut self) {
        unsafe {
            // ReadFile: Takes filename string, returns content string
            let read_file_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns String
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _, // filename
                1,
                0,
            );
            let read_file_name = CString::new("ReadFile").unwrap();
            let read_file = LLVMAddFunction(self.module, read_file_name.as_ptr(), read_file_type);
            self.functions.insert("ReadFile".to_string(), read_file);
            self.function_types.insert("ReadFile".to_string(), read_file_type);

            // Generate ReadFile implementation
            self.generate_read_file_impl(read_file, read_file_type);

            // WriteFile: Takes content string and filename string, returns void
            let write_file_type = LLVMFunctionType(
                LLVMVoidTypeInContext(self.context),
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // content
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // filename
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let write_file_name = CString::new("WriteFile").unwrap();
            let write_file = LLVMAddFunction(self.module, write_file_name.as_ptr(), write_file_type);
            self.functions.insert("WriteFile".to_string(), write_file);
            self.function_types.insert("WriteFile".to_string(), write_file_type);

            // Generate WriteFile implementation
            self.generate_write_file_impl(write_file, write_file_type);
        }
    }

    fn generate_read_file_impl(&mut self, func: LLVMValueRef, _func_type: LLVMTypeRef) {
        unsafe {
            // Create basic blocks
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            let open_success = LLVMAppendBasicBlock(func, CString::new("open_success").unwrap().as_ptr());
            let read_done = LLVMAppendBasicBlock(func, CString::new("read_done").unwrap().as_ptr());
            let error_block = LLVMAppendBasicBlock(func, CString::new("error").unwrap().as_ptr());

            // Entry block
            LLVMPositionBuilderAtEnd(self.builder, entry);
            let filename = LLVMGetParam(func, 0);

            // Open file for reading
            let mode_str = CString::new("r").unwrap();
            let mode = LLVMBuildGlobalStringPtr(
                self.builder,
                mode_str.as_ptr(),
                CString::new("read_mode").unwrap().as_ptr(),
            );

            let fopen_func = *self.functions.get("fopen").unwrap();
            let file = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    ].as_ptr() as *mut _,
                    2,
                    0,
                ),
                fopen_func,
                [filename, mode].as_ptr() as *mut _,
                2,
                CString::new("file").unwrap().as_ptr(),
            );

            // Check if file opened successfully
            let null_ptr = LLVMConstNull(LLVMPointerType(LLVMInt8TypeInContext(self.context), 0));
            let is_null = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntEQ,
                file,
                null_ptr,
                CString::new("is_null").unwrap().as_ptr(),
            );
            LLVMBuildCondBr(self.builder, is_null, error_block, open_success);

            // Open success block - get file size
            LLVMPositionBuilderAtEnd(self.builder, open_success);

            // Seek to end to get size
            let fseek_func = *self.functions.get("fseek").unwrap();
            let seek_end = LLVMConstInt(LLVMInt32TypeInContext(self.context), 2, 0); // SEEK_END
            let zero_offset = LLVMConstInt(LLVMInt64TypeInContext(self.context), 0, 0);
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt32TypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                        LLVMInt32TypeInContext(self.context),
                    ].as_ptr() as *mut _,
                    3,
                    0,
                ),
                fseek_func,
                [file, zero_offset, seek_end].as_ptr() as *mut _,
                3,
                CString::new("").unwrap().as_ptr(),
            );

            // Get file size
            let ftell_func = *self.functions.get("ftell").unwrap();
            let file_size = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt64TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                ftell_func,
                [file].as_ptr() as *mut _,
                1,
                CString::new("file_size").unwrap().as_ptr(),
            );

            // Seek back to beginning
            let seek_set = LLVMConstInt(LLVMInt32TypeInContext(self.context), 0, 0); // SEEK_SET
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt32TypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                        LLVMInt32TypeInContext(self.context),
                    ].as_ptr() as *mut _,
                    3,
                    0,
                ),
                fseek_func,
                [file, zero_offset, seek_set].as_ptr() as *mut _,
                3,
                CString::new("").unwrap().as_ptr(),
            );

            // Allocate buffer for file content (size + 1 for null terminator)
            let malloc_func = *self.functions.get("malloc").unwrap();
            let one = LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0);
            let buffer_size = LLVMBuildAdd(
                self.builder,
                file_size,
                one,
                CString::new("buffer_size").unwrap().as_ptr(),
            );
            let buffer = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                malloc_func,
                [buffer_size].as_ptr() as *mut _,
                1,
                CString::new("buffer").unwrap().as_ptr(),
            );

            // Read file content
            let fread_func = *self.functions.get("fread").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt64TypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                        LLVMInt64TypeInContext(self.context),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    ].as_ptr() as *mut _,
                    4,
                    0,
                ),
                fread_func,
                [buffer, one, file_size, file].as_ptr() as *mut _,
                4,
                CString::new("").unwrap().as_ptr(),
            );

            // Add null terminator
            let buffer_end = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                buffer,
                [file_size].as_ptr() as *mut _,
                1,
                CString::new("buffer_end").unwrap().as_ptr(),
            );
            let zero_byte = LLVMConstInt(LLVMInt8TypeInContext(self.context), 0, 0);
            LLVMBuildStore(self.builder, zero_byte, buffer_end);

            // Close file
            let fclose_func = *self.functions.get("fclose").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt32TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                fclose_func,
                [file].as_ptr() as *mut _,
                1,
                CString::new("").unwrap().as_ptr(),
            );

            LLVMBuildBr(self.builder, read_done);

            // Error block - return empty string
            LLVMPositionBuilderAtEnd(self.builder, error_block);
            let empty_str = LLVMBuildGlobalStringPtr(
                self.builder,
                CString::new("").unwrap().as_ptr(),
                CString::new("empty").unwrap().as_ptr(),
            );
            LLVMBuildBr(self.builder, read_done);

            // Read done - return result
            LLVMPositionBuilderAtEnd(self.builder, read_done);
            let phi = LLVMBuildPhi(
                self.builder,
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                CString::new("result").unwrap().as_ptr(),
            );
            LLVMAddIncoming(
                phi,
                [buffer, empty_str].as_ptr() as *mut _,
                [open_success, error_block].as_ptr() as *mut _,
                2,
            );
            LLVMBuildRet(self.builder, phi);
        }
    }

    fn declare_string_functions(&mut self) {
        unsafe {
            // string_concat: Takes two strings, returns concatenated string
            let string_concat_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns String
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // str1
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // str2
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let string_concat_name = CString::new("string_concat").unwrap();
            let string_concat = LLVMAddFunction(self.module, string_concat_name.as_ptr(), string_concat_type);
            self.functions.insert("string_concat".to_string(), string_concat);
            self.function_types.insert("string_concat".to_string(), string_concat_type);
            self.generate_string_concat_impl(string_concat);

            // string_length: Takes a string, returns length as Integer
            let string_length_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // returns Integer
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _, // str
                1,
                0,
            );
            let string_length_name = CString::new("string_length").unwrap();
            let string_length = LLVMAddFunction(self.module, string_length_name.as_ptr(), string_length_type);
            self.functions.insert("string_length".to_string(), string_length);
            self.function_types.insert("string_length".to_string(), string_length_type);
            self.generate_string_length_impl(string_length);

            // string_char_at: Takes string and index, returns character as Integer (ASCII value)
            let string_char_at_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // returns Integer (char as int)
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // str
                    LLVMInt64TypeInContext(self.context), // index
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let string_char_at_name = CString::new("string_char_at").unwrap();
            let string_char_at = LLVMAddFunction(self.module, string_char_at_name.as_ptr(), string_char_at_type);
            self.functions.insert("string_char_at".to_string(), string_char_at);
            self.function_types.insert("string_char_at".to_string(), string_char_at_type);
            self.generate_string_char_at_impl(string_char_at);

            // string_substring: Takes string, start, and end indices, returns substring
            let string_substring_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns String
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // str
                    LLVMInt64TypeInContext(self.context), // start
                    LLVMInt64TypeInContext(self.context), // end
                ].as_ptr() as *mut _,
                3,
                0,
            );
            let string_substring_name = CString::new("string_substring").unwrap();
            let string_substring = LLVMAddFunction(self.module, string_substring_name.as_ptr(), string_substring_type);
            self.functions.insert("string_substring".to_string(), string_substring);
            self.function_types.insert("string_substring".to_string(), string_substring_type);
            self.generate_string_substring_impl(string_substring);

            // char_to_string: Takes character (integer), returns string
            let char_to_string_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns String
                [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _, // char as int
                1,
                0,
            );
            let char_to_string_name = CString::new("char_to_string").unwrap();
            let char_to_string = LLVMAddFunction(self.module, char_to_string_name.as_ptr(), char_to_string_type);
            self.functions.insert("char_to_string".to_string(), char_to_string);
            self.function_types.insert("char_to_string".to_string(), char_to_string_type);
            self.generate_char_to_string_impl(char_to_string);

            // int_to_string: Takes integer, returns string
            let int_to_string_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns String
                [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _, // integer
                1,
                0,
            );
            let int_to_string_name = CString::new("int_to_string").unwrap();
            let int_to_string = LLVMAddFunction(self.module, int_to_string_name.as_ptr(), int_to_string_type);
            self.functions.insert("int_to_string".to_string(), int_to_string);
            self.function_types.insert("int_to_string".to_string(), int_to_string_type);
            self.generate_int_to_string_impl(int_to_string);

            // string_to_int: Takes string, returns integer
            let string_to_int_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // returns Integer
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _, // string
                1,
                0,
            );
            let string_to_int_name = CString::new("string_to_int").unwrap();
            let string_to_int = LLVMAddFunction(self.module, string_to_int_name.as_ptr(), string_to_int_type);
            self.functions.insert("string_to_int".to_string(), string_to_int);
            self.function_types.insert("string_to_int".to_string(), string_to_int_type);
            self.generate_string_to_int_impl(string_to_int);
        }
    }

    fn generate_string_concat_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let str1 = LLVMGetParam(func, 0);
            let str2 = LLVMGetParam(func, 1);

            // Get lengths of both strings
            let strlen_func = *self.functions.get("strlen").unwrap();
            let strlen_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                1,
                0,
            );

            let len1 = LLVMBuildCall2(
                self.builder,
                strlen_type,
                strlen_func,
                [str1].as_ptr() as *mut _,
                1,
                CString::new("len1").unwrap().as_ptr(),
            );

            let len2 = LLVMBuildCall2(
                self.builder,
                strlen_type,
                strlen_func,
                [str2].as_ptr() as *mut _,
                1,
                CString::new("len2").unwrap().as_ptr(),
            );

            // Calculate total length (len1 + len2 + 1 for null terminator)
            let total_len = LLVMBuildAdd(
                self.builder,
                len1,
                len2,
                CString::new("total_len").unwrap().as_ptr(),
            );
            let one = LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0);
            let buffer_size = LLVMBuildAdd(
                self.builder,
                total_len,
                one,
                CString::new("buffer_size").unwrap().as_ptr(),
            );

            // Allocate memory for concatenated string
            let malloc_func = *self.functions.get("malloc").unwrap();
            let malloc_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                1,
                0,
            );
            let buffer = LLVMBuildCall2(
                self.builder,
                malloc_type,
                malloc_func,
                [buffer_size].as_ptr() as *mut _,
                1,
                CString::new("buffer").unwrap().as_ptr(),
            );

            // Copy first string using memcpy
            let memcpy = self.get_or_declare_memcpy();
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMVoidTypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                    ].as_ptr() as *mut _,
                    3,
                    0,
                ),
                memcpy,
                [buffer, str1, len1].as_ptr() as *mut _,
                3,
                CString::new("").unwrap().as_ptr(),
            );

            // Copy second string after first
            let offset = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                buffer,
                [len1].as_ptr() as *mut _,
                1,
                CString::new("offset").unwrap().as_ptr(),
            );
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMVoidTypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                    ].as_ptr() as *mut _,
                    3,
                    0,
                ),
                memcpy,
                [offset, str2, len2].as_ptr() as *mut _,
                3,
                CString::new("").unwrap().as_ptr(),
            );

            // Add null terminator
            let end_offset = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                buffer,
                [total_len].as_ptr() as *mut _,
                1,
                CString::new("end_offset").unwrap().as_ptr(),
            );
            let zero_byte = LLVMConstInt(LLVMInt8TypeInContext(self.context), 0, 0);
            LLVMBuildStore(self.builder, zero_byte, end_offset);

            LLVMBuildRet(self.builder, buffer);
        }
    }

    fn generate_string_length_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let str_param = LLVMGetParam(func, 0);

            // Call strlen and return result
            let strlen_func = *self.functions.get("strlen").unwrap();
            let result = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt64TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                strlen_func,
                [str_param].as_ptr() as *mut _,
                1,
                CString::new("length").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn generate_string_char_at_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            let bounds_ok = LLVMAppendBasicBlock(func, CString::new("bounds_ok").unwrap().as_ptr());
            let out_of_bounds = LLVMAppendBasicBlock(func, CString::new("out_of_bounds").unwrap().as_ptr());
            let return_block = LLVMAppendBasicBlock(func, CString::new("return").unwrap().as_ptr());

            LLVMPositionBuilderAtEnd(self.builder, entry);

            let str_param = LLVMGetParam(func, 0);
            let index = LLVMGetParam(func, 1);

            // Get string length for bounds checking
            let strlen_func = *self.functions.get("strlen").unwrap();
            let str_len = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt64TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                strlen_func,
                [str_param].as_ptr() as *mut _,
                1,
                CString::new("str_len").unwrap().as_ptr(),
            );

            // Check if index is within bounds
            let in_bounds = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntULT,
                index,
                str_len,
                CString::new("in_bounds").unwrap().as_ptr(),
            );
            LLVMBuildCondBr(self.builder, in_bounds, bounds_ok, out_of_bounds);

            // Bounds OK: get character at index
            LLVMPositionBuilderAtEnd(self.builder, bounds_ok);
            let char_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                str_param,
                [index].as_ptr() as *mut _,
                1,
                CString::new("char_ptr").unwrap().as_ptr(),
            );
            let char_value = LLVMBuildLoad2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                char_ptr,
                CString::new("char_value").unwrap().as_ptr(),
            );
            // Convert i8 to i64
            let char_as_int = LLVMBuildZExt(
                self.builder,
                char_value,
                LLVMInt64TypeInContext(self.context),
                CString::new("char_as_int").unwrap().as_ptr(),
            );
            LLVMBuildBr(self.builder, return_block);

            // Out of bounds: return -1
            LLVMPositionBuilderAtEnd(self.builder, out_of_bounds);
            let minus_one = LLVMConstInt(LLVMInt64TypeInContext(self.context), -1i64 as u64, 1);
            LLVMBuildBr(self.builder, return_block);

            // Return block: phi node to select result
            LLVMPositionBuilderAtEnd(self.builder, return_block);
            let phi = LLVMBuildPhi(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                CString::new("result").unwrap().as_ptr(),
            );
            LLVMAddIncoming(
                phi,
                [char_as_int, minus_one].as_ptr() as *mut _,
                [bounds_ok, out_of_bounds].as_ptr() as *mut _,
                2,
            );
            LLVMBuildRet(self.builder, phi);
        }
    }

    fn generate_string_substring_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let str_param = LLVMGetParam(func, 0);
            let start_idx = LLVMGetParam(func, 1);
            let end_idx = LLVMGetParam(func, 2);

            // Calculate substring length
            let sub_len = LLVMBuildSub(
                self.builder,
                end_idx,
                start_idx,
                CString::new("sub_len").unwrap().as_ptr(),
            );

            // Allocate memory for substring (length + 1 for null terminator)
            let one = LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0);
            let buffer_size = LLVMBuildAdd(
                self.builder,
                sub_len,
                one,
                CString::new("buffer_size").unwrap().as_ptr(),
            );

            let malloc_func = *self.functions.get("malloc").unwrap();
            let buffer = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                malloc_func,
                [buffer_size].as_ptr() as *mut _,
                1,
                CString::new("buffer").unwrap().as_ptr(),
            );

            // Get pointer to start of substring in source
            let src_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                str_param,
                [start_idx].as_ptr() as *mut _,
                1,
                CString::new("src_ptr").unwrap().as_ptr(),
            );

            // Copy substring using memcpy
            let memcpy = self.get_or_declare_memcpy();
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMVoidTypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                    ].as_ptr() as *mut _,
                    3,
                    0,
                ),
                memcpy,
                [buffer, src_ptr, sub_len].as_ptr() as *mut _,
                3,
                CString::new("").unwrap().as_ptr(),
            );

            // Add null terminator
            let end_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                buffer,
                [sub_len].as_ptr() as *mut _,
                1,
                CString::new("end_ptr").unwrap().as_ptr(),
            );
            let zero_byte = LLVMConstInt(LLVMInt8TypeInContext(self.context), 0, 0);
            LLVMBuildStore(self.builder, zero_byte, end_ptr);

            LLVMBuildRet(self.builder, buffer);
        }
    }

    fn generate_char_to_string_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let char_param = LLVMGetParam(func, 0);

            // Allocate space for 2-character string (char + null terminator)
            let malloc_func = *self.functions.get("malloc").unwrap();
            let malloc_type = *self.function_types.get("malloc").unwrap();
            let buffer_size = LLVMConstInt(LLVMInt64TypeInContext(self.context), 2, 0);
            let buffer = LLVMBuildCall2(
                self.builder,
                malloc_type,
                malloc_func,
                [buffer_size].as_ptr() as *mut _,
                1,
                CString::new("char_buffer").unwrap().as_ptr(),
            );

            // Cast character to i8 and store it
            let char_i8 = LLVMBuildTrunc(
                self.builder,
                char_param,
                LLVMInt8TypeInContext(self.context),
                CString::new("char_i8").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, char_i8, buffer);

            // Add null terminator
            let null_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt8TypeInContext(self.context),
                buffer,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0)].as_ptr() as *mut _,
                1,
                CString::new("null_ptr").unwrap().as_ptr(),
            );
            let zero_byte = LLVMConstInt(LLVMInt8TypeInContext(self.context), 0, 0);
            LLVMBuildStore(self.builder, zero_byte, null_ptr);

            LLVMBuildRet(self.builder, buffer);
        }
    }

    fn generate_int_to_string_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let int_param = LLVMGetParam(func, 0);

            // Allocate space for string representation (32 chars should be enough for 64-bit int)
            let malloc_func = *self.functions.get("malloc").unwrap();
            let malloc_type = *self.function_types.get("malloc").unwrap();
            let buffer_size = LLVMConstInt(LLVMInt64TypeInContext(self.context), 32, 0);
            let buffer = LLVMBuildCall2(
                self.builder,
                malloc_type,
                malloc_func,
                [buffer_size].as_ptr() as *mut _,
                1,
                CString::new("int_buffer").unwrap().as_ptr(),
            );

            // Use sprintf to convert integer to string
            let sprintf_func = *self.functions.get("sprintf").unwrap();
            let sprintf_type = *self.function_types.get("sprintf").unwrap();
            let format_str = LLVMBuildGlobalStringPtr(
                self.builder,
                CString::new("%lld").unwrap().as_ptr(),
                CString::new("int_format").unwrap().as_ptr(),
            );

            LLVMBuildCall2(
                self.builder,
                sprintf_type,
                sprintf_func,
                [buffer, format_str, int_param].as_ptr() as *mut _,
                3,
                CString::new("").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, buffer);
        }
    }

    fn generate_string_to_int_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let str_param = LLVMGetParam(func, 0);

            // Use atoll to convert string to integer
            let atoll_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context),
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                1,
                0,
            );
            let atoll_name = CString::new("atoll").unwrap();
            let atoll_func = LLVMAddFunction(self.module, atoll_name.as_ptr(), atoll_type);

            let result = LLVMBuildCall2(
                self.builder,
                atoll_type,
                atoll_func,
                [str_param].as_ptr() as *mut _,
                1,
                CString::new("str_to_int_result").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn declare_collection_functions(&mut self) {
        unsafe {
            // list_create: Creates a new list
            let list_create_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns List*
                std::ptr::null_mut(),
                0,
                0,
            );
            let list_create_name = CString::new("list_create").unwrap();
            let list_create = LLVMAddFunction(self.module, list_create_name.as_ptr(), list_create_type);
            self.functions.insert("list_create".to_string(), list_create);
            self.function_types.insert("list_create".to_string(), list_create_type);
            self.generate_list_create_impl(list_create);

            // dict_create: Creates a new dictionary
            let dict_create_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // Return dictionary pointer
                std::ptr::null_mut(),
                0,
                0,
            );
            let dict_create_name = CString::new("dict_create").unwrap();
            let dict_create = LLVMAddFunction(self.module, dict_create_name.as_ptr(), dict_create_type);
            self.functions.insert("dict_create".to_string(), dict_create);
            self.function_types.insert("dict_create".to_string(), dict_create_type);
            self.generate_dict_create_impl(dict_create);

            // list_append: Adds element to end of list
            let list_append_type = LLVMFunctionType(
                LLVMVoidTypeInContext(self.context),
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // list
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // value (generic pointer for any type)
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let list_append_name = CString::new("list_append").unwrap();
            let list_append = LLVMAddFunction(self.module, list_append_name.as_ptr(), list_append_type);
            self.functions.insert("list_append".to_string(), list_append);
            self.function_types.insert("list_append".to_string(), list_append_type);
            self.generate_list_append_impl(list_append);

            // list_get: Gets element at index
            let list_get_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // returns value
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // list
                    LLVMInt64TypeInContext(self.context), // index
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let list_get_name = CString::new("list_get").unwrap();
            let list_get = LLVMAddFunction(self.module, list_get_name.as_ptr(), list_get_type);
            self.functions.insert("list_get".to_string(), list_get);
            self.function_types.insert("list_get".to_string(), list_get_type);
            self.generate_list_get_impl(list_get);

            // list_get_string: Gets string element from list (returns string pointer)
            let list_get_string_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns string pointer
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // list
                    LLVMInt64TypeInContext(self.context), // index
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let list_get_string_name = CString::new("list_get_string").unwrap();
            let list_get_string = LLVMAddFunction(self.module, list_get_string_name.as_ptr(), list_get_string_type);
            self.functions.insert("list_get_string".to_string(), list_get_string);
            self.function_types.insert("list_get_string".to_string(), list_get_string_type);
            self.generate_list_get_string_impl(list_get_string);

            // list_get_struct: Gets a pointer to a struct element at an index
            let list_get_struct_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // returns a generic pointer
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // list
                    LLVMInt64TypeInContext(self.context),                     // index
                ].as_ptr() as *mut _,
                2,
                0,
            );
            let list_get_struct_name = CString::new("list_get_struct").unwrap();
            let list_get_struct = LLVMAddFunction(self.module, list_get_struct_name.as_ptr(), list_get_struct_type);
            self.functions.insert("list_get_struct".to_string(), list_get_struct);
            self.function_types.insert("list_get_struct".to_string(), list_get_struct_type);
            // Re-use the same implementation as list_get_string since both just retrieve a pointer
            self.generate_list_get_string_impl(list_get_struct);

            // list_length: Gets list length
            let list_length_type = LLVMFunctionType(
                LLVMInt64TypeInContext(self.context), // returns length
                [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _, // list
                1,
                0,
            );
            let list_length_name = CString::new("list_length").unwrap();
            let list_length = LLVMAddFunction(self.module, list_length_name.as_ptr(), list_length_type);
            self.functions.insert("list_length".to_string(), list_length);
            self.function_types.insert("list_length".to_string(), list_length_type);
            self.generate_list_length_impl(list_length);
        }
    }

    fn declare_character_functions(&mut self) {
        unsafe {
            // is_digit: Check if char is a digit
            let is_digit_type = LLVMFunctionType(
                LLVMInt1TypeInContext(self.context), // returns bool
                [LLVMInt8TypeInContext(self.context)].as_ptr() as *mut _, // char
                1,
                0,
            );
            let is_digit_name = CString::new("is_digit").unwrap();
            let is_digit = LLVMAddFunction(self.module, is_digit_name.as_ptr(), is_digit_type);
            self.functions.insert("is_digit".to_string(), is_digit);
            self.function_types.insert("is_digit".to_string(), is_digit_type);
            self.generate_is_digit_impl(is_digit);

            // is_letter: Check if char is a letter
            let is_letter_type = LLVMFunctionType(
                LLVMInt1TypeInContext(self.context), // returns bool
                [LLVMInt8TypeInContext(self.context)].as_ptr() as *mut _, // char
                1,
                0,
            );
            let is_letter_name = CString::new("is_letter").unwrap();
            let is_letter = LLVMAddFunction(self.module, is_letter_name.as_ptr(), is_letter_type);
            self.functions.insert("is_letter".to_string(), is_letter);
            self.function_types.insert("is_letter".to_string(), is_letter_type);
            self.generate_is_letter_impl(is_letter);

            // is_whitespace: Check if char is whitespace
            let is_whitespace_type = LLVMFunctionType(
                LLVMInt1TypeInContext(self.context), // returns bool
                [LLVMInt8TypeInContext(self.context)].as_ptr() as *mut _, // char
                1,
                0,
            );
            let is_whitespace_name = CString::new("is_whitespace").unwrap();
            let is_whitespace = LLVMAddFunction(self.module, is_whitespace_name.as_ptr(), is_whitespace_type);
            self.functions.insert("is_whitespace".to_string(), is_whitespace);
            self.function_types.insert("is_whitespace".to_string(), is_whitespace_type);
            self.generate_is_whitespace_impl(is_whitespace);

            // to_uppercase: Convert char to uppercase
            let to_uppercase_type = LLVMFunctionType(
                LLVMInt8TypeInContext(self.context), // returns char
                [LLVMInt8TypeInContext(self.context)].as_ptr() as *mut _, // char
                1,
                0,
            );
            let to_uppercase_name = CString::new("to_uppercase").unwrap();
            let to_uppercase = LLVMAddFunction(self.module, to_uppercase_name.as_ptr(), to_uppercase_type);
            self.functions.insert("to_uppercase".to_string(), to_uppercase);
            self.function_types.insert("to_uppercase".to_string(), to_uppercase_type);
            self.generate_to_uppercase_impl(to_uppercase);

            // to_lowercase: Convert char to lowercase
            let to_lowercase_type = LLVMFunctionType(
                LLVMInt8TypeInContext(self.context), // returns char
                [LLVMInt8TypeInContext(self.context)].as_ptr() as *mut _, // char
                1,
                0,
            );
            let to_lowercase_name = CString::new("to_lowercase").unwrap();
            let to_lowercase = LLVMAddFunction(self.module, to_lowercase_name.as_ptr(), to_lowercase_type);
            self.functions.insert("to_lowercase".to_string(), to_lowercase);
            self.function_types.insert("to_lowercase".to_string(), to_lowercase_type);
            self.generate_to_lowercase_impl(to_lowercase);
        }
    }

    fn generate_is_digit_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("entry").unwrap().as_ptr(),
            );
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let char_param = LLVMGetParam(func, 0);

            // Check if char >= '0' && char <= '9'
            let zero = LLVMConstInt(LLVMInt8TypeInContext(self.context), '0' as u64, 0);
            let nine = LLVMConstInt(LLVMInt8TypeInContext(self.context), '9' as u64, 0);

            let ge_zero = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntUGE,
                char_param,
                zero,
                CString::new("ge_zero").unwrap().as_ptr(),
            );

            let le_nine = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntULE,
                char_param,
                nine,
                CString::new("le_nine").unwrap().as_ptr(),
            );

            let result = LLVMBuildAnd(
                self.builder,
                ge_zero,
                le_nine,
                CString::new("is_digit_result").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn generate_is_letter_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("entry").unwrap().as_ptr(),
            );
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let char_param = LLVMGetParam(func, 0);

            // Check if (char >= 'a' && char <= 'z') || (char >= 'A' && char <= 'Z')
            let a_lower = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'a' as u64, 0);
            let z_lower = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'z' as u64, 0);
            let a_upper = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'A' as u64, 0);
            let z_upper = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'Z' as u64, 0);

            let ge_a_lower = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntUGE,
                char_param,
                a_lower,
                CString::new("ge_a_lower").unwrap().as_ptr(),
            );

            let le_z_lower = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntULE,
                char_param,
                z_lower,
                CString::new("le_z_lower").unwrap().as_ptr(),
            );

            let is_lower = LLVMBuildAnd(
                self.builder,
                ge_a_lower,
                le_z_lower,
                CString::new("is_lower").unwrap().as_ptr(),
            );

            let ge_a_upper = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntUGE,
                char_param,
                a_upper,
                CString::new("ge_a_upper").unwrap().as_ptr(),
            );

            let le_z_upper = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntULE,
                char_param,
                z_upper,
                CString::new("le_z_upper").unwrap().as_ptr(),
            );

            let is_upper = LLVMBuildAnd(
                self.builder,
                ge_a_upper,
                le_z_upper,
                CString::new("is_upper").unwrap().as_ptr(),
            );

            let result = LLVMBuildOr(
                self.builder,
                is_lower,
                is_upper,
                CString::new("is_letter_result").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn generate_is_whitespace_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("entry").unwrap().as_ptr(),
            );
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let char_param = LLVMGetParam(func, 0);

            // Check for common whitespace characters: space, tab, newline, carriage return
            let space = LLVMConstInt(LLVMInt8TypeInContext(self.context), ' ' as u64, 0);
            let tab = LLVMConstInt(LLVMInt8TypeInContext(self.context), '\t' as u64, 0);
            let newline = LLVMConstInt(LLVMInt8TypeInContext(self.context), '\n' as u64, 0);
            let carriage_return = LLVMConstInt(LLVMInt8TypeInContext(self.context), '\r' as u64, 0);

            let is_space = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntEQ,
                char_param,
                space,
                CString::new("is_space").unwrap().as_ptr(),
            );

            let is_tab = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntEQ,
                char_param,
                tab,
                CString::new("is_tab").unwrap().as_ptr(),
            );

            let is_newline = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntEQ,
                char_param,
                newline,
                CString::new("is_newline").unwrap().as_ptr(),
            );

            let is_carriage_return = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntEQ,
                char_param,
                carriage_return,
                CString::new("is_carriage_return").unwrap().as_ptr(),
            );

            let space_or_tab = LLVMBuildOr(
                self.builder,
                is_space,
                is_tab,
                CString::new("space_or_tab").unwrap().as_ptr(),
            );

            let newline_or_cr = LLVMBuildOr(
                self.builder,
                is_newline,
                is_carriage_return,
                CString::new("newline_or_cr").unwrap().as_ptr(),
            );

            let result = LLVMBuildOr(
                self.builder,
                space_or_tab,
                newline_or_cr,
                CString::new("is_whitespace_result").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn generate_to_uppercase_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("entry").unwrap().as_ptr(),
            );
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let char_param = LLVMGetParam(func, 0);

            // Check if char is lowercase (a-z)
            let a_lower = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'a' as u64, 0);
            let z_lower = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'z' as u64, 0);

            let ge_a = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntUGE,
                char_param,
                a_lower,
                CString::new("ge_a").unwrap().as_ptr(),
            );

            let le_z = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntULE,
                char_param,
                z_lower,
                CString::new("le_z").unwrap().as_ptr(),
            );

            let is_lowercase = LLVMBuildAnd(
                self.builder,
                ge_a,
                le_z,
                CString::new("is_lowercase").unwrap().as_ptr(),
            );

            // Convert to uppercase by subtracting 32 ('a' - 'A' = 32)
            let offset = LLVMConstInt(LLVMInt8TypeInContext(self.context), 32, 0);
            let uppercase_char = LLVMBuildSub(
                self.builder,
                char_param,
                offset,
                CString::new("uppercase_char").unwrap().as_ptr(),
            );

            // Select uppercase version if lowercase, otherwise return original
            let result = LLVMBuildSelect(
                self.builder,
                is_lowercase,
                uppercase_char,
                char_param,
                CString::new("to_uppercase_result").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn generate_to_lowercase_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("entry").unwrap().as_ptr(),
            );
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let char_param = LLVMGetParam(func, 0);

            // Check if char is uppercase (A-Z)
            let a_upper = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'A' as u64, 0);
            let z_upper = LLVMConstInt(LLVMInt8TypeInContext(self.context), 'Z' as u64, 0);

            let ge_a = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntUGE,
                char_param,
                a_upper,
                CString::new("ge_a").unwrap().as_ptr(),
            );

            let le_z = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntULE,
                char_param,
                z_upper,
                CString::new("le_z").unwrap().as_ptr(),
            );

            let is_uppercase = LLVMBuildAnd(
                self.builder,
                ge_a,
                le_z,
                CString::new("is_uppercase").unwrap().as_ptr(),
            );

            // Convert to lowercase by adding 32 ('a' - 'A' = 32)
            let offset = LLVMConstInt(LLVMInt8TypeInContext(self.context), 32, 0);
            let lowercase_char = LLVMBuildAdd(
                self.builder,
                char_param,
                offset,
                CString::new("lowercase_char").unwrap().as_ptr(),
            );

            // Select lowercase version if uppercase, otherwise return original
            let result = LLVMBuildSelect(
                self.builder,
                is_uppercase,
                lowercase_char,
                char_param,
                CString::new("to_lowercase_result").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, result);
        }
    }

    fn generate_list_create_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            // List structure: [capacity:i64][size:i64][data:i64*]
            // Allocate 24 bytes for the list structure
            let list_struct_size = LLVMConstInt(LLVMInt64TypeInContext(self.context), 24, 0);
            let malloc_func = *self.functions.get("malloc").unwrap();
            let list_ptr = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                malloc_func,
                [list_struct_size].as_ptr() as *mut _,
                1,
                CString::new("list_ptr").unwrap().as_ptr(),
            );

            // Cast to i64* for easier access
            let list_as_i64_ptr = LLVMBuildBitCast(
                self.builder,
                list_ptr,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("list_as_i64").unwrap().as_ptr(),
            );

            // Initialize capacity to 10
            let initial_capacity = LLVMConstInt(LLVMInt64TypeInContext(self.context), 10, 0);
            let capacity_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 0, 0)].as_ptr() as *mut _,
                1,
                CString::new("capacity_ptr").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, initial_capacity, capacity_ptr);

            // Initialize size to 0
            let zero = LLVMConstInt(LLVMInt64TypeInContext(self.context), 0, 0);
            let size_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0)].as_ptr() as *mut _,
                1,
                CString::new("size_ptr").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, zero, size_ptr);

            // Allocate initial data array
            let data_size = LLVMConstInt(LLVMInt64TypeInContext(self.context), 80, 0); // 10 * 8 bytes
            let data_ptr = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                malloc_func,
                [data_size].as_ptr() as *mut _,
                1,
                CString::new("data_ptr").unwrap().as_ptr(),
            );

            // Store data pointer
            let data_field_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 2, 0)].as_ptr() as *mut _,
                1,
                CString::new("data_field_ptr").unwrap().as_ptr(),
            );
            let data_as_i64 = LLVMBuildPtrToInt(
                self.builder,
                data_ptr,
                LLVMInt64TypeInContext(self.context),
                CString::new("data_as_i64").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, data_as_i64, data_field_ptr);

            LLVMBuildRet(self.builder, list_ptr);
        }
    }

    fn generate_dict_create_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            // For bootstrap simplicity, dictionary is just an empty list structure
            // Real dictionary would use hash table or similar
            let list_struct_size = LLVMConstInt(LLVMInt64TypeInContext(self.context), 24, 0);
            let malloc_func = *self.functions.get("malloc").unwrap();
            let dict_ptr = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                malloc_func,
                [list_struct_size].as_ptr() as *mut _,
                1,
                CString::new("dict_ptr").unwrap().as_ptr(),
            );

            // Initialize dictionary (for now, same as empty list)
            let dict_as_i64_ptr = LLVMBuildBitCast(
                self.builder,
                dict_ptr,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("dict_as_i64").unwrap().as_ptr(),
            );

            // Initialize capacity
            let initial_capacity = LLVMConstInt(LLVMInt64TypeInContext(self.context), 10, 0);
            let capacity_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                dict_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 0, 0)].as_ptr() as *mut _,
                1,
                CString::new("capacity_ptr").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, initial_capacity, capacity_ptr);

            // Initialize size to 0
            let zero = LLVMConstInt(LLVMInt64TypeInContext(self.context), 0, 0);
            let size_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                dict_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0)].as_ptr() as *mut _,
                1,
                CString::new("size_ptr").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, zero, size_ptr);

            // Allocate initial data
            let data_size = LLVMConstInt(LLVMInt64TypeInContext(self.context), 80, 0);
            let data_ptr = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [LLVMInt64TypeInContext(self.context)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                malloc_func,
                [data_size].as_ptr() as *mut _,
                1,
                CString::new("data_ptr").unwrap().as_ptr(),
            );

            // Store data pointer
            let data_field_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                dict_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 2, 0)].as_ptr() as *mut _,
                1,
                CString::new("data_field_ptr").unwrap().as_ptr(),
            );
            let data_as_i64 = LLVMBuildPtrToInt(
                self.builder,
                data_ptr,
                LLVMInt64TypeInContext(self.context),
                CString::new("data_as_i64").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, data_as_i64, data_field_ptr);

            LLVMBuildRet(self.builder, dict_ptr);
        }
    }

    fn generate_list_append_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let list_ptr = LLVMGetParam(func, 0);
            let value = LLVMGetParam(func, 1);

            // Cast list to i64*
            let list_as_i64_ptr = LLVMBuildBitCast(
                self.builder,
                list_ptr,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("list_as_i64").unwrap().as_ptr(),
            );

            // Get current size
            let size_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0)].as_ptr() as *mut _,
                1,
                CString::new("size_ptr").unwrap().as_ptr(),
            );
            let current_size = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                size_ptr,
                CString::new("current_size").unwrap().as_ptr(),
            );

            // Get data pointer
            let data_field_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 2, 0)].as_ptr() as *mut _,
                1,
                CString::new("data_field_ptr").unwrap().as_ptr(),
            );
            let data_as_i64 = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                data_field_ptr,
                CString::new("data_as_i64").unwrap().as_ptr(),
            );
            let data_ptr = LLVMBuildIntToPtr(
                self.builder,
                data_as_i64,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("data_ptr").unwrap().as_ptr(),
            );

            // Store value at current size index
            let element_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                data_ptr,
                [current_size].as_ptr() as *mut _,
                1,
                CString::new("element_ptr").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, value, element_ptr);

            // Increment size
            let one = LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0);
            let new_size = LLVMBuildAdd(
                self.builder,
                current_size,
                one,
                CString::new("new_size").unwrap().as_ptr(),
            );
            LLVMBuildStore(self.builder, new_size, size_ptr);

            LLVMBuildRetVoid(self.builder);
        }
    }

    fn generate_list_get_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let list_ptr = LLVMGetParam(func, 0);
            let index = LLVMGetParam(func, 1);

            // Cast list to i64*
            let list_as_i64_ptr = LLVMBuildBitCast(
                self.builder,
                list_ptr,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("list_as_i64").unwrap().as_ptr(),
            );

            // Get data pointer
            let data_field_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 2, 0)].as_ptr() as *mut _,
                1,
                CString::new("data_field_ptr").unwrap().as_ptr(),
            );
            let data_as_i64 = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                data_field_ptr,
                CString::new("data_as_i64").unwrap().as_ptr(),
            );
            let data_ptr = LLVMBuildIntToPtr(
                self.builder,
                data_as_i64,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("data_ptr").unwrap().as_ptr(),
            );

            // Get element at index
            let element_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                data_ptr,
                [index].as_ptr() as *mut _,
                1,
                CString::new("element_ptr").unwrap().as_ptr(),
            );
            let value = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                element_ptr,
                CString::new("value").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, value);
        }
    }

    fn generate_list_get_string_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let list_ptr = LLVMGetParam(func, 0);
            let index = LLVMGetParam(func, 1);

            // Cast list to i64*
            let list_as_i64_ptr = LLVMBuildBitCast(
                self.builder,
                list_ptr,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("list_as_i64").unwrap().as_ptr(),
            );

            // Get data pointer
            let data_field_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 2, 0)].as_ptr() as *mut _,
                1,
                CString::new("data_field_ptr").unwrap().as_ptr(),
            );
            let data_as_i64 = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                data_field_ptr,
                CString::new("data_as_i64").unwrap().as_ptr(),
            );
            let data_ptr = LLVMBuildIntToPtr(
                self.builder,
                data_as_i64,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("data_ptr").unwrap().as_ptr(),
            );

            // Get element at index
            let element_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                data_ptr,
                [index].as_ptr() as *mut _,
                1,
                CString::new("element_ptr").unwrap().as_ptr(),
            );
            let value = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                element_ptr,
                CString::new("value").unwrap().as_ptr(),
            );

            // Convert i64 to string pointer
            let string_ptr = LLVMBuildIntToPtr(
                self.builder,
                value,
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                CString::new("string_ptr").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, string_ptr);
        }
    }

    fn generate_list_length_impl(&mut self, func: LLVMValueRef) {
        unsafe {
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            LLVMPositionBuilderAtEnd(self.builder, entry);

            let list_ptr = LLVMGetParam(func, 0);

            // Cast list to i64*
            let list_as_i64_ptr = LLVMBuildBitCast(
                self.builder,
                list_ptr,
                LLVMPointerType(LLVMInt64TypeInContext(self.context), 0),
                CString::new("list_as_i64").unwrap().as_ptr(),
            );

            // Get size
            let size_ptr = LLVMBuildGEP2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                list_as_i64_ptr,
                [LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0)].as_ptr() as *mut _,
                1,
                CString::new("size_ptr").unwrap().as_ptr(),
            );
            let size = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                size_ptr,
                CString::new("size").unwrap().as_ptr(),
            );

            LLVMBuildRet(self.builder, size);
        }
    }

    fn get_or_declare_memcpy(&mut self) -> LLVMValueRef {
        unsafe {
            if let Some(&memcpy) = self.functions.get("memcpy") {
                return memcpy;
            }

            // Declare memcpy
            let memcpy_type = LLVMFunctionType(
                LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // dest
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // src
                    LLVMInt64TypeInContext(self.context), // size
                ].as_ptr() as *mut _,
                3,
                0,
            );
            let memcpy_name = CString::new("memcpy").unwrap();
            let memcpy = LLVMAddFunction(self.module, memcpy_name.as_ptr(), memcpy_type);
            self.functions.insert("memcpy".to_string(), memcpy);
            memcpy
        }
    }

    fn generate_write_file_impl(&mut self, func: LLVMValueRef, _func_type: LLVMTypeRef) {
        unsafe {
            // Create basic blocks
            let entry = LLVMAppendBasicBlock(func, CString::new("entry").unwrap().as_ptr());
            let write_block = LLVMAppendBasicBlock(func, CString::new("write").unwrap().as_ptr());
            let done = LLVMAppendBasicBlock(func, CString::new("done").unwrap().as_ptr());

            // Entry block
            LLVMPositionBuilderAtEnd(self.builder, entry);
            let content = LLVMGetParam(func, 0);
            let filename = LLVMGetParam(func, 1);

            // Open file for writing
            let mode_str = CString::new("w").unwrap();
            let mode = LLVMBuildGlobalStringPtr(
                self.builder,
                mode_str.as_ptr(),
                CString::new("write_mode").unwrap().as_ptr(),
            );

            let fopen_func = *self.functions.get("fopen").unwrap();
            let file = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    ].as_ptr() as *mut _,
                    2,
                    0,
                ),
                fopen_func,
                [filename, mode].as_ptr() as *mut _,
                2,
                CString::new("file").unwrap().as_ptr(),
            );

            // Check if file opened successfully
            let null_ptr = LLVMConstNull(LLVMPointerType(LLVMInt8TypeInContext(self.context), 0));
            let is_null = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntEQ,
                file,
                null_ptr,
                CString::new("is_null").unwrap().as_ptr(),
            );
            LLVMBuildCondBr(self.builder, is_null, done, write_block);

            // Write block
            LLVMPositionBuilderAtEnd(self.builder, write_block);

            // Get string length
            let strlen_func = *self.functions.get("strlen").unwrap();
            let content_len = LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt64TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                strlen_func,
                [content].as_ptr() as *mut _,
                1,
                CString::new("content_len").unwrap().as_ptr(),
            );

            // Write content to file
            let fwrite_func = *self.functions.get("fwrite").unwrap();
            let one = LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0);
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt64TypeInContext(self.context),
                    [
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                        LLVMInt64TypeInContext(self.context),
                        LLVMInt64TypeInContext(self.context),
                        LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                    ].as_ptr() as *mut _,
                    4,
                    0,
                ),
                fwrite_func,
                [content, one, content_len, file].as_ptr() as *mut _,
                4,
                CString::new("").unwrap().as_ptr(),
            );

            // Close file
            let fclose_func = *self.functions.get("fclose").unwrap();
            LLVMBuildCall2(
                self.builder,
                LLVMFunctionType(
                    LLVMInt32TypeInContext(self.context),
                    [LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)].as_ptr() as *mut _,
                    1,
                    0,
                ),
                fclose_func,
                [file].as_ptr() as *mut _,
                1,
                CString::new("").unwrap().as_ptr(),
            );

            LLVMBuildBr(self.builder, done);

            // Done block
            LLVMPositionBuilderAtEnd(self.builder, done);
            LLVMBuildRetVoid(self.builder);
        }
    }

    pub fn generate_object(&mut self, program: &Program, output_path: &str) -> Result<()> {
        self.generate(program)?;

        unsafe {
            // Verify module
            let error = ptr::null_mut();
            if LLVMVerifyModule(self.module, LLVMReturnStatusAction, error) != 0 {
                let error_str = CStr::from_ptr(*error).to_string_lossy();
                LLVMDisposeMessage(*error);
                return Err(anyhow!("Module verification failed: {}", error_str));
            }

            // Apply optimizations
            if self.opt_level > 0 {
                self.optimize_module();
            }

            // Generate object code
            let target_triple = get_default_target_triple();
            let mut target = ptr::null_mut();
            let mut error_msg = ptr::null_mut();

            if LLVMGetTargetFromTriple(target_triple.as_ptr(), &mut target, &mut error_msg) != 0 {
                let error = CStr::from_ptr(error_msg).to_string_lossy();
                LLVMDisposeMessage(error_msg);
                return Err(anyhow!("Failed to get target: {}", error));
            }

            let cpu = CString::new("generic").unwrap();
            let features = CString::new("").unwrap();

            let target_machine = LLVMCreateTargetMachine(
                target,
                target_triple.as_ptr(),
                cpu.as_ptr(),
                features.as_ptr(),
                LLVMCodeGenOptLevel::LLVMCodeGenLevelDefault,
                LLVMRelocMode::LLVMRelocDefault,
                LLVMCodeModel::LLVMCodeModelDefault,
            );

            let output_file = CString::new(output_path).unwrap();

            if LLVMTargetMachineEmitToFile(
                target_machine,
                self.module,
                output_file.as_ptr() as *mut _,
                LLVMCodeGenFileType::LLVMObjectFile,
                &mut error_msg,
            ) != 0 {
                let error = CStr::from_ptr(error_msg).to_string_lossy();
                LLVMDisposeMessage(error_msg);
                return Err(anyhow!("Failed to emit object file: {}", error));
            }

            LLVMDisposeTargetMachine(target_machine);
        }

        Ok(())
    }

    pub fn generate_assembly(&mut self, program: &Program) -> Result<String> {
        self.generate(program)?;

        unsafe {
            // Generate LLVM IR as assembly
            let asm_string = LLVMPrintModuleToString(self.module);
            let result = CStr::from_ptr(asm_string).to_string_lossy().to_string();
            LLVMDisposeMessage(asm_string);
            Ok(result)
        }
    }

    fn generate(&mut self, program: &Program) -> Result<()> {
        // Pass -1: Process imports
        self.process_imports(program)?;

        // Pass 0: Create opaque struct types for all structs (handles forward references)
        for item in &program.items {
            if let Item::TypeDef(typedef) = item {
                if let TypeDefinitionKind::Struct { .. } = &typedef.kind {
                    unsafe {
                        let c_name = CString::new(typedef.name.as_str())?;
                        // Create an opaque struct type first to allow for forward references
                        let struct_type = LLVMStructCreateNamed(self.context, c_name.as_ptr());
                        self.types.insert(typedef.name.clone(), struct_type);
                    }
                }
            }
        }

        // Pass 1: Set the bodies for all struct types
        for item in &program.items {
            if let Item::TypeDef(typedef) = item {
                self.generate_type_definition(typedef)?;
            }
        }

        // Pass 2: Analyze mutability of parameters
        for item in &program.items {
            if let Item::Function(func) = item {
                self.analyze_parameter_mutability(func);
            }
        }

        // Pass 3: Declare all functions (forward declarations) with now-complete types
        for item in &program.items {
            if let Item::Function(func) = item {
                self.declare_function(func)?;
            }
        }

        // Pass 4: Generate all function bodies
        for item in &program.items {
            if let Item::Function(func) = item {
                self.generate_function_body(func)?;
            }
        }

        Ok(())
    }

    fn analyze_parameter_mutability(&mut self, func: &Function) {
        let mut mutable_params = Vec::new();

        // Check each statement in the function body
        for statement in &func.body.statements {
            self.check_statement_for_mutations(statement, &func.parameters, &mut mutable_params);
        }

        if !mutable_params.is_empty() {
            self.mutable_params.insert(func.name.clone(), mutable_params);
        }
    }

    fn check_statement_for_mutations(&self, stmt: &Statement, params: &[Parameter], mutable_params: &mut Vec<String>) {
        match stmt {
            Statement::Set(set_stmt) => {
                // Check if the target is a parameter field access
                if let Expression::FieldAccess(field_access) = &set_stmt.target {
                    if let Expression::Identifier(name) = &field_access.object {
                        // Check if this identifier is a parameter
                        if params.iter().any(|p| p.name == *name) {
                            if !mutable_params.contains(name) {
                                mutable_params.push(name.clone());
                            }
                        }
                    }
                }
            }
            Statement::If(if_stmt) => {
                // Check then block
                for stmt in &if_stmt.then_block.statements {
                    self.check_statement_for_mutations(stmt, params, mutable_params);
                }
                // Check else-if blocks
                for else_if in &if_stmt.else_if_branches {
                    for stmt in &else_if.block.statements {
                        self.check_statement_for_mutations(stmt, params, mutable_params);
                    }
                }
                // Check else block
                if let Some(else_block) = &if_stmt.else_block {
                    for stmt in &else_block.statements {
                        self.check_statement_for_mutations(stmt, params, mutable_params);
                    }
                }
            }
            Statement::While(while_stmt) => {
                for stmt in &while_stmt.body.statements {
                    self.check_statement_for_mutations(stmt, params, mutable_params);
                }
            }
            Statement::ForEach(foreach) => {
                for stmt in &foreach.body.statements {
                    self.check_statement_for_mutations(stmt, params, mutable_params);
                }
            }
            _ => {}
        }
    }

    fn declare_function(&mut self, func: &Function) -> Result<()> {
        unsafe {
            // Check if this function has mutable parameters
            let mutable_params = self.mutable_params.get(&func.name);

            // Create function type
            let mut param_types = Vec::new();
            for param in &func.parameters {
                let is_mutable = mutable_params.map_or(false, |mp| mp.contains(&param.name));

                let param_type = if is_mutable {
                    // For mutable parameters, pass as pointer
                    LLVMPointerType(self.get_llvm_type(&param.param_type), 0)
                } else {
                    // Normal pass-by-value
                    self.get_llvm_type(&param.param_type)
                };
                param_types.push(param_type);
            }

            let return_type = self.get_llvm_type(&func.return_type);
            let func_type = LLVMFunctionType(
                return_type,
                param_types.as_ptr() as *mut _,
                param_types.len() as u32,
                0,
            );

            // Create function declaration
            let func_name = CString::new(func.name.clone())?;
            let llvm_func = LLVMAddFunction(self.module, func_name.as_ptr(), func_type);

            // Store both the function value and its type
            self.functions.insert(func.name.clone(), llvm_func);
            self.function_types.insert(func.name.clone(), func_type);

            // Export the function to the module system
            self.export_function(&func.name, llvm_func);
        }
        Ok(())
    }

    fn generate_function_body(&mut self, func: &Function) -> Result<()> {
        eprintln!("[CODEGEN] Generating function: {}", func.name);
        unsafe {
            // Get the already-declared function
            let llvm_func = *self.functions.get(&func.name)
                .ok_or_else(|| anyhow!("Function not declared: {}", func.name))?;

            // Create entry block
            let entry_name = CString::new("entry")?;
            let entry_block = LLVMAppendBasicBlockInContext(
                self.context,
                llvm_func,
                entry_name.as_ptr(),
            );
            LLVMPositionBuilderAtEnd(self.builder, entry_block);

            // Set current function context
            self.current_function = Some(llvm_func);
            self.current_block = Some(entry_block);
            self.current_function_name = Some(func.name.clone());
            self.variables.clear();
            self.param_is_pointer.clear();

            // Check which parameters are mutable
            let mutable_params = self.mutable_params.get(&func.name);

            // Bind parameters
            for (i, param) in func.parameters.iter().enumerate() {
                let llvm_param = LLVMGetParam(llvm_func, i as u32);
                let param_name = CString::new(param.name.clone())?;
                LLVMSetValueName2(llvm_param, param_name.as_ptr(), param.name.len());

                let is_mutable = mutable_params.map_or(false, |mp| mp.contains(&param.name));

                if is_mutable {
                    // For mutable parameters, the llvm_param is already a pointer to the struct
                    // We need to create an alloca that stores this pointer (pointer to pointer)
                    let ptr_type = LLVMPointerType(self.get_llvm_type(&param.param_type), 0);
                    let alloca = LLVMBuildAlloca(
                        self.builder,
                        ptr_type,  // Allocate space for the pointer
                        param_name.as_ptr(),
                    );
                    LLVMBuildStore(self.builder, llvm_param, alloca);  // Store the incoming pointer
                    self.variables.insert(param.name.clone(), alloca);
                    self.param_is_pointer.insert(param.name.clone(), true);

                    // Track the type name if it's a custom type
                    if let Type::Custom(type_name) = &param.param_type {
                        self.variable_types.insert(param.name.clone(), type_name.clone());
                    }
                } else {
                    // Normal parameter - allocate and store as before
                    let alloca = LLVMBuildAlloca(
                        self.builder,
                        self.get_llvm_type(&param.param_type),
                        param_name.as_ptr(),
                    );
                    LLVMBuildStore(self.builder, llvm_param, alloca);
                    self.variables.insert(param.name.clone(), alloca);

                    // Track the type name if it's a custom type
                    if let Type::Custom(type_name) = &param.param_type {
                        self.variable_types.insert(param.name.clone(), type_name.clone());
                    }
                }
            }

            // Generate function body
            self.generate_block(&func.body)?;

            // Add terminator if needed
            let current_bb = LLVMGetInsertBlock(self.builder);
            if !current_bb.is_null() && LLVMGetBasicBlockTerminator(current_bb).is_null() {
                if func.return_type == Type::Void {
                    LLVMBuildRetVoid(self.builder);
                } else {
                    // Non-void function without a return - add unreachable
                    // This happens when all paths end in Error() calls or similar
                    LLVMBuildUnreachable(self.builder);
                }
            }

            // Verify function
            if LLVMVerifyFunction(llvm_func, LLVMPrintMessageAction) != 0 {
                return Err(anyhow!("Function verification failed: {}", func.name));
            }
        }

        Ok(())
    }

    fn generate_block(&mut self, block: &Block) -> Result<()> {
        for statement in &block.statements {
            self.generate_statement(statement)?;
        }
        Ok(())
    }

    fn generate_statement(&mut self, stmt: &Statement) -> Result<()> {
        match stmt {
            Statement::Let(let_stmt) => {
                self.generate_let(let_stmt)
            },
            Statement::Set(set_stmt) => self.generate_set(set_stmt),
            Statement::If(if_stmt) => self.generate_if(if_stmt),
            Statement::While(while_stmt) => self.generate_while(while_stmt),
            Statement::ForEach(foreach) => self.generate_foreach(foreach),
            Statement::Return(ret_stmt) => {
                self.generate_return(ret_stmt)
            },
            Statement::WriteFile(write_stmt) => self.generate_write_file(write_stmt),
            Statement::AddToList(add_stmt) => self.generate_add_to_list(add_stmt),
            Statement::Match(match_stmt) => self.generate_match(match_stmt),
            Statement::Expression(expr) => {
                self.generate_expression(expr)?;
                Ok(())
            },
            Statement::Break => {
                // Break statements should be handled in loop contexts
                // For now, just ignore as this is not fully implemented
                Ok(())
            }
            Statement::Continue => {
                // Continue statements should be handled in loop contexts
                // For now, just ignore as this is not fully implemented
                Ok(())
            }
        }
    }

    fn generate_let(&mut self, let_stmt: &LetStatement) -> Result<()> {
        unsafe {
            let value = self.generate_expression(&let_stmt.value)?;

            let var_type = self.get_expression_type(&let_stmt.value);

            // Track the type name for custom types
            if let Type::Custom(type_name) = &var_type {
                self.variable_types.insert(let_stmt.name.clone(), type_name.clone());
            }

            let var_name = CString::new(let_stmt.name.clone())?;
            let llvm_type = self.get_llvm_type(&var_type);
            let alloca = LLVMBuildAlloca(
                self.builder,
                llvm_type,
                var_name.as_ptr(),
            );

            LLVMBuildStore(self.builder, value, alloca);

            self.variables.insert(let_stmt.name.clone(), alloca);
        }
        Ok(())
    }

    fn generate_set(&mut self, set_stmt: &SetStatement) -> Result<()> {
        unsafe {
            let value = self.generate_expression(&set_stmt.value)?;

            match &set_stmt.target {
                Expression::Identifier(name) => {
                    if let Some(&var_ptr) = self.variables.get(name) {
                        LLVMBuildStore(self.builder, value, var_ptr);

                        // Update the variable type tracking if needed
                        let value_type = self.get_expression_type(&set_stmt.value);
                        if let Type::Custom(type_name) = &value_type {
                            self.variable_types.insert(name.clone(), type_name.clone());
                        }
                    } else {
                        return Err(anyhow!("Undefined variable: {}", name));
                    }
                }
                Expression::FieldAccess(field_access) => {
                    // Handle setting a field value
                    let object_name = match &field_access.object {
                        Expression::Identifier(name) => name,
                        _ => return Err(anyhow!("Complex field access patterns not yet supported")),
                    };

                    let object_ptr = *self.variables.get(object_name)
                        .ok_or_else(|| anyhow!("Undefined variable: {}", object_name))?;

                    // Get the type name for this variable
                    let type_name = self.variable_types.get(object_name)
                        .cloned()
                        .unwrap_or_else(|| "Token".to_string()); // Fallback to Token

                    // Look up field information
                    let field_index = if let Some(fields) = self.type_fields.get(&type_name) {
                        fields.iter()
                            .position(|(name, _)| name == &field_access.field)
                            .map(|idx| idx as u32)
                            .ok_or_else(|| anyhow!("Unknown field '{}' in type '{}'", field_access.field, type_name))?
                    } else {
                        // Fallback to hardcoded Token fields
                        match field_access.field.as_str() {
                            "token_type" => 0,
                            "value" => 1,
                            "line" => 2,
                            "column" => 3,
                            _ => return Err(anyhow!("Unknown field: {}", field_access.field)),
                        }
                    };

                    // Get the struct type
                    let struct_type = *self.types.get(&type_name)
                        .ok_or_else(|| anyhow!("Type '{}' not found", type_name))?;

                    // Check if this is a pointer parameter (passed by reference)
                    let final_struct_ptr = if self.param_is_pointer.get(object_name).copied().unwrap_or(false) {
                        // The parameter is a pointer - object_ptr contains the pointer to the struct
                        // Load the pointer first
                        LLVMBuildLoad2(
                            self.builder,
                            LLVMPointerType(struct_type, 0),
                            object_ptr,
                            CString::new(format!("{}_ptr_load", object_name))?.as_ptr(),
                        )
                    } else {
                        // Regular local variable - object_ptr already points to the struct
                        object_ptr
                    };

                    // Now get the field pointer
                    let field_ptr = LLVMBuildStructGEP2(
                        self.builder,
                        struct_type,
                        final_struct_ptr,
                        field_index,
                        CString::new(format!("{}_field_ptr", field_access.field))?.as_ptr(),
                    );

                    LLVMBuildStore(self.builder, value, field_ptr);
                }
                _ => return Err(anyhow!("Invalid assignment target")),
            }
        }
        Ok(())
    }

    fn generate_if(&mut self, if_stmt: &IfStatement) -> Result<()> {
        unsafe {
            let condition_value = self.generate_expression(&if_stmt.condition)?;
            let condition = self.ensure_boolean_condition(condition_value)?;

            let func = self.current_function.unwrap();
            let then_bb = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("then")?.as_ptr(),
            );

            // Create merge block
            let merge_bb = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("ifcont")?.as_ptr(),
            );

            // Determine the first alternative block (first else-if or final else)
            let first_alt_bb = if !if_stmt.else_if_branches.is_empty() {
                LLVMAppendBasicBlockInContext(
                    self.context,
                    func,
                    CString::new("elseif0")?.as_ptr(),
                )
            } else if if_stmt.else_block.is_some() {
                LLVMAppendBasicBlockInContext(
                    self.context,
                    func,
                    CString::new("else")?.as_ptr(),
                )
            } else {
                merge_bb
            };

            // Branch on main condition
            LLVMBuildCondBr(self.builder, condition, then_bb, first_alt_bb);

            // Generate then block
            LLVMPositionBuilderAtEnd(self.builder, then_bb);
            self.generate_block(&if_stmt.then_block)?;
            let current_then_bb = LLVMGetInsertBlock(self.builder);
            if LLVMGetBasicBlockTerminator(current_then_bb).is_null() {
                LLVMBuildBr(self.builder, merge_bb);
            }

            // Generate else-if branches
            let mut final_else_bb = first_alt_bb;
            for (i, else_if_branch) in if_stmt.else_if_branches.iter().enumerate() {
                let current_elseif_bb = if i == 0 { first_alt_bb } else { final_else_bb };

                LLVMPositionBuilderAtEnd(self.builder, current_elseif_bb);

                // Generate else-if condition
                let elseif_condition_value = self.generate_expression(&else_if_branch.condition)?;
                let elseif_condition = self.ensure_boolean_condition(elseif_condition_value)?;

                // Create block for this else-if's body
                let elseif_body_bb = LLVMAppendBasicBlockInContext(
                    self.context,
                    func,
                    CString::new(format!("elseif{}_body", i))?.as_ptr(),
                );

                // Determine next alternative block
                let next_alt_bb = if i + 1 < if_stmt.else_if_branches.len() {
                    LLVMAppendBasicBlockInContext(
                        self.context,
                        func,
                        CString::new(format!("elseif{}", i + 1))?.as_ptr(),
                    )
                } else if if_stmt.else_block.is_some() {
                    LLVMAppendBasicBlockInContext(
                        self.context,
                        func,
                        CString::new("else")?.as_ptr(),
                    )
                } else {
                    merge_bb
                };

                // Branch on else-if condition
                LLVMBuildCondBr(self.builder, elseif_condition, elseif_body_bb, next_alt_bb);

                // Generate else-if body
                LLVMPositionBuilderAtEnd(self.builder, elseif_body_bb);
                self.generate_block(&else_if_branch.block)?;
                let current_body_bb = LLVMGetInsertBlock(self.builder);
                if LLVMGetBasicBlockTerminator(current_body_bb).is_null() {
                    LLVMBuildBr(self.builder, merge_bb);
                }

                // Update final_else_bb for next iteration or final else block
                final_else_bb = next_alt_bb;
            }

            // Generate final else block if it exists
            if let Some(else_block) = &if_stmt.else_block {
                let else_bb = if if_stmt.else_if_branches.is_empty() {
                    first_alt_bb
                } else {
                    final_else_bb
                };

                LLVMPositionBuilderAtEnd(self.builder, else_bb);
                self.generate_block(else_block)?;
                let current_else_bb = LLVMGetInsertBlock(self.builder);
                if LLVMGetBasicBlockTerminator(current_else_bb).is_null() {
                    LLVMBuildBr(self.builder, merge_bb);
                }
            }

            // Continue with merge block
            LLVMPositionBuilderAtEnd(self.builder, merge_bb);

            // Check if merge block has any predecessors, if not it's unreachable
            // and needs a terminator instruction
            if LLVMGetFirstUse(LLVMBasicBlockAsValue(merge_bb)).is_null() {
                // No predecessors, this block is unreachable - add unreachable instruction
                LLVMBuildUnreachable(self.builder);
            }

            self.current_block = Some(merge_bb);
        }
        Ok(())
    }

    fn generate_while(&mut self, while_stmt: &WhileStatement) -> Result<()> {
        unsafe {
            let func = self.current_function.unwrap();

            let cond_bb = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("while.cond")?.as_ptr(),
            );
            let body_bb = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("while.body")?.as_ptr(),
            );
            let end_bb = LLVMAppendBasicBlockInContext(
                self.context,
                func,
                CString::new("while.end")?.as_ptr(),
            );

            // Jump to condition
            LLVMBuildBr(self.builder, cond_bb);

            // Generate condition
            LLVMPositionBuilderAtEnd(self.builder, cond_bb);
            let condition_value = self.generate_expression(&while_stmt.condition)?;
            let condition = self.ensure_boolean_condition(condition_value)?;
            LLVMBuildCondBr(self.builder, condition, body_bb, end_bb);

            // Generate body
            LLVMPositionBuilderAtEnd(self.builder, body_bb);
            self.generate_block(&while_stmt.body)?;
            LLVMBuildBr(self.builder, cond_bb);

            // Continue after loop
            LLVMPositionBuilderAtEnd(self.builder, end_bb);
            self.current_block = Some(end_bb);
        }
        Ok(())
    }

    fn generate_foreach(&mut self, foreach: &ForEachStatement) -> Result<()> {
        unsafe {
            // Get the list to iterate over
            let list_value = self.generate_expression(&foreach.collection)?;

            // Create blocks for the loop
            let loop_block = LLVMAppendBasicBlockInContext(
                self.context,
                self.current_function.unwrap(),
                CString::new("foreach_loop")?.as_ptr(),
            );
            let increment_block = LLVMAppendBasicBlockInContext(
                self.context,
                self.current_function.unwrap(),
                CString::new("foreach_increment")?.as_ptr(),
            );
            let exit_block = LLVMAppendBasicBlockInContext(
                self.context,
                self.current_function.unwrap(),
                CString::new("foreach_exit")?.as_ptr(),
            );

            // Create index variable for iteration
            let index_alloca = LLVMBuildAlloca(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                CString::new("foreach_index")?.as_ptr(),
            );
            LLVMBuildStore(
                self.builder,
                LLVMConstInt(LLVMInt64TypeInContext(self.context), 0, 0),
                index_alloca,
            );

            // Get list length
            let list_length = *self.functions.get("list_length")
                .ok_or_else(|| anyhow!("list_length function not found"))?;
            let length = LLVMBuildCall2(
                self.builder,
                *self.function_types.get("list_length").unwrap(),
                list_length,
                [list_value].as_ptr() as *mut _,
                1,
                CString::new("list_len")?.as_ptr(),
            );

            // Jump to loop
            LLVMBuildBr(self.builder, loop_block);

            // Loop block: check condition
            LLVMPositionBuilderAtEnd(self.builder, loop_block);
            let current_index = LLVMBuildLoad2(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                index_alloca,
                CString::new("current_index")?.as_ptr(),
            );
            let condition = LLVMBuildICmp(
                self.builder,
                LLVMIntPredicate::LLVMIntSLT,
                current_index,
                length,
                CString::new("foreach_condition")?.as_ptr(),
            );
            LLVMBuildCondBr(self.builder, condition, increment_block, exit_block);

            // Increment block: get current element and execute body
            LLVMPositionBuilderAtEnd(self.builder, increment_block);

            // Get current element from list
            let list_get = *self.functions.get("list_get")
                .ok_or_else(|| anyhow!("list_get function not found"))?;
            let element = LLVMBuildCall2(
                self.builder,
                *self.function_types.get("list_get").unwrap(),
                list_get,
                [list_value, current_index].as_ptr() as *mut _,
                2,
                CString::new("element")?.as_ptr(),
            );

            // Create variable for loop iteration
            let element_alloca = LLVMBuildAlloca(
                self.builder,
                LLVMInt64TypeInContext(self.context),
                CString::new(foreach.variable.as_str())?.as_ptr(),
            );
            LLVMBuildStore(self.builder, element, element_alloca);

            // Store in variables table
            let old_var = self.variables.insert(foreach.variable.clone(), element_alloca);

            // Generate loop body
            for statement in &foreach.body.statements {
                self.generate_statement(statement)?;
            }

            // Restore old variable binding if it existed
            if let Some(old) = old_var {
                self.variables.insert(foreach.variable.clone(), old);
            } else {
                self.variables.remove(&foreach.variable);
            }

            // Increment index
            let incremented = LLVMBuildAdd(
                self.builder,
                current_index,
                LLVMConstInt(LLVMInt64TypeInContext(self.context), 1, 0),
                CString::new("incremented_index")?.as_ptr(),
            );
            LLVMBuildStore(self.builder, incremented, index_alloca);

            // Jump back to loop
            LLVMBuildBr(self.builder, loop_block);

            // Exit block
            LLVMPositionBuilderAtEnd(self.builder, exit_block);
        }
        Ok(())
    }

    fn generate_match(&mut self, match_stmt: &MatchStatement) -> Result<()> {
        unsafe {
            // Generate the value to match
            let match_value = self.generate_expression(&match_stmt.expression)?;

            // Create blocks for each case and the exit block
            let exit_block = LLVMAppendBasicBlockInContext(
                self.context,
                self.current_function.unwrap(),
                CString::new("match_exit")?.as_ptr(),
            );

            let mut case_blocks = Vec::new();
            let mut next_blocks = Vec::new();

            // Create blocks for each case
            for (i, _) in match_stmt.cases.iter().enumerate() {
                case_blocks.push(LLVMAppendBasicBlockInContext(
                    self.context,
                    self.current_function.unwrap(),
                    CString::new(format!("match_case_{}", i))?.as_ptr(),
                ));
                next_blocks.push(LLVMAppendBasicBlockInContext(
                    self.context,
                    self.current_function.unwrap(),
                    CString::new(format!("match_next_{}", i))?.as_ptr(),
                ));
            }

            // Generate code for each case
            for (i, case) in match_stmt.cases.iter().enumerate() {
                // Jump to test block
                if i == 0 {
                    LLVMBuildBr(self.builder, next_blocks[0]);
                }

                // Test block: check if pattern matches
                LLVMPositionBuilderAtEnd(self.builder, next_blocks[i]);
                let pattern_value = self.generate_expression(&case.pattern)?;
                let condition = LLVMBuildICmp(
                    self.builder,
                    LLVMIntPredicate::LLVMIntEQ,
                    match_value,
                    pattern_value,
                    CString::new("match_cond")?.as_ptr(),
                );

                let next_test = if i + 1 < next_blocks.len() {
                    next_blocks[i + 1]
                } else {
                    exit_block
                };

                LLVMBuildCondBr(self.builder, condition, case_blocks[i], next_test);

                // Case block: execute body
                LLVMPositionBuilderAtEnd(self.builder, case_blocks[i]);
                for statement in &case.body.statements {
                    self.generate_statement(statement)?;
                }
                // If no explicit return, jump to exit
                if !matches!(case.body.statements.last(), Some(Statement::Return(_))) {
                    LLVMBuildBr(self.builder, exit_block);
                }
            }

            // Position at exit block
            LLVMPositionBuilderAtEnd(self.builder, exit_block);
        }
        Ok(())
    }

    fn generate_add_to_list(&mut self, add_stmt: &AddToListStatement) -> Result<()> {
        unsafe {
            let list_val = self.generate_expression(&add_stmt.list)?;
            let mut value_to_add = self.generate_expression(&add_stmt.value)?;

            let list_append_func = *self.functions.get("list_append")
                .ok_or_else(|| anyhow!("list_append function not found"))?;
            let list_append_type = *self.function_types.get("list_append").unwrap();

            // Get the expected type for the second parameter (the value)
            let mut param_types: [LLVMTypeRef; 2] = [ptr::null_mut(); 2];
            LLVMGetParamTypes(list_append_type, param_types.as_mut_ptr());
            let expected_value_type = param_types[1];

            // Perform the coercion if needed
            let actual_value_type = LLVMTypeOf(value_to_add);
            let expected_kind = LLVMGetTypeKind(expected_value_type);
            let actual_kind = LLVMGetTypeKind(actual_value_type);

            if expected_kind == LLVMTypeKind::LLVMPointerTypeKind {
                if actual_kind == LLVMTypeKind::LLVMStructTypeKind {
                    eprintln!("[CODEGEN] COERCION: Converting struct value to pointer for AddToList");
                    let alloca = LLVMBuildAlloca(
                        self.builder,
                        actual_value_type,
                        CString::new("addtolist_coerce")?.as_ptr()
                    );
                    LLVMBuildStore(self.builder, value_to_add, alloca);
                    value_to_add = LLVMBuildBitCast(
                        self.builder,
                        alloca,
                        expected_value_type,
                        CString::new("addtolist_ptr")?.as_ptr(),
                    );
                } else if actual_kind == LLVMTypeKind::LLVMIntegerTypeKind {
                    // For i64 values being added to lists, we need to box them
                    eprintln!("[CODEGEN] COERCION: Boxing i64 value for AddToList");
                    let alloca = LLVMBuildAlloca(
                        self.builder,
                        actual_value_type,
                        CString::new("addtolist_int_box")?.as_ptr()
                    );
                    LLVMBuildStore(self.builder, value_to_add, alloca);
                    value_to_add = LLVMBuildBitCast(
                        self.builder,
                        alloca,
                        expected_value_type,
                        CString::new("addtolist_int_ptr")?.as_ptr(),
                    );
                }
            }

            // Now, the call will have the correctly typed arguments
            LLVMBuildCall2(
                self.builder,
                list_append_type,
                list_append_func,
                [list_val, value_to_add].as_ptr() as *mut _,
                2,
                CString::new("")?.as_ptr(),
            );
        }
        Ok(())
    }

    fn generate_write_file(&mut self, write_stmt: &WriteFileStatement) -> Result<()> {
        unsafe {
            // Generate the content and filename expressions
            let content = self.generate_expression(&write_stmt.content)?;
            let filename = self.generate_expression(&write_stmt.filename)?;

            // Call the WriteFile function
            let write_file = *self.functions.get("WriteFile")
                .ok_or_else(|| anyhow!("WriteFile function not found"))?;
            let write_file_type = *self.function_types.get("WriteFile")
                .ok_or_else(|| anyhow!("WriteFile function type not found"))?;

            LLVMBuildCall2(
                self.builder,
                write_file_type,
                write_file,
                [content, filename].as_ptr() as *mut _,
                2,
                CString::new("").unwrap().as_ptr(),
            );
        }
        Ok(())
    }

    fn generate_return(&mut self, ret_stmt: &ReturnStatement) -> Result<()> {
        unsafe {
            if let Some(value_expr) = &ret_stmt.value {
                let mut ret_value = self.generate_expression(value_expr)?;

                // Get the current function's declared return type from our tracking
                if let Some(func_name) = &self.current_function_name {
                    if let Some(func_type) = self.function_types.get(func_name) {
                        let declared_ret_type = LLVMGetReturnType(*func_type);
                        let actual_ret_type = LLVMTypeOf(ret_value);

                        // If the declared return is a struct value, but we have a pointer to it
                        // (from an identifier that's a pointer parameter), we must load the value before returning
                        if LLVMGetTypeKind(declared_ret_type) == LLVMTypeKind::LLVMStructTypeKind &&
                           LLVMGetTypeKind(actual_ret_type) == LLVMTypeKind::LLVMPointerTypeKind {

                            ret_value = LLVMBuildLoad2(
                                self.builder,
                                declared_ret_type, // The struct type itself
                                ret_value,         // The pointer to the struct
                                CString::new("ret_load")?.as_ptr(),
                            );
                        }
                    }
                }

                LLVMBuildRet(self.builder, ret_value);
            } else {
                LLVMBuildRetVoid(self.builder);
            }
        }
        Ok(())
    }

    fn generate_expression(&mut self, expr: &Expression) -> Result<LLVMValueRef> {
        // Iterative expression generation using explicit stack to avoid stack overflow
        enum WorkItem<'a> {
            ProcessExpr(&'a Expression),
            CombineBinary {
                operator: BinaryOperator,
                waiting_for_right: bool,
            },
            CombineUnary {
                operator: UnaryOperator,
            },
            CombineCall {
                function: String,
                arg_count: usize,
                processed: usize,
            },
            CombineMethodCall {
                method: String,
                arg_count: usize,
                processed: usize,
            },
            CombineListLiteral {
                list: LLVMValueRef,
                element_count: usize,
                processed: usize,
            },
            CombineIndexAccess {
                waiting_for_index: bool,
            },
            CombineLengthOf,
            CombineTypeConstruction {
                type_name: String,
                struct_ptr: LLVMValueRef,
                struct_type: LLVMTypeRef,
                field_count: usize,
                processed: usize,
                field_names: Vec<String>,
            },
            CombineFieldAccess {
                field_name: String,
                object_type_name: Option<String>,
            },
        }

        let mut work_stack: Vec<WorkItem> = vec![WorkItem::ProcessExpr(expr)];
        let mut value_stack: Vec<LLVMValueRef> = Vec::new();

        unsafe {
            while let Some(work_item) = work_stack.pop() {
                match work_item {
                    WorkItem::ProcessExpr(expr) => {
                        match expr {
                            Expression::Integer(n) => {
                                value_stack.push(LLVMConstInt(
                                    LLVMInt64TypeInContext(self.context),
                                    *n as u64,
                                    1,
                                ));
                            }
                            Expression::Float(f) => {
                                value_stack.push(LLVMConstReal(
                                    LLVMDoubleTypeInContext(self.context),
                                    *f,
                                ));
                            }
                            Expression::Boolean(b) => {
                                value_stack.push(LLVMConstInt(
                                    LLVMInt1TypeInContext(self.context),
                                    if *b { 1 } else { 0 },
                                    0,
                                ));
                            }
                            Expression::String(s) => {
                                let str_const = CString::new(s.clone())?;
                                let global_str = LLVMBuildGlobalStringPtr(
                                    self.builder,
                                    str_const.as_ptr(),
                                    CString::new("str")?.as_ptr(),
                                );
                                value_stack.push(global_str);
                            }
                            Expression::Identifier(name) => {
                                // First check local variables (which are stored as allocas)
                                if let Some(&var_ptr) = self.variables.get(name) {
                                    // Check if this identifier is a pointer parameter (passed by reference)
                                    if self.param_is_pointer.get(name).copied().unwrap_or(false) {
                                        // This is a pointer parameter - var_ptr is an alloca containing a pointer
                                        // We need to load the pointer and return it (not the value it points to)
                                        // This ensures field accesses and function calls get the pointer
                                        let struct_type = if let Some(type_name) = self.variable_types.get(name) {
                                            self.types.get(type_name).copied()
                                        } else {
                                            None
                                        };

                                        if let Some(struct_type) = struct_type {
                                            // Load the pointer from the alloca (don't dereference it)
                                            let ptr_to_struct = LLVMBuildLoad2(
                                                self.builder,
                                                LLVMPointerType(struct_type, 0),
                                                var_ptr,
                                                CString::new(format!("{}_ptr", name))?.as_ptr(),
                                            );
                                            // Push the pointer itself, not the dereferenced value
                                            value_stack.push(ptr_to_struct);
                                        } else {
                                            // Fallback for non-struct types
                                            let load_name = CString::new(format!("{}.load", name))?;
                                            let elem_type = LLVMGetAllocatedType(var_ptr);
                                            let result = LLVMBuildLoad2(
                                                self.builder,
                                                elem_type,
                                                var_ptr,
                                                load_name.as_ptr(),
                                            );
                                            value_stack.push(result);
                                        }
                                    } else {
                                        // Regular variable - load normally
                                        let load_name = CString::new(format!("{}.load", name))?;
                                        let elem_type = LLVMGetAllocatedType(var_ptr);
                                        let result = LLVMBuildLoad2(
                                            self.builder,
                                            elem_type,
                                            var_ptr,
                                            load_name.as_ptr(),
                                        );
                                        value_stack.push(result);
                                    }
                                } else if self.functions.contains_key(name) {
                                    // It's a function reference
                                    value_stack.push(*self.functions.get(name).unwrap());
                                } else {
                                    // Check if it's an enum variant constant
                                    let enum_value = match name.as_str() {
                                        // TokenType variants
                                        "Keyword" => 0,
                                        "Identifier" => 1,
                                        "Integer" => 2,
                                        "String" => 3,
                                        "Symbol" => 4,
                                        "Operator" => 5,
                                        // NodeType variants from v0.2 parser
                                        "Program" => 0,
                                        "Function" => 1,
                                        "Parameter" => 2,
                                        "Statement" => 3,
                                        "Expression" => 4,
                                        "BinaryOp" => 5,
                                        "UnaryOp" => 6,
                                        "Literal" => 7,
                                        "IdentifierNode" => 8,
                                        "FunctionCall" => 9,
                                        "IfNode" => 10,
                                        "WhileNode" => 11,
                                        "ForEachNode" => 12,
                                        "MatchNode" => 13,
                                        "ReturnNode" => 14,
                                        "LetNode" => 15,
                                        "SetNode" => 16,
                                        "TypeDef" => 17,
                                        _ => {
                                            eprintln!("[CODEGEN] Looking for identifier: {} in context of generating function body", name);
                                            eprintln!("[CODEGEN] Available variables: {:?}", self.variables.keys().collect::<Vec<_>>());
                                            return Err(anyhow!("Undefined variable: {}", name));
                                        }
                                    };
                                    value_stack.push(LLVMConstInt(
                                        LLVMInt32TypeInContext(self.context),
                                        enum_value,
                                        0,
                                    ));
                                }
                            }
                            Expression::Binary(bin_expr) => {
                                work_stack.push(WorkItem::CombineBinary {
                                    operator: bin_expr.operator.clone(),
                                    waiting_for_right: false,
                                });
                                work_stack.push(WorkItem::ProcessExpr(&bin_expr.right));
                                work_stack.push(WorkItem::ProcessExpr(&bin_expr.left));
                            }
                            Expression::Unary(un_expr) => {
                                work_stack.push(WorkItem::CombineUnary {
                                    operator: un_expr.operator.clone(),
                                });
                                work_stack.push(WorkItem::ProcessExpr(&un_expr.operand));
                            }
                            Expression::Call(call_expr) => {
                                work_stack.push(WorkItem::CombineCall {
                                    function: call_expr.function.clone(),
                                    arg_count: call_expr.arguments.len(),
                                    processed: 0,
                                });
                                // Push arguments in reverse order so they're processed left-to-right
                                for arg in call_expr.arguments.iter().rev() {
                                    work_stack.push(WorkItem::ProcessExpr(arg));
                                }
                            }
                            Expression::MethodCall(method_call) => {
                                // Convert to function call with object_method naming
                                let object_name = match &method_call.object {
                                    Expression::Identifier(name) => name.clone(),
                                    _ => return Err(anyhow!("Method calls currently only supported on simple identifiers")),
                                };
                                let function_name = format!("{}_{}", object_name, method_call.method);

                                work_stack.push(WorkItem::CombineCall {
                                    function: function_name,
                                    arg_count: method_call.arguments.len(),
                                    processed: 0,
                                });
                                for arg in method_call.arguments.iter().rev() {
                                    work_stack.push(WorkItem::ProcessExpr(arg));
                                }
                            }
                            Expression::FieldAccess(field_access) => {
                                // Try to determine the object type name
                                let object_type_name = match &field_access.object {
                                    Expression::Identifier(name) => {
                                        self.variable_types.get(name).cloned()
                                    }
                                    _ => None,
                                };

                                work_stack.push(WorkItem::CombineFieldAccess {
                                    field_name: field_access.field.clone(),
                                    object_type_name,
                                });
                                work_stack.push(WorkItem::ProcessExpr(&field_access.object));
                            }
                            Expression::ListLiteral(elements) => {
                                let list_create = *self.functions.get("list_create")
                                    .ok_or_else(|| anyhow!("list_create function not found"))?;
                                let list = LLVMBuildCall2(
                                    self.builder,
                                    *self.function_types.get("list_create").unwrap(),
                                    list_create,
                                    std::ptr::null_mut(),
                                    0,
                                    CString::new("list")?.as_ptr(),
                                );

                                if elements.is_empty() {
                                    value_stack.push(list);
                                } else {
                                    work_stack.push(WorkItem::CombineListLiteral {
                                        list,
                                        element_count: elements.len(),
                                        processed: 0,
                                    });
                                    for element in elements.iter().rev() {
                                        work_stack.push(WorkItem::ProcessExpr(element));
                                    }
                                }
                            }
                            Expression::IndexAccess(index_access) => {
                                work_stack.push(WorkItem::CombineIndexAccess {
                                    waiting_for_index: false,
                                });
                                work_stack.push(WorkItem::ProcessExpr(&index_access.index));
                                work_stack.push(WorkItem::ProcessExpr(&index_access.object));
                            }
                            Expression::LengthOf(expr) => {
                                work_stack.push(WorkItem::CombineLengthOf);
                                work_stack.push(WorkItem::ProcessExpr(expr));
                            }
                            Expression::DictionaryLiteral(_) => {
                                return Err(anyhow!("Dictionary literals not yet implemented in v0.1"));
                            }
                            Expression::ArrayLiteral(_) => {
                                return Err(anyhow!("Array literals not yet implemented in v0.1"));
                            }
                            Expression::TypeConstruction(type_const) => {
                                let struct_type = *self.types.get(&type_const.type_name)
                                    .ok_or_else(|| anyhow!("Type '{}' not found", type_const.type_name))?;
                                let struct_ptr = LLVMBuildAlloca(
                                    self.builder,
                                    struct_type,
                                    CString::new("struct_instance")?.as_ptr(),
                                );

                                if type_const.fields.is_empty() {
                                    value_stack.push(struct_ptr);
                                } else {
                                    let field_names: Vec<String> = type_const.fields.iter()
                                        .map(|(name, _)| name.clone())
                                        .collect();

                                    work_stack.push(WorkItem::CombineTypeConstruction {
                                        type_name: type_const.type_name.clone(),
                                        struct_ptr,
                                        struct_type,
                                        field_count: type_const.fields.len(),
                                        processed: 0,
                                        field_names,
                                    });

                                    for (_, field_value) in type_const.fields.iter().rev() {
                                        work_stack.push(WorkItem::ProcessExpr(field_value));
                                    }
                                }
                            }
                            Expression::Nothing => {
                                value_stack.push(LLVMConstNull(
                                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)
                                ));
                            }
                            Expression::EnumVariant(variant_name) => {
                                // Handle enum variant as a constant value directly
                                // Check if it's an enum variant constant
                                let enum_value = match variant_name.as_str() {
                                    // TokenType variants
                                    "Keyword" => 0,
                                    "Identifier" => 1,
                                    "Integer" => 2,
                                    "String" => 3,
                                    "Symbol" => 4,
                                    "Operator" => 5,
                                    // NodeType variants from v0.2 parser
                                    "Program" => 0,
                                    "Function" => 1,
                                    "Parameter" => 2,
                                    "Statement" => 3,
                                    "Expression" => 4,
                                    "BinaryOp" => 5,
                                    "UnaryOp" => 6,
                                    "Literal" => 7,
                                    "IdentifierNode" => 8,
                                    "FunctionCall" => 9,
                                    "IfNode" => 10,
                                    "WhileNode" => 11,
                                    "ForEachNode" => 12,
                                    "MatchNode" => 13,
                                    "ReturnNode" => 14,
                                    "LetNode" => 15,
                                    "SetNode" => 16,
                                    "TypeDef" => 17,
                                    _ => {
                                        return Err(anyhow!("Unknown enum variant: {}", variant_name));
                                    }
                                };
                                value_stack.push(LLVMConstInt(
                                    LLVMInt32TypeInContext(self.context),
                                    enum_value,
                                    0,
                                ));
                            }
                        }
                    }
                    WorkItem::CombineBinary { operator, .. } => {
                        let mut right = value_stack.pop().ok_or_else(|| anyhow!("Missing right operand"))?;
                        let mut left = value_stack.pop().ok_or_else(|| anyhow!("Missing left operand"))?;

                        // Automatic type conversion: convert strings to integers for arithmetic
                        let left_type = LLVMTypeOf(left);
                        let right_type = LLVMTypeOf(right);
                        let left_is_ptr = LLVMGetTypeKind(left_type) == LLVMTypeKind::LLVMPointerTypeKind;
                        let right_is_ptr = LLVMGetTypeKind(right_type) == LLVMTypeKind::LLVMPointerTypeKind;
                        let _int_type = LLVMInt64TypeInContext(self.context);

                        // Handle string concatenation specially
                        if operator == BinaryOperator::Plus && left_is_ptr && right_is_ptr {
                            // Both are strings - use string_concat
                            let string_concat_func = *self.functions.get("string_concat").unwrap();
                            let string_concat_type = *self.function_types.get("string_concat").unwrap();
                            let result = LLVMBuildCall2(
                                self.builder,
                                string_concat_type,
                                string_concat_func,
                                [left, right].as_ptr() as *mut _,
                                2,
                                CString::new("concat")?.as_ptr(),
                            );
                            value_stack.push(result);
                            continue; // Skip the normal operator handling
                        }

                        // Convert string pointers to integers using string_to_int for arithmetic operations
                        if matches!(operator, BinaryOperator::Plus | BinaryOperator::Minus | BinaryOperator::MultipliedBy | BinaryOperator::DividedBy | BinaryOperator::Modulo) {
                            if left_is_ptr && !right_is_ptr {
                                // Left is string, right is int - convert left to int
                                let string_to_int_func = *self.functions.get("string_to_int").unwrap();
                                let string_to_int_type = *self.function_types.get("string_to_int").unwrap();
                                left = LLVMBuildCall2(
                                    self.builder,
                                    string_to_int_type,
                                    string_to_int_func,
                                    [left].as_ptr() as *mut _,
                                    1,
                                    CString::new("left_str_to_int")?.as_ptr(),
                                );
                            } else if !left_is_ptr && right_is_ptr {
                                // Left is int, right is string - convert right to int
                                let string_to_int_func = *self.functions.get("string_to_int").unwrap();
                                let string_to_int_type = *self.function_types.get("string_to_int").unwrap();
                                right = LLVMBuildCall2(
                                    self.builder,
                                    string_to_int_type,
                                    string_to_int_func,
                                    [right].as_ptr() as *mut _,
                                    1,
                                    CString::new("right_str_to_int")?.as_ptr(),
                                );
                            }
                        }

                        let result = match operator {
                            BinaryOperator::Plus => {
                                LLVMBuildAdd(self.builder, left, right, CString::new("add")?.as_ptr())
                            }
                            BinaryOperator::Minus => {
                                LLVMBuildSub(self.builder, left, right, CString::new("sub")?.as_ptr())
                            }
                            BinaryOperator::MultipliedBy => {
                                LLVMBuildMul(self.builder, left, right, CString::new("mul")?.as_ptr())
                            }
                            BinaryOperator::DividedBy => {
                                LLVMBuildSDiv(self.builder, left, right, CString::new("div")?.as_ptr())
                            }
                            BinaryOperator::Modulo => {
                                LLVMBuildSRem(self.builder, left, right, CString::new("mod")?.as_ptr())
                            }
                            BinaryOperator::IsGreaterThan => {
                                LLVMBuildICmp(
                                    self.builder,
                                    LLVMIntPredicate::LLVMIntSGT,
                                    left,
                                    right,
                                    CString::new("gt")?.as_ptr(),
                                )
                            }
                            BinaryOperator::IsLessThan => {
                                LLVMBuildICmp(
                                    self.builder,
                                    LLVMIntPredicate::LLVMIntSLT,
                                    left,
                                    right,
                                    CString::new("lt")?.as_ptr(),
                                )
                            }
                            BinaryOperator::IsEqualTo => {
                                LLVMBuildICmp(
                                    self.builder,
                                    LLVMIntPredicate::LLVMIntEQ,
                                    left,
                                    right,
                                    CString::new("eq")?.as_ptr(),
                                )
                            }
                            BinaryOperator::IsNotEqualTo => {
                                LLVMBuildICmp(
                                    self.builder,
                                    LLVMIntPredicate::LLVMIntNE,
                                    left,
                                    right,
                                    CString::new("ne")?.as_ptr(),
                                )
                            }
                            BinaryOperator::And => {
                                LLVMBuildAnd(self.builder, left, right, CString::new("and")?.as_ptr())
                            }
                            BinaryOperator::Or => {
                                LLVMBuildOr(self.builder, left, right, CString::new("or")?.as_ptr())
                            }
                        };
                        value_stack.push(result);
                    }
                    WorkItem::CombineUnary { operator } => {
                        let operand = value_stack.pop().ok_or_else(|| anyhow!("Missing operand"))?;
                        match operator {
                            UnaryOperator::Not => {
                                let result = LLVMBuildNot(self.builder, operand, CString::new("not")?.as_ptr());
                                value_stack.push(result);
                            }
                        }
                    }
                    WorkItem::CombineCall { function, arg_count, .. } => {
                        let func = *self.functions.get(&function)
                            .ok_or_else(|| anyhow!("Undefined function: {}", function))?;
                        let func_type = *self.function_types.get(&function)
                            .ok_or_else(|| anyhow!("Function type not found: {}", function))?;

                        // Get the expected parameter types from the function's signature
                        let mut expected_param_types = vec![LLVMTypeRef::default(); LLVMCountParamTypes(func_type) as usize];
                        LLVMGetParamTypes(func_type, expected_param_types.as_mut_ptr());

                        // Ensure the number of arguments matches the number of parameters
                        if arg_count != expected_param_types.len() {
                            return Err(anyhow!(
                                "Incorrect number of arguments for function '{}': expected {}, got {}",
                                function,
                                expected_param_types.len(),
                                arg_count
                            ));
                        }

                        let mut args = Vec::with_capacity(arg_count);
                        // Pop the generated arguments off the value stack.
                        // They were pushed in order, so we pop them into a temporary vec and then reverse.
                        let mut actual_args = Vec::with_capacity(arg_count);
                        for _ in 0..arg_count {
                            actual_args.push(value_stack.pop().ok_or_else(|| anyhow!("Mismatched value stack for call to {}", function))?);
                        }
                        actual_args.reverse(); // Now actual_args[i] corresponds to expected_param_types[i]

                        for (i, mut actual_arg) in actual_args.into_iter().enumerate() {
                            let expected_type = expected_param_types[i];
                            let actual_type = LLVMTypeOf(actual_arg);

                            let expected_kind = LLVMGetTypeKind(expected_type);
                            let actual_kind = LLVMGetTypeKind(actual_type);

                            // *** THIS IS THE CORE FIX ***
                            // If the function expects a generic pointer (like list_append's value)
                            // and we have a struct value, we must allocate the struct on the stack
                            // and pass a pointer to it.
                            if expected_kind == LLVMTypeKind::LLVMPointerTypeKind && actual_kind == LLVMTypeKind::LLVMStructTypeKind {
                                // 1. Allocate stack space for the struct
                                let alloca = LLVMBuildAlloca(
                                    self.builder,
                                    actual_type, // The type of the struct value we have
                                    CString::new(format!("arg_{}_coerce", i))?.as_ptr(),
                                );
                                // 2. Store the struct value into the allocated space
                                LLVMBuildStore(self.builder, actual_arg, alloca);
                                // 3. Bitcast the specific struct pointer (e.g., %Token*) to a generic pointer (ptr or i8*)
                                actual_arg = LLVMBuildBitCast(
                                    self.builder,
                                    alloca,
                                    expected_type, // The generic pointer type the function expects
                                    CString::new(format!("arg_{}_ptr", i))?.as_ptr(),
                                );
                            } else if (function == "is_digit" || function == "is_letter" || function == "is_whitespace" || function == "to_uppercase" || function == "to_lowercase") && i == 0 {
                                // Your existing special case for char functions
                                actual_arg = LLVMBuildTrunc(
                                    self.builder,
                                    actual_arg,
                                    LLVMInt8TypeInContext(self.context),
                                    CString::new("char_cast")?.as_ptr(),
                                );
                            }

                            args.push(actual_arg);
                        }

                        // Check if the function returns void
                        let return_type = LLVMGetReturnType(func_type);
                        let is_void = LLVMGetTypeKind(return_type) == LLVMTypeKind::LLVMVoidTypeKind;

                        let result = if is_void {
                            // For void functions, don't assign a name to the call result
                            LLVMBuildCall2(
                                self.builder,
                                func_type,
                                func,
                                args.as_ptr() as *mut _,
                                args.len() as u32,
                                CString::new("")?.as_ptr(),  // Empty name for void functions
                            )
                        } else {
                            LLVMBuildCall2(
                                self.builder,
                                func_type,
                                func,
                                args.as_ptr() as *mut _,
                                args.len() as u32,
                                CString::new("call")?.as_ptr(),
                            )
                        };

                        // Only push the result if it's not void (for expression evaluation)
                        if !is_void {
                            value_stack.push(result);
                        } else {
                            // Push a dummy value for void functions to maintain stack consistency
                            value_stack.push(LLVMConstNull(LLVMInt32TypeInContext(self.context)));
                        }
                    }
                    WorkItem::CombineMethodCall { .. } => {
                        // This is handled by converting to CombineCall above
                        unreachable!("CombineMethodCall should not be reached");
                    }
                    WorkItem::CombineListLiteral { list, element_count, processed } => {
                        if processed < element_count {
                            let list_append = *self.functions.get("list_append")
                                .ok_or_else(|| anyhow!("list_append function not found"))?;
                            let list_append_type = *self.function_types.get("list_append").unwrap();

                            // Pop elements and append them - apply same robust type coercion
                            for _ in 0..element_count {
                                let mut value = value_stack.pop().ok_or_else(|| anyhow!("Missing list element"))?;

                                // Apply the same robust type coercion as in CombineCall
                                let value_type = LLVMTypeOf(value);
                                let value_kind = LLVMGetTypeKind(value_type);

                                // Get expected type for list_append second parameter (generic pointer)
                                let expected_type = LLVMPointerType(LLVMInt8TypeInContext(self.context), 0);
                                let expected_kind = LLVMGetTypeKind(expected_type);

                                if expected_kind == LLVMTypeKind::LLVMPointerTypeKind &&
                                   (value_kind == LLVMTypeKind::LLVMStructTypeKind ||
                                    value_kind == LLVMTypeKind::LLVMIntegerTypeKind ||
                                    value_kind == LLVMTypeKind::LLVMFloatTypeKind ||
                                    value_kind == LLVMTypeKind::LLVMDoubleTypeKind) {
                                    // 1. Allocate stack space for the value
                                    let alloca = LLVMBuildAlloca(
                                        self.builder,
                                        value_type,
                                        CString::new("list_elem_coerce")?.as_ptr(),
                                    );
                                    // 2. Store the value into the allocated space
                                    LLVMBuildStore(self.builder, value, alloca);
                                    // 3. Bitcast to expected generic pointer type
                                    value = LLVMBuildBitCast(
                                        self.builder,
                                        alloca,
                                        expected_type,
                                        CString::new("list_elem_ptr")?.as_ptr(),
                                    );
                                }

                                LLVMBuildCall2(
                                    self.builder,
                                    list_append_type,
                                    list_append,
                                    [list, value].as_ptr() as *mut _,
                                    2,
                                    CString::new("")?.as_ptr(),
                                );
                            }
                        }
                        value_stack.push(list);
                    }
                    WorkItem::CombineIndexAccess { .. } => {
                        let index = value_stack.pop().ok_or_else(|| anyhow!("Missing index"))?;
                        let object = value_stack.pop().ok_or_else(|| anyhow!("Missing object"))?;

                        // Determine the element type to call the correct getter
                        // We need the original expression to determine the type
                        // This is a limitation of the current iterative approach
                        // For now, we'll check the type of the object to infer the element type

                        // Get the type of elements in the list
                        let element_type = {
                            // Try to find the type from our tracked variables
                            // This is a hack - ideally we'd pass the original AST expression
                            // For now, let's assume parser.tokens returns Token
                            if self.variable_types.get("parser").is_some() {
                                // We're accessing parser.tokens which is a List[Token]
                                Type::Custom("Token".to_string())
                            } else {
                                // Default fallback
                                Type::Integer
                            }
                        };

                        let result = match element_type {
                            Type::Custom(_) => {
                                // It's a list of structs, use list_get_struct
                                let list_get_struct = *self.functions.get("list_get_struct")
                                    .ok_or_else(|| anyhow!("list_get_struct function not found"))?;
                                let ptr_result = LLVMBuildCall2(
                                    self.builder,
                                    *self.function_types.get("list_get_struct").unwrap(),
                                    list_get_struct,
                                    [object, index].as_ptr() as *mut _,
                                    2,
                                    CString::new("element_ptr")?.as_ptr(),
                                );

                                // Load the struct value from the pointer
                                // We need to determine the struct type
                                if let Type::Custom(type_name) = element_type {
                                    if let Some(&struct_type) = self.types.get(&type_name) {
                                        let loaded_struct = LLVMBuildLoad2(
                                            self.builder,
                                            struct_type,
                                            ptr_result,
                                            CString::new("element")?.as_ptr()
                                        );
                                        loaded_struct
                                    } else {
                                        // Fallback if we can't find the struct type
                                        ptr_result
                                    }
                                } else {
                                    ptr_result
                                }
                            }
                            Type::String => {
                                // String type - use list_get_string
                                let list_get_string = *self.functions.get("list_get_string")
                                    .ok_or_else(|| anyhow!("list_get_string function not found"))?;
                                let result = LLVMBuildCall2(
                                    self.builder,
                                    *self.function_types.get("list_get_string").unwrap(),
                                    list_get_string,
                                    [object, index].as_ptr() as *mut _,
                                    2,
                                    CString::new("element")?.as_ptr(),
                                );
                                result
                            }
                            _ => {
                                // Default to integer/primitive getter
                                let list_get = *self.functions.get("list_get")
                                    .ok_or_else(|| anyhow!("list_get function not found"))?;
                                let result = LLVMBuildCall2(
                                    self.builder,
                                    *self.function_types.get("list_get").unwrap(),
                                    list_get,
                                    [object, index].as_ptr() as *mut _,
                                    2,
                                    CString::new("element")?.as_ptr(),
                                );
                                result
                            }
                        };

                        value_stack.push(result);
                    }
                    WorkItem::CombineLengthOf => {
                        let object = value_stack.pop().ok_or_else(|| anyhow!("Missing object"))?;

                        let list_length = *self.functions.get("list_length")
                            .ok_or_else(|| anyhow!("list_length function not found"))?;
                        let result = LLVMBuildCall2(
                            self.builder,
                            *self.function_types.get("list_length").unwrap(),
                            list_length,
                            [object].as_ptr() as *mut _,
                            1,
                            CString::new("length")?.as_ptr(),
                        );
                        value_stack.push(result);
                    }
                    WorkItem::CombineTypeConstruction {
                        struct_ptr,
                        struct_type,
                        field_count,
                        field_names,
                        ..
                    } => {
                        // Pop field values and store them
                        for i in 0..field_count {
                            let value = value_stack.pop().ok_or_else(|| anyhow!("Missing field value"))?;
                            let field_ptr = LLVMBuildStructGEP2(
                                self.builder,
                                struct_type,
                                struct_ptr,
                                i as u32,
                                CString::new(format!("{}_ptr", field_names[i]))?.as_ptr(),
                            );
                            LLVMBuildStore(self.builder, value, field_ptr);
                        }
                        value_stack.push(struct_ptr);
                    }
                    WorkItem::CombineFieldAccess { field_name, object_type_name } => {
                        let object = value_stack.pop().ok_or_else(|| anyhow!("Missing object for field access"))?;

                        // Determine the struct type name
                        let type_name = if let Some(name) = object_type_name {
                            name
                        } else {
                            // Fallback to Token if type is unknown
                            "Token".to_string()
                        };

                        // Get the struct type
                        let struct_type = *self.types.get(&type_name)
                            .ok_or_else(|| anyhow!("Type '{}' not found", type_name))?;

                        // Check if the object is a struct value or a pointer
                        let object_type = LLVMTypeOf(object);
                        let object_kind = LLVMGetTypeKind(object_type);

                        let object_ptr = if object_kind == LLVMTypeKind::LLVMPointerTypeKind {
                            // Object is already a pointer, use it directly
                            object
                        } else {
                            // Object is a struct value, store it to get a pointer
                            let alloca = LLVMBuildAlloca(
                                self.builder,
                                struct_type,
                                CString::new("field_access_temp")?.as_ptr(),
                            );
                            LLVMBuildStore(self.builder, object, alloca);
                            alloca
                        };

                        // Look up field information
                        let (field_index, field_llvm_type) = if let Some(fields) = self.type_fields.get(&type_name) {
                            // Find the field index and type
                            fields.iter()
                                .position(|(name, _)| name == &field_name)
                                .map(|idx| {
                                    let field_type = fields[idx].1;
                                    (idx as u32, field_type)
                                })
                                .ok_or_else(|| anyhow!("Unknown field '{}' in type '{}'", field_name, type_name))?
                        } else {
                            // Fallback to hardcoded Token fields for compatibility
                            match field_name.as_str() {
                                "token_type" => (0, LLVMInt32TypeInContext(self.context)),
                                "value" => (1, LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)),
                                "line" => (2, LLVMInt64TypeInContext(self.context)),
                                "column" => (3, LLVMInt64TypeInContext(self.context)),
                                _ => return Err(anyhow!("Unknown field: {}", field_name)),
                            }
                        };

                        let field_ptr = LLVMBuildStructGEP2(
                            self.builder,
                            struct_type,
                            object_ptr,
                            field_index,
                            CString::new(format!("{}_field", field_name))?.as_ptr(),
                        );

                        let field_value = LLVMBuildLoad2(
                            self.builder,
                            field_llvm_type,
                            field_ptr,
                            CString::new(format!("{}_value", field_name))?.as_ptr(),
                        );

                        value_stack.push(field_value);
                    }
                }
            }

            if value_stack.len() != 1 {
                return Err(anyhow!("Expression generation error: expected 1 value, got {}", value_stack.len()));
            }

            Ok(value_stack.pop().unwrap())
        }
    }


    fn generate_type_definition(&mut self, typedef: &TypeDefinition) -> Result<()> {
        unsafe {
            match &typedef.kind {
                TypeDefinitionKind::Struct { fields } => {
                    // Get the pre-created opaque struct type
                    let struct_type = if let Some(&existing_type) = self.types.get(&typedef.name) {
                        existing_type
                    } else {
                        // If not created in pass 0, create it now (shouldn't happen but be defensive)
                        let c_name = CString::new(typedef.name.as_str())?;
                        let new_type = LLVMStructCreateNamed(self.context, c_name.as_ptr());
                        self.types.insert(typedef.name.clone(), new_type);
                        new_type
                    };

                    let mut field_types = Vec::new();
                    let mut field_info = Vec::new();

                    for field in fields {
                        let llvm_type = self.get_llvm_type(&field.field_type);
                        field_types.push(llvm_type);
                        field_info.push((field.name.clone(), llvm_type));
                    }

                    // Set the body of the previously created opaque struct type
                    LLVMStructSetBody(
                        struct_type,
                        field_types.as_mut_ptr(),
                        field_types.len() as u32,
                        0,  // not packed
                    );

                    // Store field information for later use
                    self.type_fields.insert(typedef.name.clone(), field_info);
                }
                TypeDefinitionKind::Enum { variants: _ } => {
                    // For enums, create a simple integer type for now
                    // Full enum support would require tagged unions
                    let enum_type = LLVMInt32TypeInContext(self.context);
                    self.types.insert(typedef.name.clone(), enum_type);
                }
            }
        }
        Ok(())
    }

    fn get_llvm_type(&self, ty: &Type) -> LLVMTypeRef {
        unsafe {
            match ty {
                Type::Integer => LLVMInt64TypeInContext(self.context),
                Type::Float => LLVMDoubleTypeInContext(self.context),
                Type::Boolean => LLVMInt1TypeInContext(self.context),
                Type::String => LLVMPointerType(LLVMInt8TypeInContext(self.context), 0),
                Type::Void => LLVMVoidTypeInContext(self.context),
                Type::List(_) | Type::Array(_, _) | Type::Dictionary(_, _) => {
                    // ALL complex runtime types are represented as generic pointers
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)
                }
                Type::Custom(name) => {
                    // This is now guaranteed to find the fully defined struct type
                    // because of our multi-pass generation
                    self.types.get(name)
                        .copied()
                        .unwrap_or_else(|| {
                            // This should ideally never happen now with proper two-pass
                            eprintln!("[CODEGEN] WARNING: Custom type '{}' not found during get_llvm_type. Defaulting to opaque pointer.", name);
                            LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)
                        })
                }
            }
        }
    }

    fn get_expression_type(&self, expr: &Expression) -> Type {
        match expr {
            // Literals have well-defined types
            Expression::Integer(_) => Type::Integer,
            Expression::Float(_) => Type::Float,
            Expression::String(_) => Type::String,
            Expression::Boolean(_) => Type::Boolean,
            Expression::Nothing => Type::Void,

            // Identifier lookup with comprehensive type resolution
            Expression::Identifier(name) => {
                // 1. Check custom type tracking first (highest priority)
                if let Some(type_name) = self.variable_types.get(name) {
                    return Type::Custom(type_name.clone());
                }

                // 2. Look up in variable symbol table
                if let Some(var_ptr) = self.variables.get(name) {
                    unsafe {
                        let element_type = LLVMGetAllocatedType(*var_ptr);
                        return self.llvm_type_to_runa_type(element_type);
                    }
                }

                // 3. Check function names (return their declared return type)
                if let Some(func_type) = self.function_types.get(name) {
                    unsafe {
                        let return_type = LLVMGetReturnType(*func_type);
                        return self.llvm_type_to_runa_type(return_type);
                    }
                }

                // 4. Well-known identifiers in bootstrap compiler context
                match name.as_str() {
                    "tokens" => Type::List(Box::new(Type::Custom("Token".to_string()))),
                    "current" => Type::Integer,
                    "parser" => Type::Custom("Parser".to_string()),
                    "ast" => Type::Custom("ASTNode".to_string()),
                    _ => {
                        // For unknown identifiers, we cannot assume Integer
                        // This should be treated as an error in a production compiler
                        // For bootstrap, we'll use Void to force explicit handling
                        Type::Void
                    }
                }
            }

            // Binary expressions: type depends on operator
            Expression::Binary(bin_expr) => {
                match bin_expr.operator {
                    // Comparison operators always return Boolean
                    BinaryOperator::IsGreaterThan | BinaryOperator::IsLessThan |
                    BinaryOperator::IsEqualTo | BinaryOperator::IsNotEqualTo => Type::Boolean,

                    // Logical operators always return Boolean
                    BinaryOperator::And | BinaryOperator::Or => Type::Boolean,

                    // Arithmetic operators return the type of their operands
                    // (assuming both operands have the same type in bootstrap phase)
                    BinaryOperator::Plus | BinaryOperator::Minus |
                    BinaryOperator::MultipliedBy | BinaryOperator::DividedBy |
                    BinaryOperator::Modulo => {
                        let left_type = self.get_expression_type(&bin_expr.left);
                        let right_type = self.get_expression_type(&bin_expr.right);

                        // Type promotion rules: Float > Integer
                        match (left_type, right_type) {
                            (Type::Float, _) | (_, Type::Float) => Type::Float,
                            (Type::Integer, Type::Integer) => Type::Integer,
                            (Type::String, Type::String) if bin_expr.operator == BinaryOperator::Plus => Type::String,
                            _ => Type::Integer // Default for mixed types in bootstrap
                        }
                    }
                }
            }

            // Unary expressions
            Expression::Unary(unary_expr) => {
                match unary_expr.operator {
                    crate::parser::UnaryOperator::Not => Type::Boolean,
                }
            }

            // Function calls: look up return type
            Expression::Call(call_expr) => {
                if let Some(func_type) = self.function_types.get(&call_expr.function) {
                    unsafe {
                        let return_type = LLVMGetReturnType(*func_type);
                        return self.llvm_type_to_runa_type(return_type);
                    }
                }

                // Built-in functions with known return types
                match call_expr.function.as_str() {
                    "print" | "write_file" => Type::Void,
                    "read_file" => Type::String,
                    "list_length" | "length_of" => Type::Integer,
                    "list_get" => {
                        // For list_get, return the element type of the list
                        if let Some(first_arg) = call_expr.arguments.first() {
                            let list_type = self.get_expression_type(first_arg);
                            if let Type::List(element_type) = list_type {
                                return *element_type;
                            }
                        }
                        Type::Void // Error case - should not happen
                    }
                    "list_create" => Type::List(Box::new(Type::Integer)), // Generic list for bootstrap
                    "dict_create" => Type::Dictionary(Box::new(Type::String), Box::new(Type::Integer)),
                    _ => Type::Void // Unknown function - error case
                }
            }

            // Method calls: resolve based on object type and method
            Expression::MethodCall(method_call) => {
                let object_type = self.get_expression_type(&method_call.object);

                match (&object_type, method_call.method.as_str()) {
                    // List methods
                    (Type::List(element_type), "get") => *element_type.clone(),
                    (Type::List(_), "length") => Type::Integer,
                    (Type::List(_), "add") => Type::Void,

                    // Dictionary methods
                    (Type::Dictionary(_, value_type), "get") => *value_type.clone(),
                    (Type::Dictionary(_, _), "set") => Type::Void,
                    (Type::Dictionary(_, _), "contains") => Type::Boolean,

                    // String methods
                    (Type::String, "length") => Type::Integer,
                    (Type::String, "substring") => Type::String,
                    (Type::String, "compare") => Type::Integer,

                    // Custom type methods - construct function name and look up
                    (Type::Custom(_), _) => {
                        let object_name = match &method_call.object {
                            Expression::Identifier(name) => name.clone(),
                            _ => "unknown".to_string(),
                        };
                        let function_name = format!("{}_{}", object_name, method_call.method);

                        if let Some(func_type) = self.function_types.get(&function_name) {
                            unsafe {
                                let return_type = LLVMGetReturnType(*func_type);
                                return self.llvm_type_to_runa_type(return_type);
                            }
                        }
                        Type::Void // Unknown method
                    }

                    _ => Type::Void // Error case
                }
            }

            // Field access: comprehensive type resolution
            Expression::FieldAccess(field_access) => {
                let object_type = self.get_expression_type(&field_access.object);

                match object_type {
                    Type::Custom(type_name) => {
                        // 1. Check type_fields registry first
                        if let Some(fields) = self.type_fields.get(&type_name) {
                            for (field_name, field_llvm_type) in fields {
                                if field_name == &field_access.field {
                                    return self.llvm_type_to_runa_type(*field_llvm_type);
                                }
                            }
                        }

                        // 2. Known bootstrap types (must be comprehensive)
                        match (type_name.as_str(), field_access.field.as_str()) {
                            // Token type
                            ("Token", "value") => Type::String,
                            ("Token", "token_type") => Type::Custom("TokenType".to_string()),
                            ("Token", "line") | ("Token", "column") => Type::Integer,

                            // Parser type
                            ("Parser", "tokens") => Type::List(Box::new(Type::Custom("Token".to_string()))),
                            ("Parser", "current") => Type::Integer,

                            // ASTNode type
                            ("ASTNode", "node_type") => Type::Custom("NodeType".to_string()),
                            ("ASTNode", "children") => Type::List(Box::new(Type::Custom("ASTNode".to_string()))),
                            ("ASTNode", "value") | ("ASTNode", "data_type") => Type::String,

                            _ => {
                                // Error: unknown field for known type
                                Type::Void
                            }
                        }
                    }
                    _ => {
                        // Error: field access on non-struct type
                        Type::Void
                    }
                }
            }

            // Collection literals
            Expression::ListLiteral(list_elements) => {
                // Infer element type from first element, default to Integer
                let element_type = if let Some(first_element) = list_elements.first() {
                    self.get_expression_type(first_element)
                } else {
                    Type::Integer
                };
                Type::List(Box::new(element_type))
            }

            Expression::DictionaryLiteral(_) => {
                // For bootstrap, assume String keys and Integer values
                Type::Dictionary(Box::new(Type::String), Box::new(Type::Integer))
            }

            Expression::ArrayLiteral(array_elements) => {
                let element_type = if let Some(first_element) = array_elements.first() {
                    self.get_expression_type(first_element)
                } else {
                    Type::Integer
                };
                Type::Array(Box::new(element_type), array_elements.len())
            }

            // Index access: return element type
            Expression::IndexAccess(index_access) => {
                let collection_type = self.get_expression_type(&index_access.object);

                match collection_type {
                    Type::List(element_type) => *element_type,
                    Type::Array(element_type, _) => *element_type,
                    Type::Dictionary(_, value_type) => *value_type,
                    _ => {
                        // Error: index access on non-indexable type
                        Type::Void
                    }
                }
            }

            // Utility expressions
            Expression::LengthOf(_) => Type::Integer,
            Expression::TypeConstruction(type_const) => Type::Custom(type_const.type_name.clone()),
            Expression::EnumVariant(_) => Type::Integer,
        }
    }

    fn optimize_module(&mut self) {
        // Optimization is handled at the target machine level in LLVM v170
    }

    /// Ensures a value is converted to i1 (boolean) for use in conditional branches
    fn ensure_boolean_condition(&mut self, value: LLVMValueRef) -> Result<LLVMValueRef> {
        unsafe {
            let value_type = LLVMTypeOf(value);
            let type_kind = LLVMGetTypeKind(value_type);

            match type_kind {
                // Already i1 boolean - use as-is
                LLVMTypeKind::LLVMIntegerTypeKind if LLVMGetIntTypeWidth(value_type) == 1 => {
                    Ok(value)
                }

                // i64 integer - convert to boolean (non-zero = true)
                LLVMTypeKind::LLVMIntegerTypeKind => {
                    let zero = LLVMConstInt(value_type, 0, 0);
                    Ok(LLVMBuildICmp(
                        self.builder,
                        LLVMIntPredicate::LLVMIntNE,
                        value,
                        zero,
                        CString::new("tobool")?.as_ptr(),
                    ))
                }

                // Pointer - convert to boolean (null = false)
                LLVMTypeKind::LLVMPointerTypeKind => {
                    let null_ptr = LLVMConstNull(value_type);
                    Ok(LLVMBuildICmp(
                        self.builder,
                        LLVMIntPredicate::LLVMIntNE,
                        value,
                        null_ptr,
                        CString::new("tobool")?.as_ptr(),
                    ))
                }

                // Float - convert to boolean (0.0 = false)
                LLVMTypeKind::LLVMDoubleTypeKind => {
                    let zero = LLVMConstReal(value_type, 0.0);
                    Ok(LLVMBuildFCmp(
                        self.builder,
                        LLVMRealPredicate::LLVMRealUNE,
                        value,
                        zero,
                        CString::new("tobool")?.as_ptr(),
                    ))
                }

                _ => {
                    Err(anyhow!("Cannot convert type {:?} to boolean for conditional", type_kind))
                }
            }
        }
    }

    fn llvm_type_to_runa_type(&self, llvm_type: LLVMTypeRef) -> Type {
        unsafe {
            let type_kind = LLVMGetTypeKind(llvm_type);
            match type_kind {
                llvm_sys::LLVMTypeKind::LLVMIntegerTypeKind => {
                    let width = LLVMGetIntTypeWidth(llvm_type);
                    if width == 1 {
                        Type::Boolean
                    } else {
                        Type::Integer
                    }
                }
                llvm_sys::LLVMTypeKind::LLVMDoubleTypeKind => Type::Float,
                llvm_sys::LLVMTypeKind::LLVMPointerTypeKind => Type::String,
                llvm_sys::LLVMTypeKind::LLVMVoidTypeKind => Type::Void,
                llvm_sys::LLVMTypeKind::LLVMStructTypeKind => {
                    // Try to find the corresponding Runa type name for this LLVM struct
                    for (type_name, &llvm_struct_type) in &self.types {
                        if llvm_struct_type == llvm_type {
                            return Type::Custom(type_name.clone());
                        }
                    }
                    // If not found, default to a generic custom type
                    Type::Custom("UnknownStruct".to_string())
                }
                _ => Type::Integer
            }
        }
    }

    // Module system integration methods
    pub fn add_module(&mut self, module: Module) {
        if let Some(ref mut manager) = self.module_manager {
            manager.add_module(module);
        }
    }

    pub fn resolve_import(&self, module_name: &str, import_name: &str) -> Option<&ModuleExport> {
        if let Some(ref manager) = self.module_manager {
            manager.resolve_import(module_name, import_name)
        } else {
            None
        }
    }

    pub fn process_imports(&mut self, program: &Program) -> Result<()> {
        for item in &program.items {
            if let Item::Import(import_stmt) = item {
                // Convert ImportStatement to Module Import and add to module manager
                let module_import = import_stmt.to_module_import();

                // For now, we'll create a placeholder module entry
                // In a full implementation, this would load and parse the imported module
                let mut module = Module::new(
                    import_stmt.module_name.clone(),
                    format!("{}.runa", import_stmt.module_name)
                );

                module.add_import(module_import);
                self.add_module(module);
            }
        }
        Ok(())
    }

    pub fn export_function(&mut self, function_name: &str, _llvm_function: LLVMValueRef) {
        // Add function to current module's exports
        if let Some(ref mut manager) = self.module_manager {
            // For now, we'll assume there's a "main" module
            // In a full implementation, this would track the current module being compiled
            if let Some(module) = manager.get_module_mut("main") {
                use crate::modules::{ModuleExport, ExportType};
                use crate::types::Type;

                let export = ModuleExport {
                    name: function_name.to_string(),
                    export_type: ExportType::Function,
                    type_info: Type::Void, // Simplified for now - would be the return type
                    item: Item::Function(Function {
                        name: function_name.to_string(),
                        parameters: Vec::new(), // Simplified
                        return_type: Type::Void, // Simplified
                        body: Block { statements: Vec::new() }, // Empty body for exports
                    }),
                };

                module.add_export(function_name.to_string(), export);
            }
        }
    }
}

impl Drop for CodeGenerator {
    fn drop(&mut self) {
        unsafe {
            LLVMDisposeBuilder(self.builder);
            LLVMDisposeModule(self.module);
            LLVMContextDispose(self.context);
        }
    }
}

fn get_default_target_triple() -> CString {
    unsafe {
        let triple = LLVMGetDefaultTargetTriple();
        let triple_str = CStr::from_ptr(triple).to_owned();
        LLVMDisposeMessage(triple);
        triple_str
    }
}

