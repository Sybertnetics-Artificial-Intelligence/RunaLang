#!/usr/bin/env python3
"""
Shell Converter - Bidirectional Shell ↔ Runa AST Conversion

Provides comprehensive conversion between Shell scripts and Runa AST including:
- Shell commands to Runa system/process calls
- Shell functions to Runa function declarations
- Variable assignments and parameter expansions
- Pipelines to Runa stream processing
- Control structures (if/while/for) to Runa equivalents
- I/O redirection to Runa file operations
- Command substitution to Runa execution contexts
- Shell-specific constructs to infrastructure patterns

Maintains semantic equivalence and supports round-trip conversion.
"""

from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass

from .shell_ast import *
from runa.languages.shared.runa_ast import *


class ShellToRunaConverter:
    """Converts Shell AST to Runa AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.shell_metadata: Dict[str, Any] = {}
        self.variable_mappings: Dict[str, str] = {}
        self.function_mappings: Dict[str, str] = {}
        
        # Shell command to Runa function mappings
        self.command_mappings = {
            # File operations
            "ls": "runa.fs.list_dir",
            "cp": "runa.fs.copy",
            "mv": "runa.fs.move", 
            "rm": "runa.fs.remove",
            "mkdir": "runa.fs.create_dir",
            "rmdir": "runa.fs.remove_dir",
            "cat": "runa.fs.read_file",
            "touch": "runa.fs.create_file",
            "chmod": "runa.fs.set_permissions",
            "chown": "runa.fs.set_owner",
            
            # Text processing
            "echo": "runa.io.print",
            "printf": "runa.io.printf",
            "grep": "runa.text.grep",
            "sed": "runa.text.sed",
            "awk": "runa.text.awk",
            "sort": "runa.text.sort",
            "uniq": "runa.text.unique",
            "head": "runa.text.head",
            "tail": "runa.text.tail",
            "wc": "runa.text.word_count",
            "tr": "runa.text.translate",
            
            # Process management
            "ps": "runa.process.list",
            "kill": "runa.process.kill",
            "killall": "runa.process.kill_all",
            "jobs": "runa.process.jobs",
            "bg": "runa.process.background",
            "fg": "runa.process.foreground",
            "nohup": "runa.process.detach",
            
            # System info
            "pwd": "runa.fs.current_dir",
            "whoami": "runa.system.current_user",
            "hostname": "runa.system.hostname",
            "uname": "runa.system.info",
            "date": "runa.system.date",
            "uptime": "runa.system.uptime",
            "df": "runa.system.disk_usage",
            "free": "runa.system.memory_usage",
            
            # Network
            "ping": "runa.net.ping",
            "wget": "runa.net.download",
            "curl": "runa.net.request",
            "ssh": "runa.net.ssh",
            "scp": "runa.net.copy",
            
            # Archives
            "tar": "runa.archive.tar",
            "zip": "runa.archive.zip",
            "unzip": "runa.archive.unzip",
            "gzip": "runa.archive.gzip",
            "gunzip": "runa.archive.gunzip",
            
            # Shell built-ins
            "cd": "runa.fs.change_dir",
            "export": "runa.env.set_variable",
            "unset": "runa.env.unset_variable",
            "source": "runa.shell.source",
            "exec": "runa.process.exec",
            "exit": "runa.system.exit",
            "return": "runa.function.return",
            "test": "runa.test.condition",
            "read": "runa.io.read_input",
        }
        
        # Shell operators to Runa operators
        self.operator_mappings = {
            "&&": "and",
            "||": "or", 
            "!": "not",
            "==": "==",
            "!=": "!=",
            "-eq": "==",
            "-ne": "!=",
            "-lt": "<",
            "-le": "<=",
            "-gt": ">",
            "-ge": ">=",
            "-z": "is_empty",
            "-n": "is_not_empty",
            "-f": "is_file",
            "-d": "is_directory",
            "-e": "exists",
        }
    
    def convert(self, shell_script: ShellScript) -> RunaModule:
        """Convert Shell script to Runa module"""
        runa_declarations = []
        imports = []
        
        # Add standard imports for shell functionality
        imports.extend([
            RunaImport(path="runa.fs", alias=None, items=["read_file", "write_file", "list_dir"]),
            RunaImport(path="runa.process", alias=None, items=["run", "pipe", "spawn"]),
            RunaImport(path="runa.io", alias=None, items=["print", "println", "read_input"]),
            RunaImport(path="runa.system", alias=None, items=["exit", "env"]),
            RunaImport(path="runa.shell", alias=None, items=["execute", "pipeline"]),
        ])
        
        # Convert shell functions first
        for func in shell_script.functions:
            runa_func = self._convert_function_definition(func)
            runa_declarations.append(runa_func)
        
        # Convert main script statements
        main_statements = []
        for stmt in shell_script.statements:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    main_statements.extend(runa_stmt)
                else:
                    main_statements.append(runa_stmt)
        
        # Create main function if we have statements
        if main_statements:
            main_function = ProcessDefinition(
                name="main",
                parameters=[],
                return_type=RunaNominalType("Unit"),
                body=Block(statements=main_statements),
                annotations=[RunaAnnotation("shell_main", {})],
                metadata={
                    "shell_script": True,
                    "shebang": shell_script.shebang
                }
            )
            runa_declarations.append(main_function)
        
        return RunaModule(
            name="shell_script",
            imports=imports,
            declarations=runa_declarations,
            exports=[],
            metadata={
                "source_language": "shell",
                "shebang": shell_script.shebang,
                "shell_type": self._detect_shell_type(shell_script.shebang),
                "command_count": len([s for s in shell_script.statements if isinstance(s, ShellCommand)]),
                "function_count": len(shell_script.functions)
            }
        )
    
    def _convert_statement(self, stmt: ShellStatement) -> Optional[Union[Statement, List[Statement]]]:
        """Convert shell statement to Runa statement(s)"""
        if isinstance(stmt, ShellCommand):
            return self._convert_command(stmt)
        elif isinstance(stmt, ShellPipeline):
            return self._convert_pipeline(stmt)
        elif isinstance(stmt, ShellVariableAssignment):
            return self._convert_variable_assignment(stmt)
        elif isinstance(stmt, ShellConditional):
            return self._convert_conditional(stmt)
        elif isinstance(stmt, ShellLoop):
            return self._convert_loop(stmt)
        elif isinstance(stmt, ShellCompoundCommand):
            return self._convert_compound_command(stmt)
        elif isinstance(stmt, ShellFunctionDefinition):
            return self._convert_function_definition(stmt)
        else:
            return None
    
    def _convert_command(self, cmd: ShellCommand) -> Statement:
        """Convert shell command to Runa function call"""
        # Map shell command to Runa function
        if cmd.command in self.command_mappings:
            runa_function = self.command_mappings[cmd.command]
        else:
            # Use generic shell execution for unknown commands
            runa_function = "runa.shell.execute"
        
        # Convert arguments
        args = [StringLiteral(cmd.command)] if runa_function == "runa.shell.execute" else []
        for arg in cmd.arguments:
            args.append(self._convert_shell_argument(arg))
        
        # Handle redirections
        if cmd.redirections:
            redirection_config = self._convert_redirections(cmd.redirections)
            args.append(RunaStructLiteral(
                fields=[RunaStructField(name="redirections", value=redirection_config)]
            ))
        
        # Handle background execution
        if cmd.background:
            args.append(RunaStructLiteral(
                fields=[RunaStructField(name="background", value=BooleanLiteral(True))]
            ))
        
        function_call = FunctionCall(
            function=Identifier(runa_function),
            args=args,
            metadata={
                "shell_command": cmd.command,
                "original_args": cmd.arguments,
                "is_builtin": cmd.is_builtin
            }
        )
        
        return ExpressionStatement(function_call)
    
    def _convert_pipeline(self, pipeline: ShellPipeline) -> Statement:
        """Convert shell pipeline to Runa pipeline call"""
        command_calls = []
        
        for cmd in pipeline.commands:
            cmd_call = self._convert_command(cmd)
            if isinstance(cmd_call, ExpressionStatement):
                command_calls.append(cmd_call.expression)
        
        pipeline_call = FunctionCall(
            function=Identifier("runa.shell.pipeline"),
            args=[ListLiteral(command_calls)],
            metadata={
                "shell_pipeline": True,
                "command_count": len(pipeline.commands),
                "negated": pipeline.negated
            }
        )
        
        if pipeline.negated:
            # Wrap in negation
            negated_call = FunctionCall(
                function=Identifier("runa.logic.not"),
                args=[pipeline_call]
            )
            return ExpressionStatement(negated_call)
        
        return ExpressionStatement(pipeline_call)
    
    def _convert_variable_assignment(self, assignment: ShellVariableAssignment) -> Statement:
        """Convert shell variable assignment to Runa variable declaration"""
        # Handle array assignments
        if assignment.array:
            value = ListLiteral([
                StringLiteral(val) for val in assignment.array_values
            ])
            var_type = GenericType("List", [RunaNominalType("String")])
        else:
            value = self._convert_shell_value(assignment.value)
            var_type = self._infer_shell_value_type(assignment.value)
        
        # Add annotations for shell-specific behavior
        annotations = []
        if assignment.export:
            annotations.append(RunaAnnotation("export", {}))
        if assignment.readonly:
            annotations.append(RunaAnnotation("readonly", {}))
        if assignment.local:
            annotations.append(RunaAnnotation("local", {}))
        
        # Apply annotations to type
        annotated_type = var_type
        if annotations:
            annotated_type = RunaAnnotatedType(
                base_type=var_type,
                annotations=annotations
            )
        
        return LetStatement(
            name=assignment.variable,
            type=annotated_type,
            value=value,
            is_mutable=not assignment.readonly,
            metadata={
                "shell_variable": True,
                "export": assignment.export,
                "readonly": assignment.readonly,
                "local": assignment.local
            }
        )
    
    def _convert_conditional(self, conditional: ShellConditional) -> Statement:
        """Convert shell conditional to Runa if statement"""
        condition_expr = self._convert_shell_condition(conditional.condition)
        
        # Convert then body
        then_statements = []
        for stmt in conditional.then_body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    then_statements.extend(runa_stmt)
                else:
                    then_statements.append(runa_stmt)
        
        then_block = Block(statements=then_statements)
        
        # Convert else body
        else_block = None
        if conditional.else_body:
            else_statements = []
            for stmt in conditional.else_body:
                runa_stmt = self._convert_statement(stmt)
                if runa_stmt:
                    if isinstance(runa_stmt, list):
                        else_statements.extend(runa_stmt)
                    else:
                        else_statements.append(runa_stmt)
            else_block = Block(statements=else_statements)
        
        # Handle elif clauses by nesting if statements
        if conditional.elif_clauses:
            # Build nested if statements for elif clauses
            current_else = else_block
            for elif_condition, elif_body in reversed(conditional.elif_clauses):
                elif_statements = []
                for stmt in elif_body:
                    runa_stmt = self._convert_statement(stmt)
                    if runa_stmt:
                        if isinstance(runa_stmt, list):
                            elif_statements.extend(runa_stmt)
                        else:
                            elif_statements.append(runa_stmt)
                
                elif_if = IfStatement(
                    condition=self._convert_shell_condition(elif_condition),
                    then_block=Block(statements=elif_statements),
                    else_block=current_else
                )
                current_else = Block(statements=[elif_if])
            
            else_block = current_else
        
        # Handle case statements
        if conditional.is_case_statement:
            return self._convert_case_statement(conditional)
        
        return IfStatement(
            condition=condition_expr,
            then_block=then_block,
            else_block=else_block,
            metadata={
                "shell_conditional": True,
                "conditional_type": conditional.conditional_type
            }
        )
    
    def _convert_loop(self, loop: ShellLoop) -> Statement:
        """Convert shell loop to Runa loop statement"""
        if loop.is_for_loop:
            return self._convert_for_loop(loop)
        elif loop.is_while_loop:
            return self._convert_while_loop(loop)
        elif loop.is_until_loop:
            return self._convert_until_loop(loop)
        else:
            raise ValueError(f"Unknown loop type: {loop.loop_type}")
    
    def _convert_for_loop(self, loop: ShellLoop) -> Statement:
        """Convert shell for loop to Runa for loop"""
        # Convert loop body
        body_statements = []
        for stmt in loop.body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    body_statements.extend(runa_stmt)
                else:
                    body_statements.append(runa_stmt)
        
        body_block = Block(statements=body_statements)
        
        # Handle iterable
        if loop.iterable:
            iterable_expr = self._convert_shell_value(loop.iterable)
        else:
            # Default to positional parameters $@
            iterable_expr = Identifier("runa.shell.args")
        
        return RunaForLoop(
            variable=loop.variable or "item",
            iterable=iterable_expr,
            body=body_block,
            metadata={
                "shell_for_loop": True,
                "original_condition": loop.condition
            }
        )
    
    def _convert_while_loop(self, loop: ShellLoop) -> Statement:
        """Convert shell while loop to Runa while loop"""
        condition_expr = self._convert_shell_condition(loop.condition)
        
        # Convert loop body
        body_statements = []
        for stmt in loop.body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    body_statements.extend(runa_stmt)
                else:
                    body_statements.append(runa_stmt)
        
        body_block = Block(statements=body_statements)
        
        return WhileLoop(
            condition=condition_expr,
            body=body_block,
            metadata={
                "shell_while_loop": True,
                "original_condition": loop.condition
            }
        )
    
    def _convert_until_loop(self, loop: ShellLoop) -> Statement:
        """Convert shell until loop to Runa while loop with negated condition"""
        condition_expr = self._convert_shell_condition(loop.condition)
        
        # Negate the condition for until loop
        negated_condition = FunctionCall(
            function=Identifier("runa.logic.not"),
            args=[condition_expr]
        )
        
        # Convert loop body
        body_statements = []
        for stmt in loop.body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    body_statements.extend(runa_stmt)
                else:
                    body_statements.append(runa_stmt)
        
        body_block = Block(statements=body_statements)
        
        return WhileLoop(
            condition=negated_condition,
            body=body_block,
            metadata={
                "shell_until_loop": True,
                "original_condition": loop.condition
            }
        )
    
    def _convert_function_definition(self, func: ShellFunctionDefinition) -> ProcessDefinition:
        """Convert shell function to Runa function declaration"""
        # Convert function body
        body_statements = []
        for stmt in func.body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    body_statements.extend(runa_stmt)
                else:
                    body_statements.append(runa_stmt)
        
        # Shell functions implicitly have access to positional parameters
        parameters = [
            Parameter(
                name="args",
                type=GenericType("List", [RunaNominalType("String")]),
                default_value=None
            )
        ]
        
        return ProcessDefinition(
            name=func.name,
            parameters=parameters,
            return_type=RunaNominalType("Int"),  # Shell functions return exit codes
            body=Block(statements=body_statements),
            annotations=[RunaAnnotation("shell_function", {})],
            metadata={
                "shell_function": True,
                "original_parameters": func.parameters,
                "local_variables": func.local_variables
            }
        )
    
    def _convert_compound_command(self, compound: ShellCompoundCommand) -> Statement:
        """Convert shell compound command to Runa block or function call"""
        body_statements = []
        for stmt in compound.body:
            runa_stmt = self._convert_statement(stmt)
            if runa_stmt:
                if isinstance(runa_stmt, list):
                    body_statements.extend(runa_stmt)
                else:
                    body_statements.append(runa_stmt)
        
        if compound.is_subshell:
            # Subshell - wrap in subprocess call
            subshell_call = FunctionCall(
                function=Identifier("runa.process.subshell"),
                args=[RunaFunctionLiteral(
                    parameters=[],
                    body=Block(statements=body_statements)
                )],
                metadata={"shell_subshell": True}
            )
            return ExpressionStatement(subshell_call)
        else:
            # Command group - just return block
            return Block(statements=body_statements)
    
    def _convert_case_statement(self, conditional: ShellConditional) -> Statement:
        """Convert shell case statement to Runa match expression"""
        # For now, convert to nested if-else chain
        # TODO: Use proper match expression when available
        test_value = self._convert_shell_value(conditional.condition)
        
        current_else = None
        
        # Build nested if statements from patterns
        for pattern, body in reversed(conditional.case_patterns):
            pattern_statements = []
            for stmt in body:
                runa_stmt = self._convert_statement(stmt)
                if runa_stmt:
                    if isinstance(runa_stmt, list):
                        pattern_statements.extend(runa_stmt)
                    else:
                        pattern_statements.append(runa_stmt)
            
            # Create pattern match condition
            pattern_condition = FunctionCall(
                function=Identifier("runa.pattern.match"),
                args=[test_value, StringLiteral(pattern)]
            )
            
            pattern_if = IfStatement(
                condition=pattern_condition,
                then_block=Block(statements=pattern_statements),
                else_block=current_else
            )
            current_else = Block(statements=[pattern_if])
        
        return current_else.statements[0] if current_else else Block(statements=[])
    
    def _convert_shell_condition(self, condition: str) -> Expression:
        """Convert shell condition to Runa expression"""
        # Simple condition parsing - would be more sophisticated in practice
        if "test" in condition or "[" in condition:
            # Extract test condition
            test_expr = condition.replace("test", "").replace("[", "").replace("]", "").strip()
            return self._parse_test_expression(test_expr)
        else:
            # Command condition - check exit code
            return FunctionCall(
                function=Identifier("runa.shell.success"),
                args=[StringLiteral(condition)]
            )
    
    def _parse_test_expression(self, expr: str) -> Expression:
        """Parse shell test expression"""
        # Simple parser - would be more sophisticated in practice
        parts = expr.split()
        
        if len(parts) == 3:
            left, op, right = parts
            
            if op in self.operator_mappings:
                runa_op = self.operator_mappings[op]
                left_expr = self._convert_shell_value(left)
                right_expr = self._convert_shell_value(right)
                
                if runa_op in ("==", "!=", "<", "<=", ">", ">="):
                    return BinaryExpression(
                        left=left_expr,
                        operator=runa_op,
                        right=right_expr
                    )
                else:
                    # Use function call for special operators
                    return FunctionCall(
                        function=Identifier(f"runa.test.{runa_op}"),
                        args=[left_expr, right_expr] if runa_op not in ("is_empty", "is_not_empty") else [left_expr]
                    )
        
        # Fallback to string literal
        return StringLiteral(expr)
    
    def _convert_shell_argument(self, arg: str) -> Expression:
        """Convert shell argument to Runa expression"""
        # Handle parameter expansions, command substitutions, etc.
        if arg.startswith("$"):
            return self._convert_shell_expansion(arg)
        else:
            return StringLiteral(arg)
    
    def _convert_shell_value(self, value: str) -> Expression:
        """Convert shell value to Runa expression"""
        # Handle different shell value types
        if value.startswith("$"):
            return self._convert_shell_expansion(value)
        elif value.startswith('"') and value.endswith('"'):
            return StringLiteral(value[1:-1])
        elif value.startswith("'") and value.endswith("'"):
            return StringLiteral(value[1:-1])
        elif value.isdigit():
            return IntegerLiteral(int(value))
        else:
            return StringLiteral(value)
    
    def _convert_shell_expansion(self, expansion: str) -> Expression:
        """Convert shell parameter expansion to Runa expression"""
        if expansion.startswith("${"):
            # Parameter expansion
            var_name = expansion[2:-1]
            return FunctionCall(
                function=Identifier("runa.env.get"),
                args=[StringLiteral(var_name)]
            )
        elif expansion.startswith("$("):
            # Command substitution  
            command = expansion[2:-1]
            return FunctionCall(
                function=Identifier("runa.shell.capture"),
                args=[StringLiteral(command)]
            )
        elif expansion.startswith("$"):
            # Simple variable
            var_name = expansion[1:]
            return FunctionCall(
                function=Identifier("runa.env.get"),
                args=[StringLiteral(var_name)]
            )
        else:
            return StringLiteral(expansion)
    
    def _convert_redirections(self, redirections: List[ShellRedirection]) -> Expression:
        """Convert shell redirections to Runa redirection config"""
        redirection_fields = []
        
        for redir in redirections:
            if redir.is_output_redirection:
                redirection_fields.append(RunaStructField(
                    name="stdout",
                    value=StringLiteral(redir.target)
                ))
            elif redir.is_input_redirection:
                redirection_fields.append(RunaStructField(
                    name="stdin", 
                    value=StringLiteral(redir.target)
                ))
        
        return RunaStructLiteral(fields=redirection_fields)
    
    def _infer_shell_value_type(self, value: str) -> BasicType:
        """Infer Runa type from shell value"""
        if value.isdigit():
            return RunaNominalType("Int")
        elif value.replace(".", "").isdigit():
            return RunaNominalType("Float")
        elif value.lower() in ("true", "false"):
            return RunaNominalType("Bool")
        else:
            return RunaNominalType("String")
    
    def _detect_shell_type(self, shebang: Optional[str]) -> str:
        """Detect shell type from shebang"""
        if not shebang:
            return "sh"
        
        if "bash" in shebang:
            return "bash"
        elif "zsh" in shebang:
            return "zsh"
        elif "fish" in shebang:
            return "fish"
        elif "dash" in shebang:
            return "dash"
        else:
            return "sh"


class RunaToShellConverter:
    """Converts Runa AST to Shell AST"""
    
    def __init__(self):
        self.context_stack: List[Dict[str, Any]] = [{}]
        self.function_mappings: Dict[str, str] = {}
        
        # Reverse mappings from Runa to Shell
        self.runa_to_shell_commands = {
            "runa.fs.list_dir": "ls",
            "runa.fs.copy": "cp",
            "runa.fs.move": "mv",
            "runa.fs.remove": "rm",
            "runa.fs.create_dir": "mkdir",
            "runa.fs.remove_dir": "rmdir",
            "runa.fs.read_file": "cat",
            "runa.fs.write_file": "tee",
            "runa.fs.current_dir": "pwd",
            "runa.fs.change_dir": "cd",
            
            "runa.io.print": "echo",
            "runa.io.println": "echo",
            "runa.io.printf": "printf",
            "runa.io.read_input": "read",
            
            "runa.process.run": "",  # Direct command execution
            "runa.process.kill": "kill",
            "runa.process.list": "ps",
            
            "runa.system.exit": "exit",
            "runa.system.hostname": "hostname",
            "runa.system.date": "date",
            
            "runa.text.grep": "grep",
            "runa.text.sed": "sed",
            "runa.text.awk": "awk",
            "runa.text.sort": "sort",
        }
    
    def convert(self, runa_module: RunaModule) -> ShellScript:
        """Convert Runa module to Shell script"""
        script = ShellScript()
        
        # Set shebang from metadata
        if runa_module.metadata and "shebang" in runa_module.metadata:
            script.shebang = runa_module.metadata["shebang"]
        else:
            script.shebang = "#!/bin/bash"
        
        # Convert declarations
        for decl in runa_module.declarations:
            if isinstance(decl, ProcessDefinition):
                if decl.name == "main":
                    # Convert main function body to script statements
                    for stmt in decl.body.statements:
                        shell_stmt = self._convert_statement(stmt)
                        if shell_stmt:
                            if isinstance(shell_stmt, list):
                                script.statements.extend(shell_stmt)
                            else:
                                script.statements.append(shell_stmt)
                else:
                    # Convert to shell function
                    shell_func = self._convert_function_declaration(decl)
                    script.add_function(shell_func)
            elif isinstance(decl, LetStatement):
                # Convert to shell variable assignment
                shell_var = self._convert_variable_declaration(decl)
                script.add_statement(shell_var)
        
        return script
    
    def _convert_statement(self, stmt: Statement) -> Optional[Union[ShellStatement, List[ShellStatement]]]:
        """Convert Runa statement to Shell statement(s)"""
        if isinstance(stmt, ExpressionStatement):
            return self._convert_expression_statement(stmt)
        elif isinstance(stmt, LetStatement):
            return self._convert_variable_declaration(stmt)
        elif isinstance(stmt, IfStatement):
            return self._convert_if_statement(stmt)
        elif isinstance(stmt, RunaForLoop):
            return self._convert_for_loop(stmt)
        elif isinstance(stmt, WhileLoop):
            return self._convert_while_loop(stmt)
        elif isinstance(stmt, Block):
            statements = []
            for s in stmt.statements:
                shell_stmt = self._convert_statement(s)
                if shell_stmt:
                    if isinstance(shell_stmt, list):
                        statements.extend(shell_stmt)
                    else:
                        statements.append(shell_stmt)
            return statements
        else:
            return None
    
    def _convert_expression_statement(self, stmt: ExpressionStatement) -> Optional[ShellStatement]:
        """Convert Runa expression statement to Shell command"""
        if isinstance(stmt.expression, FunctionCall):
            return self._convert_function_call_to_command(stmt.expression)
        else:
            return None
    
    def _convert_function_call_to_command(self, call: FunctionCall) -> Optional[ShellStatement]:
        """Convert Runa function call to Shell command"""
        if isinstance(call.function, Identifier):
            func_name = call.function.name
            
            # Check if it's a shell command mapping
            if func_name in self.runa_to_shell_commands:
                shell_cmd = self.runa_to_shell_commands[func_name]
                
                if shell_cmd:  # Not empty string
                    args = []
                    for arg in call.args:
                        if isinstance(arg, StringLiteral):
                            args.append(arg.value)
                        else:
                            args.append(str(arg))  # Simplified conversion
                    
                    return ShellCommand(command=shell_cmd, arguments=args)
                else:
                    # Direct command execution
                    if call.args and isinstance(call.args[0], StringLiteral):
                        return ShellCommand(command=call.args[0].value)
            
            # Handle shell-specific functions
            elif func_name == "runa.shell.pipeline":
                return self._convert_pipeline_call(call)
            elif func_name == "runa.shell.execute":
                if call.args and isinstance(call.args[0], StringLiteral):
                    cmd_args = [arg.value for arg in call.args[1:] if isinstance(arg, StringLiteral)]
                    return ShellCommand(command=call.args[0].value, arguments=cmd_args)
        
        return None
    
    def _convert_pipeline_call(self, call: FunctionCall) -> Optional[ShellPipeline]:
        """Convert Runa pipeline call to Shell pipeline"""
        if call.args and isinstance(call.args[0], ListLiteral):
            commands = []
            for elem in call.args[0].elements:
                if isinstance(elem, FunctionCall):
                    shell_cmd = self._convert_function_call_to_command(elem)
                    if isinstance(shell_cmd, ShellCommand):
                        commands.append(shell_cmd)
            
            if commands:
                return ShellPipeline(commands=commands)
        
        return None
    
    def _convert_variable_declaration(self, decl: LetStatement) -> ShellVariableAssignment:
        """Convert Runa variable declaration to Shell variable assignment"""
        value = ""
        if isinstance(decl.value, StringLiteral):
            value = decl.value.value
        elif isinstance(decl.value, IntegerLiteral):
            value = str(decl.value.value)
        elif isinstance(decl.value, BooleanLiteral):
            value = "true" if decl.value.value else "false"
        else:
            value = str(decl.value)  # Simplified conversion
        
        # Check annotations for shell-specific flags
        export = False
        readonly = False
        local = False
        
        if isinstance(decl.type, RunaAnnotatedType):
            for ann in decl.type.annotations:
                if ann.name == "export":
                    export = True
                elif ann.name == "readonly":
                    readonly = True
                elif ann.name == "local":
                    local = True
        
        return ShellVariableAssignment(
            variable=decl.name,
            value=value,
            export=export,
            readonly=readonly,
            local=local
        )
    
    def _convert_function_declaration(self, decl: ProcessDefinition) -> ShellFunctionDefinition:
        """Convert Runa function declaration to Shell function"""
        func = ShellFunctionDefinition(name=decl.name)
        
        # Convert function body
        for stmt in decl.body.statements:
            shell_stmt = self._convert_statement(stmt)
            if shell_stmt:
                if isinstance(shell_stmt, list):
                    func.body.extend(shell_stmt)
                else:
                    func.body.append(shell_stmt)
        
        return func
    
    def _convert_if_statement(self, stmt: IfStatement) -> ShellConditional:
        """Convert Runa if statement to Shell conditional"""
        conditional = ShellConditional(
            conditional_type="if",
            condition=self._convert_condition_to_shell(stmt.condition)
        )
        
        # Convert then block
        for s in stmt.then_block.statements:
            shell_stmt = self._convert_statement(s)
            if shell_stmt:
                if isinstance(shell_stmt, list):
                    conditional.then_body.extend(shell_stmt)
                else:
                    conditional.then_body.append(shell_stmt)
        
        # Convert else block
        if stmt.else_block:
            for s in stmt.else_block.statements:
                shell_stmt = self._convert_statement(s)
                if shell_stmt:
                    if isinstance(shell_stmt, list):
                        conditional.else_body.extend(shell_stmt)
                    else:
                        conditional.else_body.append(shell_stmt)
        
        return conditional
    
    def _convert_for_loop(self, loop: RunaForLoop) -> ShellLoop:
        """Convert Runa for loop to Shell for loop"""
        shell_loop = ShellLoop(
            loop_type="for",
            variable=loop.variable,
            condition="",  # Will be set based on iterable
            iterable=self._convert_expression_to_shell(loop.iterable)
        )
        
        # Convert loop body
        for stmt in loop.body.statements:
            shell_stmt = self._convert_statement(stmt)
            if shell_stmt:
                if isinstance(shell_stmt, list):
                    shell_loop.body.extend(shell_stmt)
                else:
                    shell_loop.body.append(shell_stmt)
        
        return shell_loop
    
    def _convert_while_loop(self, loop: WhileLoop) -> ShellLoop:
        """Convert Runa while loop to Shell while loop"""
        shell_loop = ShellLoop(
            loop_type="while",
            condition=self._convert_condition_to_shell(loop.condition)
        )
        
        # Convert loop body
        for stmt in loop.body.statements:
            shell_stmt = self._convert_statement(stmt)
            if shell_stmt:
                if isinstance(shell_stmt, list):
                    shell_loop.body.extend(shell_stmt)
                else:
                    shell_loop.body.append(shell_stmt)
        
        return shell_loop
    
    def _convert_condition_to_shell(self, condition: Expression) -> str:
        """Convert Runa condition to Shell test expression"""
        if isinstance(condition, BinaryExpression):
            left = self._convert_expression_to_shell(condition.left)
            right = self._convert_expression_to_shell(condition.right)
            op = condition.operator
            
            # Map Runa operators to shell test operators
            if op == "==":
                return f'[ "{left}" = "{right}" ]'
            elif op == "!=":
                return f'[ "{left}" != "{right}" ]'
            elif op == "<":
                return f'[ "{left}" -lt "{right}" ]'
            elif op == "<=":
                return f'[ "{left}" -le "{right}" ]'
            elif op == ">":
                return f'[ "{left}" -gt "{right}" ]'
            elif op == ">=":
                return f'[ "{left}" -ge "{right}" ]'
        
        # Fallback to string representation
        return str(condition)
    
    def _convert_expression_to_shell(self, expr: Expression) -> str:
        """Convert Runa expression to Shell string"""
        if isinstance(expr, StringLiteral):
            return expr.value
        elif isinstance(expr, IntegerLiteral):
            return str(expr.value)
        elif isinstance(expr, Identifier):
            return f"${expr.name}"
        else:
            return str(expr)  # Simplified conversion


def shell_to_runa(shell_script: ShellScript) -> RunaModule:
    """Convert Shell script to Runa module"""
    converter = ShellToRunaConverter()
    return converter.convert(shell_script)


def runa_to_shell(runa_module: RunaModule) -> ShellScript:
    """Convert Runa module to Shell script"""
    converter = RunaToShellConverter()
    return converter.convert(runa_module) 