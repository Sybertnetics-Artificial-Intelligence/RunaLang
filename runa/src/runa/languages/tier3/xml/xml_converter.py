#!/usr/bin/env python3
"""
XML to Runa AST Converter

Bidirectional converter between XML AST and Runa AST for the universal
translation system.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from ....core.runa_ast import *
from .xml_ast import *


class XmlToRunaConverter:
    """Converts XML AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, xml_node: XmlNode) -> ASTNode:
        """Convert XML AST node to Runa AST."""
        try:
            if isinstance(xml_node, XmlDocument):
                return self._convert_document(xml_node)
            elif isinstance(xml_node, XmlElement):
                return self._convert_element(xml_node)
            elif isinstance(xml_node, XmlText):
                return self._convert_text(xml_node)
            elif isinstance(xml_node, XmlComment):
                return self._convert_comment(xml_node)
            else:
                # Create a simple variable for other node types
                return Variable(identifier="xml_node", type_hint=StringType())
        except Exception as e:
            self.logger.error(f"XML to Runa conversion failed: {e}")
            raise RuntimeError(f"Failed to convert XML to Runa: {e}")
    
    def _convert_document(self, document: XmlDocument) -> Program:
        """Convert XML document to Runa program."""
        statements = []
        
        # Create document metadata
        if document.version != "1.0" or document.encoding != "UTF-8":
            version_stmt = VariableDeclaration(
                identifier="xml version",
                expression=StringLiteral(document.version),
                type_hint=StringType()
            )
            statements.append(version_stmt)
            
            encoding_stmt = VariableDeclaration(
                identifier="xml encoding", 
                expression=StringLiteral(document.encoding),
                type_hint=StringType()
            )
            statements.append(encoding_stmt)
        
        # Convert root element
        if document.root_element:
            root_stmt = VariableDeclaration(
                identifier="root element",
                expression=self._element_to_expression(document.root_element),
                type_hint=DictionaryType(StringType(), StringType())
            )
            statements.append(root_stmt)
        
        # Add demonstration operations
        demo_stmt = self._create_demo_operations(document)
        statements.extend(demo_stmt)
        
        return Program(statements=statements)
    
    def _convert_element(self, element: XmlElement) -> Expression:
        """Convert XML element to Runa expression."""
        return self._element_to_expression(element)
    
    def _element_to_expression(self, element: XmlElement) -> Expression:
        """Convert XML element to dictionary expression."""
        # Create dictionary for element
        items = []
        
        # Add tag name
        items.append(DictionaryItem(
            key=StringLiteral("tag"),
            value=StringLiteral(element.tag_name)
        ))
        
        # Add namespace if present
        if element.namespace_prefix:
            items.append(DictionaryItem(
                key=StringLiteral("namespace"),
                value=StringLiteral(element.namespace_prefix)
            ))
        
        # Add attributes
        if element.attributes:
            attr_items = []
            for attr_name, attr in element.attributes.items():
                attr_items.append(DictionaryItem(
                    key=StringLiteral(attr_name),
                    value=StringLiteral(attr.value)
                ))
            
            items.append(DictionaryItem(
                key=StringLiteral("attributes"),
                value=DictionaryLiteral(items=attr_items)
            ))
        
        # Add children
        if element.children:
            child_items = []
            for child in element.children:
                if isinstance(child, XmlElement):
                    child_items.append(self._element_to_expression(child))
                elif isinstance(child, XmlText):
                    content = child.content.strip()
                    if content:
                        child_items.append(StringLiteral(content))
                elif isinstance(child, XmlComment):
                    # Skip comments in data representation
                    pass
            
            if child_items:
                items.append(DictionaryItem(
                    key=StringLiteral("children"),
                    value=ListLiteral(elements=child_items)
                ))
        
        # Handle self-closing elements
        if element.is_self_closing:
            items.append(DictionaryItem(
                key=StringLiteral("self_closing"),
                value=BooleanLiteral(True)
            ))
        
        return DictionaryLiteral(items=items)
    
    def _convert_text(self, text: XmlText) -> StringLiteral:
        """Convert XML text to string literal."""
        return StringLiteral(text.content)
    
    def _convert_comment(self, comment: XmlComment) -> StringLiteral:
        """Convert XML comment to string literal."""
        return StringLiteral(f"<!-- {comment.content} -->")
    
    def _create_demo_operations(self, document: XmlDocument) -> List[Statement]:
        """Create demonstration operations for XML processing."""
        statements = []
        
        if not document.root_element:
            return statements
        
        # Add text extraction operation
        extract_stmt = VariableDeclaration(
            identifier="extracted text",
            expression=FunctionCall(
                function_name="extract text from element",
                arguments=[Variable(identifier="root element")]
            ),
            type_hint=StringType()
        )
        statements.append(extract_stmt)
        
        # Add attribute access operation
        if document.root_element.attributes:
            attr_name = next(iter(document.root_element.attributes.keys()))
            attr_stmt = VariableDeclaration(
                identifier=f"{attr_name} attribute",
                expression=FunctionCall(
                    function_name="get attribute",
                    arguments=[
                        Variable(identifier="root element"),
                        StringLiteral(attr_name)
                    ]
                ),
                type_hint=StringType()
            )
            statements.append(attr_stmt)
        
        # Add child element access if children exist
        if document.root_element.children:
            for child in document.root_element.children:
                if isinstance(child, XmlElement):
                    child_stmt = VariableDeclaration(
                        identifier=f"first {child.tag_name} element",
                        expression=FunctionCall(
                            function_name="find element by tag",
                            arguments=[
                                Variable(identifier="root element"),
                                StringLiteral(child.tag_name)
                            ]
                        ),
                        type_hint=DictionaryType(StringType(), StringType())
                    )
                    statements.append(child_stmt)
                    break
        
        return statements


class RunaToXmlConverter:
    """Converts Runa AST to XML AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: ASTNode) -> XmlNode:
        """Convert Runa AST node to XML AST."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, DictionaryLiteral):
                return self._convert_dictionary_to_element(runa_node)
            elif isinstance(runa_node, ListLiteral):
                return self._convert_list_to_sequence(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return XmlText(content=runa_node.value)
            else:
                # Create a simple text node for other types
                return XmlText(content=str(runa_node))
        except Exception as e:
            self.logger.error(f"Runa to XML conversion failed: {e}")
            raise RuntimeError(f"Failed to convert Runa to XML: {e}")
    
    def _convert_program(self, program: Program) -> XmlDocument:
        """Convert Runa program to XML document."""
        document = XmlDocument()
        
        # Look for XML-specific declarations
        root_element = None
        
        for stmt in program.statements:
            if isinstance(stmt, VariableDeclaration):
                if stmt.identifier == "xml version" and isinstance(stmt.expression, StringLiteral):
                    document.version = stmt.expression.value
                elif stmt.identifier == "xml encoding" and isinstance(stmt.expression, StringLiteral):
                    document.encoding = stmt.expression.value
                elif stmt.identifier == "root element" and isinstance(stmt.expression, DictionaryLiteral):
                    root_element = self._convert_dictionary_to_element(stmt.expression)
                elif "element" in stmt.identifier.lower() and isinstance(stmt.expression, DictionaryLiteral):
                    # Fallback: any element-like declaration
                    if root_element is None:
                        root_element = self._convert_dictionary_to_element(stmt.expression)
        
        # If no root element found, create a simple one
        if root_element is None:
            root_element = XmlElement(tag_name="root")
            root_element.add_child(XmlText("Generated from Runa code"))
        
        document.root_element = root_element
        return document
    
    def _convert_dictionary_to_element(self, dict_literal: DictionaryLiteral) -> XmlElement:
        """Convert dictionary literal to XML element."""
        tag_name = "element"
        namespace_prefix = None
        attributes = {}
        children = []
        is_self_closing = False
        
        # Process dictionary items
        for item in dict_literal.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "tag" and isinstance(item.value, StringLiteral):
                    tag_name = item.value.value
                elif key == "namespace" and isinstance(item.value, StringLiteral):
                    namespace_prefix = item.value.value
                elif key == "attributes" and isinstance(item.value, DictionaryLiteral):
                    for attr_item in item.value.items:
                        if isinstance(attr_item.key, StringLiteral) and isinstance(attr_item.value, StringLiteral):
                            attr_name = attr_item.key.value
                            attr_value = attr_item.value.value
                            attributes[attr_name] = XmlAttribute(name=attr_name, value=attr_value)
                elif key == "children" and isinstance(item.value, ListLiteral):
                    for child_expr in item.value.elements:
                        if isinstance(child_expr, DictionaryLiteral):
                            children.append(self._convert_dictionary_to_element(child_expr))
                        elif isinstance(child_expr, StringLiteral):
                            children.append(XmlText(content=child_expr.value))
                elif key == "self_closing" and isinstance(item.value, BooleanLiteral):
                    is_self_closing = item.value.value
                elif isinstance(item.value, StringLiteral):
                    # Treat as text content if not a special key
                    children.append(XmlText(content=item.value.value))
        
        element = XmlElement(
            tag_name=tag_name,
            namespace_prefix=namespace_prefix,
            is_self_closing=is_self_closing
        )
        
        element.attributes = attributes
        
        for child in children:
            element.add_child(child)
        
        return element
    
    def _convert_list_to_sequence(self, list_literal: ListLiteral) -> XmlElement:
        """Convert list literal to XML sequence (as container element)."""
        container = XmlElement(tag_name="list")
        
        for expr in list_literal.elements:
            if isinstance(expr, DictionaryLiteral):
                container.add_child(self._convert_dictionary_to_element(expr))
            elif isinstance(expr, StringLiteral):
                item_element = XmlElement(tag_name="item")
                item_element.add_child(XmlText(content=expr.value))
                container.add_child(item_element)
            elif isinstance(expr, (IntegerLiteral, FloatLiteral, BooleanLiteral)):
                item_element = XmlElement(tag_name="item")
                item_element.add_child(XmlText(content=str(expr.value)))
                container.add_child(item_element)
        
        return container


# Convenience functions
def xml_to_runa(xml_node: XmlNode) -> ASTNode:
    """Convert XML AST to Runa AST."""
    converter = XmlToRunaConverter()
    return converter.convert(xml_node)


def runa_to_xml(runa_node: ASTNode) -> XmlNode:
    """Convert Runa AST to XML AST."""
    converter = RunaToXmlConverter()
    return converter.convert(runa_node)


def xml_document_to_runa_program(document: XmlDocument) -> Program:
    """Convert XML document to Runa program."""
    converter = XmlToRunaConverter()
    return converter.convert(document)


def runa_program_to_xml_document(program: Program) -> XmlDocument:
    """Convert Runa program to XML document."""
    converter = RunaToXmlConverter()
    result = converter.convert(program)
    if isinstance(result, XmlDocument):
        return result
    else:
        # Wrap in document
        document = XmlDocument()
        if isinstance(result, XmlElement):
            document.root_element = result
        return document