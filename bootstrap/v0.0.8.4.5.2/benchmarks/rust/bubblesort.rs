fn main() {
    let n = 1000;
    let mut arr: Vec<i32> = (0..n).map(|i| n - i).collect();

    let mut sorted = false;
    while !sorted {
        sorted = true;
        for i in 0..n - 1 {
            if arr[i as usize] > arr[(i + 1) as usize] {
                arr.swap(i as usize, (i + 1) as usize);
                sorted = false;
            }
        }
    }

    std::process::exit(0);
}
