#!/usr/bin/env python3
"""
CMake ↔ Runa AST Converter

Bidirectional conversion between CMake AST and Runa AST including:
- Build targets and libraries
- Variables and properties
- Modern CMake target-based approach
- Cross-platform build configurations
"""

from typing import List, Dict, Any, Optional, Union
from runa.core.ast import *
from .cmake_ast import *


class CMakeToRunaConverter:
    """Converts CMake AST to Runa AST."""
    
    def convert(self, cmake_node: CMakeNode) -> RunaNode:
        """Convert a CMake AST node to Runa AST."""
        if isinstance(cmake_node, CMakeFile):
            return self._convert_cmake_file(cmake_node)
        elif isinstance(cmake_node, CommandInvocation):
            return self._convert_command_invocation(cmake_node)
        elif isinstance(cmake_node, ProjectCommand):
            return self._convert_project_command(cmake_node)
        elif isinstance(cmake_node, AddExecutable):
            return self._convert_add_executable(cmake_node)
        elif isinstance(cmake_node, AddLibrary):
            return self._convert_add_library(cmake_node)
        elif isinstance(cmake_node, SetCommand):
            return self._convert_set_command(cmake_node)
        elif isinstance(cmake_node, StringLiteral):
            return self._convert_string_literal(cmake_node)
        elif isinstance(cmake_node, VariableRef):
            return self._convert_variable_ref(cmake_node)
        else:
            raise ValueError(f"Unsupported CMake node type: {type(cmake_node)}")
    
    def _convert_cmake_file(self, node: CMakeFile) -> Module:
        """Convert CMake file to Runa Module."""
        statements = []
        
        # Add minimum required version
        if node.cmake_minimum_required:
            version_decl = VariableDeclaration(
                name="cmake_minimum_required",
                value=StringLiteral(node.cmake_minimum_required),
                is_constant=True
            )
            statements.append(version_decl)
        
        # Convert statements
        for stmt in node.statements:
            runa_stmt = self.convert(stmt)
            if runa_stmt:
                statements.append(runa_stmt)
        
        return Module(
            name=node.project_name or "cmake_project",
            statements=statements,
            imports=[],
            exports=[]
        )
    
    def _convert_command_invocation(self, node: CommandInvocation) -> FunctionCall:
        """Convert command invocation to Runa function call."""
        arguments = []
        
        for arg in node.arguments:
            runa_arg = self.convert(arg)
            arguments.append(Argument(
                name=None,
                value=runa_arg,
                is_keyword=False
            ))
        
        return FunctionCall(
            function=Identifier(node.command_name),
            arguments=arguments
        )
    
    def _convert_project_command(self, node: ProjectCommand) -> FunctionCall:
        """Convert project command to Runa function call."""
        arguments = [
            Argument(name="name", value=StringLiteral(node.name), is_keyword=True)
        ]
        
        if node.version:
            arguments.append(Argument(
                name="version", 
                value=StringLiteral(node.version), 
                is_keyword=True
            ))
        
        if node.languages:
            lang_list = ListLiteral([StringLiteral(lang) for lang in node.languages])
            arguments.append(Argument(
                name="languages",
                value=lang_list,
                is_keyword=True
            ))
        
        return FunctionCall(
            function=Identifier("project"),
            arguments=arguments
        )
    
    def _convert_add_executable(self, node: AddExecutable) -> FunctionCall:
        """Convert add_executable to Runa function call."""
        arguments = [
            Argument(name="name", value=StringLiteral(node.name), is_keyword=True)
        ]
        
        if node.sources:
            sources_list = ListLiteral([StringLiteral(src) for src in node.sources])
            arguments.append(Argument(
                name="sources",
                value=sources_list,
                is_keyword=True
            ))
        
        return FunctionCall(
            function=Identifier("add_executable"),
            arguments=arguments
        )
    
    def _convert_add_library(self, node: AddLibrary) -> FunctionCall:
        """Convert add_library to Runa function call."""
        arguments = [
            Argument(name="name", value=StringLiteral(node.name), is_keyword=True),
            Argument(name="type", value=StringLiteral(node.library_type), is_keyword=True)
        ]
        
        if node.sources:
            sources_list = ListLiteral([StringLiteral(src) for src in node.sources])
            arguments.append(Argument(
                name="sources",
                value=sources_list,
                is_keyword=True
            ))
        
        return FunctionCall(
            function=Identifier("add_library"),
            arguments=arguments
        )
    
    def _convert_set_command(self, node: SetCommand) -> VariableDeclaration:
        """Convert set command to Runa variable declaration."""
        if isinstance(node.value, list):
            value = ListLiteral([StringLiteral(v) for v in node.value])
        else:
            value = StringLiteral(str(node.value))
        
        return VariableDeclaration(
            name=node.variable,
            value=value,
            is_constant=node.cache
        )
    
    def _convert_string_literal(self, node: StringLiteral) -> StringLiteral:
        """Convert string literal to Runa string literal."""
        return StringLiteral(node.value)
    
    def _convert_variable_ref(self, node: VariableRef) -> Identifier:
        """Convert variable reference to Runa identifier."""
        return Identifier(node.variable)


class RunaToCMakeConverter:
    """Converts Runa AST to CMake AST."""
    
    def convert(self, runa_node: RunaNode) -> CMakeNode:
        """Convert a Runa AST node to CMake AST."""
        if isinstance(runa_node, Module):
            return self._convert_module(runa_node)
        elif isinstance(runa_node, FunctionCall):
            return self._convert_function_call(runa_node)
        elif isinstance(runa_node, VariableDeclaration):
            return self._convert_variable_declaration(runa_node)
        elif isinstance(runa_node, StringLiteral):
            return self._convert_string_literal(runa_node)
        elif isinstance(runa_node, Identifier):
            return self._convert_identifier(runa_node)
        else:
            raise ValueError(f"Unsupported Runa node type: {type(runa_node)}")
    
    def _convert_module(self, node: Module) -> CMakeFile:
        """Convert Runa Module to CMake file."""
        statements = []
        cmake_minimum_required = None
        project_name = node.name
        
        for stmt in node.statements:
            cmake_stmt = self.convert(stmt)
            if cmake_stmt:
                statements.append(cmake_stmt)
                
                # Extract metadata
                if isinstance(stmt, VariableDeclaration) and stmt.name == "cmake_minimum_required":
                    cmake_minimum_required = stmt.value.value if hasattr(stmt.value, 'value') else None
        
        return CMakeFile(
            file_path="CMakeLists.txt",
            statements=statements,
            cmake_minimum_required=cmake_minimum_required,
            project_name=project_name
        )
    
    def _convert_function_call(self, node: FunctionCall) -> CommandInvocation:
        """Convert function call to CMake command."""
        command_name = node.function.name if isinstance(node.function, Identifier) else str(node.function)
        
        # Convert to specific command types
        if command_name == "project":
            return self._convert_to_project_command(node)
        elif command_name == "add_executable":
            return self._convert_to_add_executable(node)
        elif command_name == "add_library":
            return self._convert_to_add_library(node)
        else:
            # Generic command invocation
            arguments = []
            for arg in node.arguments:
                cmake_arg = self.convert(arg.value)
                arguments.append(cmake_arg)
            
            return CommandInvocation(
                command_name=command_name,
                arguments=arguments
            )
    
    def _convert_to_project_command(self, node: FunctionCall) -> ProjectCommand:
        """Convert to CMake project command."""
        name = ""
        version = None
        languages = []
        
        for arg in node.arguments:
            if arg.name == "name" and isinstance(arg.value, StringLiteral):
                name = arg.value.value
            elif arg.name == "version" and isinstance(arg.value, StringLiteral):
                version = arg.value.value
            elif arg.name == "languages" and isinstance(arg.value, ListLiteral):
                languages = [elem.value for elem in arg.value.elements if hasattr(elem, 'value')]
        
        return ProjectCommand(
            name=name,
            version=version,
            languages=languages
        )
    
    def _convert_to_add_executable(self, node: FunctionCall) -> AddExecutable:
        """Convert to CMake add_executable command."""
        name = ""
        sources = []
        
        for arg in node.arguments:
            if arg.name == "name" and isinstance(arg.value, StringLiteral):
                name = arg.value.value
            elif arg.name == "sources" and isinstance(arg.value, ListLiteral):
                sources = [elem.value for elem in arg.value.elements if hasattr(elem, 'value')]
        
        return AddExecutable(name=name, sources=sources)
    
    def _convert_to_add_library(self, node: FunctionCall) -> AddLibrary:
        """Convert to CMake add_library command."""
        name = ""
        library_type = "STATIC"
        sources = []
        
        for arg in node.arguments:
            if arg.name == "name" and isinstance(arg.value, StringLiteral):
                name = arg.value.value
            elif arg.name == "type" and isinstance(arg.value, StringLiteral):
                library_type = arg.value.value
            elif arg.name == "sources" and isinstance(arg.value, ListLiteral):
                sources = [elem.value for elem in arg.value.elements if hasattr(elem, 'value')]
        
        return AddLibrary(name=name, library_type=library_type, sources=sources)
    
    def _convert_variable_declaration(self, node: VariableDeclaration) -> SetCommand:
        """Convert variable declaration to CMake set command."""
        if isinstance(node.value, ListLiteral):
            value = [elem.value for elem in node.value.elements if hasattr(elem, 'value')]
        else:
            value = node.value.value if hasattr(node.value, 'value') else str(node.value)
        
        return SetCommand(
            variable=node.name,
            value=value,
            cache=node.is_constant
        )
    
    def _convert_string_literal(self, node: StringLiteral) -> StringLiteral:
        """Convert string literal to CMake string literal."""
        return StringLiteral(node.value)
    
    def _convert_identifier(self, node: Identifier) -> VariableRef:
        """Convert identifier to CMake variable reference."""
        return VariableRef(node.name)


# Public API functions
def cmake_to_runa(cmake_node: CMakeNode) -> RunaNode:
    """Convert CMake AST to Runa AST."""
    converter = CMakeToRunaConverter()
    return converter.convert(cmake_node)


def runa_to_cmake(runa_node: RunaNode) -> CMakeNode:
    """Convert Runa AST to CMake AST."""
    converter = RunaToCMakeConverter()
    return converter.convert(runa_node)


# Export converter classes and functions
__all__ = [
    'CMakeToRunaConverter',
    'RunaToCMakeConverter',
    'cmake_to_runa',
    'runa_to_cmake'
] 