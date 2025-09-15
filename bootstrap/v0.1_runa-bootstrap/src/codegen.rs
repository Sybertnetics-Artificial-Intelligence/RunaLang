use anyhow::{anyhow, Result};
use llvm_sys::core::*;
use llvm_sys::prelude::*;
use llvm_sys::target::*;
use llvm_sys::target_machine::*;
use llvm_sys::analysis::*;
use llvm_sys::analysis::LLVMVerifierFailureAction::*;
use llvm_sys::LLVMIntPredicate;
use std::collections::HashMap;
use std::ffi::{CString, CStr};
use std::ptr;

use crate::parser::*;
use crate::types::Type;

pub struct CodeGenerator {
    context: LLVMContextRef,
    module: LLVMModuleRef,
    builder: LLVMBuilderRef,

    // Symbol tables
    functions: HashMap<String, LLVMValueRef>,
    function_types: HashMap<String, LLVMTypeRef>,  // Store function types separately
    variables: HashMap<String, LLVMValueRef>,
    types: HashMap<String, LLVMTypeRef>,

    // Current function context
    current_function: Option<LLVMValueRef>,
    current_block: Option<LLVMBasicBlockRef>,

    // Optimization level
    opt_level: u8,
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
                types: HashMap::new(),
                current_function: None,
                current_block: None,
                opt_level,
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

            // list_append: Adds element to end of list
            let list_append_type = LLVMFunctionType(
                LLVMVoidTypeInContext(self.context),
                [
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0), // list
                    LLVMInt64TypeInContext(self.context), // value (simplified to int for now)
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
        // First pass: Declare all functions (forward declarations)
        for item in &program.items {
            if let Item::Function(func) = item {
                self.declare_function(func)?;
            }
        }

        // Second pass: Generate all items with bodies
        for item in &program.items {
            match item {
                Item::Function(func) => self.generate_function_body(func)?,
                Item::TypeDef(typedef) => self.generate_type_definition(typedef)?,
                Item::Import(_) => {} // Imports handled separately
            }
        }
        Ok(())
    }

    fn declare_function(&mut self, func: &Function) -> Result<()> {
        unsafe {
            // Create function type
            let mut param_types = Vec::new();
            for param in &func.parameters {
                param_types.push(self.get_llvm_type(&param.param_type));
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
        }
        Ok(())
    }

    fn generate_function_body(&mut self, func: &Function) -> Result<()> {
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
            self.variables.clear();

            // Bind parameters
            for (i, param) in func.parameters.iter().enumerate() {
                let llvm_param = LLVMGetParam(llvm_func, i as u32);
                let param_name = CString::new(param.name.clone())?;
                LLVMSetValueName2(llvm_param, param_name.as_ptr(), param.name.len());

                // Allocate stack space for parameter
                let alloca = LLVMBuildAlloca(
                    self.builder,
                    self.get_llvm_type(&param.param_type),
                    param_name.as_ptr(),
                );
                LLVMBuildStore(self.builder, llvm_param, alloca);
                self.variables.insert(param.name.clone(), alloca);
            }

            // Generate function body
            self.generate_block(&func.body)?;

            // Add default return if needed
            if func.return_type == Type::Void {
                LLVMBuildRetVoid(self.builder);
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
            }
        }
    }

    fn generate_let(&mut self, let_stmt: &LetStatement) -> Result<()> {
        unsafe {
            let value = self.generate_expression(&let_stmt.value)?;

            let var_type = self.get_expression_type(&let_stmt.value);

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
                    } else {
                        return Err(anyhow!("Undefined variable: {}", name));
                    }
                }
                Expression::FieldAccess(field_access) => {
                    // Generate field store
                    let _object = self.generate_expression(&field_access.object)?;
                    // Field access requires struct field tracking
                    return Err(anyhow!("Field access not yet implemented in v0.1"));
                }
                _ => return Err(anyhow!("Invalid assignment target")),
            }
        }
        Ok(())
    }

    fn generate_if(&mut self, if_stmt: &IfStatement) -> Result<()> {
        unsafe {
            let condition = self.generate_expression(&if_stmt.condition)?;

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
                let elseif_condition = self.generate_expression(&else_if_branch.condition)?;

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
            let condition = self.generate_expression(&while_stmt.condition)?;
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
            let value = self.generate_expression(&add_stmt.value)?;
            let list = self.generate_expression(&add_stmt.list)?;

            // Call list_append
            let list_append = *self.functions.get("list_append")
                .ok_or_else(|| anyhow!("list_append function not found"))?;
            LLVMBuildCall2(
                self.builder,
                *self.function_types.get("list_append").unwrap(),
                list_append,
                [list, value].as_ptr() as *mut _,
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
            if let Some(value) = &ret_stmt.value {
                let ret_value = self.generate_expression(value)?;
                LLVMBuildRet(self.builder, ret_value);
            } else {
                LLVMBuildRetVoid(self.builder);
            }
        }
        Ok(())
    }

    fn generate_expression(&mut self, expr: &Expression) -> Result<LLVMValueRef> {
        unsafe {
            match expr {
                Expression::Integer(n) => {
                    Ok(LLVMConstInt(LLVMInt64TypeInContext(self.context), *n as u64, 1))
                }
                Expression::Float(f) => {
                    Ok(LLVMConstReal(LLVMDoubleTypeInContext(self.context), *f))
                }
                Expression::Boolean(b) => {
                    Ok(LLVMConstInt(LLVMInt1TypeInContext(self.context), if *b { 1 } else { 0 }, 0))
                }
                Expression::String(s) => {
                    let str_const = CString::new(s.clone())?;
                    let global_str = LLVMBuildGlobalStringPtr(
                        self.builder,
                        str_const.as_ptr(),
                        CString::new("str")?.as_ptr(),
                    );
                    Ok(global_str)
                }
                Expression::Identifier(name) => {
                    if let Some(&var_ptr) = self.variables.get(name) {
                        let load_name = CString::new(format!("{}.load", name))?;

                        // Get the actual type of the allocated variable
                        let elem_type = LLVMGetAllocatedType(var_ptr);

                        let result = LLVMBuildLoad2(
                            self.builder,
                            elem_type,
                            var_ptr,
                            load_name.as_ptr(),
                        );
                        Ok(result)
                    } else {
                        Err(anyhow!("Undefined variable: {}", name))
                    }
                }
                Expression::Binary(bin_expr) => self.generate_binary_expression(bin_expr),
                Expression::Unary(un_expr) => self.generate_unary_expression(un_expr),
                Expression::Call(call_expr) => self.generate_call_expression(call_expr),
                Expression::MethodCall(method_call) => self.generate_method_call_expression(method_call),
                Expression::FieldAccess(field_access) => {
                    // Get the object (should be a struct pointer)
                    let _object = self.generate_expression(&field_access.object)?;

                    // For now, we'll need to track field indices manually
                    // In a full implementation, we'd have a field name -> index mapping
                    // For testing, assume field order matches definition order

                    // This is a simplified implementation - we need the type info
                    // to properly resolve field indices
                    Err(anyhow!("Field access requires type tracking - deferred to v0.2"))
                }
                Expression::ListLiteral(elements) => {
                    // Create a new list
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

                    // Append each element
                    let list_append = *self.functions.get("list_append")
                        .ok_or_else(|| anyhow!("list_append function not found"))?;
                    let list_append_type = *self.function_types.get("list_append").unwrap();
                    for element in elements {
                        let value = self.generate_expression(element)?;
                        LLVMBuildCall2(
                            self.builder,
                            list_append_type,
                            list_append,
                            [list, value].as_ptr() as *mut _,
                            2,
                            CString::new("")?.as_ptr(),
                        );
                    }

                    Ok(list)
                }
                Expression::IndexAccess(index_access) => {
                    let object = self.generate_expression(&index_access.object)?;
                    let index = self.generate_expression(&index_access.index)?;

                    // Call list_get function
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
                    Ok(result)
                }
                Expression::LengthOf(expr) => {
                    let object = self.generate_expression(expr)?;

                    // Call list_length function
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
                    Ok(result)
                }
                Expression::DictionaryLiteral(_) => {
                    // Dictionary support not implemented in this simplified version
                    Err(anyhow!("Dictionary literals not yet implemented in v0.1"))
                }
                Expression::ArrayLiteral(_) => {
                    // Array support not implemented in this simplified version
                    Err(anyhow!("Array literals not yet implemented in v0.1"))
                }
                Expression::TypeConstruction(type_const) => {
                    // Get the struct type
                    let struct_type = *self.types.get(&type_const.type_name)
                        .ok_or_else(|| anyhow!("Type '{}' not found", type_const.type_name))?;

                    // Allocate memory for the struct
                    let struct_ptr = LLVMBuildAlloca(
                        self.builder,
                        struct_type,
                        CString::new("struct_instance")?.as_ptr(),
                    );

                    // Initialize fields
                    for (i, (field_name, field_value)) in type_const.fields.iter().enumerate() {
                        let value = self.generate_expression(field_value)?;
                        let field_ptr = LLVMBuildStructGEP2(
                            self.builder,
                            struct_type,
                            struct_ptr,
                            i as u32,
                            CString::new(format!("{}_ptr", field_name))?.as_ptr(),
                        );
                        LLVMBuildStore(self.builder, value, field_ptr);
                    }

                    // Return the pointer to the struct
                    Ok(struct_ptr)
                }
                Expression::Nothing => {
                    Ok(LLVMConstNull(LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)))
                }
            }
        }
    }

    fn generate_binary_expression(&mut self, bin_expr: &BinaryExpression) -> Result<LLVMValueRef> {
        unsafe {
            let left = self.generate_expression(&bin_expr.left)?;
            let right = self.generate_expression(&bin_expr.right)?;

            let result = match bin_expr.operator {
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

            Ok(result)
        }
    }

    fn generate_unary_expression(&mut self, un_expr: &UnaryExpression) -> Result<LLVMValueRef> {
        unsafe {
            let operand = self.generate_expression(&un_expr.operand)?;

            match un_expr.operator {
                UnaryOperator::Not => {
                    Ok(LLVMBuildNot(self.builder, operand, CString::new("not")?.as_ptr()))
                }
            }
        }
    }

    fn generate_call_expression(&mut self, call_expr: &CallExpression) -> Result<LLVMValueRef> {
        unsafe {
            let func = *self.functions.get(&call_expr.function)
                .ok_or_else(|| anyhow!("Undefined function: {}", call_expr.function))?;

            let mut args = Vec::new();
            for (i, arg) in call_expr.arguments.iter().enumerate() {
                let mut arg_value = self.generate_expression(arg)?;

                // Special handling for character functions that need i8 arguments
                if (call_expr.function == "is_digit" || call_expr.function == "is_letter") && i == 0 {
                    // Cast i64 to i8 for character functions
                    arg_value = LLVMBuildTrunc(
                        self.builder,
                        arg_value,
                        LLVMInt8TypeInContext(self.context),
                        CString::new("char_cast")?.as_ptr(),
                    );
                }

                args.push(arg_value);
            }

            // Get the stored function type
            let func_type = *self.function_types.get(&call_expr.function)
                .ok_or_else(|| anyhow!("Function type not found: {}", call_expr.function))?;

            let result = LLVMBuildCall2(
                self.builder,
                func_type,
                func,
                args.as_ptr() as *mut _,
                args.len() as u32,
                CString::new("call")?.as_ptr(),
            );

            Ok(result)
        }
    }

    fn generate_method_call_expression(&mut self, method_call: &MethodCallExpression) -> Result<LLVMValueRef> {
        // For method calls like Lexer.tokenize(source), we treat them as function calls
        // with a naming convention: object_method
        // So Lexer.tokenize becomes "Lexer_tokenize"

        // First, get the object name (only support simple identifiers for now)
        let object_name = match &method_call.object {
            Expression::Identifier(name) => name.clone(),
            _ => return Err(anyhow!("Method calls currently only supported on simple identifiers")),
        };

        // Create the function name using object_method convention
        let function_name = format!("{}_{}", object_name, method_call.method);

        // Create a CallExpression and delegate to the existing call handler
        let call_expr = CallExpression {
            function: function_name,
            arguments: method_call.arguments.clone(),
        };

        self.generate_call_expression(&call_expr)
    }

    fn generate_type_definition(&mut self, typedef: &TypeDefinition) -> Result<()> {
        unsafe {
            match &typedef.kind {
                TypeDefinitionKind::Struct { fields } => {
                    let mut field_types = Vec::new();
                    for field in fields {
                        field_types.push(self.get_llvm_type(&field.field_type));
                    }

                    let struct_type = LLVMStructTypeInContext(
                        self.context,
                        field_types.as_ptr() as *mut _,
                        field_types.len() as u32,
                        0,
                    );

                    self.types.insert(typedef.name.clone(), struct_type);
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
                    // For now, represent complex types as opaque pointers
                    LLVMPointerType(LLVMInt8TypeInContext(self.context), 0)
                }
                Type::Custom(name) => {
                    self.types.get(name)
                        .copied()
                        .unwrap_or_else(|| LLVMPointerType(LLVMInt8TypeInContext(self.context), 0))
                }
            }
        }
    }

    fn get_expression_type(&self, expr: &Expression) -> Type {
        match expr {
            Expression::Integer(_) => Type::Integer,
            Expression::Float(_) => Type::Float,
            Expression::String(_) => Type::String,
            Expression::Boolean(_) => Type::Boolean,
            Expression::Nothing => Type::Void,
            Expression::Identifier(name) => {
                // Look up variable type in symbol table
                if let Some(var_ptr) = self.variables.get(name) {
                    unsafe {
                        // Get the element type since variables are allocas (pointers)
                        let element_type = LLVMGetAllocatedType(*var_ptr);
                        self.llvm_type_to_runa_type(element_type)
                    }
                } else if self.functions.contains_key(name) {
                    // It's a function name, return a default
                    Type::Integer
                } else {
                    // Unknown identifier
                    Type::Integer
                }
            }
            Expression::Binary(bin_expr) => {
                match bin_expr.operator {
                    BinaryOperator::IsGreaterThan | BinaryOperator::IsLessThan |
                    BinaryOperator::IsEqualTo | BinaryOperator::IsNotEqualTo |
                    BinaryOperator::And | BinaryOperator::Or => Type::Boolean,
                    _ => self.get_expression_type(&bin_expr.left),
                }
            }
            Expression::Unary(_) => Type::Boolean,
            Expression::Call(call_expr) => {
                // Look up function return type
                if let Some(func_type) = self.function_types.get(&call_expr.function) {
                    unsafe {
                        let return_type = LLVMGetReturnType(*func_type);
                        self.llvm_type_to_runa_type(return_type)
                    }
                } else {
                    // Unknown function
                    Type::Integer
                }
            }
            Expression::MethodCall(method_call) => {
                // For method calls, construct the function name and look up its type
                let object_name = match &method_call.object {
                    Expression::Identifier(name) => name.clone(),
                    _ => return Type::Integer, // Default for complex objects
                };
                let function_name = format!("{}_{}", object_name, method_call.method);

                if let Some(func_type) = self.function_types.get(&function_name) {
                    unsafe {
                        let return_type = LLVMGetReturnType(*func_type);
                        self.llvm_type_to_runa_type(return_type)
                    }
                } else {
                    // Unknown method
                    Type::Integer
                }
            }
            Expression::FieldAccess(_) => {
                // Field access requires full struct field type tracking
                // Not implemented in v0.1
                Type::Integer
            }
            Expression::ListLiteral(_) => Type::List(Box::new(Type::Integer)),
            Expression::DictionaryLiteral(_) => {
                Type::Dictionary(Box::new(Type::String), Box::new(Type::Integer))
            }
            Expression::ArrayLiteral(_) => Type::Array(Box::new(Type::Integer), 0),
            Expression::IndexAccess(_) => Type::Integer,
            Expression::LengthOf(_) => Type::Integer,
            Expression::TypeConstruction(type_const) => Type::Custom(type_const.type_name.clone()),
        }
    }

    fn optimize_module(&mut self) {
        // Optimization is handled at the target machine level in LLVM v170
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
                _ => Type::Integer
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

