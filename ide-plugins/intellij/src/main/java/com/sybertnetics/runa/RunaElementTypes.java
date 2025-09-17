package com.sybertnetics.runa;

import com.intellij.psi.tree.IElementType;

/**
 * Element types for the Runa language AST (Abstract Syntax Tree).
 * These represent different structural elements in Runa code.
 */
public class RunaElementTypes {
    
    // Statement types
    public static final IElementType LET_STATEMENT = new RunaElementType("LET_STATEMENT");
    public static final IElementType DEFINE_STATEMENT = new RunaElementType("DEFINE_STATEMENT");
    public static final IElementType SET_STATEMENT = new RunaElementType("SET_STATEMENT");
    public static final IElementType PROCESS_STATEMENT = new RunaElementType("PROCESS_STATEMENT");
    public static final IElementType IF_STATEMENT = new RunaElementType("IF_STATEMENT");
    public static final IElementType FOR_STATEMENT = new RunaElementType("FOR_STATEMENT");
    public static final IElementType WHILE_STATEMENT = new RunaElementType("WHILE_STATEMENT");
    public static final IElementType DISPLAY_STATEMENT = new RunaElementType("DISPLAY_STATEMENT");
    public static final IElementType RETURN_STATEMENT = new RunaElementType("RETURN_STATEMENT");
    public static final IElementType EXPRESSION_STATEMENT = new RunaElementType("EXPRESSION_STATEMENT");
    
    // Expression types
    public static final IElementType EXPRESSION = new RunaElementType("EXPRESSION");
    public static final IElementType BINARY_EXPRESSION = new RunaElementType("BINARY_EXPRESSION");
    public static final IElementType UNARY_EXPRESSION = new RunaElementType("UNARY_EXPRESSION");
    public static final IElementType FUNCTION_CALL = new RunaElementType("FUNCTION_CALL");
    public static final IElementType IDENTIFIER_EXPRESSION = new RunaElementType("IDENTIFIER_EXPRESSION");
    public static final IElementType LITERAL_EXPRESSION = new RunaElementType("LITERAL_EXPRESSION");
    
    // Control flow
    public static final IElementType IF_CONDITION = new RunaElementType("IF_CONDITION");
    public static final IElementType FOR_LOOP = new RunaElementType("FOR_LOOP");
    public static final IElementType WHILE_LOOP = new RunaElementType("WHILE_LOOP");
    public static final IElementType MATCH_EXPRESSION = new RunaElementType("MATCH_EXPRESSION");
    
    // Function and type definitions
    public static final IElementType FUNCTION_DEFINITION = new RunaElementType("FUNCTION_DEFINITION");
    public static final IElementType PARAMETER_LIST = new RunaElementType("PARAMETER_LIST");
    public static final IElementType PARAMETER = new RunaElementType("PARAMETER");
    public static final IElementType TYPE_ANNOTATION = new RunaElementType("TYPE_ANNOTATION");
    public static final IElementType TYPE_DEFINITION = new RunaElementType("TYPE_DEFINITION");
    
    // Imports and exports
    public static final IElementType IMPORT_STATEMENT = new RunaElementType("IMPORT_STATEMENT");
    public static final IElementType EXPORT_STATEMENT = new RunaElementType("EXPORT_STATEMENT");
    
    // Error handling
    public static final IElementType TRY_STATEMENT = new RunaElementType("TRY_STATEMENT");
    public static final IElementType CATCH_CLAUSE = new RunaElementType("CATCH_CLAUSE");
    public static final IElementType FINALLY_CLAUSE = new RunaElementType("FINALLY_CLAUSE");
    
    // Collections
    public static final IElementType LIST_EXPRESSION = new RunaElementType("LIST_EXPRESSION");
    public static final IElementType DICTIONARY_EXPRESSION = new RunaElementType("DICTIONARY_EXPRESSION");
    
    // Special constructs
    public static final IElementType COMMENT_BLOCK = new RunaElementType("COMMENT_BLOCK");
    public static final IElementType STRING_INTERPOLATION = new RunaElementType("STRING_INTERPOLATION");
    
    private RunaElementTypes() {
        // Utility class
    }
}
