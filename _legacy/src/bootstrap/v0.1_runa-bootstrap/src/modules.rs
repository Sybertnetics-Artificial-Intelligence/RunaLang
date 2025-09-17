use std::collections::HashMap;
use crate::parser::{Program, Item};
use crate::types::Type;

#[derive(Debug, Clone)]
pub struct ModuleExport {
    pub name: String,
    pub export_type: ExportType,
    pub type_info: Type,
    pub item: Item,
}

#[derive(Debug, Clone)]
pub enum ExportType {
    Function,
    Type,
    Constant,
    Process,
}

#[derive(Debug, Clone)]
pub struct Import {
    pub module_name: String,
    pub imported_items: Vec<String>,
    pub alias: Option<String>,
}

#[derive(Debug, Clone)]
pub struct Module {
    pub name: String,
    pub file_path: String,
    pub exports: HashMap<String, ModuleExport>,
    pub imports: Vec<Import>,
    pub program: Option<Program>,
    pub is_compiled: bool,
}

impl Module {
    pub fn new(name: String, file_path: String) -> Self {
        Module {
            name,
            file_path,
            exports: HashMap::new(),
            imports: Vec::new(),
            program: None,
            is_compiled: false,
        }
    }

    pub fn add_export(&mut self, name: String, export: ModuleExport) {
        self.exports.insert(name, export);
    }

    pub fn add_import(&mut self, import: Import) {
        self.imports.push(import);
    }

    pub fn get_export(&self, name: &str) -> Option<&ModuleExport> {
        self.exports.get(name)
    }

    pub fn has_export(&self, name: &str) -> bool {
        self.exports.contains_key(name)
    }

    pub fn set_program(&mut self, program: Program) {
        self.program = Some(program);
    }

    pub fn mark_compiled(&mut self) {
        self.is_compiled = true;
    }
}

#[derive(Debug)]
pub struct ModuleManager {
    modules: HashMap<String, Module>,
    module_search_paths: Vec<String>,
}

impl ModuleManager {
    pub fn new() -> Self {
        ModuleManager {
            modules: HashMap::new(),
            module_search_paths: vec!["./".to_string()],
        }
    }

    pub fn add_module(&mut self, module: Module) {
        self.modules.insert(module.name.clone(), module);
    }

    pub fn get_module(&self, name: &str) -> Option<&Module> {
        self.modules.get(name)
    }

    pub fn get_module_mut(&mut self, name: &str) -> Option<&mut Module> {
        self.modules.get_mut(name)
    }

    pub fn resolve_import(&self, module_name: &str, import_name: &str) -> Option<&ModuleExport> {
        if let Some(module) = self.get_module(module_name) {
            module.get_export(import_name)
        } else {
            None
        }
    }

    pub fn add_search_path(&mut self, path: String) {
        self.module_search_paths.push(path);
    }

    pub fn find_module_file(&self, module_name: &str) -> Option<String> {
        for path in &self.module_search_paths {
            let module_file = format!("{}/{}.runa", path, module_name);
            if std::path::Path::new(&module_file).exists() {
                return Some(module_file);
            }
        }
        None
    }

    pub fn check_circular_dependencies(&self, module_name: &str, visited: &mut Vec<String>) -> bool {
        if visited.contains(&module_name.to_string()) {
            return true;
        }

        visited.push(module_name.to_string());

        if let Some(module) = self.get_module(module_name) {
            for import in &module.imports {
                if self.check_circular_dependencies(&import.module_name, visited) {
                    return true;
                }
            }
        }

        visited.pop();
        false
    }

    pub fn get_dependency_order(&self) -> Result<Vec<String>, String> {
        let mut visited = Vec::new();
        let mut order = Vec::new();

        for module_name in self.modules.keys() {
            if self.check_circular_dependencies(module_name, &mut vec![]) {
                return Err(format!("Circular dependency detected involving module: {}", module_name));
            }
        }

        for module_name in self.modules.keys() {
            self.topological_sort(module_name, &mut visited, &mut order);
        }

        Ok(order)
    }

    fn topological_sort(&self, module_name: &str, visited: &mut Vec<String>, order: &mut Vec<String>) {
        if visited.contains(&module_name.to_string()) {
            return;
        }

        visited.push(module_name.to_string());

        if let Some(module) = self.get_module(module_name) {
            for import in &module.imports {
                self.topological_sort(&import.module_name, visited, order);
            }
        }

        if !order.contains(&module_name.to_string()) {
            order.push(module_name.to_string());
        }
    }
}