use std::collections::HashMap;

fn main() {
    let mut table: HashMap<i32, i32> = HashMap::new();

    // Insert 10000 key-value pairs
    for i in 0..10000 {
        table.insert(i, i * 2);
    }

    // Lookup 10000 values
    let mut total = 0;
    for i in 0..10000 {
        if let Some(&value) = table.get(&i) {
            total += value;
        }
    }

    std::process::exit(0);
}
