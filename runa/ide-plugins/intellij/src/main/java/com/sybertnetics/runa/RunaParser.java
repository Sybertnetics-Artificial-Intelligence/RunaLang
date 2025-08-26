package com.sybertnetics.runa;

import com.intellij.lang.ASTNode;
import com.intellij.lang.PsiBuilder;
import com.intellij.lang.PsiParser;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;

/**
 * Parser for the Runa programming language.
 * This is a simple parser that creates a basic AST structure for Runa code.
 */
public class RunaParser implements PsiParser {
    
    @NotNull
    @Override
    public ASTNode parse(@NotNull IElementType root, @NotNull PsiBuilder builder) {
        PsiBuilder.Marker rootMarker = builder.mark();
        
        while (!builder.eof()) {
            parseStatement(builder);
        }
        
        rootMarker.done(root);
        return builder.getTreeBuilt();
    }
    
    private void parseStatement(@NotNull PsiBuilder builder) {
        IElementType tokenType = builder.getTokenType();
        
        if (tokenType == null) {
            builder.advanceLexer();
            return;
        }
        
        // Skip whitespace and comments
        if (RunaParserDefinition.WHITESPACES.contains(tokenType) || 
            RunaParserDefinition.COMMENTS.contains(tokenType)) {
            builder.advanceLexer();
            return;
        }
        
        // Parse different types of statements based on starting token
        if (tokenType == RunaTokenTypes.LET_KEYWORD || 
            (tokenType == RunaTokenTypes.KEYWORD && "Let".equals(builder.getTokenText()))) {
            parseLetStatement(builder);
        } else if (tokenType == RunaTokenTypes.DEFINE_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "Define".equals(builder.getTokenText()))) {
            parseDefineStatement(builder);
        } else if (tokenType == RunaTokenTypes.SET_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "Set".equals(builder.getTokenText()))) {
            parseSetStatement(builder);
        } else if (tokenType == RunaTokenTypes.PROCESS_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "Process".equals(builder.getTokenText()))) {
            parseProcessStatement(builder);
        } else if (tokenType == RunaTokenTypes.IF_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "If".equals(builder.getTokenText()))) {
            parseIfStatement(builder);
        } else if (tokenType == RunaTokenTypes.FOR_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "For".equals(builder.getTokenText()))) {
            parseForStatement(builder);
        } else if (tokenType == RunaTokenTypes.WHILE_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "While".equals(builder.getTokenText()))) {
            parseWhileStatement(builder);
        } else if (tokenType == RunaTokenTypes.DISPLAY_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "Display".equals(builder.getTokenText()))) {
            parseDisplayStatement(builder);
        } else if (tokenType == RunaTokenTypes.RETURN_KEYWORD || 
                  (tokenType == RunaTokenTypes.KEYWORD && "Return".equals(builder.getTokenText()))) {
            parseReturnStatement(builder);
        } else {
            // Parse as expression statement
            parseExpression(builder);
        }
    }
    
    private void parseLetStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "Let"
        builder.advanceLexer();
        
        // Parse identifier
        if (builder.getTokenType() == RunaTokenTypes.IDENTIFIER) {
            builder.advanceLexer();
        }
        
        // Look for "be" keyword
        if (builder.getTokenType() == RunaTokenTypes.BE_KEYWORD || 
            (builder.getTokenType() == RunaTokenTypes.KEYWORD && "be".equalsIgnoreCase(builder.getTokenText()))) {
            builder.advanceLexer();
        }
        
        // Parse expression
        parseExpression(builder);
        
        marker.done(RunaElementTypes.LET_STATEMENT);
    }
    
    private void parseDefineStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "Define"
        builder.advanceLexer();
        
        // Optional "constant" keyword
        if (builder.getTokenType() == RunaTokenTypes.KEYWORD && "constant".equalsIgnoreCase(builder.getTokenText())) {
            builder.advanceLexer();
        }
        
        // Parse identifier
        if (builder.getTokenType() == RunaTokenTypes.IDENTIFIER) {
            builder.advanceLexer();
        }
        
        // Look for "as" keyword
        if (builder.getTokenType() == RunaTokenTypes.AS_KEYWORD || 
            (builder.getTokenType() == RunaTokenTypes.KEYWORD && "as".equalsIgnoreCase(builder.getTokenText()))) {
            builder.advanceLexer();
        }
        
        // Parse expression
        parseExpression(builder);
        
        marker.done(RunaElementTypes.DEFINE_STATEMENT);
    }
    
    private void parseSetStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "Set"
        builder.advanceLexer();
        
        // Parse identifier
        if (builder.getTokenType() == RunaTokenTypes.IDENTIFIER) {
            builder.advanceLexer();
        }
        
        // Look for "to" keyword
        if (builder.getTokenType() == RunaTokenTypes.TO_KEYWORD || 
            (builder.getTokenType() == RunaTokenTypes.KEYWORD && "to".equalsIgnoreCase(builder.getTokenText()))) {
            builder.advanceLexer();
        }
        
        // Parse expression
        parseExpression(builder);
        
        marker.done(RunaElementTypes.SET_STATEMENT);
    }
    
    private void parseProcessStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "Process"
        builder.advanceLexer();
        
        // Look for "called" keyword
        if (builder.getTokenType() == RunaTokenTypes.CALLED_KEYWORD || 
            (builder.getTokenType() == RunaTokenTypes.KEYWORD && "called".equalsIgnoreCase(builder.getTokenText()))) {
            builder.advanceLexer();
        }
        
        // Parse function name (string literal)
        if (builder.getTokenType() == RunaTokenTypes.STRING_LITERAL) {
            builder.advanceLexer();
        }
        
        // Parse optional parameters and return type
        parseToEndOfLine(builder);
        
        marker.done(RunaElementTypes.PROCESS_STATEMENT);
    }
    
    private void parseIfStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "If"
        builder.advanceLexer();
        
        // Parse condition
        parseExpression(builder);
        
        // Look for colon
        if (builder.getTokenType() == RunaTokenTypes.COLON || 
            builder.getTokenType() == RunaTokenTypes.PUNCTUATION && ":".equals(builder.getTokenText())) {
            builder.advanceLexer();
        }
        
        marker.done(RunaElementTypes.IF_STATEMENT);
    }
    
    private void parseForStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "For"
        builder.advanceLexer();
        
        // Parse the rest of the for statement
        parseToEndOfLine(builder);
        
        marker.done(RunaElementTypes.FOR_STATEMENT);
    }
    
    private void parseWhileStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "While"
        builder.advanceLexer();
        
        // Parse condition
        parseExpression(builder);
        
        // Look for colon
        if (builder.getTokenType() == RunaTokenTypes.COLON || 
            builder.getTokenType() == RunaTokenTypes.PUNCTUATION && ":".equals(builder.getTokenText())) {
            builder.advanceLexer();
        }
        
        marker.done(RunaElementTypes.WHILE_STATEMENT);
    }
    
    private void parseDisplayStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "Display"
        builder.advanceLexer();
        
        // Parse expression
        parseExpression(builder);
        
        marker.done(RunaElementTypes.DISPLAY_STATEMENT);
    }
    
    private void parseReturnStatement(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Consume "Return"
        builder.advanceLexer();
        
        // Parse optional expression
        parseExpression(builder);
        
        marker.done(RunaElementTypes.RETURN_STATEMENT);
    }
    
    private void parseExpression(@NotNull PsiBuilder builder) {
        PsiBuilder.Marker marker = builder.mark();
        
        // Simple expression parsing - consume tokens until end of line or statement terminator
        parseToEndOfLine(builder);
        
        marker.done(RunaElementTypes.EXPRESSION);
    }
    
    private void parseToEndOfLine(@NotNull PsiBuilder builder) {
        while (!builder.eof() && 
               builder.getTokenType() != RunaTokenTypes.NEWLINE &&
               !isStatementStart(builder.getTokenType())) {
            builder.advanceLexer();
        }
        
        // Consume newline if present
        if (builder.getTokenType() == RunaTokenTypes.NEWLINE) {
            builder.advanceLexer();
        }
    }
    
    private boolean isStatementStart(IElementType tokenType) {
        return tokenType == RunaTokenTypes.LET_KEYWORD ||
               tokenType == RunaTokenTypes.DEFINE_KEYWORD ||
               tokenType == RunaTokenTypes.SET_KEYWORD ||
               tokenType == RunaTokenTypes.PROCESS_KEYWORD ||
               tokenType == RunaTokenTypes.IF_KEYWORD ||
               tokenType == RunaTokenTypes.FOR_KEYWORD ||
               tokenType == RunaTokenTypes.WHILE_KEYWORD ||
               tokenType == RunaTokenTypes.DISPLAY_KEYWORD ||
               tokenType == RunaTokenTypes.RETURN_KEYWORD ||
               (tokenType == RunaTokenTypes.KEYWORD && isStatementKeyword(builder.getTokenText()));
    }
    
    private boolean isStatementKeyword(String text) {
        if (text == null) return false;
        return text.equals("Let") || text.equals("Define") || text.equals("Set") ||
               text.equals("Process") || text.equals("If") || text.equals("For") ||
               text.equals("While") || text.equals("Display") || text.equals("Return");
    }
}
