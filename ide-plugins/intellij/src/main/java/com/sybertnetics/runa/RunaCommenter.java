package com.sybertnetics.runa;

import com.intellij.lang.Commenter;
import org.jetbrains.annotations.Nullable;

/**
 * Commenter for Runa language.
 * Handles comment/uncomment operations according to Runa's comment syntax.
 */
public class RunaCommenter implements Commenter {
    
    @Nullable
    @Override
    public String getLineCommentPrefix() {
        return "Note: ";
    }
    
    @Nullable
    @Override
    public String getBlockCommentPrefix() {
        return "Note:";
    }
    
    @Nullable
    @Override
    public String getBlockCommentSuffix() {
        return ":End Note";
    }
    
    @Nullable
    @Override
    public String getCommentedBlockCommentPrefix() {
        return null; // Not used in Runa
    }
    
    @Nullable
    @Override
    public String getCommentedBlockCommentSuffix() {
        return null; // Not used in Runa
    }
}
