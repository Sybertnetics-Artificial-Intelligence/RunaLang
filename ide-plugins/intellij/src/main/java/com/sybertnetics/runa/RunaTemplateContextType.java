package com.sybertnetics.runa;

import com.intellij.codeInsight.template.TemplateActionContext;
import com.intellij.codeInsight.template.TemplateContextType;
import org.jetbrains.annotations.NotNull;

/**
 * Template context type for Runa live templates.
 * Determines when Runa-specific templates should be available.
 */
public class RunaTemplateContextType extends TemplateContextType {
    
    protected RunaTemplateContextType() {
        super("RUNA", "Runa");
    }
    
    @Override
    public boolean isInContext(@NotNull TemplateActionContext templateActionContext) {
        return templateActionContext.getFile() instanceof RunaFile;
    }
}
