"""
Python Code Generator for Runa IR

This module transforms Runa intermediate representation (IR) into executable
Python code. It handles natural language constructs and generates clean,
readable Python that preserves Runa's semantic meaning.
"""

from typing import Dict, List, Set, TextIO
from io import StringIO
import textwrap
import io
from typing import Union

from ..ir import *

class PythonCodeGenerator:
    """Generates Python code from IR."""
    
    def __init__(self):
        self.output = io.StringIO()
        self.indent_level = 0
        self._current_function = None
    
    def generate(self, module: IRModule) -> str:
        """Generate Python code from IR module."""
        self.output = io.StringIO()
        self.indent_level = 0
        
        # Generate imports and header
        self._emit_line("# Generated Python code from Runa")
        self._emit_line("# Natural language programming made executable")
        self._emit_line()
        self._emit_line("import sys")
        self._emit_line("import math")
        self._emit_line()
        
        # Generate helper functions
        self._generate_helpers()
        
        # Generate functions
        for func in module.functions:
            self._generate_function(func)
        
        # Generate main execution
        self._emit_line("if __name__ == '__main__':")
        self.indent_level += 1
        self._emit_line("main()")
        self.indent_level -= 1
        
        return self.output.getvalue()
    
    def _generate_function(self, func: IRFunction):
        """Generate Python code for a function with structured control flow."""
        self._current_function = func
        param_names = [self._python_var_name(p) for p in func.parameters]
        param_str = ", ".join(param_names)
        self._emit_line(f"def {func.name}({param_str}):")
        self.indent_level += 1
        
        # Declare local variables upfront
        self._declare_local_variables(func)
        
        # Generate structured control flow from basic blocks
        self._generate_structured_control_flow(func)
        
        self.indent_level -= 1
        self._emit_line()
        self._current_function = None
    
    def _declare_local_variables(self, func: IRFunction):
        """Declare all local variables at the beginning of the function."""
        variables = set()
        param_name_set = {self._python_var_name(p) for p in func.parameters}
        
        # Collect all variables used in the function
        for block in func.basic_blocks:
            for instr in block.instructions:
                if instr.result:
                    if isinstance(instr.result, (IRVariable, IRTemporary)):
                        var_name = self._python_var_name(instr.result)
                        if var_name not in param_name_set:
                            variables.add(var_name)
                
                for operand in instr.operands:
                    if isinstance(operand, (IRVariable, IRTemporary)):
                        var_name = self._python_var_name(operand)
                        if var_name not in param_name_set:
                            variables.add(var_name)
        
        if variables:
            self._emit_line("# Local variables")
            for var in sorted(variables):
                self._emit_line(f"{var} = None")
            self._emit_line()
    
    def _generate_structured_control_flow(self, func: IRFunction):
        """Generate structured control flow instead of goto-based."""
        # Find the entry block
        entry_block = None
        for block in func.basic_blocks:
            if block.label == func.entry_block:
                entry_block = block
                break
        
        if not entry_block:
            self._emit_line("pass  # No entry block found")
            return
        
        # Process blocks in control flow order, handling loops
        self._process_block_with_loops(entry_block, func, set())
    
    def _process_block_with_loops(self, block: IRBasicBlock, func: IRFunction, visited: set):
        """Process a basic block and detect/generate loop structures."""
        if block.label in visited:
            return
        visited.add(block.label)
        
        # Check if this block starts a while loop pattern
        if self._is_loop_header(block, func):
            self._generate_while_loop(block, func, visited)
            return
        
        # Process instructions in this block
        branch_instr = None
        jump_target = None
        has_return = False
        
        for instr in block.instructions:
            if isinstance(instr, IRBranchInstruction):
                branch_instr = instr
                # Don't generate the branch instruction yet
            elif instr.instruction_type == IRInstructionType.JUMP:
                # Track jump target for later processing
                jump_target = instr.metadata.get("target")
            elif instr.instruction_type == IRInstructionType.RETURN:
                self._generate_return(instr)
                has_return = True
                return  # End of this control flow path
            else:
                self._generate_instruction(instr)
        
        # Handle control flow at the end of the block
        if branch_instr:
            self._generate_structured_branch(branch_instr, func, visited)
        elif jump_target and not has_return:
            # Follow unconditional jump
            target_block = self._find_block_by_label(func, jump_target)
            if target_block:
                self._process_block_with_loops(target_block, func, visited)
    
    def _is_loop_header(self, block: IRBasicBlock, func: IRFunction) -> bool:
        """Check if a block is a loop header (has a condition and back-edge)."""
        # Look for a pattern: condition check followed by branch
        if len(block.instructions) >= 2:
            last_instr = block.instructions[-1]
            if isinstance(last_instr, IRBranchInstruction):
                # Check if one of the targets eventually jumps back to this block
                true_block = self._find_block_by_label(func, last_instr.true_label)
                if true_block and self._has_back_edge_to(true_block, block.label, func, set()):
                    return True
        return False
    
    def _has_back_edge_to(self, block: IRBasicBlock, target_label: str, func: IRFunction, visited: set) -> bool:
        """Check if a block eventually jumps back to the target label."""
        if block.label in visited:
            return False
        visited.add(block.label)
        
        # Check if this block jumps directly to target
        for instr in block.instructions:
            if instr.instruction_type == IRInstructionType.JUMP:
                jump_target = instr.metadata.get("target")
                if jump_target == target_label:
                    return True
                # Recursively check jump target
                jump_block = self._find_block_by_label(func, jump_target)
                if jump_block and self._has_back_edge_to(jump_block, target_label, func, visited.copy()):
                    return True
        
        return False
    
    def _generate_while_loop(self, header_block: IRBasicBlock, func: IRFunction, visited: set):
        """Generate a Python while loop from IR loop structure."""
        # Extract condition from header block
        condition_instr = None
        branch_instr = None
        
        for instr in header_block.instructions:
            if isinstance(instr, IRBranchInstruction):
                branch_instr = instr
                break
            else:
                self._generate_instruction(instr)
        
        if not branch_instr:
            return
        
        # Determine condition expression. Attempt to inline the comparison instead of using a temp var
        cond_expr = None
        # Look at instruction immediately before branch (if any)
        if len(header_block.instructions) >= 2:
            prev_instr = header_block.instructions[-2]
            if prev_instr.result == branch_instr.condition and prev_instr.instruction_type in [
                IRInstructionType.LESS_THAN, IRInstructionType.GREATER_THAN,
                IRInstructionType.LESS_EQUAL, IRInstructionType.GREATER_EQUAL,
                IRInstructionType.EQUALS, IRInstructionType.NOT_EQUALS,
                IRInstructionType.ADD, IRInstructionType.SUBTRACT,
                IRInstructionType.MULTIPLY, IRInstructionType.DIVIDE,
                IRInstructionType.MODULO, IRInstructionType.POWER,
            ] and len(prev_instr.operands) == 2:
                left_code = self._operand_to_python(prev_instr.operands[0])
                right_code = self._operand_to_python(prev_instr.operands[1])
                op_map = {
                    IRInstructionType.ADD: "+",
                    IRInstructionType.SUBTRACT: "-",
                    IRInstructionType.MULTIPLY: "*",
                    IRInstructionType.DIVIDE: "/",
                    IRInstructionType.MODULO: "%",
                    IRInstructionType.POWER: "**",
                    IRInstructionType.EQUALS: "==",
                    IRInstructionType.NOT_EQUALS: "!=",
                    IRInstructionType.GREATER_THAN: ">",
                    IRInstructionType.LESS_THAN: "<",
                    IRInstructionType.GREATER_EQUAL: ">=",
                    IRInstructionType.LESS_EQUAL: "<=",
                }
                op_symbol = op_map.get(prev_instr.instruction_type, None)
                if op_symbol:
                    cond_expr = f"{left_code} {op_symbol} {right_code}"
        
        if cond_expr is None:
            # Fallback: use operand directly
            cond_expr = self._operand_to_python(branch_instr.condition)
        
        # Emit while loop header
        self._emit_line(f"while {cond_expr}:")
        self.indent_level += 1
        
        # Generate loop body
        body_block = self._find_block_by_label(func, branch_instr.true_label)
        if body_block:
            visited.add(header_block.label)
            self._generate_loop_body(body_block, header_block.label, func, visited)
        
        self.indent_level -= 1
        
        # Continue with exit block
        exit_block = self._find_block_by_label(func, branch_instr.false_label)
        if exit_block:
            self._process_block_with_loops(exit_block, func, visited)
    
    def _generate_loop_body(self, block: IRBasicBlock, loop_header: str, func: IRFunction, visited: set):
        """Generate the body of a loop, stopping when we hit a back-edge."""
        if block.label in visited:
            return
        visited.add(block.label)
        
        # Process instructions, but skip jumps back to loop header
        jump_target = None
        for instr in block.instructions:
            if instr.instruction_type == IRInstructionType.JUMP:
                jump_target = instr.metadata.get("target")
                if jump_target == loop_header:
                    # This is the back-edge - don't follow it
                    return
            else:
                self._generate_instruction(instr)
        
        # Follow non-back-edge jumps
        if jump_target and jump_target != loop_header:
            target_block = self._find_block_by_label(func, jump_target)
            if target_block:
                self._generate_loop_body(target_block, loop_header, func, visited)
    
    def _generate_structured_branch(self, branch_instr: IRBranchInstruction, func: IRFunction, visited: set):
        """Generate structured if/else from branch instruction."""
        condition_code = self._operand_to_python(branch_instr.condition)
        
        # Find true and false blocks
        true_block = self._find_block_by_label(func, branch_instr.true_label)
        false_block = self._find_block_by_label(func, branch_instr.false_label)
        
        self._emit_line(f"if {condition_code}:")
        self.indent_level += 1
        
        if true_block and self._block_has_real_instructions(true_block):
            # Generate true block content without processing the block recursively
            self._generate_block_content(true_block)
        else:
            self._emit_line("pass")
        
        self.indent_level -= 1
        
        if false_block:
            self._emit_line("else:")
            self.indent_level += 1
            # Generate false block content without processing the block recursively
            if self._block_has_real_instructions(false_block):
                self._generate_block_content(false_block)
            else:
                self._emit_line("pass")
            self.indent_level -= 1
    
    def _generate_block_content(self, block: IRBasicBlock):
        """Generate the content of a basic block, including nested control flow."""
        branch_instr = None
        for instr in block.instructions:
            if isinstance(instr, IRBranchInstruction):
                # Handle branch instructions for nested control flow
                branch_instr = instr
            elif instr.instruction_type == IRInstructionType.JUMP:
                # Skip jump instructions
                pass
            elif instr.instruction_type == IRInstructionType.RETURN:
                # Skip return instructions in block content - will be handled at function level
                pass
            else:
                self._generate_instruction(instr)
        
        # Generate nested control flow if there's a branch in this block
        if branch_instr:
            # Find the containing function for nested branch resolution
            func = self._current_function  # We need to track this
            if func:
                self._generate_nested_branch(branch_instr, func)
     
    def _generate_nested_branch(self, branch_instr: IRBranchInstruction, func: IRFunction):
        """Generate nested if/else from branch instruction within a block."""
        condition_code = self._operand_to_python(branch_instr.condition)
        
        # Find true and false blocks
        true_block = self._find_block_by_label(func, branch_instr.true_label)
        false_block = self._find_block_by_label(func, branch_instr.false_label)
        
        self._emit_line(f"if {condition_code}:")
        self.indent_level += 1
        
        if true_block:
            # Generate true block content recursively
            self._generate_block_content(true_block)
        else:
            self._emit_line("pass")
        
        self.indent_level -= 1
        
        if false_block:
            self._emit_line("else:")
            self.indent_level += 1
            # Generate false block content recursively
            self._generate_block_content(false_block)
            self.indent_level -= 1
    
    def _find_block_by_label(self, func: IRFunction, label: str) -> IRBasicBlock:
        """Find a basic block by its label."""
        for block in func.basic_blocks:
            if block.label == label:
                return block
        return None
    
    def _generate_instruction(self, instr: IRInstruction):
        """Generate Python code for an IR instruction."""
        if isinstance(instr, IRDisplayInstruction):
            self._generate_display(instr)
        elif isinstance(instr, IRCallInstruction):
            self._generate_call(instr)
        elif isinstance(instr, IRBranchInstruction):
            # Handled in structured control flow
            pass
        elif isinstance(instr, IRLabelInstruction):
            # Labels are handled at the block level
            pass
        elif instr.instruction_type == IRInstructionType.ASSIGN:
            self._generate_assignment(instr)
        elif instr.instruction_type == IRInstructionType.RETURN:
            self._generate_return(instr)
        elif instr.instruction_type == IRInstructionType.JUMP:
            # Handled in structured control flow
            pass
        elif instr.instruction_type == IRInstructionType.LIST_CREATE:
            self._generate_list_create(instr)
        elif instr.instruction_type in [
            IRInstructionType.ADD, IRInstructionType.SUBTRACT,
            IRInstructionType.MULTIPLY, IRInstructionType.DIVIDE,
            IRInstructionType.MODULO, IRInstructionType.POWER,
            IRInstructionType.EQUALS, IRInstructionType.NOT_EQUALS,
            IRInstructionType.GREATER_THAN, IRInstructionType.LESS_THAN,
            IRInstructionType.GREATER_EQUAL, IRInstructionType.LESS_EQUAL,
            IRInstructionType.AND, IRInstructionType.OR
        ]:
            self._generate_binary_op(instr)
        elif instr.instruction_type == IRInstructionType.INDEX_ACCESS:
            self._generate_index_access(instr)
        else:
            # For unsupported instructions, emit a comment
            self._emit_line(f"# TODO: {instr}")
    
    def _generate_display(self, instr: IRDisplayInstruction):
        """Generate Python code for a display instruction."""
        value_code = self._operand_to_python(instr.value)
        
        if instr.prefix:
            prefix_code = self._operand_to_python(instr.prefix)
            self._emit_line(f"print({prefix_code}, {value_code})")
        else:
            self._emit_line(f"print({value_code})")
    
    def _generate_call(self, instr: IRCallInstruction):
        """Generate Python code for a function call."""
        # Map Runa function names to Python equivalents
        func_map = {
            "Calculate Interest": "calculate_interest",
            "Calculate Total": "calculate_total", 
            "Calculate Discount": "calculate_discount",
            "Format Currency": "format_currency"
        }
        
        python_func_name = func_map.get(instr.function_name, 
                                       instr.function_name.lower().replace(" ", "_"))
        
        # Generate argument list
        if instr.arguments:
            args = []
            for param_name, value in instr.arguments:
                value_code = self._operand_to_python(value)
                if python_func_name == 'len':
                    # len takes a single positional argument
                    args.append(f"{value_code}")
                else:
                    args.append(f"{param_name.lower().replace(' ', '_')}={value_code}")
            args_str = ", ".join(args)
            call_code = f"{python_func_name}({args_str})"
        else:
            call_code = f"{python_func_name}()"
        
        if instr.result:
            result_var = self._python_var_name(instr.result)
            self._emit_line(f"{result_var} = {call_code}")
        else:
            self._emit_line(call_code)
    
    def _generate_assignment(self, instr: IRInstruction):
        """Generate Python code for an assignment."""
        if instr.result and instr.operands:
            target_var = self._python_var_name(instr.result)
            source_code = self._operand_to_python(instr.operands[0])
            self._emit_line(f"{target_var} = {source_code}")
    
    def _generate_return(self, instr: IRInstruction):
        """Generate Python code for a return statement."""
        if instr.operands:
            value_code = self._operand_to_python(instr.operands[0])
            self._emit_line(f"return {value_code}")
        else:
            self._emit_line("return")
    
    def _generate_list_create(self, instr: IRInstruction):
        """Generate Python code for list creation."""
        if instr.result:
            elements = [self._operand_to_python(op) for op in instr.operands]
            elements_str = ", ".join(elements)
            result_var = self._python_var_name(instr.result)
            self._emit_line(f"{result_var} = [{elements_str}]")
    
    def _generate_binary_op(self, instr: IRInstruction):
        """Generate Python code for binary operations."""
        if instr.result and len(instr.operands) >= 2:
            left_code = self._operand_to_python(instr.operands[0])
            right_code = self._operand_to_python(instr.operands[1])
            result_var = self._python_var_name(instr.result)
            
            # Map IR operations to Python operators
            op_map = {
                IRInstructionType.ADD: "+",
                IRInstructionType.SUBTRACT: "-", 
                IRInstructionType.MULTIPLY: "*",
                IRInstructionType.DIVIDE: "/",
                IRInstructionType.MODULO: "%",
                IRInstructionType.POWER: "**",
                IRInstructionType.EQUALS: "==",
                IRInstructionType.NOT_EQUALS: "!=",
                IRInstructionType.GREATER_THAN: ">",
                IRInstructionType.LESS_THAN: "<",
                IRInstructionType.GREATER_EQUAL: ">=",
                IRInstructionType.LESS_EQUAL: "<=",
                IRInstructionType.AND: "and",
                IRInstructionType.OR: "or"
            }
            
            python_op = op_map.get(instr.instruction_type, "???")
            self._emit_line(f"{result_var} = {left_code} {python_op} {right_code}")
    
    def _generate_index_access(self, instr: IRInstruction):
        """Generate Python code for index access instruction (result = obj[index])."""
        if instr.result and len(instr.operands) == 2:
            obj_code = self._operand_to_python(instr.operands[0])
            idx_code = self._operand_to_python(instr.operands[1])
            result_var = self._python_var_name(instr.result)
            self._emit_line(f"{result_var} = {obj_code}[{idx_code}]")
    
    def _generate_helpers(self):
        """Generate helper functions for Runa built-ins."""
        self._emit_line("# Helper functions for Runa built-ins")
        self._emit_line()
        
        # Example helper functions that might be called from Runa
        helpers = [
            '''def calculate_interest(principal, rate, years=1):
    """Calculate simple interest."""
    return principal * rate * years''',
            
            '''def calculate_total(*args, **kwargs):
    """Calculate total from various arguments."""
    total = 0
    for value in args:
        if isinstance(value, (int, float)):
            total += value
    for value in kwargs.values():
        if isinstance(value, (int, float)):
            total += value
    return total''',
            
            '''def calculate_discount(original_price, discount_rate):
    """Calculate discounted price."""
    discount_amount = original_price * discount_rate
    return original_price - discount_amount''',
            
            '''def format_currency(amount, symbol="$"):
    """Format amount as currency."""
    return f"{symbol}{amount:.2f}"'''
        ]
        
        for helper in helpers:
            for line in helper.split('\n'):
                self._emit_line(line)
            self._emit_line()
    
    def _operand_to_python(self, operand: IROperand) -> str:
        """Convert an IR operand to Python code."""
        if isinstance(operand, IRConstant):
            if operand.ir_type == IRTypes.STRING:
                # Escape quotes in string literals
                escaped = operand.value.replace('"', '\\"')
                return f'"{escaped}"'
            elif operand.ir_type == IRTypes.BOOLEAN:
                return "True" if operand.value else "False"
            else:
                return str(operand.value)
        elif isinstance(operand, (IRVariable, IRTemporary)):
            return self._python_var_name(operand)
        else:
            return str(operand)
    
    def _python_var_name(self, var: Union[IRVariable, IRTemporary]) -> str:
        """Convert IR variable to Python variable name."""
        if isinstance(var, (IRVariable, IRTemporary)):
            # Convert natural language variable names to Python identifiers
            name = var.name.lower()
            name = name.replace(" ", "_")
            name = name.replace("-", "_")
            # Remove non-alphanumeric characters except underscores
            name = "".join(c for c in name if c.isalnum() or c == "_")
            # Ensure it starts with a letter or underscore
            if name and name[0].isdigit():
                name = f"var_{name}"
            return name or "var"
        return str(var)
    
    def _emit_line(self, line: str = ""):
        """Emit a line of Python code with proper indentation."""
        if line.strip():
            indent = "    " * self.indent_level
            self.output.write(f"{indent}{line}\n")
        else:
            self.output.write("\n")

    def _block_has_real_instructions(self, block: IRBasicBlock) -> bool:
        """Check if a block has instructions other than labels, jumps, or returns."""
        if not block:
            return False
        for instr in block.instructions:
            if isinstance(instr, (IRBranchInstruction, IRLabelInstruction)):
                continue
            if instr.instruction_type in [IRInstructionType.JUMP, IRInstructionType.RETURN]:
                continue
            return True  # Found a meaningful instruction
        return False

def generate_python(ir_module: IRModule) -> str:
    """Generate Python code from IR module."""
    generator = PythonCodeGenerator()
    return generator.generate(ir_module) 