package com.sybertnetics.runa;

import com.intellij.psi.tree.IElementType;

/**
 * Token types for the Runa programming language lexer.
 * These correspond to the different syntactic elements in Runa according to the language specification.
 */
public class RunaTokenTypes {
    
    // Comments
    public static final IElementType COMMENT = new RunaTokenType("COMMENT");
    
    // Literals
    public static final IElementType STRING_LITERAL = new RunaTokenType("STRING_LITERAL");
    public static final IElementType NUMBER_LITERAL = new RunaTokenType("NUMBER_LITERAL");
    public static final IElementType BOOLEAN_LITERAL = new RunaTokenType("BOOLEAN_LITERAL");
    
    // Identifiers and Keywords
    public static final IElementType IDENTIFIER = new RunaTokenType("IDENTIFIER");
    public static final IElementType KEYWORD = new RunaTokenType("KEYWORD");
    
    // Operators
    public static final IElementType NATURAL_OPERATOR = new RunaTokenType("NATURAL_OPERATOR");
    public static final IElementType MATH_SYMBOL = new RunaTokenType("MATH_SYMBOL");
    
    // Punctuation and Delimiters
    public static final IElementType PUNCTUATION = new RunaTokenType("PUNCTUATION");
    public static final IElementType COLON = new RunaTokenType("COLON");
    public static final IElementType COMMA = new RunaTokenType("COMMA");
    public static final IElementType DOT = new RunaTokenType("DOT");
    public static final IElementType LPAREN = new RunaTokenType("LPAREN");
    public static final IElementType RPAREN = new RunaTokenType("RPAREN");
    public static final IElementType LBRACKET = new RunaTokenType("LBRACKET");
    public static final IElementType RBRACKET = new RunaTokenType("RBRACKET");
    public static final IElementType LBRACE = new RunaTokenType("LBRACE");
    public static final IElementType RBRACE = new RunaTokenType("RBRACE");
    
    // Whitespace and Layout
    public static final IElementType WHITESPACE = new RunaTokenType("WHITESPACE");
    public static final IElementType NEWLINE = new RunaTokenType("NEWLINE");
    public static final IElementType INDENT = new RunaTokenType("INDENT");
    public static final IElementType DEDENT = new RunaTokenType("DEDENT");
    
    // Special tokens
    public static final IElementType BAD_CHARACTER = new RunaTokenType("BAD_CHARACTER");
    public static final IElementType EOF = new RunaTokenType("EOF");
    
    // Specific Runa keywords as tokens (for better syntax highlighting)
    public static final IElementType LET_KEYWORD = new RunaTokenType("LET_KEYWORD");
    public static final IElementType DEFINE_KEYWORD = new RunaTokenType("DEFINE_KEYWORD");
    public static final IElementType SET_KEYWORD = new RunaTokenType("SET_KEYWORD");
    public static final IElementType PROCESS_KEYWORD = new RunaTokenType("PROCESS_KEYWORD");
    public static final IElementType IF_KEYWORD = new RunaTokenType("IF_KEYWORD");
    public static final IElementType OTHERWISE_KEYWORD = new RunaTokenType("OTHERWISE_KEYWORD");
    public static final IElementType UNLESS_KEYWORD = new RunaTokenType("UNLESS_KEYWORD");
    public static final IElementType WHEN_KEYWORD = new RunaTokenType("WHEN_KEYWORD");
    public static final IElementType MATCH_KEYWORD = new RunaTokenType("MATCH_KEYWORD");
    public static final IElementType FOR_KEYWORD = new RunaTokenType("FOR_KEYWORD");
    public static final IElementType WHILE_KEYWORD = new RunaTokenType("WHILE_KEYWORD");
    public static final IElementType TRY_KEYWORD = new RunaTokenType("TRY_KEYWORD");
    public static final IElementType CATCH_KEYWORD = new RunaTokenType("CATCH_KEYWORD");
    public static final IElementType FINALLY_KEYWORD = new RunaTokenType("FINALLY_KEYWORD");
    public static final IElementType RETURN_KEYWORD = new RunaTokenType("RETURN_KEYWORD");
    public static final IElementType IMPORT_KEYWORD = new RunaTokenType("IMPORT_KEYWORD");
    public static final IElementType EXPORT_KEYWORD = new RunaTokenType("EXPORT_KEYWORD");
    public static final IElementType DISPLAY_KEYWORD = new RunaTokenType("DISPLAY_KEYWORD");
    public static final IElementType ASSERT_KEYWORD = new RunaTokenType("ASSERT_KEYWORD");
    
    // Natural language operators as specific tokens
    public static final IElementType PLUS_OP = new RunaTokenType("PLUS_OP");
    public static final IElementType MINUS_OP = new RunaTokenType("MINUS_OP");
    public static final IElementType MULTIPLIED_BY_OP = new RunaTokenType("MULTIPLIED_BY_OP");
    public static final IElementType DIVIDED_BY_OP = new RunaTokenType("DIVIDED_BY_OP");
    public static final IElementType MODULO_OP = new RunaTokenType("MODULO_OP");
    public static final IElementType EQUALS_OP = new RunaTokenType("EQUALS_OP");
    public static final IElementType GREATER_THAN_OP = new RunaTokenType("GREATER_THAN_OP");
    public static final IElementType LESS_THAN_OP = new RunaTokenType("LESS_THAN_OP");
    public static final IElementType CONTAINS_OP = new RunaTokenType("CONTAINS_OP");
    public static final IElementType FOLLOWED_BY_OP = new RunaTokenType("FOLLOWED_BY_OP");
    
    // Special constructs
    public static final IElementType BE_KEYWORD = new RunaTokenType("BE_KEYWORD");
    public static final IElementType AS_KEYWORD = new RunaTokenType("AS_KEYWORD");
    public static final IElementType TO_KEYWORD = new RunaTokenType("TO_KEYWORD");
    public static final IElementType WITH_KEYWORD = new RunaTokenType("WITH_KEYWORD");
    public static final IElementType CALLED_KEYWORD = new RunaTokenType("CALLED_KEYWORD");
    public static final IElementType THAT_KEYWORD = new RunaTokenType("THAT_KEYWORD");
    public static final IElementType TAKES_KEYWORD = new RunaTokenType("TAKES_KEYWORD");
    public static final IElementType RETURNS_KEYWORD = new RunaTokenType("RETURNS_KEYWORD");
    public static final IElementType EACH_KEYWORD = new RunaTokenType("EACH_KEYWORD");
    public static final IElementType IN_KEYWORD = new RunaTokenType("IN_KEYWORD");
    public static final IElementType FROM_KEYWORD = new RunaTokenType("FROM_KEYWORD");
    public static final IElementType BY_KEYWORD = new RunaTokenType("BY_KEYWORD");
    
    private RunaTokenTypes() {
        // Utility class - no instantiation
    }
}
