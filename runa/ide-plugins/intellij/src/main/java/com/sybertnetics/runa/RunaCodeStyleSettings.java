package com.sybertnetics.runa;

import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;

/**
 * Custom code style settings for Runa language.
 */
public class RunaCodeStyleSettings extends CustomCodeStyleSettings {
    
    public boolean SPACE_AROUND_OPERATORS = true;
    public boolean SPACE_BEFORE_COLON = false;
    public boolean SPACE_AFTER_COLON = true;
    public boolean CONVERT_SYMBOLS_TO_WORDS = true;
    public boolean ENFORCE_NATURAL_LANGUAGE = true;
    
    public RunaCodeStyleSettings(CodeStyleSettings settings) {
        super("RunaCodeStyleSettings", settings);
    }
}
