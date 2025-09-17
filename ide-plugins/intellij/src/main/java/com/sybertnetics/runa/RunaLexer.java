package com.sybertnetics.runa;

import com.intellij.lexer.LexerBase;
import com.intellij.psi.tree.IElementType;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Lexer for the Runa programming language.
 * Tokenizes Runa source code according to the language specification.
 */
public class RunaLexer extends LexerBase {
    private CharSequence buffer;
    private int startOffset;
    private int endOffset;
    private int currentOffset;
    private IElementType currentTokenType;
    private int currentTokenStart;
    private int currentTokenEnd;
    
    // Runa keywords according to specification
    private static final Set<String> KEYWORDS = new HashSet<>();
    static {
        KEYWORDS.add("Let");
        KEYWORDS.add("Define");
        KEYWORDS.add("Set");
        KEYWORDS.add("If");
        KEYWORDS.add("Otherwise");
        KEYWORDS.add("Unless");
        KEYWORDS.add("When");
        KEYWORDS.add("Match");
        KEYWORDS.add("Process");
        KEYWORDS.add("Type");
        KEYWORDS.add("Import");
        KEYWORDS.add("Export");
        KEYWORDS.add("Try");
        KEYWORDS.add("Catch");
        KEYWORDS.add("Finally");
        KEYWORDS.add("For");
        KEYWORDS.add("While");
        KEYWORDS.add("Loop");
        KEYWORDS.add("Return");
        KEYWORDS.add("Yield");
        KEYWORDS.add("Break");
        KEYWORDS.add("Continue");
        KEYWORDS.add("Throw");
        KEYWORDS.add("Assert");
        KEYWORDS.add("Display");
        KEYWORDS.add("Delete");
        KEYWORDS.add("Await");
        KEYWORDS.add("Send");
        KEYWORDS.add("Receive");
        KEYWORDS.add("Spawn");
        KEYWORDS.add("New");
        KEYWORDS.add("Static");
        KEYWORDS.add("Public");
        KEYWORDS.add("Private");
        KEYWORDS.add("Async");
        KEYWORDS.add("External");
        KEYWORDS.add("Protocol");
        KEYWORDS.add("With");
        KEYWORDS.add("As");
        KEYWORDS.add("From");
        KEYWORDS.add("To");
        KEYWORDS.add("By");
        KEYWORDS.add("In");
        KEYWORDS.add("Of");
        KEYWORDS.add("And");
        KEYWORDS.add("Or");
        KEYWORDS.add("Not");
        KEYWORDS.add("Is");
        KEYWORDS.add("Be");
        KEYWORDS.add("Plus");
        KEYWORDS.add("Minus");
        KEYWORDS.add("Times");
        KEYWORDS.add("Multiplied");
        KEYWORDS.add("Divided");
        KEYWORDS.add("Modulo");
        KEYWORDS.add("Power");
        KEYWORDS.add("Equal");
        KEYWORDS.add("Greater");
        KEYWORDS.add("Less");
        KEYWORDS.add("Than");
        KEYWORDS.add("Contains");
        KEYWORDS.add("True");
        KEYWORDS.add("False");
        KEYWORDS.add("None");
        KEYWORDS.add("Null");
        KEYWORDS.add("Nil");
    }
    
    // Natural language operators
    private static final Set<String> NATURAL_OPERATORS = new HashSet<>();
    static {
        NATURAL_OPERATORS.add("plus");
        NATURAL_OPERATORS.add("minus");
        NATURAL_OPERATORS.add("multiplied by");
        NATURAL_OPERATORS.add("divided by");
        NATURAL_OPERATORS.add("modulo");
        NATURAL_OPERATORS.add("equals");
        NATURAL_OPERATORS.add("does not equal");
        NATURAL_OPERATORS.add("is greater than");
        NATURAL_OPERATORS.add("is less than");
        NATURAL_OPERATORS.add("is greater than or equal to");
        NATURAL_OPERATORS.add("is less than or equal to");
        NATURAL_OPERATORS.add("contains");
        NATURAL_OPERATORS.add("is in");
        NATURAL_OPERATORS.add("followed by");
        NATURAL_OPERATORS.add("joined with");
    }
    
    // Regular expressions for different token types
    private static final Pattern COMMENT_SINGLE = Pattern.compile("^Note:.*");
    private static final Pattern COMMENT_BLOCK_START = Pattern.compile("^Note:\\s*$");
    private static final Pattern COMMENT_BLOCK_END = Pattern.compile("^\\s*:End Note\\s*$");
    private static final Pattern STRING_DOUBLE = Pattern.compile("^\"([^\"\\\\]|\\\\.)*\"");
    private static final Pattern STRING_SINGLE = Pattern.compile("^'([^'\\\\]|\\\\.)*'");
    private static final Pattern STRING_RAW_DOUBLE = Pattern.compile("^r\"[^\"]*\"");
    private static final Pattern STRING_RAW_SINGLE = Pattern.compile("^r'[^']*'");
    private static final Pattern STRING_FORMATTED = Pattern.compile("^f[\"']([^\"'\\\\]|\\\\.)*[\"']");
    private static final Pattern NUMBER_FLOAT = Pattern.compile("^\\d[\\d_]*\\.\\d[\\d_]*");
    private static final Pattern NUMBER_HEX = Pattern.compile("^0x[0-9a-fA-F][0-9a-fA-F_]*");
    private static final Pattern NUMBER_BINARY = Pattern.compile("^0b[01][01_]*");
    private static final Pattern NUMBER_OCTAL = Pattern.compile("^0o[0-7][0-7_]*");
    private static final Pattern NUMBER_DECIMAL = Pattern.compile("^\\d[\\d_]*");
    private static final Pattern IDENTIFIER = Pattern.compile("^[a-zA-Z_][a-zA-Z0-9_]*");
    private static final Pattern MULTI_WORD_IDENTIFIER = Pattern.compile("^[a-zA-Z_][a-zA-Z0-9_]*(?:\\s+[a-zA-Z_][a-zA-Z0-9_]*)+");
    private static final Pattern WHITESPACE = Pattern.compile("^\\s+");
    private static final Pattern MATH_SYMBOLS = Pattern.compile("^[+\\-*/%<>=!]+");
    private static final Pattern PUNCTUATION = Pattern.compile("^[()\\[\\]{}:,.]");
    
    @Override
    public void start(@NotNull CharSequence buffer, int startOffset, int endOffset, int initialState) {
        this.buffer = buffer;
        this.startOffset = startOffset;
        this.endOffset = endOffset;
        this.currentOffset = startOffset;
        advance();
    }
    
    @Override
    public int getState() {
        return 0; // Simple lexer without states
    }
    
    @Nullable
    @Override
    public IElementType getTokenType() {
        return currentTokenType;
    }
    
    @Override
    public int getTokenStart() {
        return currentTokenStart;
    }
    
    @Override
    public int getTokenEnd() {
        return currentTokenEnd;
    }
    
    @Override
    public void advance() {
        if (currentOffset >= endOffset) {
            currentTokenType = null;
            return;
        }
        
        currentTokenStart = currentOffset;
        CharSequence remainingBuffer = buffer.subSequence(currentOffset, endOffset);
        
        // Try to match different token types in order of priority
        
        // Comments
        Matcher matcher = COMMENT_SINGLE.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.COMMENT;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Block comment start
        matcher = COMMENT_BLOCK_START.matcher(remainingBuffer);
        if (matcher.find()) {
            // Find the end of block comment
            int blockEnd = findBlockCommentEnd(currentOffset + matcher.end());
            currentTokenEnd = blockEnd;
            currentTokenType = RunaTokenTypes.COMMENT;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Strings
        matcher = STRING_FORMATTED.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.STRING_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = STRING_RAW_DOUBLE.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.STRING_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = STRING_RAW_SINGLE.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.STRING_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = STRING_DOUBLE.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.STRING_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = STRING_SINGLE.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.STRING_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Numbers
        matcher = NUMBER_FLOAT.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.NUMBER_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = NUMBER_HEX.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.NUMBER_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = NUMBER_BINARY.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.NUMBER_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = NUMBER_OCTAL.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.NUMBER_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        matcher = NUMBER_DECIMAL.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.NUMBER_LITERAL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Natural language operators (multi-word)
        String naturalOp = findNaturalOperator(remainingBuffer);
        if (naturalOp != null) {
            currentTokenEnd = currentOffset + naturalOp.length();
            currentTokenType = RunaTokenTypes.NATURAL_OPERATOR;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Multi-word identifiers
        matcher = MULTI_WORD_IDENTIFIER.matcher(remainingBuffer);
        if (matcher.find()) {
            String text = matcher.group();
            currentTokenEnd = currentOffset + matcher.end();
            if (KEYWORDS.contains(text) || isKeywordPhrase(text)) {
                currentTokenType = RunaTokenTypes.KEYWORD;
            } else {
                currentTokenType = RunaTokenTypes.IDENTIFIER;
            }
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Single word identifiers and keywords
        matcher = IDENTIFIER.matcher(remainingBuffer);
        if (matcher.find()) {
            String text = matcher.group();
            currentTokenEnd = currentOffset + matcher.end();
            if (KEYWORDS.contains(text)) {
                currentTokenType = RunaTokenTypes.KEYWORD;
            } else if (text.equals("true") || text.equals("false")) {
                currentTokenType = RunaTokenTypes.BOOLEAN_LITERAL;
            } else {
                currentTokenType = RunaTokenTypes.IDENTIFIER;
            }
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Mathematical symbols
        matcher = MATH_SYMBOLS.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.MATH_SYMBOL;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Punctuation
        matcher = PUNCTUATION.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.PUNCTUATION;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Whitespace
        matcher = WHITESPACE.matcher(remainingBuffer);
        if (matcher.find()) {
            currentTokenEnd = currentOffset + matcher.end();
            currentTokenType = RunaTokenTypes.WHITESPACE;
            currentOffset = currentTokenEnd;
            return;
        }
        
        // Single character fallback
        currentTokenEnd = currentOffset + 1;
        currentTokenType = RunaTokenTypes.BAD_CHARACTER;
        currentOffset = currentTokenEnd;
    }
    
    private int findBlockCommentEnd(int startPos) {
        for (int i = startPos; i < endOffset; i++) {
            if (i + 9 <= endOffset && buffer.subSequence(i, i + 9).toString().equals(":End Note")) {
                // Find the end of the line
                while (i < endOffset && buffer.charAt(i) != '\\n') {
                    i++;
                }
                return i + 1;
            }
            if (buffer.charAt(i) == '\\n') {
                i++; // Skip newline
            }
        }
        return endOffset; // End of buffer
    }
    
    private String findNaturalOperator(CharSequence text) {
        for (String op : NATURAL_OPERATORS) {
            if (text.toString().startsWith(op)) {
                return op;
            }
        }
        return null;
    }
    
    private boolean isKeywordPhrase(String text) {
        // Check for multi-word keywords like "Process called", "that takes", etc.
        return text.startsWith("Process called") ||
               text.startsWith("that takes") ||
               text.startsWith("returns") ||
               text.startsWith("For each") ||
               text.startsWith("to the power of") ||
               text.equals("is equal to") ||
               text.equals("is not equal to") ||
               text.equals("does not equal");
    }
    
    @NotNull
    @Override
    public CharSequence getBufferSequence() {
        return buffer;
    }
    
    @Override
    public int getBufferEnd() {
        return endOffset;
    }
}
