#!/usr/bin/env python3

from src.runa.compiler.lexer import RunaLexer, TokenType

def test_ai_blocks():
    lexer = RunaLexer()
    source = "@reasoning This is AI reasoning\n@end"
    tokens = lexer.tokenize(source)
    
    print("Tokens generated:")
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type.name} = '{token.value}'")
    
    print("\nExpected vs Actual:")
    expected_types = [
        TokenType.REASONING,
        TokenType.TYPE_IDENTIFIER,  # "This" - capitalized
        TokenType.IS,
        TokenType.TYPE_IDENTIFIER,  # "AI" - capitalized
        TokenType.IDENTIFIER,  # "reasoning" - lowercase
        TokenType.NEWLINE,
        TokenType.END,
        TokenType.EOF
    ]
    
    for i, (token, expected_type) in enumerate(zip(tokens, expected_types)):
        match = "✓" if token.type == expected_type else "✗"
        print(f"  {i}: {match} Expected {expected_type.name}, got {token.type.name}")

if __name__ == "__main__":
    test_ai_blocks() 