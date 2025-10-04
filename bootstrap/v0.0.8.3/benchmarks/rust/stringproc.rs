fn string_length(s: &str) -> usize {
    s.len()
}

fn copy_string(src: &str) -> String {
    src.to_string()
}

fn main() {
    let iterations = 10000;
    let base_str = "Hello";
    let mut total_len = 0;

    for _ in 0..iterations {
        let result_str = copy_string(base_str);
        let len = string_length(&result_str);
        total_len += len;
    }

    std::process::exit(0);
}
