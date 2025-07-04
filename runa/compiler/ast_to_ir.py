"""
AST to IR Visitor - Runa Compiler

This module implements the visitor that transforms Runa AST nodes into
intermediate representation (IR) instructions. This is the core bridge
between the high-level natural language AST and the lower-level IR
suitable for code generation.
"""

from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from .ast_nodes import *
from .ir import *

@dataclass
class IRGenerationContext:
    """Context for IR generation including variable mappings and block management."""
    current_function: Optional[IRFunction] = None
    current_block: Optional[IRBasicBlock] = None
    variable_map: Dict[str, IRVariable] = None
    loop_break_labels: List[str] = None
    loop_continue_labels: List[str] = None
    label_counter: int = 0
    
    def __post_init__(self):
        if self.variable_map is None:
            self.variable_map = {}
        if self.loop_break_labels is None:
            self.loop_break_labels = []
        if self.loop_continue_labels is None:
            self.loop_continue_labels = []
    
    def generate_label(self, prefix: str = "label") -> str:
        """Generate a unique label."""
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"
    
    def get_variable(self, name: str) -> IRVariable:
        """Get or create a variable mapping."""
        if name not in self.variable_map:
            # Create new variable with inferred type (will be refined by semantic analysis)
            self.variable_map[name] = IRVariable(name, IRTypes.ANY)
        return self.variable_map[name]
    
    def set_variable(self, name: str, var: IRVariable):
        """Set variable mapping."""
        self.variable_map[name] = var

class ASTToIRVisitor:
    """Visitor that converts Runa AST nodes to IR instructions."""
    
    def __init__(self):
        self.context = IRGenerationContext()
        self.module = IRModule("main")
    
    def visit(self, node: ASTNode) -> Any:
        """Dispatch to the appropriate visit method."""
        method_name = f"visit_{type(node).__name__.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            raise NotImplementedError(f"No visitor method for {type(node).__name__}")
    
    # === PROGRAM AND STATEMENTS ===
    
    def visit_program(self, node: Program) -> IRModule:
        """Convert a Runa program to IR module."""
        # Create main function for top-level statements
        main_func = IRFunction("main", [], IRTypes.VOID, "entry")
        entry_block = IRBasicBlock("entry")
        main_func.add_block(entry_block)
        
        self.context.current_function = main_func
        self.context.current_block = entry_block
        
        # Process all statements
        for stmt in node.statements:
            self.visit(stmt)
        
        # Add return at end of main if current block doesn't end with return
        current_block = self.context.current_block
        if current_block and (not current_block.instructions or \
           not isinstance(current_block.instructions[-1], IRInstruction) or \
           current_block.instructions[-1].instruction_type != IRInstructionType.RETURN):
            current_block.add_instruction(create_return_instruction())
        
        self.module.add_function(main_func)
        return self.module
    
    def visit_letstatement(self, node: LetStatement) -> None:
        """Convert Let statement to IR."""
        # Evaluate the value expression
        value_operand = self.visit(node.value)
        
        # Create variable
        var_type = self._infer_type_from_operand(value_operand)
        variable = IRVariable(node.identifier, var_type)
        
        # Add to context and function
        self.context.set_variable(node.identifier, variable)
        if self.context.current_function:
            self.context.current_function.add_variable(node.identifier, variable)
        
        # Generate assignment instruction
        assign_instr = create_assignment_instruction(variable, value_operand)
        self.context.current_block.add_instruction(assign_instr)
    
    def visit_definestatement(self, node: DefineStatement) -> None:
        """Convert Define statement to IR (same as Let for now)."""
        self.visit_letstatement(LetStatement(node.identifier, node.type_annotation, node.value))
    
    def visit_setstatement(self, node: SetStatement) -> None:
        """Convert Set statement to IR."""
        # Evaluate the value expression
        value_operand = self.visit(node.value)
        
        # Handle target (identifier, member access, or index access)
        if isinstance(node.target, Identifier):
            target_var = self.context.get_variable(node.target.name)
            assign_instr = create_assignment_instruction(target_var, value_operand)
            self.context.current_block.add_instruction(assign_instr)
        else:
            # For now, treat complex targets as assignments to temporaries
            target_operand = self.visit(node.target)
            assign_instr = create_assignment_instruction(target_operand, value_operand)
            self.context.current_block.add_instruction(assign_instr)
    
    def visit_ifstatement(self, node: IfStatement) -> None:
        """Convert If statement to IR with conditional branches."""
        # Labels for control flow
        then_label = self.context.generate_label("if_then")
        else_label = self.context.generate_label("if_else") 
        end_label = self.context.generate_label("if_end")
        
        # Evaluate condition
        condition_operand = self.visit(node.condition)
        
        # Create branch instruction
        branch_instr = IRBranchInstruction(condition_operand, then_label, 
                                         else_label if node.else_block else end_label)
        self.context.current_block.add_instruction(branch_instr)
        
        # Then block
        then_block = IRBasicBlock(then_label)
        self.context.current_function.add_block(then_block)
        self.context.current_block = then_block
        
        for stmt in node.then_block:
            self.visit(stmt)
        
        # Don't add jump if block ends with return, otherwise continue to end
        if not self._block_ends_with_return(then_block):
            # Don't add explicit jump instruction - let control flow continue naturally
            pass
        
        # Else block (if exists)
        if node.else_block:
            else_block = IRBasicBlock(else_label)
            self.context.current_function.add_block(else_block)
            self.context.current_block = else_block
            
            for stmt in node.else_block:
                self.visit(stmt)
            
            # Don't add jump if block ends with return
            if not self._block_ends_with_return(else_block):
                # Don't add explicit jump instruction - let control flow continue naturally
                pass
        
        # End block - this becomes the new current block for continuation
        end_block = IRBasicBlock(end_label)
        self.context.current_function.add_block(end_block)
        self.context.current_block = end_block
    
    def visit_displaystatement(self, node: DisplayStatement) -> None:
        """Convert Display statement to IR."""
        value_operand = self.visit(node.value)
        prefix_operand = self.visit(node.prefix) if node.prefix else None
        
        display_instr = IRDisplayInstruction(value_operand, prefix_operand)
        self.context.current_block.add_instruction(display_instr)
    
    def visit_returnstatement(self, node: ReturnStatement) -> None:
        """Convert Return statement to IR."""
        value_operand = self.visit(node.value) if node.value else None
        return_instr = create_return_instruction(value_operand)
        self.context.current_block.add_instruction(return_instr)
    
    # === EXPRESSIONS ===
    
    def visit_integerliteral(self, node: IntegerLiteral) -> IRConstant:
        """Convert integer literal to IR constant."""
        return IRConstant(node.value, IRTypes.INTEGER)
    
    def visit_floatliteral(self, node: FloatLiteral) -> IRConstant:
        """Convert float literal to IR constant."""
        return IRConstant(node.value, IRTypes.FLOAT)
    
    def visit_stringliteral(self, node: StringLiteral) -> IRConstant:
        """Convert string literal to IR constant."""
        return IRConstant(node.value, IRTypes.STRING)
    
    def visit_booleanliteral(self, node: BooleanLiteral) -> IRConstant:
        """Convert boolean literal to IR constant."""
        return IRConstant(node.value, IRTypes.BOOLEAN)
    
    def visit_listliteral(self, node: ListLiteral) -> IROperand:
        """Convert list literal to IR."""
        # Evaluate all elements
        element_operands = [self.visit(elem) for elem in node.elements]
        
        # Create list creation instruction
        result = IRTemporary(IRTypes.list_of(IRTypes.ANY))
        create_instr = IRInstruction(IRInstructionType.LIST_CREATE, result, element_operands)
        self.context.current_block.add_instruction(create_instr)
        
        return result
    
    def visit_identifier(self, node: Identifier) -> IRVariable:
        """Convert identifier to IR variable."""
        return self.context.get_variable(node.name)
    
    def visit_binaryexpression(self, node: BinaryExpression) -> IROperand:
        """Convert binary expression to IR."""
        left_operand = self.visit(node.left)
        right_operand = self.visit(node.right)
        
        # Map Runa operators to IR instruction types
        op_map = {
            BinaryOperator.PLUS: IRInstructionType.ADD,
            BinaryOperator.MINUS: IRInstructionType.SUBTRACT,
            BinaryOperator.MULTIPLY: IRInstructionType.MULTIPLY,
            BinaryOperator.DIVIDE: IRInstructionType.DIVIDE,
            BinaryOperator.MODULO: IRInstructionType.MODULO,
            BinaryOperator.POWER: IRInstructionType.POWER,
            BinaryOperator.EQUALS: IRInstructionType.EQUALS,
            BinaryOperator.NOT_EQUALS: IRInstructionType.NOT_EQUALS,
            BinaryOperator.GREATER_THAN: IRInstructionType.GREATER_THAN,
            BinaryOperator.LESS_THAN: IRInstructionType.LESS_THAN,
            BinaryOperator.GREATER_EQUAL: IRInstructionType.GREATER_EQUAL,
            BinaryOperator.LESS_EQUAL: IRInstructionType.LESS_EQUAL,
            BinaryOperator.AND: IRInstructionType.AND,
            BinaryOperator.OR: IRInstructionType.OR,
        }
        
        ir_op = op_map.get(node.operator)
        if ir_op is None:
            raise ValueError(f"Unsupported binary operator: {node.operator}")
        
        # Create a temporary variable for the result
        result_type = self._infer_binary_result_type(node.operator, left_operand, right_operand)
        result = IRTemporary(result_type)
        
        # Create and add the instruction
        instruction = IRInstruction(ir_op, result, [left_operand, right_operand])
        self.context.current_block.add_instruction(instruction)
        
        return result
    
    def visit_functioncall(self, node: FunctionCall) -> IROperand:
        """Convert function call to IR."""
        # Evaluate arguments
        arg_operands = [(name, self.visit(value)) for name, value in node.arguments]
        
        # Create result temporary (assume ANY type for now)
        result = IRTemporary(IRTypes.ANY)
        
        # Create call instruction
        call_instr = IRCallInstruction(result, node.function_name, arg_operands)
        self.context.current_block.add_instruction(call_instr)
        
        return result
    
    # === LOOPS ===
    
    def visit_whileloop(self, node: WhileLoop) -> None:
        """Convert While loop to IR."""
        # Labels
        loop_start = self.context.generate_label("while_start")
        loop_body = self.context.generate_label("while_body")
        loop_end = self.context.generate_label("while_end")
        
        # Jump to loop start
        self.context.current_block.add_instruction(create_jump_instruction(loop_start))
        
        # Loop start block (condition check)
        start_block = IRBasicBlock(loop_start)
        self.context.current_function.add_block(start_block)
        self.context.current_block = start_block
        
        condition_operand = self.visit(node.condition)
        branch_instr = IRBranchInstruction(condition_operand, loop_body, loop_end)
        start_block.add_instruction(branch_instr)
        
        # Loop body
        body_block = IRBasicBlock(loop_body)
        self.context.current_function.add_block(body_block)
        self.context.current_block = body_block
        
        # Set up break/continue labels
        self.context.loop_break_labels.append(loop_end)
        self.context.loop_continue_labels.append(loop_start)
        
        for stmt in node.block:
            self.visit(stmt)
        
        # Jump back to condition
        if not self._block_ends_with_return(body_block):
            body_block.add_instruction(create_jump_instruction(loop_start))
        
        # Clean up break/continue labels
        self.context.loop_break_labels.pop()
        self.context.loop_continue_labels.pop()
        
        # End block
        end_block = IRBasicBlock(loop_end)
        self.context.current_function.add_block(end_block)
        self.context.current_block = end_block
    
    def visit_foreachloop(self, node: ForEachLoop) -> None:
        """Convert ForEach loop to IR using index-based while loop."""
        # Evaluate iterable expression first and store in variable
        iterable_operand = self.visit(node.iterable)
        iterable_var = IRVariable(f"{node.variable}_iterable", IRTypes.ANY)
        self.context.set_variable(iterable_var.name, iterable_var)
        assign_iterable = create_assignment_instruction(iterable_var, iterable_operand)
        self.context.current_block.add_instruction(assign_iterable)

        # Index variable
        index_var = IRVariable(f"{node.variable}_index", IRTypes.INTEGER)
        self.context.set_variable(index_var.name, index_var)
        idx_zero = IRConstant(0, IRTypes.INTEGER)
        assign_idx = create_assignment_instruction(index_var, idx_zero)
        self.context.current_block.add_instruction(assign_idx)

        # Labels
        loop_start = self.context.generate_label("for_start")
        loop_body = self.context.generate_label("for_body")
        loop_end = self.context.generate_label("for_end")

        # Jump to loop start
        self.context.current_block.add_instruction(create_jump_instruction(loop_start))

        # Loop start block: condition check
        start_block = IRBasicBlock(loop_start)
        self.context.current_function.add_block(start_block)
        self.context.current_block = start_block

        # len(iterable)
        len_result = IRTemporary(IRTypes.INTEGER)
        len_call = IRCallInstruction(len_result, "len", [("obj", iterable_var)])
        start_block.add_instruction(len_call)

        # index < len
        cond_tmp = IRTemporary(IRTypes.BOOLEAN)
        cmp_instr = IRInstruction(IRInstructionType.LESS_THAN, cond_tmp, [index_var, len_result])
        start_block.add_instruction(cmp_instr)

        branch_instr = IRBranchInstruction(cond_tmp, loop_body, loop_end)
        start_block.add_instruction(branch_instr)

        # Loop body block
        body_block = IRBasicBlock(loop_body)
        self.context.current_function.add_block(body_block)
        self.context.current_block = body_block

        # element = iterable[index]
        elem_tmp = IRVariable(node.variable, IRTypes.ANY)
        self.context.set_variable(elem_tmp.name, elem_tmp)
        index_access = IRInstruction(IRInstructionType.INDEX_ACCESS, elem_tmp, [iterable_var, index_var])
        body_block.add_instruction(index_access)

        # Process statements in loop body
        for stmt in node.block:
            self.visit(stmt)

        # index = index + 1
        one_const = IRConstant(1, IRTypes.INTEGER)
        inc_tmp = IRTemporary(IRTypes.INTEGER)
        add_instr = IRInstruction(IRInstructionType.ADD, inc_tmp, [index_var, one_const])
        body_block.add_instruction(add_instr)
        assign_inc = create_assignment_instruction(index_var, inc_tmp)
        body_block.add_instruction(assign_inc)

        # Jump back to loop start
        body_block.add_instruction(create_jump_instruction(loop_start))

        # End block
        end_block = IRBasicBlock(loop_end)
        self.context.current_function.add_block(end_block)
        self.context.current_block = end_block
    
    # === UTILITY METHODS ===
    
    def _infer_type_from_operand(self, operand: IROperand) -> IRType:
        """Infer IR type from an operand."""
        return operand.ir_type
    
    def _infer_binary_result_type(self, operator: BinaryOperator, 
                                left: IROperand, right: IROperand) -> IRType:
        """Infer the result type of a binary operation."""
        # Comparison operators always return boolean
        if operator in [BinaryOperator.EQUALS, BinaryOperator.NOT_EQUALS,
                       BinaryOperator.GREATER_THAN, BinaryOperator.LESS_THAN,
                       BinaryOperator.GREATER_EQUAL, BinaryOperator.LESS_EQUAL]:
            return IRTypes.BOOLEAN
        
        # Logical operators return boolean
        if operator in [BinaryOperator.AND, BinaryOperator.OR]:
            return IRTypes.BOOLEAN
        
        # Arithmetic operators: promote types
        if left.ir_type == IRTypes.FLOAT or right.ir_type == IRTypes.FLOAT:
            return IRTypes.FLOAT
        elif left.ir_type == IRTypes.INTEGER and right.ir_type == IRTypes.INTEGER:
            return IRTypes.INTEGER
        else:
            return IRTypes.ANY
    
    def _block_ends_with_return(self, block: IRBasicBlock) -> bool:
        """Check if a block ends with a return instruction."""
        if not block.instructions:
            return False
        last_instr = block.instructions[-1]
        return (isinstance(last_instr, IRInstruction) and 
                last_instr.instruction_type == IRInstructionType.RETURN)

    def visit_processdefinition(self, node: ProcessDefinition) -> None:
        """Convert a ProcessDefinition into a separate IRFunction and register it."""
        # Existing implementation moved from old method
        # Evaluate function parameters
        func_name = node.name.replace(" ", "_").lower()
        param_vars = []
        for param in node.parameters:
            param_var = IRVariable(param.name.replace(" ", "_").lower(), IRTypes.ANY)
            param_vars.append(param_var)
        new_func = IRFunction(name=func_name, parameters=param_vars, return_type=IRTypes.ANY, entry_block="entry")
        # Temporarily switch context
        previous_func = self.context.current_function
        previous_block = self.context.current_block
        previous_var_map = self.context.variable_map

        # Use fresh variable map for the new function scope
        self.context.variable_map = {}

        self.module.add_function(new_func)
        self.context.current_function = new_func
        # Create entry block within new function
        entry_block = IRBasicBlock(new_func.entry_block)
        new_func.add_block(entry_block)
        self.context.current_block = entry_block
        # Map parameter identifiers to IRVariables in symbol table for this function
        for param_var in param_vars:
            self.context.current_function.local_variables[param_var.name] = param_var
            self.context.set_variable(param_var.name, param_var)
        # Visit body statements
        for stmt in node.body:
            self.visit(stmt)
        # Ensure function ends with return (if not already)
        if not entry_block.instructions or entry_block.instructions[-1].instruction_type != IRInstructionType.RETURN:
            entry_block.instructions.append(IRInstruction(IRInstructionType.RETURN))
        # Restore previous context
        self.context.current_function = previous_func
        self.context.current_block = previous_block
        self.context.variable_map = previous_var_map

# === PUBLIC API ===

def ast_to_ir(ast: Program) -> IRModule:
    """Convert a Runa AST to IR module."""
    visitor = ASTToIRVisitor()
    return visitor.visit(ast) 