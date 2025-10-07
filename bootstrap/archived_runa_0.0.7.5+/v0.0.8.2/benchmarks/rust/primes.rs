fn count_primes(limit: i32) -> i32 {
    let mut count = 0;
    let mut n = 2;
    while n < limit {
        let mut is_prime = 1;
        let mut i = 2;
        while i * i <= n {
            let remainder = n % i;
            if remainder == 0 {
                is_prime = 0;
            }
            i = i + 1;
        }
        if is_prime == 1 {
            count = count + 1;
        }
        n = n + 1;
    }
    count
}

fn main() {
    let result = count_primes(10000);
    std::process::exit(result);
}