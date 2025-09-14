fn main() {
    let tokens = runa_bootstrap::lexer::tokenize(r#"
Process called "test" returns Integer:
    Return 0
End Process
"#).unwrap();
    println!("Tokens: {:?}", tokens);
}
