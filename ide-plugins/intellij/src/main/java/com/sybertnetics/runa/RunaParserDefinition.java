package com.sybertnetics.runa;

import com.intellij.lang.ASTNode;
import com.intellij.lang.ParserDefinition;
import com.intellij.lang.PsiParser;
import com.intellij.lexer.Lexer;
import com.intellij.openapi.project.Project;
import com.intellij.psi.FileViewProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IFileElementType;
import com.intellij.psi.tree.TokenSet;
import org.jetbrains.annotations.NotNull;

/**
 * Parser definition for the Runa programming language.
 * Defines how Runa source code should be parsed into PSI (Program Structure Interface) elements.
 */
public class RunaParserDefinition implements ParserDefinition {
    
    public static final IFileElementType RUNA_FILE = new IFileElementType("RUNA_FILE", RunaLanguage.INSTANCE);
    
    public static final TokenSet COMMENTS = TokenSet.create(RunaTokenTypes.COMMENT);
    public static final TokenSet STRINGS = TokenSet.create(RunaTokenTypes.STRING_LITERAL);
    public static final TokenSet WHITESPACES = TokenSet.create(RunaTokenTypes.WHITESPACE, RunaTokenTypes.NEWLINE);
    
    @NotNull
    @Override
    public Lexer createLexer(Project project) {
        return new RunaLexer();
    }
    
    @NotNull
    @Override
    public PsiParser createParser(Project project) {
        return new RunaParser();
    }
    
    @NotNull
    @Override
    public IFileElementType getFileNodeType() {
        return RUNA_FILE;
    }
    
    @NotNull
    @Override
    public TokenSet getCommentTokens() {
        return COMMENTS;
    }
    
    @NotNull
    @Override
    public TokenSet getStringLiteralElements() {
        return STRINGS;
    }
    
    @NotNull
    @Override
    public TokenSet getWhitespaceTokens() {
        return WHITESPACES;
    }
    
    @NotNull
    @Override
    public PsiElement createElement(ASTNode node) {
        return new RunaPsiElement(node);
    }
    
    @NotNull
    @Override
    public PsiFile createFile(@NotNull FileViewProvider viewProvider) {
        return new RunaFile(viewProvider);
    }
}
