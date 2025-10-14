fn swap(arr: &mut Vec<i32>, i: usize, j: usize) {
    let temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

fn partition(arr: &mut Vec<i32>, low: i32, high: i32) -> i32 {
    let pivot = arr[high as usize];
    let mut i = low - 1;

    for j in low..high {
        if arr[j as usize] < pivot {
            i += 1;
            swap(arr, i as usize, j as usize);
        }
    }
    swap(arr, (i + 1) as usize, high as usize);
    i + 1
}

fn quicksort(arr: &mut Vec<i32>, low: i32, high: i32) {
    if low < high {
        let pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

fn main() {
    let n = 10000;
    let mut arr: Vec<i32> = (0..n).map(|i| n - i).collect();

    quicksort(&mut arr, 0, (n - 1) as i32);

    std::process::exit(0);
}
