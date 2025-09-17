package com.sybertnetics.runa;

import com.intellij.application.options.CodeStyleAbstractConfigurable;
import com.intellij.application.options.CodeStyleAbstractPanel;
import com.intellij.application.options.TabbedLanguageCodeStylePanel;
import com.intellij.openapi.options.Configurable;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import com.intellij.psi.codeStyle.CodeStyleSettingsProvider;
import com.intellij.psi.codeStyle.CustomCodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Code style settings provider for Runa language.
 */
public class RunaCodeStyleSettingsProvider extends CodeStyleSettingsProvider {
    
    @Override
    public CustomCodeStyleSettings createCustomSettings(CodeStyleSettings settings) {
        return new RunaCodeStyleSettings(settings);
    }
    
    @Nullable
    @Override
    public String getConfigurableDisplayName() {
        return "Runa";
    }
    
    @NotNull
    @Override
    public Configurable createSettingsPage(CodeStyleSettings settings, CodeStyleSettings modelSettings) {
        return new CodeStyleAbstractConfigurable(settings, modelSettings, "Runa") {
            @Override
            protected CodeStyleAbstractPanel createPanel(CodeStyleSettings settings) {
                return new RunaCodeStyleMainPanel(getCurrentSettings(), settings);
            }
            
            @Nullable
            @Override
            public String getHelpTopic() {
                return null;
            }
        };
    }
    
    private static class RunaCodeStyleMainPanel extends TabbedLanguageCodeStylePanel {
        public RunaCodeStyleMainPanel(CodeStyleSettings currentSettings, CodeStyleSettings settings) {
            super(RunaLanguage.INSTANCE, currentSettings, settings);
        }
    }
}
