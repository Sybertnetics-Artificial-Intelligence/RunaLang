// Integration tests for the frontend modules

#[cfg(test)]
mod lexer_tests {
    use super::super::lexer::*;
    use std::path::Path;
    
    #[test]
    fn test_basic_tokenization() {
        let source = "Let x be 42";
        let path = Path::new("test.runa");
        let mut lexer = Lexer::new(source, path);
        let mut diagnostic_engine = crate::utils::diagnostics::DiagnosticEngine::new();
        
        let tokens = lexer.tokenize(&mut diagnostic_engine).unwrap();
        
        assert_eq!(tokens.len(), 5); // Let, x, be, 42, EOF
        assert!(matches!(tokens[0].token_type, TokenType::Let));
        assert!(matches!(tokens[1].token_type, TokenType::Identifier(_)));
        assert!(matches!(tokens[2].token_type, TokenType::Be));
        assert!(matches!(tokens[3].token_type, TokenType::Integer(42)));
        assert!(matches!(tokens[4].token_type, TokenType::Eof));
    }
    
    #[test]
    fn test_string_literal() {
        let source = r#""Hello, World!""#;
        let path = Path::new("test.runa");
        let mut lexer = Lexer::new(source, path);
        let mut diagnostic_engine = crate::utils::diagnostics::DiagnosticEngine::new();
        
        let tokens = lexer.tokenize(&mut diagnostic_engine).unwrap();
        
        assert_eq!(tokens.len(), 2); // String, EOF
        assert!(matches!(tokens[0].token_type, TokenType::String(ref s) if s == "Hello, World!"));
    }
    
    #[test]
    fn test_keywords() {
        let source = "Process called End Type";
        let path = Path::new("test.runa");
        let mut lexer = Lexer::new(source, path);
        let mut diagnostic_engine = crate::utils::diagnostics::DiagnosticEngine::new();
        
        let tokens = lexer.tokenize(&mut diagnostic_engine).unwrap();
        
        assert!(matches!(tokens[0].token_type, TokenType::Process));
        assert!(matches!(tokens[1].token_type, TokenType::Called));
        assert!(matches!(tokens[2].token_type, TokenType::End));
        assert!(matches!(tokens[3].token_type, TokenType::Type));
    }
}

#[cfg(test)]
mod parser_tests {
    use super::super::{lexer::*, parser::*, ast::*};
    use std::path::Path;
    
    #[test]
    fn test_simple_function() {
        let source = r#"
Process called "test" returns Integer:
    Return 42
End Process
        "#;
        
        let path = Path::new("test.runa");
        let mut lexer = Lexer::new(source, path);
        let mut diagnostic_engine = crate::utils::diagnostics::DiagnosticEngine::new();
        let tokens = lexer.tokenize(&mut diagnostic_engine).unwrap();
        
        let mut parser = Parser::new(tokens);
        let program = parser.parse(&mut diagnostic_engine).unwrap();
        
        assert_eq!(program.functions.len(), 1);
        assert_eq!(program.functions[0].name, "test");
        assert!(matches!(program.functions[0].return_type, Type::Integer));
        assert_eq!(program.functions[0].body.len(), 1);
    }
    
    #[test]
    fn test_variable_declaration() {
        let source = "Let x be 42";
        
        let path = Path::new("test.runa");
        let mut lexer = Lexer::new(source, path);
        let mut diagnostic_engine = crate::utils::diagnostics::DiagnosticEngine::new();
        let tokens = lexer.tokenize(&mut diagnostic_engine).unwrap();
        
        let mut parser = Parser::new(tokens);
        let statement = parser.parse_statement(&mut diagnostic_engine).unwrap();
        
        match statement {
            Statement::VariableDeclaration { name, var_type: _, initializer } => {
                assert_eq!(name, "x");
                match initializer {
                    Expression::Literal { value: LiteralValue::Integer(42) } => {},
                    _ => panic!("Expected integer literal 42"),
                }
            }
            _ => panic!("Expected variable declaration"),
        }
    }
}