package com.sybertnetics.runa;

import com.intellij.extapi.psi.PsiFileBase;
import com.intellij.openapi.fileTypes.FileType;
import com.intellij.psi.FileViewProvider;
import org.jetbrains.annotations.NotNull;

/**
 * PSI file representation for Runa source files.
 */
public class RunaFile extends PsiFileBase {
    
    public RunaFile(@NotNull FileViewProvider viewProvider) {
        super(viewProvider, RunaLanguage.INSTANCE);
    }
    
    @NotNull
    @Override
    public FileType getFileType() {
        return RunaFileType.INSTANCE;
    }
    
    @Override
    public String toString() {
        return "Runa File";
    }
}
