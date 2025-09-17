package com.sybertnetics.runa;

import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NonNls;
import org.jetbrains.annotations.NotNull;

/**
 * Token type implementation for Runa language elements.
 */
public class RunaTokenType extends IElementType {
    
    public RunaTokenType(@NotNull @NonNls String debugName) {
        super(debugName, RunaLanguage.INSTANCE);
    }
    
    @Override
    public String toString() {
        return "RunaTokenType." + super.toString();
    }
}
