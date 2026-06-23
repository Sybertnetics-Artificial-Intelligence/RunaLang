fn factorial(n: i64) -> i64 {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}

fn main() {
    let mut sum: i64 = 0;
    let mut i = 1;
    while i <= 20 {
        let result = factorial(i);
        sum = sum + result;
        i = i + 1;
    }
    std::process::exit(0);
}