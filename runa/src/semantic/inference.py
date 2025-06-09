"""
Type inference engine for the Runa programming language.

This module provides utilities for inferring types in Runa programs.
It uses constraint-based type inference with a bidirectional type checking approach.
"""

from typing import Dict, Set, List, Optional, Tuple, Any, cast
from ..parser.ast import (
    Node, BinaryOp, UnaryOp, Literal, Identifier, Assignment,
    CallExpr, IfExpr, Block, FunctionDecl, VarDecl, ReturnStmt,
    ForLoop, WhileLoop, MethodCall, PropertyAccess, ListExpr,
    DictionaryExpr, IndexAccess
)
from .types import Type, TypeSystem, TypeCategory, FunctionType, UnionType


class InferenceContext:
    """
    Context for type inference operations.
    
    This class maintains the state during type inference, including
    constraints, type variables, and the current type environment.
    
    Attributes:
        type_system: The type system to use for inference
        constraints: Type constraints collected during inference
        type_vars: Type variables created during inference
        var_types: Current known variable types
    """
    
    def __init__(self, type_system: TypeSystem):
        """
        Initialize a new InferenceContext.
        
        Args:
            type_system: The type system to use for inference
        """
        self.type_system = type_system
        self.constraints: List[Tuple[str, str]] = []  # (type1, type2) means type1 must be assignable to type2
        self.type_vars: Dict[str, str] = {}  # Maps type variables to their inferred types
        self.var_types: Dict[str, str] = {}  # Maps variable names to their types
        self.next_var_id = 0
    
    def create_type_var(self) -> str:
        """
        Create a new type variable.
        
        Returns:
            A new unique type variable name
        """
        var_name = f"T{self.next_var_id}"
        self.next_var_id += 1
        self.type_vars[var_name] = "Any"  # Initially, type variables can be anything
        return var_name
    
    def add_constraint(self, from_type: str, to_type: str) -> None:
        """
        Add a constraint that from_type must be assignable to to_type.
        
        Args:
            from_type: The source type
            to_type: The target type
        """
        self.constraints.append((from_type, to_type))
    
    def get_var_type(self, var_name: str) -> Optional[str]:
        """
        Get the type of a variable.
        
        Args:
            var_name: The name of the variable
            
        Returns:
            The type of the variable or None if not found
        """
        return self.var_types.get(var_name)
    
    def set_var_type(self, var_name: str, type_name: str) -> None:
        """
        Set the type of a variable.
        
        Args:
            var_name: The name of the variable
            type_name: The type of the variable
        """
        self.var_types[var_name] = type_name
    
    def resolve_type_var(self, type_var: str) -> str:
        """
        Resolve a type variable to its inferred type.
        
        Args:
            type_var: The type variable to resolve
            
        Returns:
            The inferred type of the type variable
        """
        if type_var in self.type_vars:
            inferred_type = self.type_vars[type_var]
            
            # If the inferred type is itself a type variable, resolve it recursively
            if inferred_type in self.type_vars:
                return self.resolve_type_var(inferred_type)
            
            return inferred_type
        
        return type_var  # Not a type variable


class TypeInferenceEngine:
    """
    Engine for inferring types in Runa programs.
    
    This class provides methods for inferring types of expressions and statements.
    It uses a bidirectional type checking approach with constraint solving.
    
    Attributes:
        type_system: The type system to use for inference
    """
    
    def __init__(self, type_system: TypeSystem):
        """
        Initialize a new TypeInferenceEngine.
        
        Args:
            type_system: The type system to use for inference
        """
        self.type_system = type_system
    
    def infer_program(self, ast: Node) -> Dict[str, str]:
        """
        Infer types for an entire program.
        
        Args:
            ast: The AST of the program
            
        Returns:
            A dictionary mapping variable names to their inferred types
        """
        context = InferenceContext(self.type_system)
        self._infer_node_type(ast, context)
        self._solve_constraints(context)
        
        # Resolve all variable types
        resolved_types = {}
        for var_name, type_name in context.var_types.items():
            resolved_type = context.resolve_type_var(type_name)
            resolved_types[var_name] = resolved_type
        
        return resolved_types
    
    def _infer_node_type(self, node: Node, context: InferenceContext) -> str:
        """
        Infer the type of a node.
        
        Args:
            node: The node to infer the type of
            context: The inference context
            
        Returns:
            The inferred type of the node
        """
        # Different inference strategies based on node type
        if isinstance(node, Literal):
            return self._infer_literal_type(node, context)
        
        elif isinstance(node, Identifier):
            return self._infer_identifier_type(node, context)
        
        elif isinstance(node, BinaryOp):
            return self._infer_binary_op_type(node, context)
        
        elif isinstance(node, UnaryOp):
            return self._infer_unary_op_type(node, context)
        
        elif isinstance(node, Assignment):
            return self._infer_assignment_type(node, context)
        
        elif isinstance(node, CallExpr):
            return self._infer_call_expr_type(node, context)
        
        elif isinstance(node, IfExpr):
            return self._infer_if_expr_type(node, context)
        
        elif isinstance(node, Block):
            return self._infer_block_type(node, context)
        
        elif isinstance(node, FunctionDecl):
            return self._infer_function_decl_type(node, context)
        
        elif isinstance(node, VarDecl):
            return self._infer_var_decl_type(node, context)
        
        elif isinstance(node, ReturnStmt):
            return self._infer_return_stmt_type(node, context)
        
        elif isinstance(node, ForLoop):
            return self._infer_for_loop_type(node, context)
        
        elif isinstance(node, WhileLoop):
            return self._infer_while_loop_type(node, context)
        
        elif isinstance(node, MethodCall):
            return self._infer_method_call_type(node, context)
        
        elif isinstance(node, PropertyAccess):
            return self._infer_property_access_type(node, context)
        
        elif isinstance(node, ListExpr):
            return self._infer_list_expr_type(node, context)
        
        elif isinstance(node, DictionaryExpr):
            return self._infer_dictionary_expr_type(node, context)
        
        elif isinstance(node, IndexAccess):
            return self._infer_index_access_type(node, context)
        
        # If we don't know how to infer the type, create a type variable
        return context.create_type_var()
    
    def _infer_literal_type(self, node: Literal, context: InferenceContext) -> str:
        """
        Infer the type of a literal.
        
        Args:
            node: The literal node
            context: The inference context
            
        Returns:
            The inferred type of the literal
        """
        if node.kind == "int":
            return "Int"
        elif node.kind == "float":
            return "Float"
        elif node.kind == "string":
            return "String"
        elif node.kind == "boolean":
            return "Boolean"
        elif node.kind == "null":
            return "Null"
        else:
            # Unknown literal type, create a type variable
            return context.create_type_var()
    
    def _infer_identifier_type(self, node: Identifier, context: InferenceContext) -> str:
        """
        Infer the type of an identifier.
        
        Args:
            node: The identifier node
            context: The inference context
            
        Returns:
            The inferred type of the identifier
        """
        # If we already know the type of this variable, return it
        var_type = context.get_var_type(node.name)
        if var_type:
            return var_type
        
        # Otherwise, create a type variable for it
        type_var = context.create_type_var()
        context.set_var_type(node.name, type_var)
        return type_var
    
    def _infer_binary_op_type(self, node: BinaryOp, context: InferenceContext) -> str:
        """
        Infer the type of a binary operation.
        
        Args:
            node: The binary operation node
            context: The inference context
            
        Returns:
            The inferred type of the binary operation
        """
        left_type = self._infer_node_type(node.left, context)
        right_type = self._infer_node_type(node.right, context)
        
        # Different operators have different type rules
        if node.op in ["+", "-", "*", "/"]:
            # Arithmetic operators work on numeric types
            if left_type in ["Int", "Float"] and right_type in ["Int", "Float"]:
                # If either operand is Float, the result is Float
                if "Float" in [left_type, right_type]:
                    return "Float"
                return "Int"
            
            # Special case for string concatenation
            if node.op == "+" and "String" in [left_type, right_type]:
                # If either operand is a string, the result is a string
                return "String"
        
        elif node.op in ["==", "!=", "<", ">", "<=", ">="]:
            # Comparison operators always return Boolean
            return "Boolean"
        
        elif node.op in ["&&", "||"]:
            # Logical operators require Boolean operands and return Boolean
            context.add_constraint(left_type, "Boolean")
            context.add_constraint(right_type, "Boolean")
            return "Boolean"
        
        # If we can't determine the type, create a type variable
        result_type = context.create_type_var()
        return result_type
    
    def _infer_unary_op_type(self, node: UnaryOp, context: InferenceContext) -> str:
        """
        Infer the type of a unary operation.
        
        Args:
            node: The unary operation node
            context: The inference context
            
        Returns:
            The inferred type of the unary operation
        """
        operand_type = self._infer_node_type(node.operand, context)
        
        if node.op == "-":
            # Negation requires a numeric type and returns the same type
            if operand_type in ["Int", "Float"]:
                return operand_type
            
            # Add constraint that operand must be numeric
            context.add_constraint(operand_type, "Int")
            context.add_constraint(operand_type, "Float")
            
            # Create a type variable for the result
            result_type = context.create_type_var()
            return result_type
        
        elif node.op == "!":
            # Logical NOT requires a Boolean and returns Boolean
            context.add_constraint(operand_type, "Boolean")
            return "Boolean"
        
        # If we can't determine the type, create a type variable
        result_type = context.create_type_var()
        return result_type
    
    def _infer_assignment_type(self, node: Assignment, context: InferenceContext) -> str:
        """
        Infer the type of an assignment.
        
        Args:
            node: The assignment node
            context: The inference context
            
        Returns:
            The inferred type of the assignment
        """
        # Infer the type of the value
        value_type = self._infer_node_type(node.value, context)
        
        # Handle simple variable assignments
        if isinstance(node.target, Identifier):
            var_name = node.target.name
            var_type = context.get_var_type(var_name)
            
            if var_type:
                # If the variable already has a type, add a constraint
                context.add_constraint(value_type, var_type)
            else:
                # Otherwise, set the variable's type to the value's type
                context.set_var_type(var_name, value_type)
            
            return value_type
        
        # Handle property assignments (obj.prop = value)
        elif isinstance(node.target, PropertyAccess):
            # Infer the type of the object
            obj_type = self._infer_node_type(node.target.obj, context)
            
            # The property must have the same type as the value
            # This is a simplification; in reality, we would need
            # to check the property's declared type in the object's type
            
            return value_type
        
        # Handle index assignments (arr[index] = value)
        elif isinstance(node.target, IndexAccess):
            # Infer the type of the collection
            collection_type = self._infer_node_type(node.target.collection, context)
            
            # For lists, the element type should match the value type
            if collection_type.startswith("List["):
                # Extract the element type
                element_type = collection_type[5:-1]
                context.add_constraint(value_type, element_type)
            
            # For dictionaries, we would need to check key and value types
            # This is a simplification
            
            return value_type
        
        # If we can't determine the type, return the value's type
        return value_type
    
    def _infer_call_expr_type(self, node: CallExpr, context: InferenceContext) -> str:
        """
        Infer the type of a function call.
        
        Args:
            node: The function call node
            context: The inference context
            
        Returns:
            The inferred type of the function call
        """
        # Infer the type of the function
        func_type = self._infer_node_type(node.func, context)
        
        # Infer the types of the arguments
        arg_types = [self._infer_node_type(arg, context) for arg in node.args]
        
        # If the function type is a FunctionType, we can determine the return type
        func_type_obj = self.type_system.get_type(func_type)
        if func_type_obj and func_type_obj.is_function():
            func_type_obj = cast(FunctionType, func_type_obj)
            
            # Check if the argument types match the parameter types
            if len(arg_types) == len(func_type_obj.parameter_types):
                for i, arg_type in enumerate(arg_types):
                    param_type = str(func_type_obj.parameter_types[i])
                    context.add_constraint(arg_type, param_type)
            
            # Return the function's return type
            return str(func_type_obj.return_type)
        
        # If we can't determine the return type, create a type variable
        result_type = context.create_type_var()
        return result_type
    
    def _infer_if_expr_type(self, node: IfExpr, context: InferenceContext) -> str:
        """
        Infer the type of an if expression.
        
        Args:
            node: The if expression node
            context: The inference context
            
        Returns:
            The inferred type of the if expression
        """
        # The condition must be a Boolean
        cond_type = self._infer_node_type(node.condition, context)
        context.add_constraint(cond_type, "Boolean")
        
        # Infer the types of the then and else branches
        then_type = self._infer_node_type(node.then_branch, context)
        else_type = self._infer_node_type(node.else_branch, context) if node.else_branch else "Null"
        
        # The type of the if expression is the common type of the then and else branches
        common_type = self.type_system.common_type(then_type, else_type)
        if common_type:
            return common_type
        
        # If there's no common type, create a union type
        return f"{then_type} | {else_type}"
    
    def _infer_block_type(self, node: Block, context: InferenceContext) -> str:
        """
        Infer the type of a block.
        
        Args:
            node: The block node
            context: The inference context
            
        Returns:
            The inferred type of the block
        """
        # Infer the types of all statements in the block
        result_type = "Null"
        for stmt in node.statements:
            stmt_type = self._infer_node_type(stmt, context)
            
            # If the statement is a return statement, the block's type is the return value's type
            if isinstance(stmt, ReturnStmt):
                result_type = stmt_type
                break
        
        return result_type
    
    def _infer_function_decl_type(self, node: FunctionDecl, context: InferenceContext) -> str:
        """
        Infer the type of a function declaration.
        
        Args:
            node: The function declaration node
            context: The inference context
            
        Returns:
            The inferred type of the function
        """
        # Create a new context for the function body
        func_context = InferenceContext(self.type_system)
        func_context.var_types = context.var_types.copy()
        
        # Set types for parameters
        param_types = []
        for param in node.params:
            param_name = param.name
            param_type = param.type_name if param.type_name else context.create_type_var()
            func_context.set_var_type(param_name, param_type)
            param_types.append(param_type)
        
        # Infer the return type from the function body
        return_type = self._infer_node_type(node.body, func_context)
        
        # If the function has a declared return type, add a constraint
        if node.return_type:
            context.add_constraint(return_type, node.return_type)
            return_type = node.return_type
        
        # Create a function type
        function_type = self.type_system.create_function_type(param_types, return_type)
        if function_type:
            return str(function_type)
        
        # If we can't create a function type, create a type variable
        return context.create_type_var()
    
    def _infer_var_decl_type(self, node: VarDecl, context: InferenceContext) -> str:
        """
        Infer the type of a variable declaration.
        
        Args:
            node: The variable declaration node
            context: The inference context
            
        Returns:
            The inferred type of the variable
        """
        # Infer the type of the initializer, if any
        if node.initializer:
            init_type = self._infer_node_type(node.initializer, context)
            
            # If the variable has a declared type, add a constraint
            if node.type_name:
                context.add_constraint(init_type, node.type_name)
                var_type = node.type_name
            else:
                var_type = init_type
            
            # Set the variable's type
            context.set_var_type(node.name, var_type)
            return var_type
        
        # If there's no initializer, use the declared type or a type variable
        var_type = node.type_name if node.type_name else context.create_type_var()
        context.set_var_type(node.name, var_type)
        return var_type
    
    def _infer_return_stmt_type(self, node: ReturnStmt, context: InferenceContext) -> str:
        """
        Infer the type of a return statement.
        
        Args:
            node: The return statement node
            context: The inference context
            
        Returns:
            The inferred type of the return value
        """
        # If there's a return value, infer its type
        if node.value:
            return self._infer_node_type(node.value, context)
        
        # Otherwise, the return type is Null
        return "Null"
    
    def _infer_for_loop_type(self, node: ForLoop, context: InferenceContext) -> str:
        """
        Infer the type of a for loop.
        
        Args:
            node: The for loop node
            context: The inference context
            
        Returns:
            The inferred type of the for loop
        """
        # Infer the type of the iterable
        iterable_type = self._infer_node_type(node.iterable, context)
        
        # The iterable must be a List or a String
        if iterable_type.startswith("List["):
            # Extract the element type
            element_type = iterable_type[5:-1]
            context.set_var_type(node.var_name, element_type)
        elif iterable_type == "String":
            # For strings, the elements are characters (strings of length 1)
            context.set_var_type(node.var_name, "String")
        else:
            # For other types, we can't determine the element type
            element_type = context.create_type_var()
            context.set_var_type(node.var_name, element_type)
        
        # Infer the type of the body
        body_type = self._infer_node_type(node.body, context)
        
        # For loops always return Null
        return "Null"
    
    def _infer_while_loop_type(self, node: WhileLoop, context: InferenceContext) -> str:
        """
        Infer the type of a while loop.
        
        Args:
            node: The while loop node
            context: The inference context
            
        Returns:
            The inferred type of the while loop
        """
        # The condition must be a Boolean
        cond_type = self._infer_node_type(node.condition, context)
        context.add_constraint(cond_type, "Boolean")
        
        # Infer the type of the body
        body_type = self._infer_node_type(node.body, context)
        
        # While loops always return Null
        return "Null"
    
    def _infer_method_call_type(self, node: MethodCall, context: InferenceContext) -> str:
        """
        Infer the type of a method call.
        
        Args:
            node: The method call node
            context: The inference context
            
        Returns:
            The inferred type of the method call
        """
        # Infer the type of the object
        obj_type = self._infer_node_type(node.obj, context)
        
        # Infer the types of the arguments
        arg_types = [self._infer_node_type(arg, context) for arg in node.args]
        
        # Get the object's type
        obj_type_obj = self.type_system.get_type(obj_type)
        if obj_type_obj and hasattr(obj_type_obj, "get_method_type"):
            # Get the method's type
            method_type = obj_type_obj.get_method_type(node.method)
            if method_type:
                # Check if the argument types match the parameter types
                if len(arg_types) == len(method_type.parameter_types):
                    for i, arg_type in enumerate(arg_types):
                        param_type = str(method_type.parameter_types[i])
                        context.add_constraint(arg_type, param_type)
                
                # Return the method's return type
                return str(method_type.return_type)
        
        # If we can't determine the return type, create a type variable
        result_type = context.create_type_var()
        return result_type
    
    def _infer_property_access_type(self, node: PropertyAccess, context: InferenceContext) -> str:
        """
        Infer the type of a property access.
        
        Args:
            node: The property access node
            context: The inference context
            
        Returns:
            The inferred type of the property
        """
        # Infer the type of the object
        obj_type = self._infer_node_type(node.obj, context)
        
        # Get the object's type
        obj_type_obj = self.type_system.get_type(obj_type)
        if obj_type_obj and hasattr(obj_type_obj, "get_field_type"):
            # Get the field's type
            field_type = obj_type_obj.get_field_type(node.prop)
            if field_type:
                return str(field_type)
        
        # If we can't determine the property's type, create a type variable
        result_type = context.create_type_var()
        return result_type
    
    def _infer_list_expr_type(self, node: ListExpr, context: InferenceContext) -> str:
        """
        Infer the type of a list expression.
        
        Args:
            node: The list expression node
            context: The inference context
            
        Returns:
            The inferred type of the list
        """
        # If the list is empty, create a type variable for the element type
        if not node.elements:
            element_type = context.create_type_var()
            return f"List[{element_type}]"
        
        # Infer the types of all elements
        element_types = [self._infer_node_type(elem, context) for elem in node.elements]
        
        # Find a common type for all elements
        common_type = element_types[0]
        for elem_type in element_types[1:]:
            common_type = self.type_system.common_type(common_type, elem_type)
            if not common_type:
                # If there's no common type, create a union type
                common_type = f"{common_type} | {elem_type}"
        
        return f"List[{common_type}]"
    
    def _infer_dictionary_expr_type(self, node: DictionaryExpr, context: InferenceContext) -> str:
        """
        Infer the type of a dictionary expression.
        
        Args:
            node: The dictionary expression node
            context: The inference context
            
        Returns:
            The inferred type of the dictionary
        """
        # If the dictionary is empty, create type variables for key and value types
        if not node.entries:
            key_type = context.create_type_var()
            value_type = context.create_type_var()
            return f"Dictionary[{key_type}, {value_type}]"
        
        # Infer the types of all keys and values
        key_types = [self._infer_node_type(entry[0], context) for entry in node.entries]
        value_types = [self._infer_node_type(entry[1], context) for entry in node.entries]
        
        # Find common types for keys and values
        common_key_type = key_types[0]
        for key_type in key_types[1:]:
            common_key_type = self.type_system.common_type(common_key_type, key_type)
            if not common_key_type:
                # If there's no common type, create a union type
                common_key_type = f"{common_key_type} | {key_type}"
        
        common_value_type = value_types[0]
        for value_type in value_types[1:]:
            common_value_type = self.type_system.common_type(common_value_type, value_type)
            if not common_value_type:
                # If there's no common type, create a union type
                common_value_type = f"{common_value_type} | {value_type}"
        
        return f"Dictionary[{common_key_type}, {common_value_type}]"
    
    def _infer_index_access_type(self, node: IndexAccess, context: InferenceContext) -> str:
        """
        Infer the type of an index access.
        
        Args:
            node: The index access node
            context: The inference context
            
        Returns:
            The inferred type of the index access
        """
        # Infer the type of the collection
        collection_type = self._infer_node_type(node.collection, context)
        
        # Infer the type of the index
        index_type = self._infer_node_type(node.index, context)
        
        # For lists, the index must be an Int
        if collection_type.startswith("List["):
            context.add_constraint(index_type, "Int")
            
            # The element type is everything between List[ and ]
            element_type = collection_type[5:-1]
            return element_type
        
        # For dictionaries, the index must match the key type
        elif collection_type.startswith("Dictionary["):
            # Extract key and value types
            key_value_type = collection_type[11:-1]
            key_type, value_type = key_value_type.split(",")
            key_type = key_type.strip()
            value_type = value_type.strip()
            
            context.add_constraint(index_type, key_type)
            return value_type
        
        # For strings, the index must be an Int and the element type is String
        elif collection_type == "String":
            context.add_constraint(index_type, "Int")
            return "String"
        
        # If we can't determine the element type, create a type variable
        result_type = context.create_type_var()
        return result_type
    
    def _solve_constraints(self, context: InferenceContext) -> None:
        """
        Solve the constraints in the context.
        
        This method attempts to find assignments to type variables
        that satisfy all the constraints.
        
        Args:
            context: The inference context
        """
        # Keep solving until we can't make any more progress
        while True:
            progress = False
            
            # Process each constraint
            for from_type, to_type in context.constraints:
                # Resolve type variables
                from_type_resolved = context.resolve_type_var(from_type)
                to_type_resolved = context.resolve_type_var(to_type)
                
                # Skip if both types are the same
                if from_type_resolved == to_type_resolved:
                    continue
                
                # If both are type variables, assign the more specific one to the less specific one
                if from_type in context.type_vars and to_type in context.type_vars:
                    # For now, just assign from_type to to_type
                    context.type_vars[to_type] = from_type
                    progress = True
                
                # If from_type is a type variable and to_type is concrete, assign to_type to from_type
                elif from_type in context.type_vars and to_type not in context.type_vars:
                    context.type_vars[from_type] = to_type
                    progress = True
                
                # If to_type is a type variable and from_type is concrete, assign from_type to to_type
                elif to_type in context.type_vars and from_type not in context.type_vars:
                    context.type_vars[to_type] = from_type
                    progress = True
                
                # If neither is a type variable, check if they're compatible
                elif not self.type_system.is_assignable(from_type_resolved, to_type_resolved):
                    # If they're not compatible, try to find a common type
                    common_type = self.type_system.common_type(from_type_resolved, to_type_resolved)
                    if common_type:
                        # Assign the common type to both type variables
                        if from_type in context.type_vars:
                            context.type_vars[from_type] = common_type
                            progress = True
                        
                        if to_type in context.type_vars:
                            context.type_vars[to_type] = common_type
                            progress = True
            
            # If we didn't make any progress, we're done
            if not progress:
                break 