"""
Tcl Converter for Runa Universal Translation Platform

Provides bidirectional conversion between Runa AST and Tcl AST,
supporting Tcl's automation scripting and text processing capabilities.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

from ...core.ast_base import ASTNode
from ...core.conversion_base import BaseConverter
from ...core.error_handler import ErrorHandler, ConversionError
from ...core.runa_ast import *

from .tcl_ast import (
    TclScript, TclCommand, TclWord, TclProc, TclIf, TclWhile, TclFor, TclForeach,
    TclVariableSubstitution, TclVariable, TclSet, TclStringLiteral, TclList,
    TclReturn, TclBreak, TclContinue, TclComment, TclExpr
)

@dataclass
class TclConversionContext:
    """Context for Tcl conversion operations"""
    current_namespace: Optional[str] = None
    in_procedure: bool = False
    string_processing_mode: bool = False

class TclConverter(BaseConverter):
    """Converter for Tcl language with automation scripting support"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        self.context = TclConversionContext()
    
    def runa_to_tcl(self, runa_node: ASTNode) -> Optional[ASTNode]:
        """Convert Runa AST to Tcl AST"""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program_to_tcl(runa_node)
            elif isinstance(runa_node, RunaFunction):
                return self._convert_function_to_tcl(runa_node)
            elif isinstance(runa_node, IfStatement):
                return self._convert_if_to_tcl(runa_node)
            elif isinstance(runa_node, WhileLoop):
                return self._convert_while_to_tcl(runa_node)
            elif isinstance(runa_node, RunaForLoop):
                return self._convert_for_to_tcl(runa_node)
            elif isinstance(runa_node, FunctionCall):
                return self._convert_function_call_to_tcl(runa_node)
            elif isinstance(runa_node, SetStatement):
                return self._convert_assignment_to_tcl(runa_node)
            elif isinstance(runa_node, RunaVariable):
                return self._convert_variable_to_tcl(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return self._convert_literal_to_tcl(runa_node)
            elif isinstance(runa_node, ListLiteral):
                return self._convert_list_to_tcl(runa_node)
            elif isinstance(runa_node, RunaComment):
                return TclComment(text=runa_node.text)
            elif isinstance(runa_node, ReturnStatement):
                return self._convert_return_to_tcl(runa_node)
            elif isinstance(runa_node, BreakStatement):
                return TclBreak()
            elif isinstance(runa_node, ContinueStatement):
                return TclContinue()
            else:
                self.logger.warning(f"Unsupported Runa node type: {type(runa_node)}")
                return None
        except Exception as e:
            self.error_handler.handle_error(ConversionError(f"Runa to Tcl conversion error: {e}"))
            return None
    
    def tcl_to_runa(self, tcl_node: ASTNode) -> Optional[ASTNode]:
        """Convert Tcl AST to Runa AST"""
        try:
            if isinstance(tcl_node, TclScript):
                return self._convert_tcl_script_to_runa(tcl_node)
            elif isinstance(tcl_node, TclCommand):
                return self._convert_tcl_command_to_runa(tcl_node)
            elif isinstance(tcl_node, TclProc):
                return self._convert_tcl_proc_to_runa(tcl_node)
            elif isinstance(tcl_node, TclSet):
                return self._convert_tcl_set_to_runa(tcl_node)
            elif isinstance(tcl_node, TclVariable):
                return RunaVariable(name=tcl_node.name)
            elif isinstance(tcl_node, TclStringLiteral):
                return RunaString(value=tcl_node.value)
            elif isinstance(tcl_node, TclList):
                return self._convert_tcl_list_to_runa(tcl_node)
            elif isinstance(tcl_node, TclComment):
                return RunaComment(text=tcl_node.text)
            elif isinstance(tcl_node, TclReturn):
                return self._convert_tcl_return_to_runa(tcl_node)
            elif isinstance(tcl_node, TclBreak):
                return BreakStatement()
            elif isinstance(tcl_node, TclContinue):
                return ContinueStatement()
            else:
                self.logger.warning(f"Unsupported Tcl node type: {type(tcl_node)}")
                return None
        except Exception as e:
            self.error_handler.handle_error(ConversionError(f"Tcl to Runa conversion error: {e}"))
            return None
    
    # Runa to Tcl conversion methods
    
    def _convert_program_to_tcl(self, program: Program) -> TclScript:
        """Convert Runa program to Tcl script"""
        script = TclScript()
        for stmt in program.statements:
            tcl_stmt = self.runa_to_tcl(stmt)
            if tcl_stmt and isinstance(tcl_stmt, TclCommand):
                script.commands.append(tcl_stmt)
        return script
    
    def _convert_function_to_tcl(self, func: RunaFunction) -> TclProc:
        """Convert Runa function to Tcl procedure"""
        tcl_proc = TclProc(
            name=func.name,
            parameters=[param.name for param in func.parameters]
        )
        if func.body:
            body_script = TclScript()
            for stmt in func.body.statements:
                tcl_stmt = self.runa_to_tcl(stmt)
                if tcl_stmt and isinstance(tcl_stmt, TclCommand):
                    body_script.commands.append(tcl_stmt)
            tcl_proc.body = body_script
        return tcl_proc
    
    def _convert_if_to_tcl(self, if_stmt: IfStatement) -> TclIf:
        """Convert Runa if statement to Tcl if"""
        condition = self._expression_to_tcl_word(if_stmt.condition)
        then_body = self._block_to_tcl_script(if_stmt.then_block)
        tcl_if = TclIf(condition=condition, then_body=then_body)
        if if_stmt.else_block:
            tcl_if.else_body = self._block_to_tcl_script(if_stmt.else_block)
        return tcl_if
    
    def _convert_while_to_tcl(self, while_loop: WhileLoop) -> TclWhile:
        """Convert Runa while loop to Tcl while"""
        condition = self._expression_to_tcl_word(while_loop.condition)
        body = self._block_to_tcl_script(while_loop.body)
        return TclWhile(condition=condition, body=body)
    
    def _convert_for_to_tcl(self, for_loop: RunaForLoop) -> TclForeach:
        """Convert Runa for loop to Tcl foreach"""
        var_name = for_loop.target.name if hasattr(for_loop.target, 'name') else str(for_loop.target)
        iterable = self._expression_to_tcl_word(for_loop.iterable)
        body = self._block_to_tcl_script(for_loop.body)
        return TclForeach(variables=[var_name], list_expr=iterable, body=body)
    
    def _convert_function_call_to_tcl(self, call: FunctionCall) -> TclCommand:
        """Convert Runa function call to Tcl command"""
        command_name = call.function.name if hasattr(call.function, 'name') else str(call.function)
        tcl_args = [self._expression_to_tcl_word(arg) for arg in call.arguments]
        return TclCommand(command_name=command_name, arguments=tcl_args)
    
    def _convert_assignment_to_tcl(self, assign: SetStatement) -> TclSet:
        """Convert Runa assignment to Tcl set command"""
        if isinstance(assign.target, RunaVariable):
            variable = TclVariable(name=assign.target.name)
            value = self._expression_to_tcl_word(assign.value)
            return TclSet(variable=variable, value=value)
        else:
            variable = TclVariable(name=str(assign.target))
            value = self._expression_to_tcl_word(assign.value)
            return TclSet(variable=variable, value=value)
    
    def _convert_variable_to_tcl(self, var: RunaVariable) -> TclVariableSubstitution:
        """Convert Runa variable to Tcl variable substitution"""
        return TclVariableSubstitution(variable_name=var.name)
    
    def _convert_literal_to_tcl(self, literal: StringLiteral) -> TclWord:
        """Convert Runa literal to Tcl word"""
        return TclWord(content=str(literal.value))
    
    def _convert_list_to_tcl(self, runa_list: ListLiteral) -> TclList:
        """Convert Runa list to Tcl list"""
        tcl_elements = [self._expression_to_tcl_word(elem) for elem in runa_list.elements]
        return TclList(elements=tcl_elements)
    
    def _convert_return_to_tcl(self, ret: ReturnStatement) -> TclReturn:
        """Convert Runa return to Tcl return"""
        if ret.value:
            value = self._expression_to_tcl_word(ret.value)
            return TclReturn(value=value)
        return TclReturn()
    
    # Tcl to Runa conversion methods
    
    def _convert_tcl_script_to_runa(self, script: TclScript) -> Program:
        """Convert Tcl script to Runa program"""
        statements = []
        for command in script.commands:
            runa_stmt = self.tcl_to_runa(command)
            if runa_stmt:
                statements.append(runa_stmt)
        return Program(statements=statements)
    
    def _convert_tcl_command_to_runa(self, command: TclCommand) -> Optional[ASTNode]:
        """Convert Tcl command to Runa node"""
        cmd_name = command.command_name.lower()
        if cmd_name == "set":
            return self._convert_tcl_set_command_to_runa(command)
        elif cmd_name == "proc":
            return self._convert_tcl_proc_command_to_runa(command)
        else:
            args = [self._tcl_word_to_runa_expression(arg) for arg in command.arguments]
            return FunctionCall(
                function=RunaVariable(name=command.command_name),
                arguments=args
            )
    
    def _convert_tcl_proc_to_runa(self, proc: TclProc) -> RunaFunction:
        """Convert Tcl procedure to Runa function"""
        parameters = [RunaVariable(name=param) for param in proc.parameters]
        body = Block(statements=[])
        if proc.body:
            for command in proc.body.commands:
                runa_stmt = self.tcl_to_runa(command)
                if runa_stmt:
                    body.statements.append(runa_stmt)
        return RunaFunction(name=proc.name, parameters=parameters, body=body)
    
    def _convert_tcl_set_to_runa(self, set_node: TclSet) -> SetStatement:
        """Convert Tcl set to Runa assignment"""
        if isinstance(set_node.variable, TclVariable):
            target = RunaVariable(name=set_node.variable.name)
        else:
            target = RunaVariable(name=str(set_node.variable))
        
        value = self._tcl_word_to_runa_expression(set_node.value) if set_node.value else RunaString(value="")
        return SetStatement(target=target, value=value)
    
    def _convert_tcl_list_to_runa(self, tcl_list: TclList) -> ListLiteral:
        """Convert Tcl list to Runa list"""
        elements = [self._tcl_word_to_runa_expression(elem) for elem in tcl_list.elements]
        return ListLiteral(elements=elements)
    
    def _convert_tcl_return_to_runa(self, ret: TclReturn) -> ReturnStatement:
        """Convert Tcl return to Runa return"""
        if ret.value:
            value = self._tcl_word_to_runa_expression(ret.value)
            return ReturnStatement(value=value)
        return ReturnStatement()
    
    # Helper methods
    
    def _expression_to_tcl_word(self, expr: ASTNode) -> TclWord:
        """Convert expression to Tcl word"""
        if isinstance(expr, RunaVariable):
            return TclWord(content=f"${expr.name}")
        elif isinstance(expr, StringLiteral):
            return TclWord(content=str(expr.value))
        elif isinstance(expr, RunaString):
            return TclWord(content=f'"{expr.value}"', is_quoted=True)
        else:
            return TclWord(content=str(expr))
    
    def _block_to_tcl_script(self, block: Block) -> TclScript:
        """Convert Runa block to Tcl script"""
        script = TclScript()
        for stmt in block.statements:
            tcl_stmt = self.runa_to_tcl(stmt)
            if tcl_stmt and isinstance(tcl_stmt, TclCommand):
                script.commands.append(tcl_stmt)
        return script
    
    def _tcl_word_to_runa_expression(self, word: TclWord) -> ASTNode:
        """Convert Tcl word to Runa expression"""
        content = word.content
        if content.startswith("$"):
            return RunaVariable(name=content[1:])
        elif word.is_quoted:
            return RunaString(value=content.strip('"'))
        else:
            try:
                if '.' in content:
                    return RunaNumber(value=float(content))
                else:
                    return RunaNumber(value=int(content))
            except ValueError:
                return RunaString(value=content)
    
    def _convert_tcl_set_command_to_runa(self, command: TclCommand) -> Optional[SetStatement]:
        """Convert Tcl set command to Runa assignment"""
        if len(command.arguments) >= 2:
            var_name = command.arguments[0].content
            value = self._tcl_word_to_runa_expression(command.arguments[1])
            return SetStatement(target=RunaVariable(name=var_name), value=value)
        return None
    
    def _convert_tcl_proc_command_to_runa(self, command: TclCommand) -> Optional[RunaFunction]:
        """Convert Tcl proc command to Runa function"""
        if len(command.arguments) >= 3:
            name = command.arguments[0].content
            params_str = command.arguments[1].content
            param_names = params_str.split() if params_str else []
            parameters = [RunaVariable(name=param) for param in param_names]
            body = Block(statements=[])
            return RunaFunction(name=name, parameters=parameters, body=body)
        return None
    
    def get_conversion_info(self) -> Dict[str, Any]:
        """Get Tcl conversion capabilities information"""
        return {
            "source_language": "tcl",
            "target_languages": ["runa"],
            "features_supported": [
                "automation_scripting", "text_processing", "string_manipulation",
                "command_substitution", "variable_substitution", "list_processing",
                "control_structures", "procedures", "file_io"
            ],
            "limitations": ["complex_tk_gui", "advanced_namespaces"]
        } 