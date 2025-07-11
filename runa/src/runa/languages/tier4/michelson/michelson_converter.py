"""
Michelson to Runa AST converter for bidirectional translation.

This module provides conversion between Michelson AST and Runa AST,
handling stack-based operations and smart contract structures.
"""

from typing import List, Dict, Any, Optional, Union
from ...runa_ast import *
from .michelson_ast import *


class MichelsonToRunaConverter:
    """Converts Michelson AST to Runa AST."""
    
    def __init__(self):
        self.stack_depth = 0
        self.temp_var_counter = 0
        self.current_function = None
    
    def generate_temp_var(self) -> str:
        """Generate a temporary variable name."""
        self.temp_var_counter += 1
        return f"_stack_temp_{self.temp_var_counter}"
    
    def convert_type(self, michelson_type: MichelsonType_Node) -> BasicType:
        """Convert Michelson type to Runa type."""
        type_mapping = {
            MichelsonType.UNIT: PrimitiveType.UNIT,
            MichelsonType.INT: PrimitiveType.INT,
            MichelsonType.NAT: PrimitiveType.INT,  # Map nat to int
            MichelsonType.STRING: PrimitiveType.STRING,
            MichelsonType.BYTES: PrimitiveType.STRING,  # Map bytes to string
            MichelsonType.BOOL: PrimitiveType.BOOL,
            MichelsonType.MUTEZ: PrimitiveType.INT,  # Map mutez to int
            MichelsonType.TEZ: PrimitiveType.INT,    # Map tez to int
            MichelsonType.ADDRESS: PrimitiveType.STRING,
            MichelsonType.KEY: PrimitiveType.STRING,
            MichelsonType.KEY_HASH: PrimitiveType.STRING,
            MichelsonType.SIGNATURE: PrimitiveType.STRING,
            MichelsonType.TIMESTAMP: PrimitiveType.INT,
            MichelsonType.CHAIN_ID: PrimitiveType.STRING,
        }
        
        if michelson_type.type_name in type_mapping:
            return BasicType(type_mapping[michelson_type.type_name])
        
        elif michelson_type.type_name == MichelsonType.PAIR:
            if len(michelson_type.args) == 2:
                left_type = self.convert_type(michelson_type.args[0])
                right_type = self.convert_type(michelson_type.args[1])
                return TupleType([left_type, right_type])
            else:
                return TupleType([self.convert_type(arg) for arg in michelson_type.args])
        
        elif michelson_type.type_name == MichelsonType.OR:
            if len(michelson_type.args) == 2:
                left_type = self.convert_type(michelson_type.args[0])
                right_type = self.convert_type(michelson_type.args[1])
                return UnionType([left_type, right_type])
        
        elif michelson_type.type_name == MichelsonType.OPTION:
            if michelson_type.args:
                inner_type = self.convert_type(michelson_type.args[0])
                return OptionalType(inner_type)
        
        elif michelson_type.type_name == MichelsonType.LIST:
            if michelson_type.args:
                element_type = self.convert_type(michelson_type.args[0])
                return ListType(element_type)
            return ListType(BasicType(PrimitiveType.ANY))
        
        elif michelson_type.type_name == MichelsonType.SET:
            if michelson_type.args:
                element_type = self.convert_michelson_type.args[0])
                return SetType(element_type)
            return SetType(BasicType(PrimitiveType.ANY))
        
        elif michelson_type.type_name == MichelsonType.MAP:
            if len(michelson_type.args) == 2:
                key_type = self.convert_type(michelson_type.args[0])
                value_type = self.convert_type(michelson_type.args[1])
                return MapType(key_type, value_type)
        
        elif michelson_type.type_name == MichelsonType.LAMBDA:
            if len(michelson_type.args) == 2:
                param_type = self.convert_type(michelson_type.args[0])
                return_type = self.convert_type(michelson_type.args[1])
                return FunctionType([param_type], return_type)
        
        # Default to any type
        return BasicType(PrimitiveType.ANY)
    
    def convert_literal(self, literal: MichelsonLiteral) -> Expression:
        """Convert Michelson literal to Runa expression."""
        if literal.type_hint == MichelsonType.INT or literal.type_hint == MichelsonType.NAT:
            return LiteralExpression(literal.value, BasicType(PrimitiveType.INT))
        elif literal.type_hint == MichelsonType.STRING:
            return LiteralExpression(literal.value, BasicType(PrimitiveType.STRING))
        elif literal.type_hint == MichelsonType.BOOL:
            return LiteralExpression(literal.value, BasicType(PrimitiveType.BOOL))
        else:
            # Try to infer type from value
            if isinstance(literal.value, int):
                return LiteralExpression(literal.value, BasicType(PrimitiveType.INT))
            elif isinstance(literal.value, str):
                return LiteralExpression(literal.value, BasicType(PrimitiveType.STRING))
            elif isinstance(literal.value, bool):
                return LiteralExpression(literal.value, BasicType(PrimitiveType.BOOL))
            else:
                return LiteralExpression(literal.value, BasicType(PrimitiveType.ANY))
    
    def convert_instruction_to_statements(self, instruction: MichelsonInstruction_Node) -> List[Statement]:
        """Convert a Michelson instruction to Runa statements."""
        statements = []
        
        if instruction.instruction == MichelsonInstruction.PUSH:
            # PUSH type value -> stack.push(value)
            if len(instruction.args) >= 2:
                type_arg = instruction.args[0]
                value_arg = instruction.args[1]
                
                if isinstance(value_arg, MichelsonLiteral):
                    temp_var = self.generate_temp_var()
                    value_expr = self.convert_literal(value_arg)
                    
                    # Create variable declaration
                    var_decl = VariableDeclaration(
                        temp_var,
                        value_expr.type,
                        value_expr
                    )
                    statements.append(var_decl)
        
        elif instruction.instruction == MichelsonInstruction.DROP:
            # DROP -> remove top of stack (no-op in high-level)
            comment = CommentStatement("Stack DROP operation")
            statements.append(comment)
        
        elif instruction.instruction == MichelsonInstruction.ADD:
            # ADD -> combine top two stack elements
            temp_var = self.generate_temp_var()
            
            # Create a binary operation (simplified)
            left_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 1}")
            right_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 2}")
            
            add_expr = BinaryOperation(
                left_var,
                BinaryOperator.ADD,
                right_var,
                BasicType(PrimitiveType.INT)
            )
            
            result_decl = VariableDeclaration(
                temp_var,
                BasicType(PrimitiveType.INT),
                add_expr
            )
            statements.append(result_decl)
        
        elif instruction.instruction == MichelsonInstruction.SUB:
            # Similar to ADD but with subtraction
            temp_var = self.generate_temp_var()
            left_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 1}")
            right_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 2}")
            
            sub_expr = BinaryOperation(
                left_var,
                BinaryOperator.SUBTRACT,
                right_var,
                BasicType(PrimitiveType.INT)
            )
            
            result_decl = VariableDeclaration(
                temp_var,
                BasicType(PrimitiveType.INT),
                sub_expr
            )
            statements.append(result_decl)
        
        elif instruction.instruction == MichelsonInstruction.MUL:
            # Multiplication
            temp_var = self.generate_temp_var()
            left_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 1}")
            right_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 2}")
            
            mul_expr = BinaryOperation(
                left_var,
                BinaryOperator.MULTIPLY,
                right_var,
                BasicType(PrimitiveType.INT)
            )
            
            result_decl = VariableDeclaration(
                temp_var,
                BasicType(PrimitiveType.INT),
                mul_expr
            )
            statements.append(result_decl)
        
        elif instruction.instruction == MichelsonInstruction.PAIR:
            # PAIR -> create tuple from top two stack elements
            temp_var = self.generate_temp_var()
            left_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 1}")
            right_var = VariableReference(f"_stack_temp_{self.temp_var_counter - 2}")
            
            tuple_expr = TupleExpression(
                [left_var, right_var],
                TupleType([BasicType(PrimitiveType.ANY), BasicType(PrimitiveType.ANY)])
            )
            
            result_decl = VariableDeclaration(
                temp_var,
                TupleType([BasicType(PrimitiveType.ANY), BasicType(PrimitiveType.ANY)]),
                tuple_expr
            )
            statements.append(result_decl)
        
        elif instruction.instruction == MichelsonInstruction.IF:
            # IF {then_branch} {else_branch}
            if len(instruction.args) >= 2:
                then_sequence = instruction.args[0]
                else_sequence = instruction.args[1]
                
                condition_var = VariableReference(f"_stack_temp_{self.temp_var_counter}")
                
                then_statements = []
                if isinstance(then_sequence, MichelsonSequence):
                    for instr in then_sequence.instructions:
                        then_statements.extend(self.convert_instruction_to_statements(instr))
                
                else_statements = []
                if isinstance(else_sequence, MichelsonSequence):
                    for instr in else_sequence.instructions:
                        else_statements.extend(self.convert_instruction_to_statements(instr))
                
                if_stmt = IfStatement(
                    condition_var,
                    BlockStatement(then_statements),
                    BlockStatement(else_statements) if else_statements else None
                )
                statements.append(if_stmt)
        
        elif instruction.instruction == MichelsonInstruction.FAILWITH:
            # FAILWITH -> throw exception
            error_var = VariableReference(f"_stack_temp_{self.temp_var_counter}")
            throw_stmt = ThrowStatement(error_var)
            statements.append(throw_stmt)
        
        elif instruction.instruction == MichelsonInstruction.NIL:
            # NIL operation -> create empty list
            temp_var = self.generate_temp_var()
            empty_list = ListExpression([], ListType(BasicType(PrimitiveType.ANY)))
            
            result_decl = VariableDeclaration(
                temp_var,
                ListType(BasicType(PrimitiveType.ANY)),
                empty_list
            )
            statements.append(result_decl)
        
        elif instruction.instruction == MichelsonInstruction.TRANSFER_TOKENS:
            # Blockchain operation - convert to function call
            temp_var = self.generate_temp_var()
            
            # Create a function call expression
            transfer_call = FunctionCall(
                VariableReference("transfer_tokens"),
                [VariableReference(f"_stack_temp_{self.temp_var_counter - 2}"),  # amount
                 VariableReference(f"_stack_temp_{self.temp_var_counter - 1}"),  # parameter
                 VariableReference(f"_stack_temp_{self.temp_var_counter}")],    # contract
                BasicType(PrimitiveType.ANY)
            )
            
            result_decl = VariableDeclaration(
                temp_var,
                BasicType(PrimitiveType.ANY),
                transfer_call
            )
            statements.append(result_decl)
        
        else:
            # Default: convert to comment
            comment = CommentStatement(f"Michelson instruction: {instruction.instruction.value}")
            statements.append(comment)
        
        return statements
    
    def convert_sequence(self, sequence: MichelsonSequence) -> List[Statement]:
        """Convert a sequence of Michelson instructions to Runa statements."""
        statements = []
        
        for instruction in sequence.instructions:
            statements.extend(self.convert_instruction_to_statements(instruction))
        
        return statements
    
    def convert_contract(self, contract: MichelsonContract) -> RunaModule:
        """Convert a Michelson contract to a Runa module."""
        
        # Convert parameter and storage types
        param_type = self.convert_type(contract.parameter_type)
        storage_type = self.convert_type(contract.storage_type)
        
        # Create contract state as a class
        storage_fields = [
            FieldDeclaration("storage", storage_type, None, AccessModifier.PUBLIC)
        ]
        
        contract_class = ClassDeclaration(
            "TezosContract",
            None,  # No base class
            storage_fields,
            [],    # No methods yet
            AccessModifier.PUBLIC
        )
        
        # Convert the main contract code to a function
        contract_statements = self.convert_sequence(contract.code)
        
        # Create main entry point function
        main_function = FunctionDeclaration(
            "main",
            [Parameter("parameter", param_type), Parameter("storage", storage_type)],
            TupleType([ListType(BasicType(PrimitiveType.ANY)), storage_type]),  # (list operation, storage)
            BlockStatement(contract_statements),
            AccessModifier.PUBLIC
        )
        
        # Add function to class
        contract_class.methods.append(main_function)
        
        # Create module
        module = RunaModule(
            "michelson_contract",
            [],  # No imports
            [contract_class],
            []   # No global functions
        )
        
        return module
    
    def convert(self, node: MichelsonASTNode) -> RunaASTNode:
        """Convert any Michelson AST node to Runa AST."""
        if isinstance(node, MichelsonContract):
            return self.convert_contract(node)
        elif isinstance(node, MichelsonSequence):
            statements = self.convert_sequence(node)
            return BlockStatement(statements)
        elif isinstance(node, MichelsonInstruction_Node):
            statements = self.convert_instruction_to_statements(node)
            return BlockStatement(statements)
        elif isinstance(node, MichelsonLiteral):
            return self.convert_literal(node)
        elif isinstance(node, MichelsonType_Node):
            return self.convert_type(node)
        else:
            # Default conversion
            return CommentStatement(f"Michelson node: {type(node).__name__}")


class RunaToMichelsonConverter:
    """Converts Runa AST to Michelson AST."""
    
    def __init__(self):
        self.stack_operations = []
        self.current_stack_depth = 0
    
    def convert_type(self, runa_type: BasicType) -> MichelsonType_Node:
        """Convert Runa type to Michelson type."""
        if isinstance(runa_type, BasicType):
            type_mapping = {
                PrimitiveType.UNIT: MichelsonType.UNIT,
                PrimitiveType.INT: MichelsonType.INT,
                PrimitiveType.STRING: MichelsonType.STRING,
                PrimitiveType.BOOL: MichelsonType.BOOL,
                PrimitiveType.FLOAT: MichelsonType.INT,  # Map float to int
            }
            
            if runa_type.primitive_type in type_mapping:
                return MichelsonType_Node(type_mapping[runa_type.primitive_type])
        
        elif isinstance(runa_type, TupleType):
            if len(runa_type.element_types) == 2:
                left_type = self.convert_type(runa_type.element_types[0])
                right_type = self.convert_type(runa_type.element_types[1])
                return MichelsonType_Node(MichelsonType.PAIR, [left_type, right_type])
        
        elif isinstance(runa_type, ListType):
            element_type = self.convert_type(runa_type.element_type)
            return MichelsonType_Node(MichelsonType.LIST, [element_type])
        
        elif isinstance(runa_type, OptionalType):
            inner_type = self.convert_type(runa_type.inner_type)
            return MichelsonType_Node(MichelsonType.OPTION, [inner_type])
        
        elif isinstance(runa_type, UnionType):
            if len(runa_type.types) == 2:
                left_type = self.convert_type(runa_type.types[0])
                right_type = self.convert_type(runa_type.types[1])
                return MichelsonType_Node(MichelsonType.OR, [left_type, right_type])
        
        elif isinstance(runa_type, FunctionType):
            if len(runa_type.parameter_types) == 1:
                param_type = self.convert_type(runa_type.parameter_types[0])
                return_type = self.convert_type(runa_type.return_type)
                return MichelsonType_Node(MichelsonType.LAMBDA, [param_type, return_type])
        
        # Default to unit
        return MichelsonType_Node(MichelsonType.UNIT)
    
    def convert_literal(self, literal: LiteralExpression) -> MichelsonInstruction_Node:
        """Convert Runa literal to Michelson PUSH instruction."""
        michelson_type = self.convert_type(literal.type)
        michelson_literal = MichelsonLiteral(literal.value, michelson_type.type_name)
        
        return MichelsonInstruction_Node(
            MichelsonInstruction.PUSH,
            [michelson_type, michelson_literal]
        )
    
    def convert_binary_operation(self, binary_op: BinaryOperation) -> List[MichelsonInstruction_Node]:
        """Convert Runa binary operation to Michelson instructions."""
        instructions = []
        
        # Push operands to stack
        if isinstance(binary_op.left, LiteralExpression):
            instructions.append(self.convert_literal(binary_op.left))
        
        if isinstance(binary_op.right, LiteralExpression):
            instructions.append(self.convert_literal(binary_op.right))
        
        # Add operation instruction
        op_mapping = {
            BinaryOperator.ADD: MichelsonInstruction.ADD,
            BinaryOperator.SUBTRACT: MichelsonInstruction.SUB,
            BinaryOperator.MULTIPLY: MichelsonInstruction.MUL,
            BinaryOperator.DIVIDE: MichelsonInstruction.DIV,
            BinaryOperator.EQUAL: MichelsonInstruction.COMPARE,
            BinaryOperator.NOT_EQUAL: MichelsonInstruction.COMPARE,
            BinaryOperator.LESS_THAN: MichelsonInstruction.COMPARE,
            BinaryOperator.GREATER_THAN: MichelsonInstruction.COMPARE,
        }
        
        if binary_op.operator in op_mapping:
            instructions.append(MichelsonInstruction_Node(op_mapping[binary_op.operator]))
        
        return instructions
    
    def convert_function_call(self, call: FunctionCall) -> List[MichelsonInstruction_Node]:
        """Convert Runa function call to Michelson instructions."""
        instructions = []
        
        # Special handling for blockchain operations
        if isinstance(call.function, VariableReference):
            func_name = call.function.name
            
            if func_name == "transfer_tokens":
                # Push arguments to stack
                for arg in call.arguments:
                    if isinstance(arg, LiteralExpression):
                        instructions.append(self.convert_literal(arg))
                
                instructions.append(MichelsonInstruction_Node(MichelsonInstruction.TRANSFER_TOKENS))
            
            else:
                # Generic function call - convert to comment
                instructions.append(MichelsonInstruction_Node(
                    MichelsonInstruction.FAILWITH,
                    [MichelsonLiteral(f"Function call: {func_name}")]
                ))
        
        return instructions
    
    def convert_statement(self, stmt: Statement) -> List[MichelsonInstruction_Node]:
        """Convert Runa statement to Michelson instructions."""
        instructions = []
        
        if isinstance(stmt, VariableDeclaration):
            if isinstance(stmt.initializer, LiteralExpression):
                instructions.append(self.convert_literal(stmt.initializer))
            elif isinstance(stmt.initializer, BinaryOperation):
                instructions.extend(self.convert_binary_operation(stmt.initializer))
        
        elif isinstance(stmt, IfStatement):
            # Convert condition
            if isinstance(stmt.condition, VariableReference):
                # Condition should already be on stack
                pass
            
            # Convert branches
            then_instructions = []
            if isinstance(stmt.then_statement, BlockStatement):
                for s in stmt.then_statement.statements:
                    then_instructions.extend(self.convert_statement(s))
            
            else_instructions = []
            if stmt.else_statement and isinstance(stmt.else_statement, BlockStatement):
                for s in stmt.else_statement.statements:
                    else_instructions.extend(self.convert_statement(s))
            
            then_sequence = MichelsonSequence(then_instructions)
            else_sequence = MichelsonSequence(else_instructions)
            
            instructions.append(MichelsonInstruction_Node(
                MichelsonInstruction.IF,
                [then_sequence, else_sequence]
            ))
        
        elif isinstance(stmt, ThrowStatement):
            # Convert throw to FAILWITH
            if isinstance(stmt.exception, VariableReference):
                # Exception should be on stack
                pass
            instructions.append(MichelsonInstruction_Node(MichelsonInstruction.FAILWITH))
        
        elif isinstance(stmt, CommentStatement):
            # Comments don't generate instructions
            pass
        
        return instructions
    
    def convert_function(self, func: FunctionDeclaration) -> MichelsonSequence:
        """Convert Runa function to Michelson instruction sequence."""
        instructions = []
        
        if isinstance(func.body, BlockStatement):
            for stmt in func.body.statements:
                instructions.extend(self.convert_statement(stmt))
        
        # Add final operations list and pair for contract
        instructions.append(MichelsonInstruction_Node(MichelsonInstruction.NIL, 
                                                    [MichelsonType_Node(MichelsonType.OPERATION)]))
        instructions.append(MichelsonInstruction_Node(MichelsonInstruction.PAIR))
        
        return MichelsonSequence(instructions)
    
    def convert_module(self, module: RunaModule) -> MichelsonContract:
        """Convert Runa module to Michelson contract."""
        # Find the contract class
        contract_class = None
        for cls in module.classes:
            if cls.name == "TezosContract":
                contract_class = cls
                break
        
        if not contract_class:
            # Create default contract
            param_type = MichelsonType_Node(MichelsonType.UNIT)
            storage_type = MichelsonType_Node(MichelsonType.UNIT)
            code = MichelsonSequence([
                MichelsonInstruction_Node(MichelsonInstruction.DROP),
                MichelsonInstruction_Node(MichelsonInstruction.NIL, [MichelsonType_Node(MichelsonType.OPERATION)]),
                MichelsonInstruction_Node(MichelsonInstruction.PAIR)
            ])
            
            return MichelsonContract(param_type, storage_type, code)
        
        # Extract parameter and storage types from main function
        main_function = None
        for method in contract_class.methods:
            if method.name == "main":
                main_function = method
                break
        
        if main_function and len(main_function.parameters) >= 2:
            param_type = self.convert_type(main_function.parameters[0].type)
            storage_type = self.convert_type(main_function.parameters[1].type)
            code = self.convert_function(main_function)
        else:
            param_type = MichelsonType_Node(MichelsonType.UNIT)
            storage_type = MichelsonType_Node(MichelsonType.UNIT)
            code = MichelsonSequence([
                MichelsonInstruction_Node(MichelsonInstruction.DROP),
                MichelsonInstruction_Node(MichelsonInstruction.NIL, [MichelsonType_Node(MichelsonType.OPERATION)]),
                MichelsonInstruction_Node(MichelsonInstruction.PAIR)
            ])
        
        return MichelsonContract(param_type, storage_type, code)
    
    def convert(self, node: RunaASTNode) -> MichelsonASTNode:
        """Convert any Runa AST node to Michelson AST."""
        if isinstance(node, RunaModule):
            return self.convert_module(node)
        elif isinstance(node, FunctionDeclaration):
            return self.convert_function(node)
        elif isinstance(node, LiteralExpression):
            return self.convert_literal(node)
        elif isinstance(node, BinaryOperation):
            instructions = self.convert_binary_operation(node)
            return MichelsonSequence(instructions)
        elif isinstance(node, BasicType):
            return self.convert_type(node)
        else:
            # Default: create empty sequence
            return MichelsonSequence([])


def michelson_to_runa(michelson_ast: MichelsonASTNode) -> RunaASTNode:
    """Convert Michelson AST to Runa AST."""
    converter = MichelsonToRunaConverter()
    return converter.convert(michelson_ast)


def runa_to_michelson(runa_ast: RunaASTNode) -> MichelsonASTNode:
    """Convert Runa AST to Michelson AST."""
    converter = RunaToMichelsonConverter()
    return converter.convert(runa_ast) 