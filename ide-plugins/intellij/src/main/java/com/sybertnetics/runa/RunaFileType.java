package com.sybertnetics.runa;

import com.intellij.openapi.fileTypes.LanguageFileType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

/**
 * File type definition for Runa programming language files (.runa extension).
 */
public class RunaFileType extends LanguageFileType {
    public static final RunaFileType INSTANCE = new RunaFileType();
    
    private RunaFileType() {
        super(RunaLanguage.INSTANCE);
    }
    
    @NotNull
    @Override
    public String getName() {
        return "Runa";
    }
    
    @NotNull
    @Override
    public String getDescription() {
        return "Runa programming language file";
    }
    
    @NotNull
    @Override
    public String getDefaultExtension() {
        return "runa";
    }
    
    @Nullable
    @Override
    public Icon getIcon() {
        return RunaIcons.FILE;
    }
    
    @Override
    public boolean isReadOnly() {
        return false;
    }
    
    @Nullable
    @Override
    public String getCharset(@NotNull com.intellij.openapi.vfs.VirtualFile file, 
                           @NotNull byte[] content) {
        return "UTF-8";
    }
}
