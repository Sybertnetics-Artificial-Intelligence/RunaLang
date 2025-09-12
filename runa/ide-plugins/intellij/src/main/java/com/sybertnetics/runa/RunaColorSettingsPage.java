package com.sybertnetics.runa;

import com.intellij.openapi.editor.colors.TextAttributesKey;
import com.intellij.openapi.fileTypes.SyntaxHighlighter;
import com.intellij.openapi.options.colors.AttributesDescriptor;
import com.intellij.openapi.options.colors.ColorDescriptor;
import com.intellij.openapi.options.colors.ColorSettingsPage;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import javax.swing.*;
import java.util.Map;

/**
 * Color settings page for Runa language.
 * Allows users to customize syntax highlighting colors.
 */
public class RunaColorSettingsPage implements ColorSettingsPage {
    
    private static final AttributesDescriptor[] DESCRIPTORS = new AttributesDescriptor[]{
        new AttributesDescriptor("Comments", RunaSyntaxHighlighter.COMMENT),
        new AttributesDescriptor("Keywords", RunaSyntaxHighlighter.KEYWORD),
        new AttributesDescriptor("Strings", RunaSyntaxHighlighter.STRING),
        new AttributesDescriptor("Numbers", RunaSyntaxHighlighter.NUMBER),
        new AttributesDescriptor("Identifiers", RunaSyntaxHighlighter.IDENTIFIER),
        new AttributesDescriptor("Natural Operators", RunaSyntaxHighlighter.NATURAL_OPERATOR),
        new AttributesDescriptor("Mathematical Symbols", RunaSyntaxHighlighter.MATH_SYMBOL),
        new AttributesDescriptor("Function Declarations", RunaSyntaxHighlighter.FUNCTION_DECLARATION),
        new AttributesDescriptor("Function Calls", RunaSyntaxHighlighter.FUNCTION_CALL),
        new AttributesDescriptor("Type Names", RunaSyntaxHighlighter.TYPE_NAME),
        new AttributesDescriptor("Variable Declarations", RunaSyntaxHighlighter.VARIABLE_DECLARATION),
        new AttributesDescriptor("Built-in Functions", RunaSyntaxHighlighter.BUILTIN_FUNCTION),
        new AttributesDescriptor("Control Flow Keywords", RunaSyntaxHighlighter.CONTROL_FLOW),
    };
    
    @Nullable
    @Override
    public Icon getIcon() {
        return RunaIcons.FILE;
    }
    
    @NotNull
    @Override
    public SyntaxHighlighter getHighlighter() {
        return new RunaSyntaxHighlighter();
    }
    
    @NotNull
    @Override
    public String getDemoText() {
        return """
            Note: Runa Language Syntax Demo
            Note:
            This demonstrates the natural language syntax
            and highlighting features of Runa
            :End Note
            
            Note: Variable declarations
            Let greeting be "Hello, World!"
            Define PI as 3.14159
            Set counter to counter plus 1
            
            Note: Function definition
            Process called "calculate area" that takes radius as Float returns Float:
                Let area be PI multiplied by radius multiplied by radius
                Return area
            
            Note: Control structures
            If temperature is greater than 25:
                Display "It's warm today!"
            Otherwise:
                Display "It's cool today!"
            
            For each item in shopping_list:
                Display "Buy: " followed by item
            
            Note: Collections
            Let numbers be list containing 1, 2, 3, 4, 5
            Let person be dictionary with:
                name as "Alice"
                age as 30
            
            Note: Function call
            Let circle_area be Calculate Area with radius as 5.0
            Display "Circle area: " followed by circle_area
            
            Note: Mathematical operations (natural language)
            Let result be a plus b multiplied by c
            Let comparison be x is greater than y
            
            Note: String operations
            Let full_name be first_name followed by " " followed by last_name
            """;
    }
    
    @Nullable
    @Override
    public Map<String, TextAttributesKey> getAdditionalHighlightingTagToDescriptorMap() {
        return null;
    }
    
    @NotNull
    @Override
    public AttributesDescriptor[] getAttributeDescriptors() {
        return DESCRIPTORS;
    }
    
    @NotNull
    @Override
    public ColorDescriptor[] getColorDescriptors() {
        return ColorDescriptor.EMPTY_ARRAY;
    }
    
    @NotNull
    @Override
    public String getDisplayName() {
        return "Runa";
    }
}
