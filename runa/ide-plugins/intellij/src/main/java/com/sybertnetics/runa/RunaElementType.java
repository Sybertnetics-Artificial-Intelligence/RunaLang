package com.sybertnetics.runa;

import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

/**
 * Element type implementation for Runa language AST nodes.
 */
public class RunaElementType extends IElementType {
    
    public RunaElementType(@NotNull @NonNls String debugName) {
        super(debugName, RunaLanguage.INSTANCE);
    }
    
    @Override
    public String toString() {
        return "RunaElementType." + super.toString();
    }
}
