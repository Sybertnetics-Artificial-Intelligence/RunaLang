#!/usr/bin/env python3
"""
Unit tests for C++ ↔ Runa Converter

Tests bidirectional conversion between C++ AST and Runa AST,
focusing on C++ features like templates, memory management, and low-level constructs.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.cpp.cpp_converter import CppToRunaConverter, RunaToCppConverter
from runa.languages.tier1.cpp.cpp_ast import *
from runa.core.runa_ast import *


class TestCppToRunaConverter(unittest.TestCase):
    """Test C++ AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = CppToRunaConverter()
    
    def test_variable_declaration(self):
        """Test conversion of variable declarations."""
        # C++: int x = 42;
        cpp_ast = CppTranslationUnit([
            CppDeclarationStatement(
                declaration=CppVariableDeclaration(
                    type=CppBuiltinType('int'),
                    declarators=[
                        CppDeclarator(
                            name='x',
                            initializer=CppIntegerLiteral(value=42)
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.type_annotation, TypeReference)
        self.assertEqual(stmt.type_annotation.name, 'int')
        self.assertIsInstance(stmt.value, NumericLiteral)
        self.assertEqual(stmt.value.value, 42)
    
    def test_pointer_declaration(self):
        """Test conversion of pointer declarations."""
        # C++: int* ptr = nullptr;
        cpp_ast = CppTranslationUnit([
            CppDeclarationStatement(
                declaration=CppVariableDeclaration(
                    type=CppPointerType(
                        pointee_type=CppBuiltinType('int')
                    ),
                    declarators=[
                        CppDeclarator(
                            name='ptr',
                            initializer=CppNullptrLiteral()
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'ptr')
        self.assertIsInstance(stmt.type_annotation, PointerType)
        self.assertEqual(stmt.type_annotation.pointee_type.name, 'int')
    
    def test_reference_declaration(self):
        """Test conversion of reference declarations."""
        # C++: int& ref = x;
        cpp_ast = CppTranslationUnit([
            CppDeclarationStatement(
                declaration=CppVariableDeclaration(
                    type=CppReferenceType(
                        referenced_type=CppBuiltinType('int')
                    ),
                    declarators=[
                        CppDeclarator(
                            name='ref',
                            initializer=CppIdentifier('x')
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'ref')
        self.assertIsInstance(stmt.type_annotation, ReferenceType)
        self.assertEqual(stmt.type_annotation.referenced_type.name, 'int')
    
    def test_function_declaration(self):
        """Test conversion of function declarations."""
        # C++: int add(int a, int b) { return a + b; }
        cpp_ast = CppTranslationUnit([
            CppFunctionDefinition(
                return_type=CppBuiltinType('int'),
                name='add',
                parameters=[
                    CppParameter(
                        type=CppBuiltinType('int'),
                        name='a'
                    ),
                    CppParameter(
                        type=CppBuiltinType('int'),
                        name='b'
                    )
                ],
                body=CppCompoundStatement([
                    CppReturnStatement(
                        expression=CppBinaryOperator(
                            left=CppIdentifier('a'),
                            operator='+',
                            right=CppIdentifier('b')
                        )
                    )
                ])
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, 'add')
        self.assertEqual(len(stmt.parameters), 2)
        self.assertEqual(stmt.parameters[0].name, 'a')
        self.assertEqual(stmt.parameters[1].name, 'b')
        self.assertEqual(stmt.return_type.name, 'int')
    
    def test_class_declaration(self):
        """Test conversion of class declarations."""
        # C++: class Person { private: std::string name; public: void setName(const std::string& n); };
        cpp_ast = CppTranslationUnit([
            CppClassDefinition(
                name='Person',
                members=[
                    CppAccessSpecifier(access='private'),
                    CppMemberVariable(
                        type=CppQualifiedType(
                            qualifier='std',
                            type=CppIdentifier('string')
                        ),
                        name='name'
                    ),
                    CppAccessSpecifier(access='public'),
                    CppMemberFunction(
                        return_type=CppBuiltinType('void'),
                        name='setName',
                        parameters=[
                            CppParameter(
                                type=CppReferenceType(
                                    referenced_type=CppConstType(
                                        type=CppQualifiedType(
                                            qualifier='std',
                                            type=CppIdentifier('string')
                                        )
                                    )
                                ),
                                name='n'
                            )
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Person')
        
        # Check member variable
        name_field = next(p for p in stmt.properties if p.name == 'name')
        self.assertEqual(name_field.access_modifier, 'private')
        
        # Check member function
        set_name_method = next(m for m in stmt.methods if m.name == 'setName')
        self.assertEqual(set_name_method.access_modifier, 'public')
    
    def test_template_function(self):
        """Test conversion of template functions."""
        # C++: template<typename T> T identity(T value) { return value; }
        cpp_ast = CppTranslationUnit([
            CppTemplateDeclaration(
                template_parameters=[
                    CppTemplateTypeParameter(name='T')
                ],
                declaration=CppFunctionDefinition(
                    return_type=CppTemplateParameter('T'),
                    name='identity',
                    parameters=[
                        CppParameter(
                            type=CppTemplateParameter('T'),
                            name='value'
                        )
                    ],
                    body=CppCompoundStatement([
                        CppReturnStatement(
                            expression=CppIdentifier('value')
                        )
                    ])
                )
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, FunctionDeclaration)
        self.assertEqual(stmt.name, 'identity')
        self.assertEqual(len(stmt.type_parameters), 1)
        self.assertEqual(stmt.type_parameters[0].name, 'T')
    
    def test_template_class(self):
        """Test conversion of template classes."""
        # C++: template<typename T> class Container { T data; };
        cpp_ast = CppTranslationUnit([
            CppTemplateDeclaration(
                template_parameters=[
                    CppTemplateTypeParameter(name='T')
                ],
                declaration=CppClassDefinition(
                    name='Container',
                    members=[
                        CppMemberVariable(
                            type=CppTemplateParameter('T'),
                            name='data'
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Container')
        self.assertEqual(len(stmt.type_parameters), 1)
        self.assertEqual(stmt.type_parameters[0].name, 'T')
    
    def test_constructor_destructor(self):
        """Test conversion of constructors and destructors."""
        # C++: class Resource { public: Resource(); ~Resource(); };
        cpp_ast = CppTranslationUnit([
            CppClassDefinition(
                name='Resource',
                members=[
                    CppAccessSpecifier(access='public'),
                    CppConstructor(
                        name='Resource',
                        parameters=[]
                    ),
                    CppDestructor(
                        name='~Resource'
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        
        # Check constructor
        self.assertIsNotNone(stmt.constructor)
        self.assertEqual(stmt.constructor.name, 'Resource')
        
        # Check destructor
        self.assertIsNotNone(stmt.destructor)
        self.assertEqual(stmt.destructor.name, '~Resource')
    
    def test_inheritance(self):
        """Test conversion of class inheritance."""
        # C++: class Dog : public Animal { };
        cpp_ast = CppTranslationUnit([
            CppClassDefinition(
                name='Dog',
                base_classes=[
                    CppBaseClass(
                        access='public',
                        name='Animal'
                    )
                ],
                members=[]
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Dog')
        self.assertIsNotNone(stmt.base_class)
        self.assertEqual(stmt.base_class.name, 'Animal')
    
    def test_operator_overloading(self):
        """Test conversion of operator overloading."""
        # C++: Vector operator+(const Vector& other) const { }
        cpp_ast = CppTranslationUnit([
            CppClassDefinition(
                name='Vector',
                members=[
                    CppOperatorOverload(
                        operator='+',
                        return_type=CppIdentifier('Vector'),
                        parameters=[
                            CppParameter(
                                type=CppReferenceType(
                                    referenced_type=CppConstType(
                                        type=CppIdentifier('Vector')
                                    )
                                ),
                                name='other'
                            )
                        ],
                        is_const=True,
                        body=CppCompoundStatement([])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        class_stmt = runa_program.statements[0]
        operator_method = next(m for m in class_stmt.methods if m.is_operator_overload)
        self.assertEqual(operator_method.operator_symbol, '+')
        self.assertTrue(operator_method.is_const)
    
    def test_namespace(self):
        """Test conversion of namespaces."""
        # C++: namespace math { int add(int a, int b); }
        cpp_ast = CppTranslationUnit([
            CppNamespaceDefinition(
                name='math',
                declarations=[
                    CppFunctionDeclaration(
                        return_type=CppBuiltinType('int'),
                        name='add',
                        parameters=[
                            CppParameter(
                                type=CppBuiltinType('int'),
                                name='a'
                            ),
                            CppParameter(
                                type=CppBuiltinType('int'),
                                name='b'
                            )
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, NamespaceDeclaration)
        self.assertEqual(stmt.name, 'math')
        self.assertEqual(len(stmt.members), 1)
    
    def test_preprocessor_includes(self):
        """Test conversion of preprocessor includes."""
        # C++: #include <iostream>
        cpp_ast = CppTranslationUnit([
            CppIncludeDirective(
                header='iostream',
                is_system_header=True
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        # Includes should be converted to imports
        import_stmts = [s for s in runa_program.statements if isinstance(s, ImportStatement)]
        self.assertEqual(len(import_stmts), 1)
        self.assertEqual(import_stmts[0].module, 'iostream')
        self.assertTrue(import_stmts[0].is_system_import)
    
    def test_memory_management(self):
        """Test conversion of memory management constructs."""
        # C++: int* ptr = new int(42); delete ptr;
        cpp_ast = CppTranslationUnit([
            CppDeclarationStatement(
                declaration=CppVariableDeclaration(
                    type=CppPointerType(
                        pointee_type=CppBuiltinType('int')
                    ),
                    declarators=[
                        CppDeclarator(
                            name='ptr',
                            initializer=CppNewExpression(
                                type=CppBuiltinType('int'),
                                arguments=[CppIntegerLiteral(value=42)]
                            )
                        )
                    ]
                )
            ),
            CppExpressionStatement(
                expression=CppDeleteExpression(
                    expression=CppIdentifier('ptr')
                )
            )
        ])
        
        runa_program = self.converter.convert(cpp_ast)
        
        # Check new expression conversion
        var_stmt = runa_program.statements[0]
        self.assertIsInstance(var_stmt.value, NewExpression)
        
        # Check delete expression conversion
        delete_stmt = runa_program.statements[1]
        self.assertIsInstance(delete_stmt.expression, DeleteExpression)


class TestRunaToCppConverter(unittest.TestCase):
    """Test Runa AST to C++ AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToCppConverter()
    
    def test_variable_declaration_conversion(self):
        """Test conversion of variable declarations."""
        # Runa: Let x as Integer be 42
        runa_program = Program([
            VariableDeclaration(
                name='x',
                type_annotation=TypeReference(name='Integer'),
                value=NumericLiteral(value=42)
            )
        ])
        
        cpp_unit = self.converter.convert(runa_program)
        
        self.assertIsInstance(cpp_unit, CppTranslationUnit)
        stmt = cpp_unit.declarations[0]
        self.assertIsInstance(stmt, CppDeclarationStatement)
        var_decl = stmt.declaration
        self.assertEqual(var_decl.type.name, 'int')  # Integer -> int mapping
        self.assertEqual(var_decl.declarators[0].name, 'x')
    
    def test_function_conversion(self):
        """Test conversion of function declarations."""
        # Runa: Define add with a as Integer and b as Integer returning Integer
        runa_program = Program([
            FunctionDeclaration(
                name='add',
                parameters=[
                    Parameter(
                        name='a',
                        type_annotation=TypeReference(name='Integer')
                    ),
                    Parameter(
                        name='b',
                        type_annotation=TypeReference(name='Integer')
                    )
                ],
                return_type=TypeReference(name='Integer'),
                body=[
                    ReturnStatement(
                        value=BinaryOperation(
                            left=Identifier(name='a'),
                            operator='plus',
                            right=Identifier(name='b')
                        )
                    )
                ]
            )
        ])
        
        cpp_unit = self.converter.convert(runa_program)
        
        func_def = cpp_unit.declarations[0]
        self.assertIsInstance(func_def, CppFunctionDefinition)
        self.assertEqual(func_def.name, 'add')
        self.assertEqual(len(func_def.parameters), 2)
        self.assertEqual(func_def.return_type.name, 'int')
    
    def test_class_conversion(self):
        """Test conversion of class declarations."""
        # Runa: Define type Person with private name as String
        runa_program = Program([
            ClassDeclaration(
                name='Person',
                properties=[
                    PropertyDeclaration(
                        name='name',
                        type_annotation=TypeReference(name='String'),
                        access_modifier='private'
                    )
                ]
            )
        ])
        
        cpp_unit = self.converter.convert(runa_program)
        
        class_def = cpp_unit.declarations[0]
        self.assertIsInstance(class_def, CppClassDefinition)
        self.assertEqual(class_def.name, 'Person')
        
        # Check private access specifier and member
        access_spec = class_def.members[0]
        self.assertIsInstance(access_spec, CppAccessSpecifier)
        self.assertEqual(access_spec.access, 'private')
    
    def test_template_conversion(self):
        """Test conversion of generic types to templates."""
        # Runa: Define generic type Container with type T
        runa_program = Program([
            ClassDeclaration(
                name='Container',
                type_parameters=[TypeParameter(name='T')],
                properties=[
                    PropertyDeclaration(
                        name='data',
                        type_annotation=TypeReference(name='T')
                    )
                ]
            )
        ])
        
        cpp_unit = self.converter.convert(runa_program)
        
        template_decl = cpp_unit.declarations[0]
        self.assertIsInstance(template_decl, CppTemplateDeclaration)
        self.assertEqual(len(template_decl.template_parameters), 1)
        self.assertEqual(template_decl.template_parameters[0].name, 'T')
    
    def test_pointer_conversion(self):
        """Test conversion of pointer types."""
        # Runa: Let ptr as Pointer to Integer be null
        runa_program = Program([
            VariableDeclaration(
                name='ptr',
                type_annotation=PointerType(
                    pointee_type=TypeReference(name='Integer')
                ),
                value=NullLiteral()
            )
        ])
        
        cpp_unit = self.converter.convert(runa_program)
        
        var_stmt = cpp_unit.declarations[0]
        var_decl = var_stmt.declaration
        self.assertIsInstance(var_decl.type, CppPointerType)
        self.assertEqual(var_decl.type.pointee_type.name, 'int')
    
    def test_namespace_conversion(self):
        """Test conversion of namespace declarations."""
        # Runa: Define namespace Math with add function
        runa_program = Program([
            NamespaceDeclaration(
                name='Math',
                members=[
                    FunctionDeclaration(
                        name='add',
                        parameters=[
                            Parameter(name='a', type_annotation=TypeReference(name='Integer')),
                            Parameter(name='b', type_annotation=TypeReference(name='Integer'))
                        ],
                        return_type=TypeReference(name='Integer')
                    )
                ]
            )
        ])
        
        cpp_unit = self.converter.convert(runa_program)
        
        namespace_def = cpp_unit.declarations[0]
        self.assertIsInstance(namespace_def, CppNamespaceDefinition)
        self.assertEqual(namespace_def.name, 'Math')
        self.assertEqual(len(namespace_def.declarations), 1)


class TestCppSpecificFeatures(unittest.TestCase):
    """Test C++-specific language features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cpp_to_runa = CppToRunaConverter()
        self.runa_to_cpp = RunaToCppConverter()
    
    def test_const_correctness(self):
        """Test handling of const correctness."""
        # C++: const int getValue() const { return value; }
        cpp_ast = CppTranslationUnit([
            CppClassDefinition(
                name='MyClass',
                members=[
                    CppMemberFunction(
                        return_type=CppConstType(
                            type=CppBuiltinType('int')
                        ),
                        name='getValue',
                        parameters=[],
                        is_const=True,
                        body=CppCompoundStatement([
                            CppReturnStatement(
                                expression=CppIdentifier('value')
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.cpp_to_runa.convert(cpp_ast)
        
        # Const methods should be marked appropriately
        class_stmt = runa_program.statements[0]
        method = class_stmt.methods[0]
        self.assertTrue(method.is_const)
    
    def test_rvalue_references(self):
        """Test handling of rvalue references (C++11)."""
        # C++: void process(std::string&& str) { }
        cpp_ast = CppTranslationUnit([
            CppFunctionDefinition(
                return_type=CppBuiltinType('void'),
                name='process',
                parameters=[
                    CppParameter(
                        type=CppRValueReferenceType(
                            referenced_type=CppQualifiedType(
                                qualifier='std',
                                type=CppIdentifier('string')
                            )
                        ),
                        name='str'
                    )
                ],
                body=CppCompoundStatement([])
            )
        ])
        
        runa_program = self.cpp_to_runa.convert(cpp_ast)
        
        # Rvalue references should be handled appropriately
        func_stmt = runa_program.statements[0]
        param = func_stmt.parameters[0]
        self.assertIsInstance(param.type_annotation, RValueReferenceType)
    
    def test_smart_pointers(self):
        """Test handling of smart pointers."""
        # C++: std::unique_ptr<int> ptr = std::make_unique<int>(42);
        cpp_ast = CppTranslationUnit([
            CppDeclarationStatement(
                declaration=CppVariableDeclaration(
                    type=CppTemplateInstantiation(
                        template=CppQualifiedType(
                            qualifier='std',
                            type=CppIdentifier('unique_ptr')
                        ),
                        arguments=[CppBuiltinType('int')]
                    ),
                    declarators=[
                        CppDeclarator(
                            name='ptr',
                            initializer=CppFunctionCall(
                                function=CppQualifiedType(
                                    qualifier='std',
                                    type=CppIdentifier('make_unique')
                                ),
                                template_arguments=[CppBuiltinType('int')],
                                arguments=[CppIntegerLiteral(value=42)]
                            )
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.cpp_to_runa.convert(cpp_ast)
        
        # Smart pointers should be converted to managed pointers
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt.type_annotation, SmartPointerType)
        self.assertEqual(stmt.type_annotation.pointer_kind, 'unique')
    
    def test_lambda_expressions(self):
        """Test handling of lambda expressions (C++11)."""
        # C++: auto lambda = [](int x) { return x * 2; };
        cpp_ast = CppTranslationUnit([
            CppDeclarationStatement(
                declaration=CppVariableDeclaration(
                    type=CppAutoType(),
                    declarators=[
                        CppDeclarator(
                            name='lambda',
                            initializer=CppLambdaExpression(
                                capture_list=[],
                                parameters=[
                                    CppParameter(
                                        type=CppBuiltinType('int'),
                                        name='x'
                                    )
                                ],
                                body=CppCompoundStatement([
                                    CppReturnStatement(
                                        expression=CppBinaryOperator(
                                            left=CppIdentifier('x'),
                                            operator='*',
                                            right=CppIntegerLiteral(value=2)
                                        )
                                    )
                                ])
                            )
                        )
                    ]
                )
            )
        ])
        
        runa_program = self.cpp_to_runa.convert(cpp_ast)
        
        # Lambda should be converted to function expression
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt.value, FunctionExpression)


class TestCppRoundTrip(unittest.TestCase):
    """Test round-trip conversion for C++-specific patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cpp_to_runa = CppToRunaConverter()
        self.runa_to_cpp = RunaToCppConverter()
    
    def test_roundtrip_template_class(self):
        """Test round-trip conversion of template classes."""
        original_cpp = CppTranslationUnit([
            CppTemplateDeclaration(
                template_parameters=[
                    CppTemplateTypeParameter(name='T'),
                    CppTemplateValueParameter(
                        type=CppBuiltinType('int'),
                        name='N'
                    )
                ],
                declaration=CppClassDefinition(
                    name='Array',
                    members=[
                        CppMemberVariable(
                            type=CppArrayType(
                                element_type=CppTemplateParameter('T'),
                                size=CppTemplateParameter('N')
                            ),
                            name='data'
                        )
                    ]
                )
            )
        ])
        
        # Round-trip conversion
        runa_program = self.cpp_to_runa.convert(original_cpp)
        converted_cpp = self.runa_to_cpp.convert(runa_program)
        
        # Verify template structure is preserved
        template_decl = converted_cpp.declarations[0]
        self.assertIsInstance(template_decl, CppTemplateDeclaration)
        self.assertEqual(len(template_decl.template_parameters), 2)
    
    def test_memory_management_preservation(self):
        """Test that C++ memory management patterns are preserved."""
        original_cpp = CppTranslationUnit([
            CppFunctionDefinition(
                return_type=CppBuiltinType('void'),
                name='processData',
                parameters=[],
                body=CppCompoundStatement([
                    CppDeclarationStatement(
                        declaration=CppVariableDeclaration(
                            type=CppPointerType(
                                pointee_type=CppBuiltinType('int')
                            ),
                            declarators=[
                                CppDeclarator(
                                    name='data',
                                    initializer=CppNewExpression(
                                        type=CppArrayType(
                                            element_type=CppBuiltinType('int')
                                        ),
                                        arguments=[CppIntegerLiteral(value=100)]
                                    )
                                )
                            ]
                        )
                    ),
                    CppExpressionStatement(
                        expression=CppDeleteExpression(
                            expression=CppIdentifier('data'),
                            is_array=True
                        )
                    )
                ])
            )
        ])
        
        # Round-trip conversion
        runa_program = self.cpp_to_runa.convert(original_cpp)
        converted_cpp = self.runa_to_cpp.convert(runa_program)
        
        # Verify memory management constructs are preserved
        func_def = converted_cpp.declarations[0]
        statements = func_def.body.statements
        
        # Check new[] expression
        var_stmt = statements[0]
        new_expr = var_stmt.declaration.declarators[0].initializer
        self.assertIsInstance(new_expr, CppNewExpression)
        
        # Check delete[] expression
        delete_stmt = statements[1]
        delete_expr = delete_stmt.expression
        self.assertIsInstance(delete_expr, CppDeleteExpression)
        self.assertTrue(delete_expr.is_array)


if __name__ == '__main__':
    unittest.main()
