package com.sybertnetics.runa;

import com.intellij.lang.BracePair;
import com.intellij.lang.PairedBraceMatcher;
import com.intellij.psi.PsiFile;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Brace matcher for Runa language.
 * Handles matching of parentheses, brackets, and braces.
 */
public class RunaBraceMatcher implements PairedBraceMatcher {
    
    private static final BracePair[] PAIRS = new BracePair[]{
        new BracePair(RunaTokenTypes.LPAREN, RunaTokenTypes.RPAREN, false),
        new BracePair(RunaTokenTypes.LBRACKET, RunaTokenTypes.RBRACKET, false),
        new BracePair(RunaTokenTypes.LBRACE, RunaTokenTypes.RBRACE, true)
    };
    
    @NotNull
    @Override
    public BracePair[] getPairs() {
        return PAIRS;
    }
    
    @Override
    public boolean isPairedBracesAllowedBeforeType(@NotNull IElementType lbraceType, 
                                                   @Nullable IElementType contextType) {
        return true;
    }
    
    @Override
    public int getCodeConstructStart(PsiFile file, int openingBraceOffset) {
        return openingBraceOffset;
    }
}
