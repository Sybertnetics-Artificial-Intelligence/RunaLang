package com.sybertnetics.runa;

import com.intellij.openapi.fileTypes.LanguageFileType;
import com.intellij.openapi.util.IconLoader;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;

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
        return "Runa language file";
    }

    @NotNull
    @Override
    public String getDefaultExtension() {
        return "runa";
    }

    @Nullable
    @Override
    public Icon getIcon() {
        return IconLoader.getIcon("/icons/runa.png", RunaFileType.class);
    }
}