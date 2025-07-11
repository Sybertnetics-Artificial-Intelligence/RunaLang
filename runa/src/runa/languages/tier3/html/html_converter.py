#!/usr/bin/env python3
"""
HTML to Runa AST Converter

Bidirectional converter between HTML AST and Runa AST for the universal
translation system.

Author: Sybertnetics AI Solutions
License: MIT
"""

from typing import List, Optional, Dict, Any, Union
import logging

from ....core.runa_ast import *
from .html_ast import *


class HtmlToRunaConverter:
    """Converts HTML AST to Runa AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, html_node: HtmlNode) -> ASTNode:
        """Convert HTML AST node to Runa AST."""
        try:
            if isinstance(html_node, HtmlDocument):
                return self._convert_document(html_node)
            elif isinstance(html_node, HtmlElement):
                return self._convert_element(html_node)
            elif isinstance(html_node, HtmlText):
                return self._convert_text(html_node)
            elif isinstance(html_node, HtmlComment):
                return self._convert_comment(html_node)
            else:
                # Create a simple variable for other node types
                return Variable(identifier="html_node", type_hint=StringType())
        except Exception as e:
            self.logger.error(f"HTML to Runa conversion failed: {e}")
            raise RuntimeError(f"Failed to convert HTML to Runa: {e}")
    
    def _convert_document(self, document: HtmlDocument) -> Program:
        """Convert HTML document to Runa program."""
        statements = []
        
        # Create document metadata
        if document.language != "en":
            lang_stmt = VariableDeclaration(
                identifier="document language",
                expression=StringLiteral(document.language),
                type_hint=StringType()
            )
            statements.append(lang_stmt)
        
        if document.encoding != "UTF-8":
            encoding_stmt = VariableDeclaration(
                identifier="document encoding", 
                expression=StringLiteral(document.encoding),
                type_hint=StringType()
            )
            statements.append(encoding_stmt)
        
        # Create DOCTYPE declaration
        if document.doctype:
            doctype_stmt = VariableDeclaration(
                identifier="document type",
                expression=StringLiteral(document.doctype.doctype_string),
                type_hint=StringType()
            )
            statements.append(doctype_stmt)
        
        # Convert root element
        if document.root_element:
            root_stmt = VariableDeclaration(
                identifier="html document",
                expression=self._element_to_expression(document.root_element),
                type_hint=DictionaryType(StringType(), StringType())
            )
            statements.append(root_stmt)
        
        # Add demonstration operations
        demo_stmt = self._create_demo_operations(document)
        statements.extend(demo_stmt)
        
        return Program(statements=statements)
    
    def _convert_element(self, element: HtmlElement) -> Expression:
        """Convert HTML element to Runa expression."""
        return self._element_to_expression(element)
    
    def _element_to_expression(self, element: HtmlElement) -> Expression:
        """Convert HTML element to dictionary expression."""
        items = []
        
        # Add tag name
        items.append(DictionaryItem(
            key=StringLiteral("tag"),
            value=StringLiteral(element.tag_name)
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
                if isinstance(child, HtmlElement):
                    child_items.append(self._element_to_expression(child))
                elif isinstance(child, HtmlText):
                    content = child.content.strip()
                    if content:
                        child_items.append(StringLiteral(content))
                elif isinstance(child, HtmlComment):
                    # Include comments as special entries
                    comment_dict = DictionaryLiteral(items=[
                        DictionaryItem(
                            key=StringLiteral("type"),
                            value=StringLiteral("comment")
                        ),
                        DictionaryItem(
                            key=StringLiteral("content"),
                            value=StringLiteral(child.content)
                        )
                    ])
                    child_items.append(comment_dict)
            
            if child_items:
                items.append(DictionaryItem(
                    key=StringLiteral("children"),
                    value=ListLiteral(elements=child_items)
                ))
        
        # Handle void elements
        if element.is_void_element:
            items.append(DictionaryItem(
                key=StringLiteral("void_element"),
                value=BooleanLiteral(True)
            ))
        
        # Handle self-closing elements
        if element.is_self_closing:
            items.append(DictionaryItem(
                key=StringLiteral("self_closing"),
                value=BooleanLiteral(True)
            ))
        
        return DictionaryLiteral(items=items)
    
    def _convert_text(self, text: HtmlText) -> StringLiteral:
        """Convert HTML text to string literal."""
        return StringLiteral(text.content)
    
    def _convert_comment(self, comment: HtmlComment) -> StringLiteral:
        """Convert HTML comment to string literal."""
        return StringLiteral(f"<!-- {comment.content} -->")
    
    def _create_demo_operations(self, document: HtmlDocument) -> List[Statement]:
        """Create demonstration operations for HTML processing."""
        statements = []
        
        if not document.root_element:
            return statements
        
        # Add text extraction operation
        extract_stmt = VariableDeclaration(
            identifier="page text content",
            expression=FunctionCall(
                function_name="extract text from document",
                arguments=[Variable(identifier="html document")]
            ),
            type_hint=StringType()
        )
        statements.append(extract_stmt)
        
        # Find and extract title
        title_elements = document.root_element.find_descendants_by_tag('title')
        if title_elements:
            title_stmt = VariableDeclaration(
                identifier="page title",
                expression=FunctionCall(
                    function_name="get element text",
                    arguments=[
                        FunctionCall(
                            function_name="find element by tag",
                            arguments=[
                                Variable(identifier="html document"),
                                StringLiteral("title")
                            ]
                        )
                    ]
                ),
                type_hint=StringType()
            )
            statements.append(title_stmt)
        
        # Extract links
        link_elements = document.root_element.find_descendants_by_tag('a')
        if link_elements:
            links_stmt = VariableDeclaration(
                identifier="page links",
                expression=FunctionCall(
                    function_name="extract all links",
                    arguments=[Variable(identifier="html document")]
                ),
                type_hint=ListType(StringType())
            )
            statements.append(links_stmt)
        
        # Extract images
        img_elements = document.root_element.find_descendants_by_tag('img')
        if img_elements:
            images_stmt = VariableDeclaration(
                identifier="page images",
                expression=FunctionCall(
                    function_name="extract all images",
                    arguments=[Variable(identifier="html document")]
                ),
                type_hint=ListType(DictionaryType(StringType(), StringType()))
            )
            statements.append(images_stmt)
        
        # Find element by ID (if any elements have IDs)
        for element in document.root_element.find_descendants_by_tag('*'):
            if isinstance(element, HtmlElement) and element.get_attribute('id'):
                element_id = element.get_attribute('id').value
                id_stmt = VariableDeclaration(
                    identifier=f"element with id {element_id}",
                    expression=FunctionCall(
                        function_name="find element by id",
                        arguments=[
                            Variable(identifier="html document"),
                            StringLiteral(element_id)
                        ]
                    ),
                    type_hint=DictionaryType(StringType(), StringType())
                )
                statements.append(id_stmt)
                break  # Just one example
        
        # Find elements by class (if any elements have classes)
        for element in document.root_element.find_descendants_by_tag('*'):
            if isinstance(element, HtmlElement) and element.get_attribute('class'):
                class_names = element.get_attribute('class').value.split()
                if class_names:
                    class_name = class_names[0]
                    class_stmt = VariableDeclaration(
                        identifier=f"elements with class {class_name}",
                        expression=FunctionCall(
                            function_name="find elements by class",
                            arguments=[
                                Variable(identifier="html document"),
                                StringLiteral(class_name)
                            ]
                        ),
                        type_hint=ListType(DictionaryType(StringType(), StringType()))
                    )
                    statements.append(class_stmt)
                    break  # Just one example
        
        return statements


class RunaToHtmlConverter:
    """Converts Runa AST to HTML AST."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert(self, runa_node: ASTNode) -> HtmlNode:
        """Convert Runa AST node to HTML AST."""
        try:
            if isinstance(runa_node, Program):
                return self._convert_program(runa_node)
            elif isinstance(runa_node, DictionaryLiteral):
                return self._convert_dictionary_to_element(runa_node)
            elif isinstance(runa_node, ListLiteral):
                return self._convert_list_to_container(runa_node)
            elif isinstance(runa_node, StringLiteral):
                return HtmlText(content=runa_node.value)
            else:
                # Create a simple text node for other types
                return HtmlText(content=str(runa_node))
        except Exception as e:
            self.logger.error(f"Runa to HTML conversion failed: {e}")
            raise RuntimeError(f"Failed to convert Runa to HTML: {e}")
    
    def _convert_program(self, program: Program) -> HtmlDocument:
        """Convert Runa program to HTML document."""
        document = HtmlDocument()
        
        # Look for HTML-specific declarations
        html_element = None
        
        for stmt in program.statements:
            if isinstance(stmt, VariableDeclaration):
                if stmt.identifier == "document language" and isinstance(stmt.expression, StringLiteral):
                    document.language = stmt.expression.value
                elif stmt.identifier == "document encoding" and isinstance(stmt.expression, StringLiteral):
                    document.encoding = stmt.expression.value
                elif stmt.identifier == "document type" and isinstance(stmt.expression, StringLiteral):
                    document.doctype = HtmlDoctype(doctype_string=stmt.expression.value)
                elif stmt.identifier == "html document" and isinstance(stmt.expression, DictionaryLiteral):
                    html_element = self._convert_dictionary_to_element(stmt.expression)
                elif "element" in stmt.identifier.lower() and isinstance(stmt.expression, DictionaryLiteral):
                    # Fallback: any element-like declaration
                    if html_element is None:
                        html_element = self._convert_dictionary_to_element(stmt.expression)
        
        # If no HTML element found, create a basic structure
        if html_element is None:
            html_element = create_html_element('html')
            head = create_html_element('head')
            head.add_child(create_html_element('title', content="Generated from Runa"))
            body = create_html_element('body')
            body.add_child(create_html_text("Generated from Runa code"))
            html_element.add_child(head)
            html_element.add_child(body)
        
        document.root_element = html_element
        
        # Set default DOCTYPE if not specified
        if document.doctype is None:
            document.doctype = HtmlDoctype(doctype_string="html")
        
        return document
    
    def _convert_dictionary_to_element(self, dict_literal: DictionaryLiteral) -> HtmlElement:
        """Convert dictionary literal to HTML element."""
        tag_name = "div"  # Default tag
        attributes = {}
        children = []
        is_void_element = False
        is_self_closing = False
        
        # Process dictionary items
        for item in dict_literal.items:
            if isinstance(item.key, StringLiteral):
                key = item.key.value
                
                if key == "tag" and isinstance(item.value, StringLiteral):
                    tag_name = item.value.value.lower()
                elif key == "attributes" and isinstance(item.value, DictionaryLiteral):
                    for attr_item in item.value.items:
                        if isinstance(attr_item.key, StringLiteral) and isinstance(attr_item.value, StringLiteral):
                            attr_name = attr_item.key.value
                            attr_value = attr_item.value.value
                            attributes[attr_name] = HtmlAttribute(
                                name=attr_name, 
                                value=attr_value,
                                is_boolean=attr_value == ""
                            )
                elif key == "children" and isinstance(item.value, ListLiteral):
                    for child_expr in item.value.elements:
                        if isinstance(child_expr, DictionaryLiteral):
                            # Check if it's a comment
                            child_dict_items = {
                                child_item.key.value: child_item.value 
                                for child_item in child_expr.items 
                                if isinstance(child_item.key, StringLiteral)
                            }
                            
                            if "type" in child_dict_items and isinstance(child_dict_items["type"], StringLiteral):
                                if child_dict_items["type"].value == "comment":
                                    if "content" in child_dict_items and isinstance(child_dict_items["content"], StringLiteral):
                                        children.append(HtmlComment(content=child_dict_items["content"].value))
                                    continue
                            
                            children.append(self._convert_dictionary_to_element(child_expr))
                        elif isinstance(child_expr, StringLiteral):
                            children.append(HtmlText(content=child_expr.value))
                elif key == "void_element" and isinstance(item.value, BooleanLiteral):
                    is_void_element = item.value.value
                elif key == "self_closing" and isinstance(item.value, BooleanLiteral):
                    is_self_closing = item.value.value
                elif isinstance(item.value, StringLiteral):
                    # Treat as text content if not a special key
                    children.append(HtmlText(content=item.value.value))
        
        # Check if tag is naturally a void element
        if tag_name in HTML5_VOID_ELEMENTS:
            is_void_element = True
        
        element = HtmlElement(
            tag_name=tag_name,
            is_void_element=is_void_element,
            is_self_closing=is_self_closing
        )
        
        element.attributes = attributes
        
        # Add children (void elements can't have children)
        if not is_void_element:
            for child in children:
                element.add_child(child)
        
        return element
    
    def _convert_list_to_container(self, list_literal: ListLiteral) -> HtmlElement:
        """Convert list literal to HTML container element."""
        container = create_html_element('div')
        container.set_attribute('class', 'runa-list')
        
        for expr in list_literal.elements:
            if isinstance(expr, DictionaryLiteral):
                container.add_child(self._convert_dictionary_to_element(expr))
            elif isinstance(expr, StringLiteral):
                item_element = create_html_element('p')
                item_element.add_child(HtmlText(content=expr.value))
                container.add_child(item_element)
            elif isinstance(expr, (IntegerLiteral, FloatLiteral, BooleanLiteral)):
                item_element = create_html_element('p')
                item_element.add_child(HtmlText(content=str(expr.value)))
                container.add_child(item_element)
        
        return container


# Convenience functions
def html_to_runa(html_node: HtmlNode) -> ASTNode:
    """Convert HTML AST to Runa AST."""
    converter = HtmlToRunaConverter()
    return converter.convert(html_node)


def runa_to_html(runa_node: ASTNode) -> HtmlNode:
    """Convert Runa AST to HTML AST."""
    converter = RunaToHtmlConverter()
    return converter.convert(runa_node)


def html_document_to_runa_program(document: HtmlDocument) -> Program:
    """Convert HTML document to Runa program."""
    converter = HtmlToRunaConverter()
    return converter.convert(document)


def runa_program_to_html_document(program: Program) -> HtmlDocument:
    """Convert Runa program to HTML document."""
    converter = RunaToHtmlConverter()
    result = converter.convert(program)
    if isinstance(result, HtmlDocument):
        return result
    else:
        # Wrap in document
        document = HtmlDocument()
        if isinstance(result, HtmlElement):
            document.root_element = result
        else:
            # Create basic HTML structure
            html_elem = create_html_element('html')
            body = create_html_element('body')
            if isinstance(result, HtmlText):
                body.add_child(result)
            else:
                body.add_child(HtmlText(content=str(result)))
            html_elem.add_child(body)
            document.root_element = html_elem
        return document