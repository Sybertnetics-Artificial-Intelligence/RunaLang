package com.sybertnetics.runa;

import com.intellij.lang.Language;

/**
 * Runa language definition for IntelliJ IDEA platform.
 * 
 * Runa is an AI-first natural programming language that uses pseudocode-like syntax
 * and enforces mathematical symbol restrictions for improved readability.
 */
public class RunaLanguage extends Language {
    public static final RunaLanguage INSTANCE = new RunaLanguage();
    
    private RunaLanguage() {
        super("Runa");
    }
    
    @Override
    public String getDisplayName() {
        return "Runa";
    }
    
    @Override
    public boolean isCaseSensitive() {
        return false; // Runa is case-insensitive according to the specification
    }
}
