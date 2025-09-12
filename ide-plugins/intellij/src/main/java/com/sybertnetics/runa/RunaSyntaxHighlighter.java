package com.sybertnetics.runa;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.HighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;

import java.util.HashMap;
import java.util.Map;

/**
 * Syntax highlighter for the Runa programming language.
 * Provides color schemes for different language elements.
 */
public class RunaSyntaxHighlighter extends SyntaxHighlighterBase {
    
    // Color scheme definitions
    public static final TextAttributesKey COMMENT = 
        TextAttributesKey.createTextAttributesKey("RUNA_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
    
    public static final TextAttributesKey KEYWORD = 
        TextAttributesKey.createTextAttributesKey("RUNA_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD);
    
    public static final TextAttributesKey STRING = 
        TextAttributesKey.createTextAttributesKey("RUNA_STRING", DefaultLanguageHighlighterColors.STRING);
    
    public static final TextAttributesKey NUMBER = 
        TextAttributesKey.createTextAttributesKey("RUNA_NUMBER", DefaultLanguageHighlighterColors.NUMBER);
    
    public static final TextAttributesKey BOOLEAN = 
        TextAttributesKey.createTextAttributesKey("RUNA_BOOLEAN", DefaultLanguageHighlighterColors.KEYWORD);
    
    public static final TextAttributesKey IDENTIFIER = 
        TextAttributesKey.createTextAttributesKey("RUNA_IDENTIFIER", DefaultLanguageHighlighterColors.IDENTIFIER);
    
    public static final TextAttributesKey NATURAL_OPERATOR = 
        TextAttributesKey.createTextAttributesKey("RUNA_NATURAL_OPERATOR", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    
    public static final TextAttributesKey MATH_SYMBOL = 
        TextAttributesKey.createTextAttributesKey("RUNA_MATH_SYMBOL", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    
    public static final TextAttributesKey PUNCTUATION = 
        TextAttributesKey.createTextAttributesKey("RUNA_PUNCTUATION", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    
    public static final TextAttributesKey FUNCTION_DECLARATION = 
        TextAttributesKey.createTextAttributesKey("RUNA_FUNCTION_DECLARATION", DefaultLanguageHighlighterColors.FUNCTION_DECLARATION);
    
    public static final TextAttributesKey FUNCTION_CALL = 
        TextAttributesKey.createTextAttributesKey("RUNA_FUNCTION_CALL", DefaultLanguageHighlighterColors.FUNCTION_CALL);
    
    public static final TextAttributesKey TYPE_NAME = 
        TextAttributesKey.createTextAttributesKey("RUNA_TYPE_NAME", DefaultLanguageHighlighterColors.CLASS_NAME);
    
    public static final TextAttributesKey VARIABLE_DECLARATION = 
        TextAttributesKey.createTextAttributesKey("RUNA_VARIABLE_DECLARATION", DefaultLanguageHighlighterColors.LOCAL_VARIABLE);
    
    public static final TextAttributesKey BAD_CHARACTER = 
        TextAttributesKey.createTextAttributesKey("RUNA_BAD_CHARACTER", HighlighterColors.BAD_CHARACTER);
    
    // Specific highlighting for important Runa constructs
    public static final TextAttributesKey PROCESS_KEYWORD = 
        TextAttributesKey.createTextAttributesKey("RUNA_PROCESS_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD);
    
    public static final TextAttributesKey LET_KEYWORD = 
        TextAttributesKey.createTextAttributesKey("RUNA_LET_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD);
    
    public static final TextAttributesKey CONTROL_FLOW = 
        TextAttributesKey.createTextAttributesKey("RUNA_CONTROL_FLOW", DefaultLanguageHighlighterColors.KEYWORD);
    
    public static final TextAttributesKey BUILTIN_FUNCTION = 
        TextAttributesKey.createTextAttributesKey("RUNA_BUILTIN_FUNCTION", DefaultLanguageHighlighterColors.PREDEFINED_SYMBOL);
    
    // Token to color mapping
    private static final Map<IElementType, TextAttributesKey> ATTRIBUTES = new HashMap<>();
    
    static {
        // Comments
        ATTRIBUTES.put(RunaTokenTypes.COMMENT, COMMENT);
        
        // Literals
        ATTRIBUTES.put(RunaTokenTypes.STRING_LITERAL, STRING);
        ATTRIBUTES.put(RunaTokenTypes.NUMBER_LITERAL, NUMBER);
        ATTRIBUTES.put(RunaTokenTypes.BOOLEAN_LITERAL, BOOLEAN);
        
        // Keywords
        ATTRIBUTES.put(RunaTokenTypes.KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.LET_KEYWORD, LET_KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.DEFINE_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.SET_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.PROCESS_KEYWORD, PROCESS_KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.IF_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.OTHERWISE_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.UNLESS_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.WHEN_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.MATCH_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.FOR_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.WHILE_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.TRY_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.CATCH_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.FINALLY_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.RETURN_KEYWORD, CONTROL_FLOW);
        ATTRIBUTES.put(RunaTokenTypes.IMPORT_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.EXPORT_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.DISPLAY_KEYWORD, BUILTIN_FUNCTION);
        ATTRIBUTES.put(RunaTokenTypes.ASSERT_KEYWORD, BUILTIN_FUNCTION);
        
        // Operators
        ATTRIBUTES.put(RunaTokenTypes.NATURAL_OPERATOR, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.MATH_SYMBOL, MATH_SYMBOL);
        ATTRIBUTES.put(RunaTokenTypes.PLUS_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.MINUS_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.MULTIPLIED_BY_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.DIVIDED_BY_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.MODULO_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.EQUALS_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.GREATER_THAN_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.LESS_THAN_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.CONTAINS_OP, NATURAL_OPERATOR);
        ATTRIBUTES.put(RunaTokenTypes.FOLLOWED_BY_OP, NATURAL_OPERATOR);
        
        // Special constructs
        ATTRIBUTES.put(RunaTokenTypes.BE_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.AS_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.TO_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.WITH_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.CALLED_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.THAT_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.TAKES_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.RETURNS_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.EACH_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.IN_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.FROM_KEYWORD, KEYWORD);
        ATTRIBUTES.put(RunaTokenTypes.BY_KEYWORD, KEYWORD);
        
        // Others
        ATTRIBUTES.put(RunaTokenTypes.IDENTIFIER, IDENTIFIER);
        ATTRIBUTES.put(RunaTokenTypes.PUNCTUATION, PUNCTUATION);
        ATTRIBUTES.put(RunaTokenTypes.BAD_CHARACTER, BAD_CHARACTER);
    }
    
    @NotNull
    @Override
    public Lexer getHighlightingLexer() {
        return new RunaLexer();
    }
    
    @NotNull
    @Override
    public TextAttributesKey[] getTokenHighlights(IElementType tokenType) {
        TextAttributesKey key = ATTRIBUTES.get(tokenType);
        return key != null ? new TextAttributesKey[]{key} : new TextAttributesKey[0];
    }
}
