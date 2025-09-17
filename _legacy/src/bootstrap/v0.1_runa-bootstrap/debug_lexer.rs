use std::fs;
use runa_bootstrap::Lexer;

fn main() {
    let source = fs::read_to_string("test_simple.runa").unwrap();
    println!("Source:\n{}", source);
    println!("\nTokenizing...");

    let mut lexer = Lexer::new(&source);
    match lexer.tokenize() {
        Ok(tokens) => {
            println!("Tokens:");
            for (i, token) in tokens.iter().enumerate() {
                println!("  {}: {:?}", i, token);
                if i > 20 {
                    println!("  ... (truncated)");
                    break;
                }
            }
        }
        Err(e) => {
            println!("Error: {}", e);
        }
    }
}