package com.sybertnetics.runa;

import com.intellij.codeInsight.completion.*;
import com.intellij.codeInsight.lookup.LookupElementBuilder;
import com.intellij.patterns.PlatformPatterns;
import com.intellij.util.ProcessingContext;
import org.jetbrains.annotations.NotNull;

/**
 * Completion contributor for Runa language.
 * Provides intelligent code completion for keywords, operators, and built-in functions.
 */
public class RunaCompletionContributor extends CompletionContributor {
    
    public RunaCompletionContributor() {
        // Complete anywhere in Runa files
        extend(CompletionType.BASIC,
               PlatformPatterns.psiElement().inFile(PlatformPatterns.psiFile(RunaFile.class)),
               new RunaCompletionProvider());
    }
    
    private static class RunaCompletionProvider extends CompletionProvider<CompletionParameters> {
        
        @Override
        protected void addCompletions(@NotNull CompletionParameters parameters,
                                    @NotNull ProcessingContext context,
                                    @NotNull CompletionResultSet resultSet) {
            
            // Runa keywords
            String[] keywords = {
                "Let", "Define", "Set", "If", "Otherwise", "Unless", "When", "Match",
                "Process", "Type", "Import", "Export", "Try", "Catch", "Finally",
                "For", "While", "Loop", "Return", "Yield", "Break", "Continue",
                "Throw", "Assert", "Display", "Delete", "Await", "Send", "Receive",
                "Spawn", "New", "Static", "Public", "Private", "Async", "External",
                "Protocol", "With", "As", "From", "To", "By", "In", "Of",
                "And", "Or", "Not", "Is", "Be"
            };
            
            for (String keyword : keywords) {
                resultSet.addElement(LookupElementBuilder.create(keyword)
                    .withIcon(RunaIcons.FILE_FALLBACK)
                    .withTypeText("keyword")
                    .bold());
            }
            
            // Natural language operators
            String[] operators = {
                "plus", "minus", "multiplied by", "divided by", "modulo",
                "equals", "does not equal", "is greater than", "is less than",
                "is greater than or equal to", "is less than or equal to",
                "contains", "is in", "followed by", "joined with", "to the power of"
            };
            
            for (String operator : operators) {
                resultSet.addElement(LookupElementBuilder.create(operator)
                    .withIcon(RunaIcons.FILE_FALLBACK)
                    .withTypeText("operator")
                    .withTailText(" (natural language)")
                    .withInsertHandler(new BasicInsertHandler<>()));
            }
            
            // Built-in functions
            String[] builtins = {
                "Display", "Input", "Length", "Type", "Convert", "Parse", "Format",
                "Range", "Enumerate", "Zip", "Map", "Filter", "Reduce", "Sort",
                "Reverse", "Split", "Join", "Replace", "Contains", "Starts_with",
                "Ends_with", "Uppercase", "Lowercase", "Trim"
            };
            
            for (String builtin : builtins) {
                resultSet.addElement(LookupElementBuilder.create(builtin)
                    .withIcon(RunaIcons.FUNCTION_FALLBACK)
                    .withTypeText("built-in function")
                    .withTailText("()")
                    .withInsertHandler(new BasicInsertHandler<>()));
            }
            
            // Data types
            String[] types = {
                "Integer", "Float", "String", "Boolean", "List", "Dictionary",
                "Function", "Optional", "Any", "Void"
            };
            
            for (String type : types) {
                resultSet.addElement(LookupElementBuilder.create(type)
                    .withIcon(RunaIcons.TYPE_FALLBACK)
                    .withTypeText("type")
                    .withInsertHandler(new BasicInsertHandler<>()));
            }
            
            // Common patterns and snippets
            addPatternCompletions(resultSet);
            
            // Boolean literals
            resultSet.addElement(LookupElementBuilder.create("true")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("boolean"));
            resultSet.addElement(LookupElementBuilder.create("false")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("boolean"));
            
            // Null values
            resultSet.addElement(LookupElementBuilder.create("null")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("null"));
            resultSet.addElement(LookupElementBuilder.create("none")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("null"));
            resultSet.addElement(LookupElementBuilder.create("nil")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("null"));
        }
        
        private void addPatternCompletions(@NotNull CompletionResultSet resultSet) {
            // Variable declaration patterns
            resultSet.addElement(LookupElementBuilder.create("Let variable be value")
                .withIcon(RunaIcons.VARIABLE_FALLBACK)
                .withTypeText("variable declaration")
                .withTailText(" (pattern)")
                .withInsertHandler((context, item) -> {
                    context.getEditor().getCaretModel().moveToOffset(
                        context.getStartOffset() + "Let ".length());
                }));
            
            // Function definition pattern
            resultSet.addElement(LookupElementBuilder.create("Process called \"function_name\" that takes parameter as Type returns Type:")
                .withIcon(RunaIcons.FUNCTION_FALLBACK)
                .withTypeText("function definition")
                .withTailText(" (pattern)")
                .withInsertHandler((context, item) -> {
                    context.getEditor().getCaretModel().moveToOffset(
                        context.getStartOffset() + "Process called \"".length());
                }));
            
            // If statement pattern
            resultSet.addElement(LookupElementBuilder.create("If condition:")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("conditional")
                .withTailText(" (pattern)")
                .withInsertHandler((context, item) -> {
                    context.getEditor().getCaretModel().moveToOffset(
                        context.getStartOffset() + "If ".length());
                }));
            
            // For each loop pattern
            resultSet.addElement(LookupElementBuilder.create("For each item in collection:")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("loop")
                .withTailText(" (pattern)")
                .withInsertHandler((context, item) -> {
                    context.getEditor().getCaretModel().moveToOffset(
                        context.getStartOffset() + "For each ".length());
                }));
            
            // List creation pattern
            resultSet.addElement(LookupElementBuilder.create("list containing item1, item2")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("list")
                .withTailText(" (pattern)")
                .withInsertHandler((context, item) -> {
                    context.getEditor().getCaretModel().moveToOffset(
                        context.getStartOffset() + "list containing ".length());
                }));
            
            // Dictionary creation pattern
            resultSet.addElement(LookupElementBuilder.create("dictionary with:\\n    key as value")
                .withIcon(RunaIcons.FILE_FALLBACK)
                .withTypeText("dictionary")
                .withTailText(" (pattern)")
                .withInsertHandler((context, item) -> {
                    context.getEditor().getCaretModel().moveToOffset(
                        context.getStartOffset() + "dictionary with:\\n    ".length());
                }));
        }
    }
}
