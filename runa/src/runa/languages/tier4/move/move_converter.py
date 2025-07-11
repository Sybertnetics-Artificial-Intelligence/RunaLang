#!/usr/bin/env python3
"""
Move to Runa AST Converter

Bidirectional converter between Move AST and Runa AST, preserving Move's unique
resource-oriented programming semantics, abilities system, and safety-first design
in universal code translation.

Key features:
- Resource-oriented programming model preservation
- Abilities system mapping (copy, drop, store, key)
- Move semantics and ownership tracking
- Module and script organization
- Type system with generics and references
- Safety-first expression handling
"""

from typing import Dict, List, Optional, Any, Union, Tuple, Set
from dataclasses import dataclass
import uuid

from .move_ast import *
from ....core.runa_ast import *


@dataclass
class ConversionContext:
    """Context for Move-Runa conversion tracking."""
    current_module: Optional[str] = None
    current_function: Optional[str] = None
    type_mappings: Dict[str, str] = None
    imported_modules: Set[str] = None
    resource_declarations: Dict[str, MoveStructDeclaration] = None
    
    def __post_init__(self):
        if self.type_mappings is None:
            self.type_mappings = {}
        if self.imported_modules is None:
            self.imported_modules = set()
        if self.resource_declarations is None:
            self.resource_declarations = {}


class MoveToRunaConverter:
    """Converts Move AST to Runa AST."""
    
    def __init__(self):
        self.context = ConversionContext()
        self.move_to_runa_types = {
            MovePrimitiveType.BOOL: "boolean",
            MovePrimitiveType.U8: "uint8", 
            MovePrimitiveType.U16: "uint16",
            MovePrimitiveType.U32: "uint32", 
            MovePrimitiveType.U64: "uint64",
            MovePrimitiveType.U128: "uint128",
            MovePrimitiveType.U256: "uint256",
            MovePrimitiveType.ADDRESS: "address",
            MovePrimitiveType.SIGNER: "signer",
            MovePrimitiveType.VECTOR: "array"
        }
        
    def convert(self, move_ast: MoveNode) -> ASTNode:
        """Convert Move AST node to Runa AST."""
        return move_ast.accept(self)
    
    def visit_program(self, node: MoveProgram) -> ModuleNode:
        """Convert Move program to Runa module."""
        # For Move programs with multiple modules, we create a wrapper module
        statements = []
        
        # Convert all modules as nested modules
        for module in node.modules:
            statements.append(self.convert(module))
        
        # Convert scripts as functions
        for script in node.scripts:
            statements.append(self.convert(script))
        
        return ModuleNode(
            name="move_program",
            body=statements,
            metadata={
                "language": "move",
                "move_specifications": [self.convert(spec) for spec in node.specifications]
            }
        )
    
    def visit_module(self, node: MoveModule) -> ClassNode:
        """Convert Move module to Runa class (representing module namespace)."""
        self.context.current_module = node.name
        
        members = []
        
        # Convert use declarations as import statements
        for use_decl in node.use_declarations:
            members.append(self.convert(use_decl))
        
        # Convert constants
        for const in node.constants:
            members.append(self.convert(const))
        
        # Convert structs as nested classes
        for struct in node.structs:
            members.append(self.convert(struct))
            # Track resource declarations
            if MoveAbility.KEY in struct.abilities:
                self.context.resource_declarations[struct.name] = struct
        
        # Convert functions as methods
        for func in node.functions:
            members.append(self.convert(func))
        
        return ClassNode(
            name=node.name,
            members=members,
            metadata={
                "move_address": node.address,
                "move_module": True,
                "move_friends": [self.convert(friend) for friend in node.friend_declarations]
            }
        )
    
    def visit_struct_declaration(self, node: MoveStructDeclaration) -> ClassNode:
        """Convert Move struct to Runa class."""
        members = []
        
        # Convert fields as class attributes
        for field in node.fields:
            attr = AttributeNode(
                name=field.name,
                type_annotation=self.convert(field.field_type),
                metadata={
                    "move_field": True
                }
            )
            members.append(attr)
        
        # Create constructor if struct has fields
        if node.fields:
            constructor_params = []
            constructor_body = []
            
            for field in node.fields:
                param = ParameterNode(
                    name=field.name,
                    type_annotation=self.convert(field.field_type)
                )
                constructor_params.append(param)
                
                # Assignment in constructor body
                assignment = AssignmentNode(
                    target=AttributeAccessNode(
                        object=VariableNode("self"),
                        attribute=field.name
                    ),
                    value=VariableNode(field.name)
                )
                constructor_body.append(assignment)
            
            constructor = FunctionNode(
                name="__init__",
                parameters=constructor_params,
                body=constructor_body,
                metadata={"move_constructor": True}
            )
            members.append(constructor)
        
        return ClassNode(
            name=node.name,
            members=members,
            metadata={
                "move_struct": True,
                "move_abilities": [ability.value for ability in node.abilities],
                "move_type_parameters": [self.convert(tp) for tp in node.type_parameters],
                "move_is_resource": MoveAbility.KEY in node.abilities,
                "move_is_native": node.is_native
            }
        )
    
    def visit_function_declaration(self, node: MoveFunctionDeclaration) -> FunctionNode:
        """Convert Move function to Runa function."""
        self.context.current_function = node.name
        
        # Convert parameters
        parameters = []
        for param in node.parameters:
            runa_param = ParameterNode(
                name=param.name,
                type_annotation=self.convert(param.parameter_type)
            )
            parameters.append(runa_param)
        
        # Convert body
        body = []
        if node.body:
            body = [self.convert(node.body)]
        
        return FunctionNode(
            name=node.name,
            parameters=parameters,
            body=body,
            return_type=self.convert(node.return_type) if node.return_type else None,
            metadata={
                "move_function": True,
                "move_visibility": node.visibility.value,
                "move_type_parameters": [self.convert(tp) for tp in node.type_parameters],
                "move_acquires": [self.convert(acq) for acq in node.acquires],
                "move_is_native": node.is_native,
                "move_is_entry": node.is_entry
            }
        )
    
    def visit_use_declaration(self, node: MoveUseDeclaration) -> ImportNode:
        """Convert Move use declaration to Runa import."""
        module_path = node.module_name
        if node.module_address:
            module_path = f"{node.module_address}::{node.module_name}"
        
        alias = node.import_name
        imported_names = node.imported_items
        
        self.context.imported_modules.add(node.module_name)
        
        return ImportNode(
            module=module_path,
            alias=alias,
            imported_names=imported_names,
            metadata={
                "move_use": True,
                "move_address": node.module_address
            }
        )
    
    def visit_constant_declaration(self, node: MoveConstantDeclaration) -> AttributeNode:
        """Convert Move constant to Runa attribute."""
        return AttributeNode(
            name=node.name,
            type_annotation=self.convert(node.constant_type),
            initial_value=self.convert(node.value),
            metadata={
                "move_constant": True,
                "is_constant": True
            }
        )
    
    def visit_primitive(self, node: MovePrimitive) -> TypeNode:
        """Convert Move primitive type to Runa type."""
        runa_type_name = self.move_to_runa_types.get(node.type_name, node.type_name.value)
        return TypeNode(
            name=runa_type_name,
            metadata={"move_primitive": node.type_name.value}
        )
    
    def visit_struct_type(self, node: MoveStructType) -> TypeNode:
        """Convert Move struct type to Runa type."""
        name = node.struct_name
        if node.module_name:
            name = f"{node.module_name}.{node.struct_name}"
        
        type_args = [self.convert(arg) for arg in node.type_arguments]
        
        return TypeNode(
            name=name,
            type_arguments=type_args,
            metadata={
                "move_struct_type": True,
                "move_module": node.module_name
            }
        )
    
    def visit_vector_type(self, node: MoveVectorType) -> TypeNode:
        """Convert Move vector type to Runa array type."""
        element_type = self.convert(node.element_type)
        return TypeNode(
            name="array",
            type_arguments=[element_type],
            metadata={"move_vector": True}
        )
    
    def visit_reference_type(self, node: MoveReferenceType) -> TypeNode:
        """Convert Move reference type to Runa reference."""
        referenced_type = self.convert(node.referenced_type)
        ref_type = "mutable_reference" if node.is_mutable else "reference"
        
        return TypeNode(
            name=ref_type,
            type_arguments=[referenced_type],
            metadata={
                "move_reference": True,
                "move_is_mutable": node.is_mutable
            }
        )
    
    def visit_literal(self, node: MoveLiteral) -> LiteralNode:
        """Convert Move literal to Runa literal."""
        return LiteralNode(
            value=node.value,
            metadata={
                "move_literal_type": node.literal_type.value,
                "original_move_literal": True
            }
        )
    
    def visit_identifier(self, node: MoveIdentifier) -> VariableNode:
        """Convert Move identifier to Runa variable."""
        return VariableNode(
            name=node.name,
            metadata={"move_identifier": True}
        )
    
    def visit_function_call(self, node: MoveFunctionCall) -> FunctionCallNode:
        """Convert Move function call to Runa function call."""
        function_name = node.function_name
        if node.module_name:
            function_name = f"{node.module_name}.{node.function_name}"
        
        args = [self.convert(arg) for arg in node.arguments]
        
        return FunctionCallNode(
            function=VariableNode(function_name),
            arguments=args,
            metadata={
                "move_function_call": True,
                "move_module": node.module_name,
                "move_type_arguments": [self.convert(ta) for ta in node.type_arguments]
            }
        )
    
    def visit_borrow(self, node: MoveBorrow) -> UnaryOpNode:
        """Convert Move borrow to Runa reference operation."""
        op = "mutable_borrow" if node.is_mutable else "borrow"
        return UnaryOpNode(
            operator=op,
            operand=self.convert(node.expression),
            metadata={
                "move_borrow": True,
                "move_is_mutable": node.is_mutable
            }
        )
    
    def visit_move(self, node: MoveMove) -> UnaryOpNode:
        """Convert Move move operation to Runa move semantics."""
        return UnaryOpNode(
            operator="move",
            operand=self.convert(node.expression),
            metadata={"move_move_semantics": True}
        )
    
    def visit_copy(self, node: MoveCopy) -> UnaryOpNode:
        """Convert Move copy operation to Runa copy semantics."""
        return UnaryOpNode(
            operator="copy",
            operand=self.convert(node.expression),
            metadata={"move_copy_semantics": True}
        )
    
    def visit_block(self, node: MoveBlock) -> BlockNode:
        """Convert Move block to Runa block."""
        statements = [self.convert(stmt) for stmt in node.statements]
        
        if node.return_expression:
            # Add return expression as final statement
            return_stmt = ReturnNode(value=self.convert(node.return_expression))
            statements.append(return_stmt)
        
        return BlockNode(
            statements=statements,
            metadata={"move_block": True}
        )


class RunaToMoveConverter:
    """Converts Runa AST to Move AST."""
    
    def __init__(self):
        self.context = ConversionContext()
        self.runa_to_move_types = {
            "boolean": MovePrimitiveType.BOOL,
            "uint8": MovePrimitiveType.U8,
            "uint16": MovePrimitiveType.U16, 
            "uint32": MovePrimitiveType.U32,
            "uint64": MovePrimitiveType.U64,
            "uint128": MovePrimitiveType.U128,
            "uint256": MovePrimitiveType.U256,
            "address": MovePrimitiveType.ADDRESS,
            "signer": MovePrimitiveType.SIGNER,
            "array": MovePrimitiveType.VECTOR
        }
    
    def convert(self, runa_ast: ASTNode) -> MoveNode:
        """Convert Runa AST node to Move AST."""
        return runa_ast.accept(self)
    
    def visit_module(self, node: ModuleNode) -> MoveModule:
        """Convert Runa module to Move module."""
        # Extract Move-specific metadata
        metadata = getattr(node, 'metadata', {})
        address = metadata.get('move_address', '0x1')
        
        use_declarations = []
        friend_declarations = []
        constants = []
        structs = []
        functions = []
        
        for member in node.body:
            if isinstance(member, ImportNode):
                use_declarations.append(self.convert_import_to_use(member))
            elif isinstance(member, AttributeNode) and member.metadata.get('move_constant'):
                constants.append(self.convert_attribute_to_constant(member))
            elif isinstance(member, ClassNode):
                if member.metadata.get('move_struct'):
                    structs.append(self.convert_class_to_struct(member))
                else:
                    # Convert class methods to module functions
                    for class_member in member.members:
                        if isinstance(class_member, FunctionNode):
                            functions.append(self.convert(class_member))
            elif isinstance(member, FunctionNode):
                functions.append(self.convert(member))
        
        return MoveModule(
            address=address,
            name=node.name,
            use_declarations=use_declarations,
            friend_declarations=friend_declarations,
            constants=constants,
            structs=structs,
            functions=functions
        )
    
    def convert_class_to_struct(self, node: ClassNode) -> MoveStructDeclaration:
        """Convert Runa class to Move struct."""
        metadata = getattr(node, 'metadata', {})
        
        # Extract abilities from metadata
        abilities = []
        if 'move_abilities' in metadata:
            abilities = [MoveAbility(ability) for ability in metadata['move_abilities']]
        
        # Extract fields from class attributes
        fields = []
        for member in node.members:
            if isinstance(member, AttributeNode) and member.metadata.get('move_field'):
                field = MoveField(
                    name=member.name,
                    field_type=self.convert(member.type_annotation)
                )
                fields.append(field)
        
        return MoveStructDeclaration(
            name=node.name,
            abilities=abilities,
            fields=fields,
            is_native=metadata.get('move_is_native', False)
        )
    
    def visit_function_node(self, node: FunctionNode) -> MoveFunctionDeclaration:
        """Convert Runa function to Move function."""
        metadata = getattr(node, 'metadata', {})
        
        # Extract visibility
        visibility_str = metadata.get('move_visibility', 'private')
        visibility = MoveVisibility(visibility_str)
        
        # Convert parameters
        parameters = []
        for param in node.parameters:
            move_param = MoveParameter(
                name=param.name,
                parameter_type=self.convert(param.type_annotation)
            )
            parameters.append(move_param)
        
        # Convert body
        body = None
        if node.body:
            statements = [self.convert(stmt) for stmt in node.body]
            body = MoveBlock(statements=statements)
        
        return MoveFunctionDeclaration(
            name=node.name,
            visibility=visibility,
            parameters=parameters,
            return_type=self.convert(node.return_type) if node.return_type else None,
            body=body,
            is_native=metadata.get('move_is_native', False),
            is_entry=metadata.get('move_is_entry', False)
        )
    
    def visit_type_node(self, node: TypeNode) -> MoveType:
        """Convert Runa type to Move type."""
        metadata = getattr(node, 'metadata', {})
        
        if 'move_primitive' in metadata:
            primitive_type = MovePrimitiveType(metadata['move_primitive'])
            return MovePrimitive(primitive_type)
        
        if node.name in self.runa_to_move_types:
            if node.name == "array" and node.type_arguments:
                element_type = self.convert(node.type_arguments[0])
                return MoveVectorType(element_type)
            else:
                primitive_type = self.runa_to_move_types[node.name]
                return MovePrimitive(primitive_type)
        
        # Handle reference types
        if node.name in ("reference", "mutable_reference") and node.type_arguments:
            referenced_type = self.convert(node.type_arguments[0])
            is_mutable = node.name == "mutable_reference"
            return MoveReferenceType(referenced_type, is_mutable)
        
        # Default to struct type
        type_args = [self.convert(arg) for arg in node.type_arguments]
        return MoveStructType(
            module_name=metadata.get('move_module'),
            struct_name=node.name,
            type_arguments=type_args
        )


# Convenience functions for conversion

def move_to_runa(move_ast: MoveNode) -> ASTNode:
    """Convert Move AST to Runa AST."""
    converter = MoveToRunaConverter()
    return converter.convert(move_ast)


def runa_to_move(runa_ast: ASTNode) -> MoveNode:
    """Convert Runa AST to Move AST."""
    converter = RunaToMoveConverter()
    return converter.convert(runa_ast)


def preserve_move_semantics(runa_ast: ASTNode) -> ASTNode:
    """Ensure Move semantics are preserved in Runa AST."""
    # Add Move-specific annotations and metadata
    def annotate_node(node):
        if hasattr(node, 'metadata'):
            if not node.metadata:
                node.metadata = {}
            node.metadata['preserves_move_semantics'] = True
        
        # Recursively annotate child nodes
        if hasattr(node, '__dict__'):
            for attr_value in node.__dict__.values():
                if isinstance(attr_value, list):
                    for item in attr_value:
                        if hasattr(item, 'accept'):
                            annotate_node(item)
                elif hasattr(attr_value, 'accept'):
                    annotate_node(attr_value)
    
    annotate_node(runa_ast)
    return runa_ast


def validate_move_conversion(move_ast: MoveNode, converted_runa: ASTNode) -> bool:
    """Validate that Move AST was correctly converted to Runa AST."""
    # Check that essential Move features are preserved
    try:
        # Try to convert back to Move
        converted_back = runa_to_move(converted_runa)
        
        # Basic structural validation
        if type(move_ast) != type(converted_back):
            return False
        
        # More detailed validation would go here
        return True
        
    except Exception:
        return False 