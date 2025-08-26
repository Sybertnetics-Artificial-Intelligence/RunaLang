package com.sybertnetics.runa;

import com.intellij.lang.annotation.AnnotationHolder;
import com.intellij.lang.annotation.Annotator;
import com.intellij.lang.annotation.HighlightSeverity;
import com.intellij.openapi.editor.DefaultLanguageHighlighterColors;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import org.jetbrains.annotations.NotNull;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Annotator for Runa language that provides real-time error detection and warnings.
 * Implements mathematical symbol enforcement according to the Runa language specification.
 */
public class RunaAnnotator implements Annotator {
    
    private static final Pattern MATH_SYMBOLS = Pattern.compile("[+\\-*/%<>=!]+");
    private static final Pattern STRING_LITERAL = Pattern.compile("^[\"'].*[\"']$");
    private static final Pattern COMMENT_LINE = Pattern.compile("^\\s*Note:");
    
    @Override
    public void annotate(@NotNull PsiElement element, @NotNull AnnotationHolder holder) {
        // Skip comments and string literals
        String elementText = element.getText();
        if (COMMENT_LINE.matcher(elementText).find() || STRING_LITERAL.matcher(elementText).matches()) {
            return;
        }
        
        // Check for mathematical symbol enforcement
        checkMathematicalSymbolUsage(element, holder);
        
        // Check for common syntax errors
        checkSyntaxErrors(element, holder);
        
        // Highlight special constructs
        highlightSpecialConstructs(element, holder);
    }
    
    private void checkMathematicalSymbolUsage(@NotNull PsiElement element, @NotNull AnnotationHolder holder) {
        String text = element.getText();
        Matcher matcher = MATH_SYMBOLS.matcher(text);
        
        while (matcher.find()) {
            String symbol = matcher.group();
            
            // Check if this is in a mathematical context
            if (!isInMathematicalContext(element, matcher.start())) {
                TextRange range = TextRange.from(element.getTextRange().getStartOffset() + matcher.start(), symbol.length());
                
                holder.newAnnotation(HighlightSeverity.WARNING,
                    "Mathematical symbol '" + symbol + "' should only be used in mathematical contexts. " +
                    "Consider using natural language equivalent: " + getRecommendedReplacement(symbol))
                    .range(range)
                    .withFix(new ConvertSymbolToWordsFix(symbol))
                    .create();
            }
        }
    }
    
    private void checkSyntaxErrors(@NotNull PsiElement element, @NotNull AnnotationHolder holder) {
        String text = element.getText().trim();
        
        // Check for common mistakes
        if (text.startsWith("let ") && !text.contains(" be ")) {
            holder.newAnnotation(HighlightSeverity.ERROR,
                "Variable declaration should use 'Let variable be value' syntax")
                .range(element.getTextRange())
                .create();
        }
        
        if (text.startsWith("set ") && !text.contains(" to ")) {
            holder.newAnnotation(HighlightSeverity.ERROR,
                "Variable assignment should use 'Set variable to value' syntax")
                .range(element.getTextRange())
                .create();
        }
        
        if (text.startsWith("define ") && !text.contains(" as ")) {
            holder.newAnnotation(HighlightSeverity.ERROR,
                "Constant definition should use 'Define constant as value' syntax")
                .range(element.getTextRange())
                .create();
        }
        
        // Check for missing colons in control structures
        if ((text.startsWith("If ") || text.startsWith("For ") || text.startsWith("While ") || 
             text.startsWith("Process ")) && !text.endsWith(":")) {
            holder.newAnnotation(HighlightSeverity.ERROR,
                "Control structure should end with a colon (:)")
                .range(element.getTextRange())
                .create();
        }
    }
    
    private void highlightSpecialConstructs(@NotNull PsiElement element, @NotNull AnnotationHolder holder) {
        String text = element.getText();
        
        // Highlight function names in process declarations
        if (text.contains("Process called")) {
            Pattern functionNamePattern = Pattern.compile("\"([^\"]+)\"");
            Matcher matcher = functionNamePattern.matcher(text);
            
            while (matcher.find()) {
                TextRange range = TextRange.from(
                    element.getTextRange().getStartOffset() + matcher.start(1), 
                    matcher.group(1).length());
                
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(range)
                    .textAttributes(DefaultLanguageHighlighterColors.FUNCTION_DECLARATION)
                    .create();
            }
        }
        
        // Highlight variable names in Let statements
        if (text.startsWith("Let ")) {
            Pattern varPattern = Pattern.compile("Let\\s+([a-zA-Z_][a-zA-Z0-9_\\s]*)\\s+be");
            Matcher matcher = varPattern.matcher(text);
            
            if (matcher.find()) {
                TextRange range = TextRange.from(
                    element.getTextRange().getStartOffset() + matcher.start(1), 
                    matcher.group(1).length());
                
                holder.newSilentAnnotation(HighlightSeverity.INFORMATION)
                    .range(range)
                    .textAttributes(DefaultLanguageHighlighterColors.LOCAL_VARIABLE)
                    .create();
            }
        }
    }
    
    private boolean isInMathematicalContext(@NotNull PsiElement element, int symbolOffset) {
        // Simple heuristic: if surrounded by numbers or numeric variables, likely mathematical
        String text = element.getText();
        
        // Check before symbol
        boolean hasNumberBefore = false;
        if (symbolOffset > 0) {
            char before = text.charAt(symbolOffset - 1);
            hasNumberBefore = Character.isDigit(before) || Character.isWhitespace(before);
        }
        
        // Check after symbol
        boolean hasNumberAfter = false;
        if (symbolOffset < text.length() - 1) {
            char after = text.charAt(symbolOffset + 1);
            hasNumberAfter = Character.isDigit(after) || Character.isWhitespace(after);
        }
        
        // If we're in a string concatenation context, probably not mathematical
        boolean inStringContext = text.contains("followed by") || text.contains("\"") || text.contains("'");
        
        return (hasNumberBefore || hasNumberAfter) && !inStringContext;
    }
    
    private String getRecommendedReplacement(String symbol) {
        switch (symbol) {
            case "+": return "plus";
            case "-": return "minus";
            case "*": return "multiplied by";
            case "/": return "divided by";
            case "%": return "modulo";
            case "==": return "equals";
            case "!=": return "does not equal";
            case ">": return "is greater than";
            case "<": return "is less than";
            case ">=": return "is greater than or equal to";
            case "<=": return "is less than or equal to";
            default: return "natural language equivalent";
        }
    }
    
    /**
     * Quick fix for converting mathematical symbols to natural language.
     */
    private static class ConvertSymbolToWordsFix {
        private final String symbol;
        
        public ConvertSymbolToWordsFix(String symbol) {
            this.symbol = symbol;
        }
        
        // Implementation would go here for the actual quick fix
        // This is a simplified version for the basic plugin
    }
}
