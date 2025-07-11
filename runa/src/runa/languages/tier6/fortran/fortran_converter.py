"""
Fortran Converter for Runa Universal Translation Platform
Handles bidirectional conversion between Runa AST and Fortran AST

This converter supports Fortran's scientific computing capabilities:
- Strong typing with precise numeric control
- Array-oriented programming and operations
- Mathematical and scientific functions
- Module system and interfaces
- Derived types and object-oriented features
- Parallel constructs and coarrays
- Memory management (allocatable, pointer)
"""

from typing import List, Optional, Dict, Any, Union
import logging
from dataclasses import dataclass, field

from .fortran_ast import *
from ...core.ast_base import ASTNode
from ...core.converter_base import BaseConverter, ConversionError
from ...shared.type_system import TypeSystem, Type

logger = logging.getLogger(__name__)

@dataclass
class FortranConversionContext:
    """Context for Fortran conversion operations"""
    current_module: Optional[str] = None
    use_statements: List[str] = field(default_factory=list)
    procedures: Dict[str, FortranProcedure] = field(default_factory=dict)
    variables: Dict[str, FortranVariableDeclaration] = field(default_factory=dict)
    precision_mode: str = "double"  # single, double, quad
    array_style: str = "modern"  # legacy, modern
    scientific_computing_mode: bool = True
    
class FortranConverter(BaseConverter):
    """Converter between Runa AST and Fortran AST"""
    
    def __init__(self):
        super().__init__()
        self.context = FortranConversionContext()
        self.type_system = TypeSystem()
        
        # Fortran type mappings
        self.fortran_type_map = {
            "String": "character",
            "Integer": "integer",
            "Float": "real",
            "Double": "real(real64)",
            "Boolean": "logical",
            "Array": "dimension",
            "Complex": "complex",
            "Function": "procedure"
        }
        
        # Fortran operators
        self.fortran_operators = {
            "+": "+", "-": "-", "*": "*", "/": "/", "**": "**",
            "==": "==", "!=": "/=", "<": "<", ">": ">",
            "<=": "<=", ">=": ">=",
            "&&": ".and.", "||": ".or.", "!": ".not.",
            "=": "=", "=>": "=>"
        }
        
    def runa_to_fortran(self, runa_node: ASTNode) -> FortranNode:
        """Convert Runa AST node to Fortran AST node"""
        try:
            node_type = getattr(runa_node, 'node_type', type(runa_node).__name__)
            
            conversion_method = f"_convert_{node_type.lower()}_to_fortran"
            if hasattr(self, conversion_method):
                return getattr(self, conversion_method)(runa_node)
            else:
                return self._convert_generic_to_fortran(runa_node)
                
        except Exception as e:
            logger.error(f"Error converting Runa to Fortran: {e}")
            raise ConversionError(f"Failed to convert {type(runa_node).__name__} to Fortran: {e}")
    
    def fortran_to_runa(self, fortran_node: FortranNode) -> ASTNode:
        """Convert Fortran AST node to Runa AST node"""
        try:
            node_type = fortran_node.node_type.value
            
            conversion_method = f"_convert_{node_type.lower()}_to_runa"
            if hasattr(self, conversion_method):
                return getattr(self, conversion_method)(fortran_node)
            else:
                return self._convert_generic_to_runa(fortran_node)
                
        except Exception as e:
            logger.error(f"Error converting Fortran to Runa: {e}")
            raise ConversionError(f"Failed to convert {fortran_node.node_type} to Runa: {e}")
    
    # Runa to Fortran conversions
    
    def _convert_program_to_fortran(self, runa_node) -> FortranProgram:
        """Convert Runa program to Fortran program"""
        name = getattr(runa_node, 'name', 'main')
        
        statements = []
        variables = []
        
        for stmt in getattr(runa_node, 'statements', []):
            fortran_stmt = self.runa_to_fortran(stmt)
            if isinstance(fortran_stmt, FortranVariableDeclaration):
                variables.append(fortran_stmt)
            else:
                statements.append(fortran_stmt)
        
        return FortranProgram(
            name=name,
            variables=variables,
            statements=statements
        )
    
    def _convert_module_to_fortran(self, runa_node) -> FortranModule:
        """Convert Runa module to Fortran module"""
        name = getattr(runa_node, 'name', 'runa_module')
        
        declarations = []
        for decl in getattr(runa_node, 'declarations', []):
            fortran_decl = self.runa_to_fortran(decl)
            declarations.append(fortran_decl)
        
        return FortranModule(name=name, declarations=declarations)
    
    def _convert_variable_declaration_to_fortran(self, runa_node) -> FortranVariableDeclaration:
        """Convert Runa variable declaration to Fortran variable declaration"""
        var_name = getattr(runa_node, 'name', 'var')
        var_type = getattr(runa_node, 'type', 'integer')
        
        # Map Runa type to Fortran type
        fortran_type = self.fortran_type_map.get(var_type, var_type.lower())
        
        # Handle precision for scientific computing
        if fortran_type == "real" and self.context.precision_mode == "double":
            fortran_type = "real(real64)"
        elif fortran_type == "real" and self.context.precision_mode == "quad":
            fortran_type = "real(real128)"
        
        type_spec = FortranTypeSpec(type_name=fortran_type)
        
        return FortranVariableDeclaration(
            names=[var_name],
            type_spec=type_spec
        )
    
    def _convert_function_declaration_to_fortran(self, runa_node) -> FortranFunction:
        """Convert Runa function to Fortran function"""
        name = getattr(runa_node, 'name', 'func')
        
        # Convert parameters
        parameters = []
        for param in getattr(runa_node, 'parameters', []):
            param_name = getattr(param, 'name', 'param')
            param_type = getattr(param, 'type', None)
            
            type_spec = None
            if param_type:
                fortran_type = self.fortran_type_map.get(param_type, param_type.lower())
                type_spec = FortranTypeSpec(type_name=fortran_type)
            
            parameters.append(FortranParameter(name=param_name, type_spec=type_spec))
        
        # Convert return type
        return_type = None
        if hasattr(runa_node, 'return_type') and runa_node.return_type:
            ret_type = runa_node.return_type
            fortran_ret_type = self.fortran_type_map.get(ret_type, ret_type.lower())
            return_type = FortranTypeSpec(type_name=fortran_ret_type)
        
        # Convert body
        statements = []
        for stmt in getattr(runa_node, 'body', []):
            statements.append(self.runa_to_fortran(stmt))
        
        return FortranFunction(
            name=name,
            parameters=parameters,
            return_type=return_type,
            statements=statements
        )
    
    def _convert_if_statement_to_fortran(self, runa_node) -> FortranIfConstruct:
        """Convert Runa if statement to Fortran if construct"""
        condition = self.runa_to_fortran(getattr(runa_node, 'condition'))
        then_block = [self.runa_to_fortran(stmt) for stmt in getattr(runa_node, 'then_block', [])]
        else_block = [self.runa_to_fortran(stmt) for stmt in getattr(runa_node, 'else_block', [])]
        
        return FortranIfConstruct(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def _convert_for_loop_to_fortran(self, runa_node) -> FortranDoConstruct:
        """Convert Runa for loop to Fortran do construct"""
        variable = getattr(runa_node, 'variable', None)
        start = self.runa_to_fortran(getattr(runa_node, 'start')) if hasattr(runa_node, 'start') else None
        end = self.runa_to_fortran(getattr(runa_node, 'end')) if hasattr(runa_node, 'end') else None
        step = self.runa_to_fortran(getattr(runa_node, 'step')) if hasattr(runa_node, 'step') else None
        
        body = [self.runa_to_fortran(stmt) for stmt in getattr(runa_node, 'body', [])]
        
        return FortranDoConstruct(
            variable=variable.name if variable else None,
            start=start,
            end=end,
            step=step,
            body=body
        )
    
    def _convert_assignment_to_fortran(self, runa_node) -> FortranAssignment:
        """Convert Runa assignment to Fortran assignment"""
        lhs = self.runa_to_fortran(getattr(runa_node, 'left'))
        rhs = self.runa_to_fortran(getattr(runa_node, 'right'))
        
        return FortranAssignment(lhs=lhs, rhs=rhs)
    
    def _convert_binary_operation_to_fortran(self, runa_node) -> FortranBinaryOperation:
        """Convert Runa binary operation to Fortran binary operation"""
        left = self.runa_to_fortran(getattr(runa_node, 'left'))
        right = self.runa_to_fortran(getattr(runa_node, 'right'))
        operator = getattr(runa_node, 'operator', '+')
        
        # Map operator to Fortran equivalent
        fortran_operator = self.fortran_operators.get(operator, operator)
        
        return FortranBinaryOperation(
            left=left,
            right=right,
            operator=fortran_operator
        )
    
    def _convert_function_call_to_fortran(self, runa_node) -> FortranFunctionCall:
        """Convert Runa function call to Fortran function call"""
        name = getattr(runa_node, 'name', 'func')
        arguments = [self.runa_to_fortran(arg) for arg in getattr(runa_node, 'arguments', [])]
        
        return FortranFunctionCall(name=name, arguments=arguments)
    
    def _convert_array_reference_to_fortran(self, runa_node) -> FortranArrayReference:
        """Convert Runa array reference to Fortran array reference"""
        array = self.runa_to_fortran(getattr(runa_node, 'array'))
        indices = [self.runa_to_fortran(idx) for idx in getattr(runa_node, 'indices', [])]
        
        return FortranArrayReference(array=array, indices=indices)
    
    def _convert_string_literal_to_fortran(self, runa_node) -> FortranCharacterLiteral:
        """Convert Runa string literal to Fortran character literal"""
        value = getattr(runa_node, 'value', '')
        return FortranCharacterLiteral(value=value)
    
    def _convert_numeric_literal_to_fortran(self, runa_node) -> Union[FortranIntegerLiteral, FortranRealLiteral]:
        """Convert Runa numeric literal to Fortran numeric literal"""
        value = getattr(runa_node, 'value', 0)
        
        if isinstance(value, int):
            return FortranIntegerLiteral(value=value)
        else:
            return FortranRealLiteral(value=float(value))
    
    def _convert_boolean_literal_to_fortran(self, runa_node) -> FortranLogicalLiteral:
        """Convert Runa boolean literal to Fortran logical literal"""
        value = getattr(runa_node, 'value', False)
        return FortranLogicalLiteral(value=value)
    
    # Fortran to Runa conversions
    
    def _convert_program_to_runa(self, fortran_node: FortranProgram):
        """Convert Fortran program to Runa program"""
        from ...core.ast_base import Program
        
        statements = []
        for stmt in fortran_node.statements:
            runa_stmt = self.fortran_to_runa(stmt)
            statements.append(runa_stmt)
        
        return Program(name=fortran_node.name, statements=statements)
    
    def _convert_module_to_runa(self, fortran_node: FortranModule):
        """Convert Fortran module to Runa module"""
        from ...core.ast_base import Module
        
        declarations = []
        for decl in fortran_node.declarations:
            runa_decl = self.fortran_to_runa(decl)
            declarations.append(runa_decl)
        
        return Module(name=fortran_node.name, declarations=declarations)
    
    def _convert_variable_declaration_to_runa(self, fortran_node: FortranVariableDeclaration):
        """Convert Fortran variable declaration to Runa variable declaration"""
        from ...core.ast_base import VariableDeclaration
        
        # Get the first variable name (Fortran allows multiple in one declaration)
        name = fortran_node.names[0] if fortran_node.names else "var"
        
        # Map Fortran type to Runa type
        fortran_type = fortran_node.type_spec.type_name.lower()
        runa_type = self._fortran_type_to_runa_type(fortran_type)
        
        return VariableDeclaration(name=name, type=runa_type)
    
    def _convert_function_to_runa(self, fortran_node: FortranFunction):
        """Convert Fortran function to Runa function"""
        from ...core.ast_base import FunctionDeclaration, Parameter
        
        # Convert parameters
        parameters = []
        for param in fortran_node.parameters:
            param_type = None
            if param.type_spec:
                param_type = self._fortran_type_to_runa_type(param.type_spec.type_name.lower())
            
            parameters.append(Parameter(name=param.name, type=param_type))
        
        # Convert return type
        return_type = None
        if fortran_node.return_type:
            return_type = self._fortran_type_to_runa_type(fortran_node.return_type.type_name.lower())
        
        # Convert body
        body = [self.fortran_to_runa(stmt) for stmt in fortran_node.statements]
        
        return FunctionDeclaration(
            name=fortran_node.name,
            parameters=parameters,
            return_type=return_type,
            body=body
        )
    
    def _convert_subroutine_to_runa(self, fortran_node: FortranSubroutine):
        """Convert Fortran subroutine to Runa function (void return)"""
        from ...core.ast_base import FunctionDeclaration, Parameter
        
        # Convert parameters
        parameters = []
        for param in fortran_node.parameters:
            param_type = None
            if param.type_spec:
                param_type = self._fortran_type_to_runa_type(param.type_spec.type_name.lower())
            
            parameters.append(Parameter(name=param.name, type=param_type))
        
        # Convert body
        body = [self.fortran_to_runa(stmt) for stmt in fortran_node.statements]
        
        return FunctionDeclaration(
            name=fortran_node.name,
            parameters=parameters,
            return_type="void",
            body=body
        )
    
    def _convert_if_construct_to_runa(self, fortran_node: FortranIfConstruct):
        """Convert Fortran if construct to Runa if statement"""
        from ...core.ast_base import IfStatement
        
        condition = self.fortran_to_runa(fortran_node.condition)
        then_block = [self.fortran_to_runa(stmt) for stmt in fortran_node.then_block]
        else_block = [self.fortran_to_runa(stmt) for stmt in fortran_node.else_block]
        
        return IfStatement(
            condition=condition,
            then_block=then_block,
            else_block=else_block
        )
    
    def _convert_do_construct_to_runa(self, fortran_node: FortranDoConstruct):
        """Convert Fortran do construct to Runa for loop"""
        from ...core.ast_base import ForLoop, VariableReference
        
        variable = VariableReference(name=fortran_node.variable) if fortran_node.variable else None
        start = self.fortran_to_runa(fortran_node.start) if fortran_node.start else None
        end = self.fortran_to_runa(fortran_node.end) if fortran_node.end else None
        step = self.fortran_to_runa(fortran_node.step) if fortran_node.step else None
        
        body = [self.fortran_to_runa(stmt) for stmt in fortran_node.body]
        
        return ForLoop(
            variable=variable,
            start=start,
            end=end,
            step=step,
            body=body
        )
    
    def _convert_assignment_to_runa(self, fortran_node: FortranAssignment):
        """Convert Fortran assignment to Runa assignment"""
        from ...core.ast_base import Assignment
        
        left = self.fortran_to_runa(fortran_node.lhs)
        right = self.fortran_to_runa(fortran_node.rhs)
        
        return Assignment(left=left, right=right)
    
    def _convert_binary_operation_to_runa(self, fortran_node: FortranBinaryOperation):
        """Convert Fortran binary operation to Runa binary operation"""
        from ...core.ast_base import BinaryOperation
        
        left = self.fortran_to_runa(fortran_node.left)
        right = self.fortran_to_runa(fortran_node.right)
        
        # Map Fortran operator to Runa operator
        operator = self._fortran_operator_to_runa_operator(fortran_node.operator)
        
        return BinaryOperation(left=left, right=right, operator=operator)
    
    def _convert_function_call_to_runa(self, fortran_node: FortranFunctionCall):
        """Convert Fortran function call to Runa function call"""
        from ...core.ast_base import FunctionCall
        
        arguments = [self.fortran_to_runa(arg) for arg in fortran_node.arguments]
        
        return FunctionCall(name=fortran_node.name, arguments=arguments)
    
    def _convert_array_reference_to_runa(self, fortran_node: FortranArrayReference):
        """Convert Fortran array reference to Runa array access"""
        from ...core.ast_base import ArrayAccess
        
        array = self.fortran_to_runa(fortran_node.array)
        indices = [self.fortran_to_runa(idx) for idx in fortran_node.indices]
        
        return ArrayAccess(array=array, indices=indices)
    
    def _convert_character_literal_to_runa(self, fortran_node: FortranCharacterLiteral):
        """Convert Fortran character literal to Runa string literal"""
        from ...core.ast_base import StringLiteral
        return StringLiteral(value=fortran_node.value)
    
    def _convert_integer_literal_to_runa(self, fortran_node: FortranIntegerLiteral):
        """Convert Fortran integer literal to Runa numeric literal"""
        from ...core.ast_base import NumericLiteral
        return NumericLiteral(value=fortran_node.value)
    
    def _convert_real_literal_to_runa(self, fortran_node: FortranRealLiteral):
        """Convert Fortran real literal to Runa numeric literal"""
        from ...core.ast_base import NumericLiteral
        return NumericLiteral(value=fortran_node.value)
    
    def _convert_logical_literal_to_runa(self, fortran_node: FortranLogicalLiteral):
        """Convert Fortran logical literal to Runa boolean literal"""
        from ...core.ast_base import BooleanLiteral
        return BooleanLiteral(value=fortran_node.value)
    
    def _convert_identifier_to_runa(self, fortran_node: FortranIdentifier):
        """Convert Fortran identifier to Runa variable reference"""
        from ...core.ast_base import VariableReference
        return VariableReference(name=fortran_node.name)
    
    # Utility methods
    
    def _fortran_type_to_runa_type(self, fortran_type: str) -> str:
        """Map Fortran type to Runa type"""
        type_map = {
            "integer": "Integer",
            "real": "Float",
            "real(real64)": "Double",
            "complex": "Complex",
            "logical": "Boolean",
            "character": "String"
        }
        return type_map.get(fortran_type, fortran_type)
    
    def _fortran_operator_to_runa_operator(self, fortran_op: str) -> str:
        """Map Fortran operator to Runa operator"""
        op_map = {
            ".and.": "&&",
            ".or.": "||",
            ".not.": "!",
            "/=": "!=",
            "**": "^"  # Power operator
        }
        return op_map.get(fortran_op, fortran_op)
    
    def _convert_generic_to_fortran(self, runa_node) -> FortranNode:
        """Generic conversion from Runa to Fortran"""
        node_name = type(runa_node).__name__.lower()
        return FortranIdentifier(name=node_name)
    
    def _convert_generic_to_runa(self, fortran_node: FortranNode):
        """Generic conversion from Fortran to Runa"""
        from ...core.ast_base import Identifier
        return Identifier(name=str(fortran_node.node_type.value))
    
    # Scientific computing specific methods
    
    def enable_scientific_computing_mode(self):
        """Enable scientific computing optimizations"""
        self.context.scientific_computing_mode = True
        self.context.precision_mode = "double"
    
    def set_precision_mode(self, mode: str):
        """Set precision mode (single, double, quad)"""
        self.context.precision_mode = mode
    
    def create_fortran_array_declaration(self, name: str, type_name: str, dimensions: List[str]):
        """Create Fortran array declaration"""
        type_spec = FortranTypeSpec(type_name=type_name)
        attributes = [f"dimension({','.join(dimensions)})"]
        
        return FortranVariableDeclaration(
            names=[name],
            type_spec=type_spec,
            attributes=attributes
        )
    
    def create_fortran_module_use(self, module_name: str, only_list: List[str] = None):
        """Create Fortran use statement"""
        return FortranUseStatement(
            module_name=module_name,
            only_list=only_list or []
        ) 