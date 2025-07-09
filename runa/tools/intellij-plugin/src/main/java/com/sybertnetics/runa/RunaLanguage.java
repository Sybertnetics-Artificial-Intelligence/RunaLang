package com.sybertnetics.runa;

import com.intellij.lang.Language;

public class RunaLanguage extends Language {
    public static final RunaLanguage INSTANCE = new RunaLanguage();

    private RunaLanguage() {
        super("Runa");
    }
}