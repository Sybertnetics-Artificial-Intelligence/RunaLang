"""
Runa API Documentation Generator

Generates documentation from Runa source code by analyzing AST nodes
and extracting function signatures, type information, and comments.
"""

import os
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
# Import from new architecture
from ...languages.runa.runa_parser import RunaParser
from ...core.runa_ast import *
from ...core.translation_result import TranslationStatus

@dataclass
class DocFunction:
    """Documentation for a function/process."""
    name: str
    parameters: List[tuple[str, str]]  # (name, type)
    return_type: Optional[str]
    description: str
    is_async: bool = False
    examples: List[str] = None

@dataclass
class DocModule:
    """Documentation for a module."""
    name: str
    description: str
    functions: List[DocFunction]
    exports: List[str]

class RunaDocGenerator:
    """Generates documentation from Runa source code."""
    
    def __init__(self):
        self.modules: Dict[str, DocModule] = {}
        self.parser = RunaParser()
    
    def generate_docs(self, source_path: str, output_path: str):
        """Generate documentation for all Runa files in source_path."""
        if os.path.isfile(source_path):
            self._process_file(source_path)
        else:
            self._process_directory(source_path)
        
        self._write_documentation(output_path)
    
    def _process_directory(self, directory: str):
        """Process all .runa files in a directory."""
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.runa'):
                    file_path = os.path.join(root, file)
                    self._process_file(file_path)
    
    def _process_file(self, file_path: str):
        """Process a single Runa file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Parse the source code
            parse_result = self.parser.parse(source)
            if parse_result.status != TranslationStatus.SUCCESS:
                raise Exception(f"Parse failed: {parse_result.error_message}")
            ast = parse_result.result
            
            # Extract module name from file path
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # Extract documentation
            doc_module = self._extract_module_docs(ast, module_name, source)
            self.modules[module_name] = doc_module
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    def _extract_module_docs(self, ast: Program, module_name: str, source: str) -> DocModule:
        """Extract documentation from AST."""
        functions = []
        exports = []
        description = self._extract_module_description(source)
        
        for statement in ast.statements:
            if isinstance(statement, ProcessDefinition):
                doc_func = self._extract_function_docs(statement, source)
                functions.append(doc_func)
            elif isinstance(statement, AsyncProcessDefinition):
                doc_func = self._extract_async_function_docs(statement, source)
                functions.append(doc_func)
            elif isinstance(statement, ExportStatement):
                if statement.exported_names:
                    exports.extend(statement.exported_names)
        
        return DocModule(module_name, description, functions, exports)
    
    def _extract_function_docs(self, func: ProcessDefinition, source: str) -> DocFunction:
        """Extract documentation for a regular function."""
        parameters = []
        for param in func.parameters:
            param_type = param.type_annotation.name if param.type_annotation else "Any"
            parameters.append((param.name, param_type))
        
        return_type = func.return_type.name if func.return_type else "Void"
        description = self._extract_function_description(func.name, source)
        examples = self._extract_function_examples(func.name, source)
        
        return DocFunction(
            name=func.name,
            parameters=parameters,
            return_type=return_type,
            description=description,
            is_async=False,
            examples=examples
        )
    
    def _extract_async_function_docs(self, func: AsyncProcessDefinition, source: str) -> DocFunction:
        """Extract documentation for an async function."""
        parameters = []
        for param in func.parameters:
            param_type = param.type_annotation.name if param.type_annotation else "Any"
            parameters.append((param.name, param_type))
        
        return_type = func.return_type.name if func.return_type else "Void"
        description = self._extract_function_description(func.name, source)
        examples = self._extract_function_examples(func.name, source)
        
        return DocFunction(
            name=func.name,
            parameters=parameters,
            return_type=return_type,
            description=description,
            is_async=True,
            examples=examples
        )
    
    def _extract_module_description(self, source: str) -> str:
        """Extract module description from comments at the top of the file."""
        lines = source.split('\n')
        description_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('Note:'):
                description_lines.append(line[5:].strip())
            elif line.startswith('//'):
                description_lines.append(line[2:].strip())
            elif line and not line.startswith('Note:') and not line.startswith('//'):
                break
        
        return ' '.join(description_lines) if description_lines else "No description available."
    
    def _extract_function_description(self, func_name: str, source: str) -> str:
        """Extract function description from comments before the function."""
        lines = source.split('\n')
        func_pattern = rf'.*Process called "{re.escape(func_name)}"'
        
        for i, line in enumerate(lines):
            if re.search(func_pattern, line):
                # Look for comments in the lines before
                description_lines = []
                j = i - 1
                while j >= 0:
                    prev_line = lines[j].strip()
                    if prev_line.startswith('Note:'):
                        description_lines.insert(0, prev_line[5:].strip())
                    elif prev_line.startswith('//'):
                        description_lines.insert(0, prev_line[2:].strip())
                    elif prev_line == '':
                        j -= 1
                        continue
                    else:
                        break
                    j -= 1
                
                return ' '.join(description_lines) if description_lines else "No description available."
        
        return "No description available."
    
    def _extract_function_examples(self, func_name: str, source: str) -> List[str]:
        """Extract usage examples for a function."""
        lines = source.split('\n')
        examples = []
        
        # Look for function calls
        call_pattern = rf'.*{re.escape(func_name.title().replace(" ", " "))}.*with'
        
        for line in lines:
            if re.search(call_pattern, line, re.IGNORECASE):
                examples.append(line.strip())
        
        return examples
    
    def _write_documentation(self, output_path: str):
        """Write documentation to files."""
        os.makedirs(output_path, exist_ok=True)
        
        # Generate index file
        self._write_index(output_path)
        
        # Generate individual module files
        for module_name, module in self.modules.items():
            self._write_module_docs(module, output_path)
    
    def _write_index(self, output_path: str):
        """Write the main index file."""
        index_path = os.path.join(output_path, 'index.md')
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Runa API Documentation\n\n")
            f.write("## Modules\n\n")
            
            for module_name, module in self.modules.items():
                f.write(f"- [{module_name}]({module_name}.md) - {module.description}\n")
            
            f.write("\n## Quick Reference\n\n")
            f.write("### Functions\n\n")
            
            for module_name, module in self.modules.items():
                for func in module.functions:
                    params = ", ".join([f"{name}: {type_}" for name, type_ in func.parameters])
                    async_prefix = "Async " if func.is_async else ""
                    f.write(f"- `{async_prefix}{func.name}({params}) -> {func.return_type}` - {func.description[:50]}...\n")
    
    def _write_module_docs(self, module: DocModule, output_path: str):
        """Write documentation for a single module."""
        module_path = os.path.join(output_path, f'{module.name}.md')
        
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(f"# {module.name}\n\n")
            f.write(f"{module.description}\n\n")
            
            if module.exports:
                f.write("## Exports\n\n")
                for export in module.exports:
                    f.write(f"- `{export}`\n")
                f.write("\n")
            
            if module.functions:
                f.write("## Functions\n\n")
                
                for func in module.functions:
                    self._write_function_docs(func, f)
    
    def _write_function_docs(self, func: DocFunction, file):
        """Write documentation for a single function."""
        async_prefix = "Async " if func.is_async else ""
        file.write(f"### {async_prefix}{func.name}\n\n")
        file.write(f"{func.description}\n\n")
        
        # Signature
        params = ", ".join([f"{name}: {type_}" for name, type_ in func.parameters])
        file.write(f"**Signature:** `{func.name}({params}) -> {func.return_type}`\n\n")
        
        # Parameters
        if func.parameters:
            file.write("**Parameters:**\n\n")
            for name, type_ in func.parameters:
                file.write(f"- `{name}` ({type_}): Parameter description\n")
            file.write("\n")
        
        # Return value
        if func.return_type != "Void":
            file.write(f"**Returns:** {func.return_type}\n\n")
        
        # Examples
        if func.examples:
            file.write("**Examples:**\n\n")
            for example in func.examples:
                file.write(f"```runa\n{example}\n```\n\n")
        
        file.write("---\n\n")

def main():
    """CLI entry point for the documentation generator."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Runa API documentation')
    parser.add_argument('source', help='Source directory or file')
    parser.add_argument('-o', '--output', default='docs/api', help='Output directory')
    
    args = parser.parse_args()
    
    generator = RunaDocGenerator()
    generator.generate_docs(args.source, args.output)
    print(f"Documentation generated in {args.output}")

if __name__ == '__main__':
    main()