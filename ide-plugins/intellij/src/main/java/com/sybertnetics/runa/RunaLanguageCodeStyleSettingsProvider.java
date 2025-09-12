package com.sybertnetics.runa;

import com.intellij.application.options.IndentOptionsEditor;
import com.intellij.application.options.SmartIndentOptionsEditor;
import com.intellij.lang.Language;
import com.intellij.psi.codeStyle.CodeStyleSettingsCustomizable;
import com.intellij.psi.codeStyle.CommonCodeStyleSettings;
import com.intellij.psi.codeStyle.LanguageCodeStyleSettingsProvider;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Language-specific code style settings provider for Runa.
 */
public class RunaLanguageCodeStyleSettingsProvider extends LanguageCodeStyleSettingsProvider {
    
    @NotNull
    @Override
    public Language getLanguage() {
        return RunaLanguage.INSTANCE;
    }
    
    @Nullable
    @Override
    public IndentOptionsEditor getIndentOptionsEditor() {
        return new SmartIndentOptionsEditor();
    }
    
    @Override
    public String getCodeSample(@NotNull SettingsType settingsType) {
        return """
            Note: Runa code style example
            
            Let greeting be "Hello, World!"
            Define PI as 3.14159
            
            Process called "calculate area" that takes radius as Float returns Float:
                Let area be PI multiplied by radius multiplied by radius
                Return area
            
            If temperature is greater than 25:
                Display "It's warm!"
            Otherwise:
                Display "It's cool!"
            
            For each item in shopping_list:
                Display "Buy: " followed by item
            """;
    }
    
    @Override
    public void customizeSettings(@NotNull CodeStyleSettingsCustomizable consumer, 
                                  @NotNull SettingsType settingsType) {
        if (settingsType == SettingsType.SPACING_SETTINGS) {
            consumer.showStandardOptions("SPACE_AROUND_ASSIGNMENT_OPERATORS");
            consumer.showStandardOptions("SPACE_BEFORE_COMMA");
            consumer.showStandardOptions("SPACE_AFTER_COMMA");
        } else if (settingsType == SettingsType.INDENT_SETTINGS) {
            consumer.showStandardOptions("INDENT_SIZE");
            consumer.showStandardOptions("USE_TAB_CHARACTER");
            consumer.showStandardOptions("TAB_SIZE");
        } else if (settingsType == SettingsType.WRAPPING_AND_BRACES_SETTINGS) {
            consumer.showStandardOptions("RIGHT_MARGIN");
            consumer.showStandardOptions("WRAP_ON_TYPING");
        }
    }
    
    @Override
    public CommonCodeStyleSettings getDefaultCommonSettings() {
        CommonCodeStyleSettings defaultSettings = new CommonCodeStyleSettings(RunaLanguage.INSTANCE);
        CommonCodeStyleSettings.IndentOptions indentOptions = defaultSettings.getIndentOptions();
        indentOptions.INDENT_SIZE = 4;
        indentOptions.CONTINUATION_INDENT_SIZE = 4;
        indentOptions.TAB_SIZE = 4;
        indentOptions.USE_TAB_CHARACTER = false;
        return defaultSettings;
    }
}
