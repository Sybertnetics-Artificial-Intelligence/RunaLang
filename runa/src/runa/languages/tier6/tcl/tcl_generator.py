"""
Tcl Code Generator for Runa Universal Translation Platform

Generates clean, idiomatic Tcl code from AST nodes,
supporting automation scripting and text processing features.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

from ...core.generation_base import BaseGenerator
from ...core.error_handler import ErrorHandler, GenerationError
from .tcl_ast import (
    TclScript, TclCommand, TclWord, TclProc, TclNamespace, TclPackage,
    TclIf, TclElseIf, TclWhile, TclFor, TclForeach, TclSwitch, TclSwitchPattern,
    TclTry, TclCatch, TclVariableSubstitution, TclCommandSubstitution,
    TclBackslashSubstitution, TclVariable, TclArrayElement, TclSet, TclGlobal,
    TclUpvar, TclStringLiteral, TclQuotedString, TclBracedString, TclList,
    TclStringMatch, TclStringMap, TclStringRange, TclStringIndex,
    TclLappend, TclLindex, TclLlength, TclLrange, TclLsort,
    TclRegexp, TclRegsub, TclOpen, TclClose, TclPuts, TclGets, TclRead,
    TclExec, TclSource, TclEval, TclError, TclReturn, TclBreak, TclContinue,
    TclExpr, TclIncr, TclUnset, TclInfo, TclComment, TclNode, TclNodeType
)

@dataclass
class TclGenerationContext:
    """Context for Tcl code generation"""
    indent_level: int = 0
    indent_size: int = 4
    current_namespace: Optional[str] = None
    in_procedure: bool = False
    automation_mode: bool = True
    string_processing_mode: bool = False
    generate_comments: bool = True
    
    def get_indent(self) -> str:
        """Get current indentation string"""
        return " " * (self.indent_level * self.indent_size)
    
    def increase_indent(self):
        """Increase indentation level"""
        self.indent_level += 1
    
    def decrease_indent(self):
        """Decrease indentation level"""
        self.indent_level = max(0, self.indent_level - 1)

class TclGenerator(BaseGenerator):
    """Generator for clean, idiomatic Tcl code"""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        self.context = TclGenerationContext()
        
        # Tcl keywords that need special handling
        self.tcl_keywords = {
            'if', 'else', 'elseif', 'while', 'for', 'foreach', 'switch',
            'proc', 'return', 'break', 'continue', 'set', 'unset', 'global',
            'upvar', 'variable', 'namespace', 'package', 'source', 'eval',
            'expr', 'incr', 'string', 'list', 'lappend', 'lindex', 'llength',
            'lrange', 'lreplace', 'lsearch', 'lsort', 'regexp', 'regsub',
            'open', 'close', 'puts', 'gets', 'read', 'exec', 'error', 'catch',
            'try', 'finally', 'throw', 'info', 'file', 'glob', 'join', 'split'
        }
        
        # Special characters that need escaping in strings
        self.escape_chars = {
            '\n': '\\n', '\t': '\\t', '\r': '\\r', '\b': '\\b',
            '\f': '\\f', '\v': '\\v', '\\': '\\\\', '"': '\\"',
            '$': '\\$', '[': '\\[', ']': '\\]', '{': '\\{', '}': '\\}'
        }
    
    def generate(self, node: TclNode) -> str:
        """Generate Tcl code from AST node"""
        try:
            if isinstance(node, TclScript):
                return self._generate_script(node)
            elif isinstance(node, TclCommand):
                return self._generate_command(node)
            elif isinstance(node, TclWord):
                return self._generate_word(node)
            elif isinstance(node, TclProc):
                return self._generate_proc(node)
            elif isinstance(node, TclNamespace):
                return self._generate_namespace(node)
            elif isinstance(node, TclPackage):
                return self._generate_package(node)
            elif isinstance(node, TclIf):
                return self._generate_if(node)
            elif isinstance(node, TclWhile):
                return self._generate_while(node)
            elif isinstance(node, TclFor):
                return self._generate_for(node)
            elif isinstance(node, TclForeach):
                return self._generate_foreach(node)
            elif isinstance(node, TclSwitch):
                return self._generate_switch(node)
            elif isinstance(node, TclTry):
                return self._generate_try(node)
            elif isinstance(node, TclSet):
                return self._generate_set(node)
            elif isinstance(node, TclVariable):
                return self._generate_variable(node)
            elif isinstance(node, TclVariableSubstitution):
                return self._generate_variable_substitution(node)
            elif isinstance(node, TclCommandSubstitution):
                return self._generate_command_substitution(node)
            elif isinstance(node, TclStringLiteral):
                return self._generate_string_literal(node)
            elif isinstance(node, TclQuotedString):
                return self._generate_quoted_string(node)
            elif isinstance(node, TclBracedString):
                return self._generate_braced_string(node)
            elif isinstance(node, TclList):
                return self._generate_list(node)
            elif isinstance(node, TclComment):
                return self._generate_comment(node)
            elif isinstance(node, TclReturn):
                return self._generate_return(node)
            elif isinstance(node, TclBreak):
                return "break"
            elif isinstance(node, TclContinue):
                return "continue"
            elif isinstance(node, TclExpr):
                return self._generate_expr(node)
            elif isinstance(node, TclIncr):
                return self._generate_incr(node)
            elif isinstance(node, TclUnset):
                return self._generate_unset(node)
            # String operations
            elif isinstance(node, TclStringMatch):
                return self._generate_string_match(node)
            elif isinstance(node, TclStringMap):
                return self._generate_string_map(node)
            elif isinstance(node, TclStringRange):
                return self._generate_string_range(node)
            elif isinstance(node, TclStringIndex):
                return self._generate_string_index(node)
            # List operations
            elif isinstance(node, TclLappend):
                return self._generate_lappend(node)
            elif isinstance(node, TclLindex):
                return self._generate_lindex(node)
            elif isinstance(node, TclLlength):
                return self._generate_llength(node)
            elif isinstance(node, TclLrange):
                return self._generate_lrange(node)
            elif isinstance(node, TclLsort):
                return self._generate_lsort(node)
            # Regular expressions
            elif isinstance(node, TclRegexp):
                return self._generate_regexp(node)
            elif isinstance(node, TclRegsub):
                return self._generate_regsub(node)
            # File I/O
            elif isinstance(node, TclOpen):
                return self._generate_open(node)
            elif isinstance(node, TclClose):
                return self._generate_close(node)
            elif isinstance(node, TclPuts):
                return self._generate_puts(node)
            elif isinstance(node, TclGets):
                return self._generate_gets(node)
            elif isinstance(node, TclRead):
                return self._generate_read(node)
            # System interaction
            elif isinstance(node, TclExec):
                return self._generate_exec(node)
            elif isinstance(node, TclSource):
                return self._generate_source(node)
            elif isinstance(node, TclEval):
                return self._generate_eval(node)
            elif isinstance(node, TclError):
                return self._generate_error(node)
            elif isinstance(node, TclInfo):
                return self._generate_info(node)
            else:
                self.logger.warning(f"Unsupported Tcl node type: {type(node)}")
                return f"# Unsupported node: {type(node)}"
                
        except Exception as e:
            self.error_handler.handle_error(
                GenerationError(f"Error generating Tcl code: {e}")
            )
            return f"# Error: {e}"
    
    def _generate_script(self, script: TclScript) -> str:
        """Generate Tcl script"""
        lines = []
        
        if self.context.generate_comments:
            lines.append("#!/usr/bin/tclsh")
            lines.append("# Generated Tcl script")
            lines.append("")
        
        for command in script.commands:
            cmd_code = self.generate(command)
            if cmd_code:
                lines.append(self.context.get_indent() + cmd_code)
        
        return "\n".join(lines)
    
    def _generate_command(self, command: TclCommand) -> str:
        """Generate Tcl command"""
        parts = [command.command_name]
        
        for arg in command.arguments:
            arg_code = self.generate(arg)
            parts.append(arg_code)
        
        return " ".join(parts)
    
    def _generate_word(self, word: TclWord) -> str:
        """Generate Tcl word"""
        if isinstance(word.content, str):
            content = word.content
            if word.is_quoted:
                return f'"{self._escape_string(content)}"'
            elif word.is_braced:
                return f"{{{content}}}"
            else:
                # Check if content needs quoting
                if self._needs_quoting(content):
                    return f'"{self._escape_string(content)}"'
                return content
        else:
            # Handle substitutions
            result = ""
            for item in word.content:
                if isinstance(item, str):
                    result += item
                else:
                    result += self.generate(item)
            
            if word.is_quoted:
                return f'"{result}"'
            elif word.is_braced:
                return f"{{{result}}}"
            return result
    
    def _generate_proc(self, proc: TclProc) -> str:
        """Generate Tcl procedure"""
        lines = []
        
        # Build parameter list
        param_parts = []
        for param in proc.parameters:
            if param in proc.default_values:
                default_val = self.generate(proc.default_values[param])
                param_parts.append(f"{{{param} {default_val}}}")
            else:
                param_parts.append(param)
        
        param_list = " ".join(param_parts)
        
        # Generate procedure header
        lines.append(f"proc {proc.name} {{{param_list}}} {{")
        
        # Generate body
        self.context.increase_indent()
        self.context.in_procedure = True
        
        if proc.body and proc.body.commands:
            for command in proc.body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
        
        self.context.in_procedure = False
        self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_namespace(self, namespace: TclNamespace) -> str:
        """Generate Tcl namespace"""
        lines = []
        lines.append(f"namespace eval {namespace.name} {{")
        
        self.context.increase_indent()
        old_namespace = self.context.current_namespace
        self.context.current_namespace = namespace.name
        
        if namespace.body and namespace.body.commands:
            for command in namespace.body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
        
        self.context.current_namespace = old_namespace
        self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_package(self, package: TclPackage) -> str:
        """Generate Tcl package declaration"""
        lines = []
        lines.append(f"package provide {package.name} {package.version}")
        
        for req in package.requirements:
            lines.append(f"package require {req}")
        
        return "\n".join(lines)
    
    def _generate_if(self, if_stmt: TclIf) -> str:
        """Generate Tcl if statement"""
        lines = []
        
        condition = self.generate(if_stmt.condition)
        lines.append(f"if {{{condition}}} {{")
        
        # Generate then block
        self.context.increase_indent()
        for command in if_stmt.then_body.commands:
            cmd_code = self.generate(command)
            if cmd_code:
                lines.append(self.context.get_indent() + cmd_code)
        self.context.decrease_indent()
        
        # Generate elseif clauses
        for elseif in if_stmt.elseif_clauses:
            elseif_condition = self.generate(elseif.condition)
            lines.append(f"}} elseif {{{elseif_condition}}} {{")
            
            self.context.increase_indent()
            for command in elseif.body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
            self.context.decrease_indent()
        
        # Generate else block
        if if_stmt.else_body:
            lines.append("} else {")
            
            self.context.increase_indent()
            for command in if_stmt.else_body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
            self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_while(self, while_loop: TclWhile) -> str:
        """Generate Tcl while loop"""
        lines = []
        
        condition = self.generate(while_loop.condition)
        lines.append(f"while {{{condition}}} {{")
        
        self.context.increase_indent()
        for command in while_loop.body.commands:
            cmd_code = self.generate(command)
            if cmd_code:
                lines.append(self.context.get_indent() + cmd_code)
        self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_for(self, for_loop: TclFor) -> str:
        """Generate Tcl for loop"""
        lines = []
        
        # Generate init, condition, and increment
        init_code = ""
        if for_loop.init.commands:
            init_parts = []
            for cmd in for_loop.init.commands:
                init_parts.append(self.generate(cmd))
            init_code = "; ".join(init_parts)
        
        condition = self.generate(for_loop.condition)
        
        increment_code = ""
        if for_loop.increment.commands:
            incr_parts = []
            for cmd in for_loop.increment.commands:
                incr_parts.append(self.generate(cmd))
            increment_code = "; ".join(incr_parts)
        
        lines.append(f"for {{{init_code}}} {{{condition}}} {{{increment_code}}} {{")
        
        self.context.increase_indent()
        for command in for_loop.body.commands:
            cmd_code = self.generate(command)
            if cmd_code:
                lines.append(self.context.get_indent() + cmd_code)
        self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_foreach(self, foreach: TclForeach) -> str:
        """Generate Tcl foreach loop"""
        lines = []
        
        var_list = " ".join(foreach.variables)
        list_expr = self.generate(foreach.list_expr)
        
        lines.append(f"foreach {{{var_list}}} {list_expr} {{")
        
        self.context.increase_indent()
        for command in foreach.body.commands:
            cmd_code = self.generate(command)
            if cmd_code:
                lines.append(self.context.get_indent() + cmd_code)
        self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_switch(self, switch: TclSwitch) -> str:
        """Generate Tcl switch statement"""
        lines = []
        
        expression = self.generate(switch.expression)
        lines.append(f"switch {expression} {{")
        
        self.context.increase_indent()
        
        for pattern in switch.patterns:
            pattern_code = self.generate(pattern.pattern)
            lines.append(f"{self.context.get_indent()}{pattern_code} {{")
            
            self.context.increase_indent()
            for command in pattern.body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
            self.context.decrease_indent()
            
            lines.append(f"{self.context.get_indent()}}}")
        
        if switch.default_body:
            lines.append(f"{self.context.get_indent()}default {{")
            
            self.context.increase_indent()
            for command in switch.default_body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
            self.context.decrease_indent()
            
            lines.append(f"{self.context.get_indent()}}}")
        
        self.context.decrease_indent()
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_try(self, try_stmt: TclTry) -> str:
        """Generate Tcl try statement"""
        lines = []
        lines.append("try {")
        
        self.context.increase_indent()
        for command in try_stmt.try_body.commands:
            cmd_code = self.generate(command)
            if cmd_code:
                lines.append(self.context.get_indent() + cmd_code)
        self.context.decrease_indent()
        
        # Generate catch clauses
        for catch in try_stmt.catch_clauses:
            catch_line = "} catch"
            
            if catch.error_types:
                error_list = " ".join(catch.error_types)
                catch_line += f" {{{error_list}}}"
            
            if catch.variable_name:
                catch_line += f" {catch.variable_name}"
            
            catch_line += " {"
            lines.append(catch_line)
            
            self.context.increase_indent()
            for command in catch.body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
            self.context.decrease_indent()
        
        # Generate finally block
        if try_stmt.finally_body:
            lines.append("} finally {")
            
            self.context.increase_indent()
            for command in try_stmt.finally_body.commands:
                cmd_code = self.generate(command)
                if cmd_code:
                    lines.append(self.context.get_indent() + cmd_code)
            self.context.decrease_indent()
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def _generate_set(self, set_cmd: TclSet) -> str:
        """Generate Tcl set command"""
        if isinstance(set_cmd.variable, TclVariable):
            var_name = set_cmd.variable.name
        elif isinstance(set_cmd.variable, TclArrayElement):
            var_name = f"{set_cmd.variable.array_name}({self.generate(set_cmd.variable.index)})"
        else:
            var_name = str(set_cmd.variable)
        
        if set_cmd.value:
            value = self.generate(set_cmd.value)
            return f"set {var_name} {value}"
        else:
            return f"set {var_name}"
    
    def _generate_variable(self, var: TclVariable) -> str:
        """Generate Tcl variable reference"""
        if var.namespace:
            return f"{var.namespace}::{var.name}"
        return var.name
    
    def _generate_variable_substitution(self, var_sub: TclVariableSubstitution) -> str:
        """Generate Tcl variable substitution"""
        if var_sub.array_index:
            index = self.generate(var_sub.array_index)
            return f"${{{var_sub.variable_name}({index})}}"
        return f"${var_sub.variable_name}"
    
    def _generate_command_substitution(self, cmd_sub: TclCommandSubstitution) -> str:
        """Generate Tcl command substitution"""
        command = self.generate(cmd_sub.command)
        return f"[{command}]"
    
    def _generate_string_literal(self, string_lit: TclStringLiteral) -> str:
        """Generate Tcl string literal"""
        return f'"{self._escape_string(string_lit.value)}"'
    
    def _generate_quoted_string(self, quoted: TclQuotedString) -> str:
        """Generate Tcl quoted string with substitutions"""
        content = ""
        for item in quoted.content:
            if isinstance(item, str):
                content += self._escape_string(item)
            else:
                content += self.generate(item)
        return f'"{content}"'
    
    def _generate_braced_string(self, braced: TclBracedString) -> str:
        """Generate Tcl braced string"""
        return f"{{{braced.content}}}"
    
    def _generate_list(self, tcl_list: TclList) -> str:
        """Generate Tcl list"""
        elements = []
        for element in tcl_list.elements:
            elem_code = self.generate(element)
            elements.append(elem_code)
        return f"{{{' '.join(elements)}}}"
    
    def _generate_comment(self, comment: TclComment) -> str:
        """Generate Tcl comment"""
        lines = comment.text.split('\n')
        comment_lines = [f"# {line}" for line in lines]
        return '\n'.join(comment_lines)
    
    def _generate_return(self, ret: TclReturn) -> str:
        """Generate Tcl return statement"""
        if ret.value:
            value = self.generate(ret.value)
            if ret.code:
                code = self.generate(ret.code)
                return f"return -code {code} {value}"
            return f"return {value}"
        return "return"
    
    def _generate_expr(self, expr: TclExpr) -> str:
        """Generate Tcl expr command"""
        expression = self.generate(expr.expression)
        return f"expr {{{expression}}}"
    
    def _generate_incr(self, incr: TclIncr) -> str:
        """Generate Tcl incr command"""
        var_name = self.generate(incr.variable)
        if incr.increment:
            increment = self.generate(incr.increment)
            return f"incr {var_name} {increment}"
        return f"incr {var_name}"
    
    def _generate_unset(self, unset: TclUnset) -> str:
        """Generate Tcl unset command"""
        vars_str = " ".join(unset.variables)
        if unset.nocomplain:
            return f"unset -nocomplain {vars_str}"
        return f"unset {vars_str}"
    
    # String operations
    
    def _generate_string_match(self, match: TclStringMatch) -> str:
        """Generate string match command"""
        pattern = self.generate(match.pattern)
        string = self.generate(match.string)
        if match.nocase:
            return f"string match -nocase {pattern} {string}"
        return f"string match {pattern} {string}"
    
    def _generate_string_map(self, map_cmd: TclStringMap) -> str:
        """Generate string map command"""
        mapping = self.generate(map_cmd.mapping)
        string = self.generate(map_cmd.string)
        if map_cmd.nocase:
            return f"string map -nocase {mapping} {string}"
        return f"string map {mapping} {string}"
    
    def _generate_string_range(self, range_cmd: TclStringRange) -> str:
        """Generate string range command"""
        string = self.generate(range_cmd.string)
        first = self.generate(range_cmd.first)
        last = self.generate(range_cmd.last)
        return f"string range {string} {first} {last}"
    
    def _generate_string_index(self, index_cmd: TclStringIndex) -> str:
        """Generate string index command"""
        string = self.generate(index_cmd.string)
        index = self.generate(index_cmd.index)
        return f"string index {string} {index}"
    
    # List operations
    
    def _generate_lappend(self, lappend: TclLappend) -> str:
        """Generate lappend command"""
        values = " ".join([self.generate(val) for val in lappend.values])
        return f"lappend {lappend.list_var} {values}"
    
    def _generate_lindex(self, lindex: TclLindex) -> str:
        """Generate lindex command"""
        list_expr = self.generate(lindex.list_expr)
        index = self.generate(lindex.index)
        return f"lindex {list_expr} {index}"
    
    def _generate_llength(self, llength: TclLlength) -> str:
        """Generate llength command"""
        list_expr = self.generate(llength.list_expr)
        return f"llength {list_expr}"
    
    def _generate_lrange(self, lrange: TclLrange) -> str:
        """Generate lrange command"""
        list_expr = self.generate(lrange.list_expr)
        first = self.generate(lrange.first)
        last = self.generate(lrange.last)
        return f"lrange {list_expr} {first} {last}"
    
    def _generate_lsort(self, lsort: TclLsort) -> str:
        """Generate lsort command"""
        list_expr = self.generate(lsort.list_expr)
        options = " ".join(lsort.options)
        if options:
            return f"lsort {options} {list_expr}"
        return f"lsort {list_expr}"
    
    # Regular expressions
    
    def _generate_regexp(self, regexp: TclRegexp) -> str:
        """Generate regexp command"""
        pattern = self.generate(regexp.pattern)
        string = self.generate(regexp.string)
        
        parts = ["regexp"]
        parts.extend(regexp.options)
        parts.append(pattern)
        parts.append(string)
        parts.extend(regexp.match_vars)
        
        return " ".join(parts)
    
    def _generate_regsub(self, regsub: TclRegsub) -> str:
        """Generate regsub command"""
        pattern = self.generate(regsub.pattern)
        string = self.generate(regsub.string)
        replacement = self.generate(regsub.replacement)
        
        parts = ["regsub"]
        parts.extend(regsub.options)
        parts.append(pattern)
        parts.append(string)
        parts.append(replacement)
        
        if regsub.var_name:
            parts.append(regsub.var_name)
        
        return " ".join(parts)
    
    # File I/O operations
    
    def _generate_open(self, open_cmd: TclOpen) -> str:
        """Generate open command"""
        filename = self.generate(open_cmd.filename)
        parts = ["open", filename]
        
        if open_cmd.access:
            access = self.generate(open_cmd.access)
            parts.append(access)
        
        if open_cmd.permissions:
            permissions = self.generate(open_cmd.permissions)
            parts.append(permissions)
        
        return " ".join(parts)
    
    def _generate_close(self, close_cmd: TclClose) -> str:
        """Generate close command"""
        channel = self.generate(close_cmd.channel)
        return f"close {channel}"
    
    def _generate_puts(self, puts: TclPuts) -> str:
        """Generate puts command"""
        parts = ["puts"]
        
        if puts.nonewline:
            parts.append("-nonewline")
        
        if puts.channel:
            channel = self.generate(puts.channel)
            parts.append(channel)
        
        string = self.generate(puts.string)
        parts.append(string)
        
        return " ".join(parts)
    
    def _generate_gets(self, gets: TclGets) -> str:
        """Generate gets command"""
        channel = self.generate(gets.channel)
        parts = ["gets", channel]
        
        if gets.var_name:
            parts.append(gets.var_name)
        
        return " ".join(parts)
    
    def _generate_read(self, read: TclRead) -> str:
        """Generate read command"""
        channel = self.generate(read.channel)
        parts = ["read"]
        
        if read.nonewline:
            parts.append("-nonewline")
        
        parts.append(channel)
        
        if read.num_chars:
            num_chars = self.generate(read.num_chars)
            parts.append(num_chars)
        
        return " ".join(parts)
    
    # System interaction
    
    def _generate_exec(self, exec_cmd: TclExec) -> str:
        """Generate exec command"""
        program = self.generate(exec_cmd.program)
        parts = ["exec"]
        parts.extend(exec_cmd.options)
        parts.append(program)
        
        for arg in exec_cmd.arguments:
            arg_code = self.generate(arg)
            parts.append(arg_code)
        
        return " ".join(parts)
    
    def _generate_source(self, source: TclSource) -> str:
        """Generate source command"""
        filename = self.generate(source.filename)
        return f"source {filename}"
    
    def _generate_eval(self, eval_cmd: TclEval) -> str:
        """Generate eval command"""
        script = self.generate(eval_cmd.script)
        return f"eval {script}"
    
    def _generate_error(self, error: TclError) -> str:
        """Generate error command"""
        message = self.generate(error.message)
        parts = ["error", message]
        
        if error.info:
            info = self.generate(error.info)
            parts.append(info)
        
        if error.code:
            code = self.generate(error.code)
            parts.append(code)
        
        return " ".join(parts)
    
    def _generate_info(self, info: TclInfo) -> str:
        """Generate info command"""
        parts = ["info", info.subcommand]
        
        for arg in info.arguments:
            arg_code = self.generate(arg)
            parts.append(arg_code)
        
        return " ".join(parts)
    
    # Helper methods
    
    def _escape_string(self, text: str) -> str:
        """Escape special characters in string"""
        result = ""
        for char in text:
            if char in self.escape_chars:
                result += self.escape_chars[char]
            else:
                result += char
        return result
    
    def _needs_quoting(self, text: str) -> bool:
        """Check if text needs to be quoted"""
        # Check for special characters that require quoting
        special_chars = {' ', '\t', '\n', '"', '$', '[', ']', '{', '}', '\\', ';'}
        return any(char in special_chars for char in text) or text in self.tcl_keywords
    
    def get_generation_info(self) -> Dict[str, Any]:
        """Get information about Tcl code generation capabilities"""
        return {
            "target_language": "tcl",
            "features_supported": [
                "automation_scripting", "text_processing", "string_manipulation",
                "procedures", "namespaces", "control_structures", "list_processing",
                "regular_expressions", "file_io", "system_interaction", "error_handling"
            ],
            "code_style": {
                "indentation": "spaces",
                "indent_size": 4,
                "brace_style": "tcl_standard",
                "string_quoting": "intelligent"
            }
        } 