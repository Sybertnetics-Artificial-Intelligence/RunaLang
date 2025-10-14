fn main() {
    let n = 10000;
    let searches = 1000;
    let arr: Vec<i32> = (0..n).collect();

    let mut total = 0;
    for i in 0..searches {
        let target = i % n;
        let mut left = 0;
        let mut right = n - 1;

        while left <= right {
            let mid = (left + right) / 2;
            if arr[mid as usize] == target {
                total += mid;
                break;
            } else if arr[mid as usize] < target {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
    }

    std::process::exit(0);
}
