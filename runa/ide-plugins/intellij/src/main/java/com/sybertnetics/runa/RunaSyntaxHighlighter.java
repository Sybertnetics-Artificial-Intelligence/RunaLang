package com.sybertnetics.runa;

import com.intellij.lexer.Lexer;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighterBase;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;

import static com.intellij.openapi.editor.colors.TextAttributesKey.createTextAttributesKey;

public class RunaSyntaxHighlighter extends SyntaxHighlighterBase {
    
    // Define highlighting colors
    public static final TextAttributesKey KEYWORD = 
            createTextAttributesKey("RUNA_KEYWORD", DefaultLanguageHighlighterColors.KEYWORD);
    public static final TextAttributesKey STRING = 
            createTextAttributesKey("RUNA_STRING", DefaultLanguageHighlighterColors.STRING);
    public static final TextAttributesKey NUMBER = 
            createTextAttributesKey("RUNA_NUMBER", DefaultLanguageHighlighterColors.NUMBER);
    public static final TextAttributesKey COMMENT = 
            createTextAttributesKey("RUNA_COMMENT", DefaultLanguageHighlighterColors.LINE_COMMENT);
    public static final TextAttributesKey FUNCTION = 
            createTextAttributesKey("RUNA_FUNCTION", DefaultLanguageHighlighterColors.FUNCTION_DECLARATION);
    public static final TextAttributesKey VARIABLE = 
            createTextAttributesKey("RUNA_VARIABLE", DefaultLanguageHighlighterColors.LOCAL_VARIABLE);
    public static final TextAttributesKey OPERATOR = 
            createTextAttributesKey("RUNA_OPERATOR", DefaultLanguageHighlighterColors.OPERATION_SIGN);
    public static final TextAttributesKey PARENTHESES = 
            createTextAttributesKey("RUNA_PARENTHESES", DefaultLanguageHighlighterColors.PARENTHESES);
    public static final TextAttributesKey BRACKETS = 
            createTextAttributesKey("RUNA_BRACKETS", DefaultLanguageHighlighterColors.BRACKETS);
    public static final TextAttributesKey BRACES = 
            createTextAttributesKey("RUNA_BRACES", DefaultLanguageHighlighterColors.BRACES);

    private static final TextAttributesKey[] KEYWORD_KEYS = new TextAttributesKey[]{KEYWORD};
    private static final TextAttributesKey[] STRING_KEYS = new TextAttributesKey[]{STRING};
    private static final TextAttributesKey[] NUMBER_KEYS = new TextAttributesKey[]{NUMBER};
    private static final TextAttributesKey[] COMMENT_KEYS = new TextAttributesKey[]{COMMENT};
    private static final TextAttributesKey[] FUNCTION_KEYS = new TextAttributesKey[]{FUNCTION};
    private static final TextAttributesKey[] VARIABLE_KEYS = new TextAttributesKey[]{VARIABLE};
    private static final TextAttributesKey[] OPERATOR_KEYS = new TextAttributesKey[]{OPERATOR};
    private static final TextAttributesKey[] PARENTHESES_KEYS = new TextAttributesKey[]{PARENTHESES};
    private static final TextAttributesKey[] BRACKETS_KEYS = new TextAttributesKey[]{BRACKETS};
    private static final TextAttributesKey[] BRACES_KEYS = new TextAttributesKey[]{BRACES};
    private static final TextAttributesKey[] EMPTY_KEYS = new TextAttributesKey[0];

    @NotNull
    @Override
    public Lexer getHighlightingLexer() {
        return new RunaLexerAdapter();
    }

    @NotNull
    @Override
    public TextAttributesKey[] getTokenHighlights(IElementType tokenType) {
        // This would need to be implemented based on the actual token types
        // For now, returning basic highlighting
        
        String tokenString = tokenType.toString();
        
        if (isKeyword(tokenString)) {
            return KEYWORD_KEYS;
        } else if (isString(tokenString)) {
            return STRING_KEYS;
        } else if (isNumber(tokenString)) {
            return NUMBER_KEYS;
        } else if (isComment(tokenString)) {
            return COMMENT_KEYS;
        } else if (isFunction(tokenString)) {
            return FUNCTION_KEYS;
        } else if (isOperator(tokenString)) {
            return OPERATOR_KEYS;
        } else if (tokenString.equals("(") || tokenString.equals(")")) {
            return PARENTHESES_KEYS;
        } else if (tokenString.equals("[") || tokenString.equals("]")) {
            return BRACKETS_KEYS;
        } else if (tokenString.equals("{") || tokenString.equals("}")) {
            return BRACES_KEYS;
        }
        
        return EMPTY_KEYS;
    }
    
    private boolean isKeyword(String token) {
        return token.equals("KEYWORD") || 
               token.equals("if") || token.equals("else") || token.equals("for") ||
               token.equals("while") || token.equals("function") || token.equals("let") ||
               token.equals("return") || token.equals("match") || token.equals("case") ||
               token.equals("try") || token.equals("catch") || token.equals("finally") ||
               token.equals("async") || token.equals("await") || token.equals("import") ||
               token.equals("export") || token.equals("from") || token.equals("as") ||
               token.equals("and") || token.equals("or") || token.equals("not") ||
               token.equals("true") || token.equals("false") || token.equals("null") ||
               token.equals("end");
    }
    
    private boolean isString(String token) {
        return token.equals("STRING") || token.startsWith("\"") || token.startsWith("'");
    }
    
    private boolean isNumber(String token) {
        return token.equals("NUMBER") || token.matches("\\d+(\\.\\d+)?");
    }
    
    private boolean isComment(String token) {
        return token.equals("COMMENT") || token.startsWith("#") || token.startsWith("/*");
    }
    
    private boolean isFunction(String token) {
        return token.equals("FUNCTION") || token.equals("print") || token.equals("input") ||
               token.equals("length") || token.equals("type") || token.equals("convert");
    }
    
    private boolean isOperator(String token) {
        return token.equals("OPERATOR") || token.equals("+") || token.equals("-") ||
               token.equals("*") || token.equals("/") || token.equals("=") ||
               token.equals("==") || token.equals("!=") || token.equals("<") ||
               token.equals(">") || token.equals("<=") || token.equals(">=");
    }
}