package com.sybertnetics.runa;

import com.intellij.extapi.psi.ASTWrapperPsiElement;
import com.intellij.lang.ASTNode;
import org.jetbrains.annotations.NotNull;

/**
 * Base PSI element for Runa language constructs.
 */
public class RunaPsiElement extends ASTWrapperPsiElement {
    
    public RunaPsiElement(@NotNull ASTNode node) {
        super(node);
    }
    
    @Override
    public String toString() {
        return getClass().getSimpleName() + "(" + getNode().getElementType().toString() + ")";
    }
}
