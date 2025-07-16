#!/usr/bin/env python3
"""
Unit tests for Java ↔ Runa Converter

Tests bidirectional conversion between Java AST and Runa AST,
focusing on Java's static typing, object-oriented features, and JVM semantics.
"""

import unittest
from unittest.mock import Mock, patch
from typing import List, Dict, Any
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../src'))

from runa.languages.tier1.java.java_converter import JavaToRunaConverter, RunaToJavaConverter
from runa.languages.tier1.java.java_ast import *
from runa.core.runa_ast import *


class TestJavaToRunaConverter(unittest.TestCase):
    """Test Java AST to Runa AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = JavaToRunaConverter()
    
    def test_variable_declaration(self):
        """Test conversion of variable declarations."""
        # Java: int x = 42;
        java_ast = JavaCompilationUnit([
            JavaVariableDeclaration(
                type=JavaPrimitiveType('int'),
                declarators=[
                    JavaVariableDeclarator(
                        name='x',
                        initializer=JavaIntegerLiteral(value=42)
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        self.assertIsInstance(runa_program, Program)
        self.assertEqual(len(runa_program.statements), 1)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertEqual(stmt.name, 'x')
        self.assertIsInstance(stmt.type_annotation, TypeReference)
        self.assertEqual(stmt.type_annotation.name, 'int')
        self.assertIsInstance(stmt.value, NumericLiteral)
        self.assertEqual(stmt.value.value, 42)
    
    def test_method_declaration(self):
        """Test conversion of method declarations."""
        # Java: public int add(int a, int b) { return a + b; }
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                name='TestClass',
                members=[
                    JavaMethodDeclaration(
                        modifiers=['public'],
                        return_type=JavaPrimitiveType('int'),
                        name='add',
                        parameters=[
                            JavaParameter(
                                type=JavaPrimitiveType('int'),
                                name='a'
                            ),
                            JavaParameter(
                                type=JavaPrimitiveType('int'),
                                name='b'
                            )
                        ],
                        body=JavaBlock([
                            JavaReturnStatement(
                                expression=JavaBinaryExpression(
                                    left=JavaIdentifier('a'),
                                    operator='+',
                                    right=JavaIdentifier('b')
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        # Find the method within the class
        class_stmt = runa_program.statements[0]
        self.assertIsInstance(class_stmt, ClassDeclaration)
        
        method = class_stmt.methods[0]
        self.assertIsInstance(method, FunctionDeclaration)
        self.assertEqual(method.name, 'add')
        self.assertEqual(len(method.parameters), 2)
        self.assertEqual(method.access_modifier, 'public')
    
    def test_class_declaration(self):
        """Test conversion of class declarations."""
        # Java: public class Person { private String name; }
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                modifiers=['public'],
                name='Person',
                members=[
                    JavaFieldDeclaration(
                        modifiers=['private'],
                        type=JavaReferenceType('String'),
                        declarators=[
                            JavaVariableDeclarator(name='name')
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Person')
        self.assertEqual(stmt.access_modifier, 'public')
        
        # Check field
        field = stmt.properties[0]
        self.assertEqual(field.name, 'name')
        self.assertEqual(field.access_modifier, 'private')
        self.assertEqual(field.type_annotation.name, 'String')
    
    def test_inheritance(self):
        """Test conversion of class inheritance."""
        # Java: public class Dog extends Animal implements Pet
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                modifiers=['public'],
                name='Dog',
                extends=JavaReferenceType('Animal'),
                implements=[JavaReferenceType('Pet')],
                members=[]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Dog')
        self.assertIsNotNone(stmt.base_class)
        self.assertEqual(stmt.base_class.name, 'Animal')
        self.assertEqual(len(stmt.interfaces), 1)
        self.assertEqual(stmt.interfaces[0].name, 'Pet')
    
    def test_generic_class(self):
        """Test conversion of generic classes."""
        # Java: public class Container<T> { private T value; }
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                modifiers=['public'],
                name='Container',
                type_parameters=[
                    JavaTypeParameter(name='T')
                ],
                members=[
                    JavaFieldDeclaration(
                        modifiers=['private'],
                        type=JavaTypeVariable('T'),
                        declarators=[
                            JavaVariableDeclarator(name='value')
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, ClassDeclaration)
        self.assertEqual(stmt.name, 'Container')
        self.assertEqual(len(stmt.type_parameters), 1)
        self.assertEqual(stmt.type_parameters[0].name, 'T')
    
    def test_interface_declaration(self):
        """Test conversion of interface declarations."""
        # Java: public interface Drawable { void draw(); }
        java_ast = JavaCompilationUnit([
            JavaInterfaceDeclaration(
                modifiers=['public'],
                name='Drawable',
                members=[
                    JavaMethodDeclaration(
                        modifiers=['public', 'abstract'],
                        return_type=JavaVoidType(),
                        name='draw',
                        parameters=[]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, InterfaceDeclaration)
        self.assertEqual(stmt.name, 'Drawable')
        self.assertEqual(len(stmt.methods), 1)
        
        method = stmt.methods[0]
        self.assertEqual(method.name, 'draw')
        self.assertTrue(method.is_abstract)
    
    def test_array_types(self):
        """Test conversion of array types."""
        # Java: int[] numbers = new int[10];
        java_ast = JavaCompilationUnit([
            JavaVariableDeclaration(
                type=JavaArrayType(
                    element_type=JavaPrimitiveType('int')
                ),
                declarators=[
                    JavaVariableDeclarator(
                        name='numbers',
                        initializer=JavaArrayCreationExpression(
                            type=JavaPrimitiveType('int'),
                            dimensions=[JavaIntegerLiteral(value=10)]
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.type_annotation, ArrayType)
        self.assertEqual(stmt.type_annotation.element_type.name, 'int')
    
    def test_exception_handling(self):
        """Test conversion of try-catch blocks."""
        # Java: try { risky(); } catch (IOException e) { handle(e); }
        java_ast = JavaCompilationUnit([
            JavaTryStatement(
                try_block=JavaBlock([
                    JavaExpressionStatement(
                        expression=JavaMethodInvocation(
                            method='risky',
                            arguments=[]
                        )
                    )
                ]),
                catch_clauses=[
                    JavaCatchClause(
                        parameter=JavaParameter(
                            type=JavaReferenceType('IOException'),
                            name='e'
                        ),
                        block=JavaBlock([
                            JavaExpressionStatement(
                                expression=JavaMethodInvocation(
                                    method='handle',
                                    arguments=[JavaIdentifier('e')]
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, TryStatement)
        self.assertEqual(len(stmt.handlers), 1)
        
        handler = stmt.handlers[0]
        self.assertEqual(handler.exception_type.name, 'IOException')
        self.assertEqual(handler.variable_name, 'e')
    
    def test_static_members(self):
        """Test conversion of static members."""
        # Java: public static final String CONSTANT = "value";
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                name='Constants',
                members=[
                    JavaFieldDeclaration(
                        modifiers=['public', 'static', 'final'],
                        type=JavaReferenceType('String'),
                        declarators=[
                            JavaVariableDeclarator(
                                name='CONSTANT',
                                initializer=JavaStringLiteral(value="value")
                            )
                        ]
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        class_stmt = runa_program.statements[0]
        field = class_stmt.properties[0]
        self.assertTrue(field.is_static)
        self.assertTrue(field.is_final)
        self.assertEqual(field.access_modifier, 'public')
    
    def test_constructor(self):
        """Test conversion of constructors."""
        # Java: public Person(String name) { this.name = name; }
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                name='Person',
                members=[
                    JavaConstructorDeclaration(
                        modifiers=['public'],
                        name='Person',
                        parameters=[
                            JavaParameter(
                                type=JavaReferenceType('String'),
                                name='name'
                            )
                        ],
                        body=JavaBlock([
                            JavaExpressionStatement(
                                expression=JavaAssignmentExpression(
                                    left=JavaFieldAccess(
                                        expression=JavaThisExpression(),
                                        field='name'
                                    ),
                                    operator='=',
                                    right=JavaIdentifier('name')
                                )
                            )
                        ])
                    )
                ]
            )
        ])
        
        runa_program = self.converter.convert(java_ast)
        
        class_stmt = runa_program.statements[0]
        constructor = class_stmt.constructor
        self.assertIsNotNone(constructor)
        self.assertEqual(len(constructor.parameters), 1)
        self.assertEqual(constructor.parameters[0].name, 'name')


class TestRunaToJavaConverter(unittest.TestCase):
    """Test Runa AST to Java AST conversion."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.converter = RunaToJavaConverter()
    
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
        
        java_unit = self.converter.convert(runa_program)
        
        self.assertIsInstance(java_unit, JavaCompilationUnit)
        stmt = java_unit.declarations[0]
        self.assertIsInstance(stmt, JavaVariableDeclaration)
        self.assertEqual(stmt.type.name, 'int')  # Integer -> int mapping
        self.assertEqual(stmt.declarators[0].name, 'x')
    
    def test_function_conversion(self):
        """Test conversion of function declarations."""
        # Runa: Define public add with a as Integer and b as Integer returning Integer
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
                access_modifier='public',
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
        
        java_unit = self.converter.convert(runa_program)
        
        # Function should be converted to method in a generated class
        class_decl = java_unit.declarations[0]
        self.assertIsInstance(class_decl, JavaClassDeclaration)
        
        method = class_decl.members[0]
        self.assertIsInstance(method, JavaMethodDeclaration)
        self.assertEqual(method.name, 'add')
        self.assertEqual(len(method.parameters), 2)
        self.assertIn('public', method.modifiers)
    
    def test_class_conversion(self):
        """Test conversion of class declarations."""
        # Runa: Define public type Person with private name as String
        runa_program = Program([
            ClassDeclaration(
                name='Person',
                access_modifier='public',
                properties=[
                    PropertyDeclaration(
                        name='name',
                        type_annotation=TypeReference(name='String'),
                        access_modifier='private'
                    )
                ]
            )
        ])
        
        java_unit = self.converter.convert(runa_program)
        
        class_decl = java_unit.declarations[0]
        self.assertIsInstance(class_decl, JavaClassDeclaration)
        self.assertEqual(class_decl.name, 'Person')
        self.assertIn('public', class_decl.modifiers)
        
        field = class_decl.members[0]
        self.assertIsInstance(field, JavaFieldDeclaration)
        self.assertIn('private', field.modifiers)
    
    def test_interface_conversion(self):
        """Test conversion of interface declarations."""
        # Runa: Define interface Drawable with abstract draw
        runa_program = Program([
            InterfaceDeclaration(
                name='Drawable',
                methods=[
                    FunctionDeclaration(
                        name='draw',
                        parameters=[],
                        is_abstract=True
                    )
                ]
            )
        ])
        
        java_unit = self.converter.convert(runa_program)
        
        interface_decl = java_unit.declarations[0]
        self.assertIsInstance(interface_decl, JavaInterfaceDeclaration)
        self.assertEqual(interface_decl.name, 'Drawable')
        
        method = interface_decl.members[0]
        self.assertEqual(method.name, 'draw')
        self.assertIn('abstract', method.modifiers)
    
    def test_generic_conversion(self):
        """Test conversion of generic types."""
        # Runa: Define generic type Container with type T
        runa_program = Program([
            ClassDeclaration(
                name='Container',
                type_parameters=[TypeParameter(name='T')],
                properties=[
                    PropertyDeclaration(
                        name='value',
                        type_annotation=TypeReference(name='T')
                    )
                ]
            )
        ])
        
        java_unit = self.converter.convert(runa_program)
        
        class_decl = java_unit.declarations[0]
        self.assertEqual(len(class_decl.type_parameters), 1)
        self.assertEqual(class_decl.type_parameters[0].name, 'T')


class TestJavaSpecificFeatures(unittest.TestCase):
    """Test Java-specific language features."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.java_to_runa = JavaToRunaConverter()
        self.runa_to_java = RunaToJavaConverter()
    
    def test_package_declaration(self):
        """Test handling of package declarations."""
        # Java: package com.example.app;
        java_ast = JavaCompilationUnit([
            JavaPackageDeclaration(
                name='com.example.app'
            )
        ])
        
        runa_program = self.java_to_runa.convert(java_ast)
        
        # Package should be converted to module declaration
        self.assertIsInstance(runa_program, Program)
        # Check for module or namespace construct
        module_stmt = next((s for s in runa_program.statements if isinstance(s, NamespaceDeclaration)), None)
        if module_stmt:
            self.assertEqual(module_stmt.name, 'com.example.app')
    
    def test_annotation_handling(self):
        """Test handling of Java annotations."""
        # Java: @Override public void method() {}
        java_ast = JavaCompilationUnit([
            JavaClassDeclaration(
                name='TestClass',
                members=[
                    JavaMethodDeclaration(
                        annotations=[
                            JavaAnnotation(name='Override')
                        ],
                        modifiers=['public'],
                        return_type=JavaVoidType(),
                        name='method',
                        parameters=[],
                        body=JavaBlock([])
                    )
                ]
            )
        ])
        
        runa_program = self.java_to_runa.convert(java_ast)
        
        # Annotations should be preserved as decorators
        class_stmt = runa_program.statements[0]
        method = class_stmt.methods[0]
        self.assertGreater(len(method.decorators), 0)
        self.assertEqual(method.decorators[0].name, 'Override')
    
    def test_enum_declaration(self):
        """Test handling of enum declarations."""
        # Java: public enum Color { RED, GREEN, BLUE }
        java_ast = JavaCompilationUnit([
            JavaEnumDeclaration(
                modifiers=['public'],
                name='Color',
                constants=[
                    JavaEnumConstant(name='RED'),
                    JavaEnumConstant(name='GREEN'),
                    JavaEnumConstant(name='BLUE')
                ]
            )
        ])
        
        runa_program = self.java_to_runa.convert(java_ast)
        
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, EnumDeclaration)
        self.assertEqual(stmt.name, 'Color')
        self.assertEqual(len(stmt.members), 3)
    
    def test_lambda_expressions(self):
        """Test handling of lambda expressions (Java 8+)."""
        # Java: Function<Integer, Integer> square = x -> x * x;
        java_ast = JavaCompilationUnit([
            JavaVariableDeclaration(
                type=JavaParameterizedType(
                    raw_type=JavaReferenceType('Function'),
                    type_arguments=[
                        JavaReferenceType('Integer'),
                        JavaReferenceType('Integer')
                    ]
                ),
                declarators=[
                    JavaVariableDeclarator(
                        name='square',
                        initializer=JavaLambdaExpression(
                            parameters=[JavaIdentifier('x')],
                            body=JavaBinaryExpression(
                                left=JavaIdentifier('x'),
                                operator='*',
                                right=JavaIdentifier('x')
                            )
                        )
                    )
                ]
            )
        ])
        
        runa_program = self.java_to_runa.convert(java_ast)
        
        # Lambda should be converted to function expression
        stmt = runa_program.statements[0]
        self.assertIsInstance(stmt, VariableDeclaration)
        self.assertIsInstance(stmt.value, FunctionExpression)


class TestJavaRoundTrip(unittest.TestCase):
    """Test round-trip conversion for Java-specific patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.java_to_runa = JavaToRunaConverter()
        self.runa_to_java = RunaToJavaConverter()
    
    def test_roundtrip_class_hierarchy(self):
        """Test round-trip conversion of class hierarchy."""
        original_java = JavaCompilationUnit([
            JavaClassDeclaration(
                modifiers=['public'],
                name='Dog',
                extends=JavaReferenceType('Animal'),
                implements=[JavaReferenceType('Pet')],
                members=[
                    JavaMethodDeclaration(
                        modifiers=['public'],
                        return_type=JavaVoidType(),
                        name='bark',
                        parameters=[],
                        body=JavaBlock([])
                    )
                ]
            )
        ])
        
        # Round-trip conversion
        runa_program = self.java_to_runa.convert(original_java)
        converted_java = self.runa_to_java.convert(runa_program)
        
        # Verify class structure is preserved
        self.assertIsInstance(converted_java, JavaCompilationUnit)
        class_decl = converted_java.declarations[0]
        self.assertIsInstance(class_decl, JavaClassDeclaration)
        self.assertEqual(class_decl.name, 'Dog')
        self.assertIsNotNone(class_decl.extends)
        self.assertEqual(len(class_decl.implements), 1)
    
    def test_type_preservation_accuracy(self):
        """Test that Java's static typing is preserved."""
        original_java = JavaCompilationUnit([
            JavaMethodDeclaration(
                modifiers=['public', 'static'],
                return_type=JavaParameterizedType(
                    raw_type=JavaReferenceType('List'),
                    type_arguments=[JavaReferenceType('String')]
                ),
                name='process',
                parameters=[
                    JavaParameter(
                        type=JavaArrayType(
                            element_type=JavaReferenceType('String')
                        ),
                        name='items'
                    )
                ],
                body=JavaBlock([
                    JavaReturnStatement(
                        expression=JavaMethodInvocation(
                            expression=JavaReferenceType('Arrays'),
                            method='asList',
                            arguments=[JavaIdentifier('items')]
                        )
                    )
                ])
            )
        ])
        
        # Round-trip conversion
        runa_program = self.java_to_runa.convert(original_java)
        converted_java = self.runa_to_java.convert(runa_program)
        
        # Verify type information is preserved
        method = converted_java.declarations[0]
        self.assertIsInstance(method.return_type, JavaParameterizedType)
        self.assertIsInstance(method.parameters[0].type, JavaArrayType)


if __name__ == '__main__':
    unittest.main()
