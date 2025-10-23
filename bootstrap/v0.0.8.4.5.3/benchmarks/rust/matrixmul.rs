fn main() {
    let n = 100;
    let mut a = vec![vec![0; n]; n];
    let mut b = vec![vec![0; n]; n];
    let mut c = vec![vec![0; n]; n];

    for i in 0..n {
        for j in 0..n {
            a[i][j] = (i + j) as i32;
            b[i][j] = (i as i32) - (j as i32);
        }
    }

    for i in 0..n {
        for j in 0..n {
            let mut sum = 0;
            for k in 0..n {
                sum += a[i][k] * b[k][j];
            }
            c[i][j] = sum;
        }
    }

    std::process::exit(0);
}
