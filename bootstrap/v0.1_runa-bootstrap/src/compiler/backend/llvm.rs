use anyhow::Result;
use llvm_sys::prelude::*;
use llvm_sys::core::*;
use llvm_sys::target::*;
use llvm_sys::target_machine::*;
use std::ffi::CString;

pub struct LLVMBackend {
    context: LLVMContextRef,
    module: LLVMModuleRef,
    builder: LLVMBuilderRef,
    target: String,
    opt_level: u8,
}

impl LLVMBackend {
    pub fn new(target: &str, opt_level: u8) -> Result<Self> {
        unsafe {
            // Initialize LLVM
            LLVM_InitializeAllTargets();
            LLVM_InitializeAllTargetMCs();
            LLVM_InitializeAllAsmPrinters();
            LLVM_InitializeAllAsmParsers();
            
            let context = LLVMContextCreate();
            let module_name = CString::new("runa_module").unwrap();
            let module = LLVMModuleCreateWithNameInContext(module_name.as_ptr(), context);
            let builder = LLVMCreateBuilderInContext(context);
            
            Ok(Self {
                context,
                module,
                builder,
                target: target.to_string(),
                opt_level,
            })
        }
    }
    
    pub fn get_context(&self) -> LLVMContextRef {
        self.context
    }
    
    pub fn get_module(&self) -> LLVMModuleRef {
        self.module
    }
    
    pub fn get_builder(&self) -> LLVMBuilderRef {
        self.builder
    }
    
    pub fn create_function(&mut self, name: &str, param_types: &[LLVMTypeRef], return_type: LLVMTypeRef) -> Result<LLVMValueRef> {
        unsafe {
            let function_name = CString::new(name).unwrap();
            let function_type = LLVMFunctionType(
                return_type,
                param_types.as_ptr() as *mut LLVMTypeRef,
                param_types.len() as u32,
                0 // Not variadic
            );
            
            let function = LLVMAddFunction(self.module, function_name.as_ptr(), function_type);
            Ok(function)
        }
    }
    
    pub fn create_basic_block(&mut self, function: LLVMValueRef, name: &str) -> Result<LLVMBasicBlockRef> {
        unsafe {
            let block_name = CString::new(name).unwrap();
            let basic_block = LLVMAppendBasicBlockInContext(
                self.context,
                function,
                block_name.as_ptr()
            );
            Ok(basic_block)
        }
    }
    
    pub fn position_builder_at_end(&mut self, basic_block: LLVMBasicBlockRef) {
        unsafe {
            LLVMPositionBuilderAtEnd(self.builder, basic_block);
        }
    }
    
    pub fn build_return(&mut self, value: Option<LLVMValueRef>) -> LLVMValueRef {
        unsafe {
            match value {
                Some(val) => LLVMBuildRet(self.builder, val),
                None => LLVMBuildRetVoid(self.builder),
            }
        }
    }
    
    pub fn build_alloca(&mut self, ty: LLVMTypeRef, name: &str) -> LLVMValueRef {
        unsafe {
            let var_name = CString::new(name).unwrap();
            LLVMBuildAlloca(self.builder, ty, var_name.as_ptr())
        }
    }
    
    pub fn build_store(&mut self, value: LLVMValueRef, ptr: LLVMValueRef) -> LLVMValueRef {
        unsafe {
            LLVMBuildStore(self.builder, value, ptr)
        }
    }
    
    pub fn build_load(&mut self, ptr: LLVMValueRef, name: &str) -> LLVMValueRef {
        unsafe {
            let load_name = CString::new(name).unwrap();
            LLVMBuildLoad2(self.builder, LLVMTypeOf(ptr), ptr, load_name.as_ptr())
        }
    }
    
    pub fn get_int32_type(&self) -> LLVMTypeRef {
        unsafe {
            LLVMInt32TypeInContext(self.context)
        }
    }
    
    pub fn get_int64_type(&self) -> LLVMTypeRef {
        unsafe {
            LLVMInt64TypeInContext(self.context)
        }
    }
    
    pub fn get_float_type(&self) -> LLVMTypeRef {
        unsafe {
            LLVMFloatTypeInContext(self.context)
        }
    }
    
    pub fn get_double_type(&self) -> LLVMTypeRef {
        unsafe {
            LLVMDoubleTypeInContext(self.context)
        }
    }
    
    pub fn get_void_type(&self) -> LLVMTypeRef {
        unsafe {
            LLVMVoidTypeInContext(self.context)
        }
    }
    
    pub fn get_pointer_type(&self, element_type: LLVMTypeRef) -> LLVMTypeRef {
        unsafe {
            LLVMPointerType(element_type, 0)
        }
    }
    
    pub fn const_int(&self, ty: LLVMTypeRef, value: u64) -> LLVMValueRef {
        unsafe {
            LLVMConstInt(ty, value, 0)
        }
    }
    
    pub fn const_real(&self, ty: LLVMTypeRef, value: f64) -> LLVMValueRef {
        unsafe {
            LLVMConstReal(ty, value)
        }
    }
    
    pub fn emit_to_file(&mut self, output_path: &str) -> Result<()> {
        unsafe {
            // Verify the module
            let mut error: *mut i8 = std::ptr::null_mut();
            let result = LLVMVerifyModule(
                self.module,
                LLVMVerifierFailureAction::LLVMPrintMessageAction,
                &mut error
            );
            
            if result != 0 {
                if !error.is_null() {
                    let error_str = std::ffi::CStr::from_ptr(error).to_string_lossy();
                    LLVMDisposeMessage(error);
                    return Err(anyhow::anyhow!("LLVM module verification failed: {}", error_str));
                }
            }
            
            // Create target machine
            let target_triple = CString::new(self.get_target_triple()).unwrap();
            LLVMSetTarget(self.module, target_triple.as_ptr());
            
            let mut target: LLVMTargetRef = std::ptr::null_mut();
            let mut error_message: *mut i8 = std::ptr::null_mut();
            
            let result = LLVMGetTargetFromTriple(
                target_triple.as_ptr(),
                &mut target,
                &mut error_message
            );
            
            if result != 0 {
                if !error_message.is_null() {
                    let error_str = std::ffi::CStr::from_ptr(error_message).to_string_lossy();
                    LLVMDisposeMessage(error_message);
                    return Err(anyhow::anyhow!("Failed to get LLVM target: {}", error_str));
                }
            }
            
            let cpu = CString::new("generic").unwrap();
            let features = CString::new("").unwrap();
            let target_machine = LLVMCreateTargetMachine(
                target,
                target_triple.as_ptr(),
                cpu.as_ptr(),
                features.as_ptr(),
                self.get_llvm_opt_level(),
                LLVMRelocMode::LLVMRelocDefault,
                LLVMCodeModel::LLVMCodeModelDefault
            );
            
            if target_machine.is_null() {
                return Err(anyhow::anyhow!("Failed to create target machine"));
            }
            
            // Emit object file
            let output_file = CString::new(output_path).unwrap();
            let mut error_message: *mut i8 = std::ptr::null_mut();
            
            let result = LLVMTargetMachineEmitToFile(
                target_machine,
                self.module,
                output_file.as_ptr() as *mut i8,
                LLVMCodeGenFileType::LLVMObjectFile,
                &mut error_message
            );
            
            LLVMDisposeTargetMachine(target_machine);
            
            if result != 0 {
                if !error_message.is_null() {
                    let error_str = std::ffi::CStr::from_ptr(error_message).to_string_lossy();
                    LLVMDisposeMessage(error_message);
                    return Err(anyhow::anyhow!("Failed to emit object file: {}", error_str));
                }
            }
            
            Ok(())
        }
    }
    
    fn get_target_triple(&self) -> String {
        match self.target.as_str() {
            "linux_x64" => "x86_64-unknown-linux-gnu".to_string(),
            "linux_arm64" => "aarch64-unknown-linux-gnu".to_string(),
            "windows_x64" => "x86_64-pc-windows-msvc".to_string(),
            "windows_arm64" => "aarch64-pc-windows-msvc".to_string(),
            "macos_x64" => "x86_64-apple-darwin".to_string(),
            "macos_arm64" => "aarch64-apple-darwin".to_string(),
            "freebsd_x64" => "x86_64-unknown-freebsd".to_string(),
            "openbsd_x64" => "x86_64-unknown-openbsd".to_string(),
            "netbsd_x64" => "x86_64-unknown-netbsd".to_string(),
            _ => "x86_64-unknown-linux-gnu".to_string(), // Default
        }
    }
    
    fn get_llvm_opt_level(&self) -> LLVMCodeGenOptLevel {
        match self.opt_level {
            0 => LLVMCodeGenOptLevel::LLVMCodeGenLevelNone,
            1 => LLVMCodeGenOptLevel::LLVMCodeGenLevelLess,
            2 => LLVMCodeGenOptLevel::LLVMCodeGenLevelDefault,
            3 => LLVMCodeGenOptLevel::LLVMCodeGenLevelAggressive,
            _ => LLVMCodeGenOptLevel::LLVMCodeGenLevelDefault,
        }
    }
}

impl Drop for LLVMBackend {
    fn drop(&mut self) {
        unsafe {
            LLVMDisposeBuilder(self.builder);
            LLVMDisposeModule(self.module);
            LLVMContextDispose(self.context);
        }
    }
}