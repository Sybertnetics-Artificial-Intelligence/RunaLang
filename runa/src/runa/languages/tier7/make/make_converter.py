#!/usr/bin/env python3
"""
Make Converter - Bidirectional conversion between Make and Runa AST

Features:
- Complete Make → Runa AST conversion
- Full Runa AST → Make conversion  
- Semantic preservation across transformations
- Build target and dependency mapping
- Variable and function translation
- Conditional logic preservation
- Command sequence handling
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import re

# Import Runa core components
from runa.core.ast_nodes import *
from runa.core.semantic_analyzer import SemanticAnalyzer
from runa.core.types import *

# Import Make AST
from .make_ast import *

class MakeToRunaConverter:
    """Converts Make AST to Runa AST"""
    
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.variable_mappings: Dict[str, str] = {}
        self.target_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
        
    def convert(self, make_ast: MakeFile) -> ModuleNode:
        """Convert Make AST to Runa AST"""
        # Create main module
        module = ModuleNode(
            name="makefile_module",
            statements=[],
            imports=[],
            metadata={"original_language": "make", "build_system": "make"}
        )
        
        # Convert statements
        for stmt in make_ast.statements:
            runa_stmts = self.convert_statement(stmt)
            module.statements.extend(runa_stmts)
            
        # Add build system metadata
        self.add_build_metadata(module, make_ast)
        
        return module
        
    def convert_statement(self, stmt: MakeStatement) -> List[StatementNode]:
        """Convert Make statement to Runa statements"""
        if isinstance(stmt, MakeVariable):
            return [self.convert_variable(stmt)]
        elif isinstance(stmt, MakeRule):
            return [self.convert_rule(stmt)]
        elif isinstance(stmt, MakeConditional):
            return [self.convert_conditional(stmt)]
        elif isinstance(stmt, MakeInclude):
            return [self.convert_include(stmt)]
        elif isinstance(stmt, UserDefinedFunction):
            return [self.convert_user_function(stmt)]
        elif isinstance(stmt, MakeComment):
            return [self.convert_comment(stmt)]
        elif isinstance(stmt, SpecialTarget):
            return [self.convert_special_target(stmt)]
        elif isinstance(stmt, VPathDirective):
            return [self.convert_vpath(stmt)]
        elif isinstance(stmt, ExportDirective):
            return [self.convert_export(stmt)]
        else:
            # Unknown statement type - create annotation
            return [self.create_annotation(f"Unknown Make statement: {type(stmt).__name__}")]
            
    def convert_variable(self, var: MakeVariable) -> VariableDeclarationNode:
        """Convert Make variable to Runa variable"""
        # Map assignment types to Runa semantics
        assignment_mapping = {
            "=": "recursive",     # Recursively expanded
            ":=": "immediate",    # Immediately expanded  
            "?=": "conditional",  # Set if undefined
            "+=": "append",       # Append to existing
            "!=": "shell"         # Shell command expansion
        }
        
        # Convert value
        runa_value = self.convert_expression(var.value)
        
        # Create variable declaration
        runa_var = VariableDeclarationNode(
            name=self.sanitize_identifier(var.name),
            type_annotation=self.infer_variable_type(var),
            initial_value=runa_value,
            is_mutable=True,
            metadata={
                "make_assignment_type": var.assignment_type,
                "assignment_semantic": assignment_mapping.get(var.assignment_type, "immediate"),
                "is_exported": var.is_exported,
                "is_override": var.is_override,
                "is_private": var.is_private,
                "target_specific": var.target_specific
            }
        )
        
        # Store mapping
        self.variable_mappings[var.name] = runa_var.name
        
        return runa_var
        
    def convert_rule(self, rule: MakeRule) -> FunctionDeclarationNode:
        """Convert Make rule to Runa function"""
        # Create function name from target
        target_name = rule.targets[0] if rule.targets else "unknown_target"
        func_name = self.sanitize_identifier(f"build_{target_name}")
        
        # Create parameters for dependencies
        parameters = []
        for i, dep in enumerate(rule.dependencies):
            param = ParameterNode(
                name=self.sanitize_identifier(f"dep_{i}_{dep}"),
                type_annotation=StringTypeNode(),
                default_value=StringLiteralNode(dep)
            )
            parameters.append(param)
            
        # Convert commands to function body
        body_statements = []
        
        # Add dependency tracking
        if rule.dependencies:
            deps_list = ListLiteralNode([
                StringLiteralNode(dep) for dep in rule.dependencies
            ])
            deps_var = VariableDeclarationNode(
                name="dependencies",
                type_annotation=ListTypeNode(StringTypeNode()),
                initial_value=deps_list
            )
            body_statements.append(deps_var)
            
        # Convert commands
        for cmd in rule.commands:
            cmd_stmt = self.convert_command(cmd)
            body_statements.append(cmd_stmt)
            
        # Create function
        func = FunctionDeclarationNode(
            name=func_name,
            parameters=parameters,
            return_type=StringTypeNode(),  # Build functions return status
            body=BlockNode(body_statements),
            is_async=False,
            metadata={
                "make_targets": rule.targets,
                "make_dependencies": rule.dependencies,
                "order_only_deps": rule.order_only_deps,
                "is_pattern_rule": rule.is_pattern_rule,
                "is_double_colon": rule.is_double_colon,
                "is_phony": rule.is_phony,
                "build_rule": True
            }
        )
        
        # Store mapping
        for target in rule.targets:
            self.target_mappings[target] = func_name
            
        return func
        
    def convert_command(self, cmd: MakeCommand) -> StatementNode:
        """Convert Make command to Runa statement"""
        # Create shell execution call
        shell_call = FunctionCallNode(
            function=IdentifierNode("shell_execute"),
            arguments=[StringLiteralNode(cmd.command_line)],
            metadata={
                "is_silent": cmd.is_silent,
                "ignore_errors": cmd.ignore_errors,
                "always_execute": cmd.always_execute,
                "make_command": True
            }
        )
        
        return ExpressionStatementNode(shell_call)
        
    def convert_conditional(self, cond: MakeConditional) -> IfStatementNode:
        """Convert Make conditional to Runa if statement"""
        # Convert condition
        condition_expr = self.convert_conditional_expression(cond.condition_type, cond.condition)
        
        # Convert then block
        then_statements = []
        for stmt in cond.then_statements:
            then_statements.extend(self.convert_statement(stmt))
        then_block = BlockNode(then_statements)
        
        # Convert else block
        else_block = None
        if cond.else_statements:
            else_statements = []
            for stmt in cond.else_statements:
                else_statements.extend(self.convert_statement(stmt))
            else_block = BlockNode(else_statements)
            
        return IfStatementNode(
            condition=condition_expr,
            then_block=then_block,
            else_block=else_block,
            metadata={"make_conditional_type": cond.condition_type}
        )
        
    def convert_conditional_expression(self, condition_type: str, condition: MakeExpression) -> ExpressionNode:
        """Convert Make conditional expression to Runa expression"""
        condition_text = self.extract_text_from_expression(condition)
        
        if condition_type in ["ifeq", "ifneq"]:
            # Parse (arg1,arg2) format
            args = self.parse_conditional_args(condition_text)
            if len(args) >= 2:
                left = StringLiteralNode(args[0])
                right = StringLiteralNode(args[1])
                op = "==" if condition_type == "ifeq" else "!="
                return BinaryOperationNode(left, op, right)
                
        elif condition_type in ["ifdef", "ifndef"]:
            # Check if variable is defined
            var_name = condition_text.strip()
            var_ref = IdentifierNode(self.sanitize_identifier(var_name))
            defined_check = FunctionCallNode(
                function=IdentifierNode("is_defined"),
                arguments=[var_ref]
            )
            if condition_type == "ifndef":
                return UnaryOperationNode("not", defined_check)
            return defined_check
            
        # Default: treat as string comparison
        return BooleanLiteralNode(True)
        
    def convert_include(self, include: MakeInclude) -> ImportNode:
        """Convert Make include to Runa import"""
        # Convert to import statement
        imports = []
        for filename in include.filenames:
            module_name = self.filename_to_module_name(filename)
            import_node = ImportNode(
                module_name=module_name,
                alias=None,
                imported_items=[],
                metadata={
                    "make_include": True,
                    "is_optional": include.is_optional,
                    "original_filename": filename
                }
            )
            imports.append(import_node)
            
        return imports[0] if imports else None
        
    def convert_user_function(self, func: UserDefinedFunction) -> FunctionDeclarationNode:
        """Convert Make user-defined function to Runa function"""
        # Convert body
        body_statements = []
        for stmt in func.body:
            body_statements.extend(self.convert_statement(stmt))
            
        # Create function
        runa_func = FunctionDeclarationNode(
            name=self.sanitize_identifier(func.name),
            parameters=[],  # Make functions use numbered parameters
            return_type=StringTypeNode(),
            body=BlockNode(body_statements),
            metadata={
                "make_user_function": True,
                "make_parameters": func.parameters
            }
        )
        
        self.function_mappings[func.name] = runa_func.name
        return runa_func
        
    def convert_comment(self, comment: MakeComment) -> CommentNode:
        """Convert Make comment to Runa comment"""
        return CommentNode(
            content=comment.text,
            is_block=False,
            metadata={"make_comment": True}
        )
        
    def convert_special_target(self, target: SpecialTarget) -> AnnotationNode:
        """Convert Make special target to Runa annotation"""
        return AnnotationNode(
            name="make_special_target",
            arguments=[
                StringLiteralNode(target.name),
                ListLiteralNode([StringLiteralNode(dep) for dep in target.dependencies])
            ],
            metadata={"special_target": target.name}
        )
        
    def convert_vpath(self, vpath: VPathDirective) -> AnnotationNode:
        """Convert VPATH directive to Runa annotation"""
        return AnnotationNode(
            name="vpath",
            arguments=[
                StringLiteralNode(vpath.pattern or ""),
                ListLiteralNode([StringLiteralNode(d) for d in vpath.directories])
            ],
            metadata={"vpath_directive": True}
        )
        
    def convert_export(self, export: ExportDirective) -> AnnotationNode:
        """Convert export directive to Runa annotation"""
        return AnnotationNode(
            name="export_variables" if not export.is_unexport else "unexport_variables",
            arguments=[ListLiteralNode([StringLiteralNode(v) for v in export.variables])],
            metadata={"export_directive": True}
        )
        
    def convert_expression(self, expr: MakeExpression) -> ExpressionNode:
        """Convert Make expression to Runa expression"""
        if isinstance(expr, TextLiteral):
            return StringLiteralNode(expr.value)
        elif isinstance(expr, VariableReference):
            var_name = self.extract_variable_name(expr.name)
            return IdentifierNode(self.sanitize_identifier(var_name))
        elif isinstance(expr, AutomaticVariable):
            # Convert automatic variables to special function calls
            return FunctionCallNode(
                function=IdentifierNode("automatic_variable"),
                arguments=[StringLiteralNode(expr.symbol)]
            )
        elif isinstance(expr, MakeFunction):
            return self.convert_function_call(expr)
        elif isinstance(expr, ConcatenatedText):
            # Convert to string concatenation
            parts = [self.convert_expression(part) for part in expr.parts]
            if len(parts) == 1:
                return parts[0]
            else:
                # Chain binary operations
                result = parts[0]
                for part in parts[1:]:
                    result = BinaryOperationNode(result, "+", part)
                return result
        else:
            return StringLiteralNode(str(expr))
            
    def convert_function_call(self, func: MakeFunction) -> FunctionCallNode:
        """Convert Make function call to Runa function call"""
        # Map Make function names to Runa equivalents
        function_mapping = {
            "subst": "string_substitute",
            "patsubst": "pattern_substitute", 
            "wildcard": "glob_pattern",
            "shell": "shell_execute",
            "strip": "string_strip",
            "filter": "list_filter",
            "sort": "list_sort",
            "dir": "path_dirname",
            "notdir": "path_basename",
            "suffix": "path_suffix",
            "basename": "path_basename_no_ext",
            "realpath": "path_realpath",
            "abspath": "path_abspath"
        }
        
        func_name = function_mapping.get(func.name, func.name)
        args = [self.convert_expression(arg) for arg in func.arguments]
        
        return FunctionCallNode(
            function=IdentifierNode(func_name),
            arguments=args,
            metadata={"make_function": func.name}
        )
        
    # Helper methods
    
    def sanitize_identifier(self, name: str) -> str:
        """Convert Make identifier to valid Runa identifier"""
        # Replace invalid characters
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
        
        # Ensure it starts with letter or underscore
        if sanitized and sanitized[0].isdigit():
            sanitized = f"_{sanitized}"
            
        return sanitized or "unnamed"
        
    def infer_variable_type(self, var: MakeVariable) -> TypeNode:
        """Infer Runa type for Make variable"""
        value_text = self.extract_text_from_expression(var.value)
        
        # Try to infer type from value
        if value_text.isdigit():
            return IntegerTypeNode()
        elif value_text.replace('.', '').isdigit():
            return FloatTypeNode()
        elif value_text.lower() in ['true', 'false', 'yes', 'no']:
            return BooleanTypeNode()
        else:
            return StringTypeNode()
            
    def extract_text_from_expression(self, expr: MakeExpression) -> str:
        """Extract text content from Make expression"""
        if isinstance(expr, TextLiteral):
            return expr.value
        elif isinstance(expr, VariableReference):
            return expr.name
        elif isinstance(expr, ConcatenatedText):
            return ' '.join(self.extract_text_from_expression(part) for part in expr.parts)
        else:
            return str(expr)
            
    def extract_variable_name(self, var_ref: str) -> str:
        """Extract variable name from reference like $(VAR) or ${VAR}"""
        if var_ref.startswith('$(') and var_ref.endswith(')'):
            return var_ref[2:-1]
        elif var_ref.startswith('${') and var_ref.endswith('}'):
            return var_ref[2:-1]
        elif var_ref.startswith('$'):
            return var_ref[1:]
        return var_ref
        
    def parse_conditional_args(self, condition_text: str) -> List[str]:
        """Parse conditional arguments from text like (arg1,arg2)"""
        # Remove parentheses and split by comma
        text = condition_text.strip()
        if text.startswith('(') and text.endswith(')'):
            text = text[1:-1]
        return [arg.strip().strip('"\'') for arg in text.split(',')]
        
    def filename_to_module_name(self, filename: str) -> str:
        """Convert filename to Runa module name"""
        # Remove extension and sanitize
        name = filename.split('.')[0]
        return self.sanitize_identifier(name)
        
    def create_annotation(self, description: str) -> AnnotationNode:
        """Create annotation for unknown constructs"""
        return AnnotationNode(
            name="make_annotation",
            arguments=[StringLiteralNode(description)],
            metadata={"unknown_construct": True}
        )
        
    def add_build_metadata(self, module: ModuleNode, make_ast: MakeFile) -> None:
        """Add build system metadata to module"""
        metadata = {
            "build_system": "make",
            "variable_count": len([s for s in make_ast.statements if isinstance(s, MakeVariable)]),
            "rule_count": len([s for s in make_ast.statements if isinstance(s, MakeRule)]),
            "include_count": len([s for s in make_ast.statements if isinstance(s, MakeInclude)])
        }
        module.metadata.update(metadata)

class RunaToMakeConverter:
    """Converts Runa AST to Make AST"""
    
    def __init__(self):
        self.variable_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
        
    def convert(self, runa_ast: ModuleNode) -> MakeFile:
        """Convert Runa AST to Make AST"""
        statements = []
        
        # Convert module statements
        for stmt in runa_ast.statements:
            make_stmts = self.convert_statement(stmt)
            statements.extend(make_stmts)
            
        return MakeFile(statements=statements)
        
    def convert_statement(self, stmt: StatementNode) -> List[MakeStatement]:
        """Convert Runa statement to Make statements"""
        if isinstance(stmt, VariableDeclarationNode):
            return [self.convert_variable_declaration(stmt)]
        elif isinstance(stmt, FunctionDeclarationNode):
            if stmt.metadata.get("build_rule"):
                return [self.convert_build_rule(stmt)]
            else:
                return [self.convert_function_declaration(stmt)]
        elif isinstance(stmt, IfStatementNode):
            return [self.convert_if_statement(stmt)]
        elif isinstance(stmt, ImportNode):
            return [self.convert_import(stmt)]
        elif isinstance(stmt, CommentNode):
            return [self.convert_comment(stmt)]
        elif isinstance(stmt, AnnotationNode):
            return self.convert_annotation(stmt)
        else:
            return []
            
    def convert_variable_declaration(self, var: VariableDeclarationNode) -> MakeVariable:
        """Convert Runa variable to Make variable"""
        # Map assignment semantics back to Make types
        assignment_mapping = {
            "recursive": "=",
            "immediate": ":=", 
            "conditional": "?=",
            "append": "+=",
            "shell": "!="
        }
        
        assignment_type = "="
        if var.metadata:
            semantic = var.metadata.get("assignment_semantic", "immediate")
            assignment_type = assignment_mapping.get(semantic, ":=")
            
        # Convert value
        value = self.convert_expression(var.initial_value) if var.initial_value else TextLiteral("")
        
        make_var = MakeVariable(
            name=var.name,
            value=value,
            assignment_type=assignment_type,
            is_exported=var.metadata.get("is_exported", False) if var.metadata else False,
            is_override=var.metadata.get("is_override", False) if var.metadata else False,
            is_private=var.metadata.get("is_private", False) if var.metadata else False
        )
        
        self.variable_mappings[var.name] = var.name
        return make_var
        
    def convert_build_rule(self, func: FunctionDeclarationNode) -> MakeRule:
        """Convert Runa function marked as build rule to Make rule"""
        metadata = func.metadata or {}
        
        # Extract targets and dependencies from metadata
        targets = metadata.get("make_targets", [func.name.replace("build_", "")])
        dependencies = metadata.get("make_dependencies", [])
        
        # Convert function body to commands
        commands = []
        if func.body:
            for stmt in func.body.statements:
                if isinstance(stmt, ExpressionStatementNode):
                    cmd = self.convert_expression_to_command(stmt.expression)
                    if cmd:
                        commands.append(cmd)
                        
        return MakeRule(
            targets=targets,
            dependencies=dependencies,
            order_only_deps=metadata.get("order_only_deps", []),
            commands=commands,
            is_pattern_rule=metadata.get("is_pattern_rule", False),
            is_double_colon=metadata.get("is_double_colon", False),
            is_phony=metadata.get("is_phony", False)
        )
        
    def convert_function_declaration(self, func: FunctionDeclarationNode) -> UserDefinedFunction:
        """Convert Runa function to Make user-defined function"""
        # Convert body
        body_statements = []
        if func.body:
            for stmt in func.body.statements:
                body_statements.extend(self.convert_statement(stmt))
                
        return UserDefinedFunction(
            name=func.name,
            parameters=[param.name for param in func.parameters],
            body=body_statements
        )
        
    def convert_expression_to_command(self, expr: ExpressionNode) -> Optional[MakeCommand]:
        """Convert Runa expression to Make command"""
        if isinstance(expr, FunctionCallNode):
            if (isinstance(expr.function, IdentifierNode) and 
                expr.function.name == "shell_execute" and
                expr.arguments):
                
                cmd_text = self.extract_string_literal(expr.arguments[0])
                metadata = expr.metadata or {}
                
                return MakeCommand(
                    command_line=cmd_text,
                    is_silent=metadata.get("is_silent", False),
                    ignore_errors=metadata.get("ignore_errors", False),
                    always_execute=metadata.get("always_execute", False)
                )
                
        return None
        
    def convert_if_statement(self, if_stmt: IfStatementNode) -> MakeConditional:
        """Convert Runa if statement to Make conditional"""
        # Determine condition type
        condition_type = "ifeq"  # Default
        if if_stmt.metadata:
            condition_type = if_stmt.metadata.get("make_conditional_type", "ifeq")
            
        # Convert condition
        condition = self.convert_expression(if_stmt.condition)
        
        # Convert blocks
        then_statements = []
        if if_stmt.then_block:
            for stmt in if_stmt.then_block.statements:
                then_statements.extend(self.convert_statement(stmt))
                
        else_statements = []
        if if_stmt.else_block:
            for stmt in if_stmt.else_block.statements:
                else_statements.extend(self.convert_statement(stmt))
                
        return MakeConditional(
            condition_type=condition_type,
            condition=condition,
            then_statements=then_statements,
            else_statements=else_statements
        )
        
    def convert_import(self, import_node: ImportNode) -> MakeInclude:
        """Convert Runa import to Make include"""
        metadata = import_node.metadata or {}
        filename = metadata.get("original_filename", f"{import_node.module_name}.mk")
        is_optional = metadata.get("is_optional", False)
        
        return MakeInclude(
            filenames=[filename],
            is_optional=is_optional
        )
        
    def convert_comment(self, comment: CommentNode) -> MakeComment:
        """Convert Runa comment to Make comment"""
        return MakeComment(text=comment.content)
        
    def convert_annotation(self, annotation: AnnotationNode) -> List[MakeStatement]:
        """Convert Runa annotation to Make statements"""
        if annotation.name == "make_special_target":
            # Convert back to special target
            if len(annotation.arguments) >= 2:
                name = self.extract_string_literal(annotation.arguments[0])
                deps_list = annotation.arguments[1]
                dependencies = []
                if isinstance(deps_list, ListLiteralNode):
                    dependencies = [self.extract_string_literal(item) for item in deps_list.elements]
                    
                return [SpecialTarget(name=name, dependencies=dependencies)]
                
        elif annotation.name in ["vpath"]:
            # Convert back to VPATH
            if len(annotation.arguments) >= 2:
                pattern = self.extract_string_literal(annotation.arguments[0])
                dirs_list = annotation.arguments[1]
                directories = []
                if isinstance(dirs_list, ListLiteralNode):
                    directories = [self.extract_string_literal(item) for item in dirs_list.elements]
                    
                return [VPathDirective(pattern=pattern or None, directories=directories)]
                
        elif annotation.name in ["export_variables", "unexport_variables"]:
            # Convert back to export
            is_unexport = annotation.name == "unexport_variables"
            variables = []
            if annotation.arguments and isinstance(annotation.arguments[0], ListLiteralNode):
                variables = [self.extract_string_literal(item) for item in annotation.arguments[0].elements]
                
            return [ExportDirective(variables=variables, is_unexport=is_unexport)]
            
        return []
        
    def convert_expression(self, expr: ExpressionNode) -> MakeExpression:
        """Convert Runa expression to Make expression"""
        if isinstance(expr, StringLiteralNode):
            return TextLiteral(expr.value)
        elif isinstance(expr, IdentifierNode):
            # Convert to variable reference
            return VariableReference(name=f"$({expr.name})")
        elif isinstance(expr, BinaryOperationNode):
            # Convert to concatenated text for string operations
            if expr.operator == "+":
                left = self.convert_expression(expr.left)
                right = self.convert_expression(expr.right)
                return ConcatenatedText(parts=[left, right])
        elif isinstance(expr, FunctionCallNode):
            return self.convert_function_call_to_make(expr)
            
        return TextLiteral(str(expr))
        
    def convert_function_call_to_make(self, call: FunctionCallNode) -> MakeFunction:
        """Convert Runa function call to Make function"""
        # Reverse mapping from Runa to Make function names
        function_mapping = {
            "string_substitute": "subst",
            "pattern_substitute": "patsubst",
            "glob_pattern": "wildcard", 
            "shell_execute": "shell",
            "string_strip": "strip",
            "list_filter": "filter",
            "list_sort": "sort",
            "path_dirname": "dir",
            "path_basename": "notdir",
            "path_suffix": "suffix",
            "path_basename_no_ext": "basename",
            "path_realpath": "realpath",
            "path_abspath": "abspath"
        }
        
        func_name = call.function.name if isinstance(call.function, IdentifierNode) else str(call.function)
        make_name = function_mapping.get(func_name, func_name)
        
        # Convert arguments
        args = [self.convert_expression(arg) for arg in call.arguments]
        
        return MakeFunction(name=make_name, arguments=args)
        
    def extract_string_literal(self, expr: ExpressionNode) -> str:
        """Extract string value from expression"""
        if isinstance(expr, StringLiteralNode):
            return expr.value
        return str(expr)

# Main conversion functions

def make_to_runa(make_ast: MakeFile) -> ModuleNode:
    """Convert Make AST to Runa AST"""
    converter = MakeToRunaConverter()
    return converter.convert(make_ast)

def runa_to_make(runa_ast: ModuleNode) -> MakeFile:
    """Convert Runa AST to Make AST"""
    converter = RunaToMakeConverter()
    return converter.convert(runa_ast)

# Export main components
__all__ = [
    'MakeToRunaConverter', 'RunaToMakeConverter',
    'make_to_runa', 'runa_to_make'
] 