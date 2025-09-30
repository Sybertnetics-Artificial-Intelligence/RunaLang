fn fibonacci(n: i32) -> i32 {
    if n < 2 {
        n
    } else {
        let a = fibonacci(n - 1);
        let b = fibonacci(n - 2);
        a + b
    }
}

fn main() {
    let result = fibonacci(35);
    std::process::exit(result);
}