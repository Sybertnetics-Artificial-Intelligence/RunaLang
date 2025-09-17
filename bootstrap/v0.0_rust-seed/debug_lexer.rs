use std::fs;
mod lexer;
use lexer::Lexer;

fn main() {
    let source = r#"Process called "test" that takes nothing:
    Let x be "test:colon"
End Process"#;
    
    let mut lexer = Lexer::new(&source);
    let tokens = lexer.tokenize().unwrap();
    
    for token in &tokens {
        println!("{:?}", token);
    }
}
