"""
Runa AST to Control Flow Graph (CFG) Builder

This module provides the `CFGBuilder` class, which traverses a Runa AST
and converts it into a language-agnostic Control Flow Graph (CFG) as defined
in the `ir.py` module.
"""

from ..core.runa_ast import *
from .definitions import *

class CFGBuilder:
    """Builds a CFG from a Runa AST."""

    def __init__(self):
        self.cfg = None
        self.current_block = None
        self.temp_count = 0

    def build(self, program: Program) -> ControlFlowGraph:
        """Build a CFG for an entire Runa program."""
        entry_block = self._new_basic_block()
        exit_block = self._new_basic_block()
        
        self.cfg = ControlFlowGraph(entry_block=entry_block, exit_block=exit_block)
        self.current_block = self.cfg.entry_block
        
        for statement in program.statements:
            statement.accept(self)
            
        # Ensure the last block jumps to the exit block
        self._add_instruction(UnconditionalJump(target=self.cfg.exit_block))
        
        return self.cfg

    def _new_basic_block(self) -> BasicBlock:
        """Create a new basic block and add it to the CFG."""
        if not hasattr(self, 'cfg') or self.cfg is None:
             # Initial case for entry/exit blocks before CFG exists
            block = BasicBlock(id=0)
            return block

        block_id = len(self.cfg.blocks)
        block = BasicBlock(id=block_id)
        self.cfg.blocks.append(block)
        return block

    def _new_temp(self) -> Var:
        """Create a new temporary variable."""
        name = f"__temp{self.temp_count}"
        self.temp_count += 1
        return Var(name)

    def _add_instruction(self, instruction: IRInstruction):
        """Add an instruction to the current basic block."""
        self.current_block.instructions.append(instruction)

    # --- Expression Visitors ---

    def visit_binary_expression(self, node: BinaryExpression) -> Operand:
        """Convert a binary expression into IR instructions."""
        left_operand = node.left.accept(self)
        right_operand = node.right.accept(self)
        target_var = self._new_temp()
        
        self._add_instruction(BinaryOperation(
            target=target_var,
            op=node.operator.value,
            left=left_operand,
            right=right_operand
        ))
        return target_var

    def visit_integer_literal(self, node: IntegerLiteral) -> Constant:
        return Constant(node.value)

    def visit_float_literal(self, node: FloatLiteral) -> Constant:
        return Constant(node.value)

    def visit_string_literal(self, node: StringLiteral) -> Constant:
        return Constant(node.value)

    def visit_boolean_literal(self, node: BooleanLiteral) -> Constant:
        return Constant(node.value)

    def visit_identifier(self, node: Identifier) -> Var:
        return Var(node.name)

    # --- Statement Visitors ---

    def visit_let_statement(self, node: LetStatement):
        """Convert a let statement."""
        value_operand = node.value.accept(self)
        target_var = Var(node.identifier)
        self._add_instruction(Assign(target=target_var, source=value_operand))
        
    def visit_define_statement(self, node: DefineStatement):
        """Convert a define statement."""
        value_operand = node.value.accept(self)
        target_var = Var(node.identifier)
        self._add_instruction(Assign(target=target_var, source=value_operand))

    def visit_set_statement(self, node: SetStatement):
        """Convert a set statement."""
        if isinstance(node.target, Identifier):
            value_operand = node.value.accept(self)
            target_var = Var(node.target.name)
            self._add_instruction(Assign(target=target_var, source=value_operand))
        else:
            # More complex assignments (member access, etc.) are not yet supported.
            pass
            
    def visit_expression_statement(self, node: ExpressionStatement):
        """Convert an expression statement."""
        node.expression.accept(self)

    # --- Generic Visitor ---
    
    def generic_visit(self, node):
        """Default visitor for unhandled AST nodes."""
        # For nodes that don't generate code but have children that might,
        # we can visit them. For now, we'll stop traversal at unhandled nodes.
        pass 