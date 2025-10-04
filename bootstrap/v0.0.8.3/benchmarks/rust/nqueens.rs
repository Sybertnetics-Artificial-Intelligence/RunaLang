fn is_safe(board: &Vec<Vec<i32>>, row: usize, col: usize, n: usize) -> bool {
    for i in 0..col {
        if board[row][i] == 1 {
            return false;
        }
    }

    let mut i = row as i32 - 1;
    let mut j = col as i32 - 1;
    while i >= 0 && j >= 0 {
        if board[i as usize][j as usize] == 1 {
            return false;
        }
        i -= 1;
        j -= 1;
    }

    let mut i = row + 1;
    let mut j = col as i32 - 1;
    while i < n && j >= 0 {
        if board[i][j as usize] == 1 {
            return false;
        }
        i += 1;
        j -= 1;
    }

    true
}

fn solve(board: &mut Vec<Vec<i32>>, col: usize, n: usize) -> bool {
    if col >= n {
        return true;
    }

    for i in 0..n {
        if is_safe(board, i, col, n) {
            board[i][col] = 1;
            if solve(board, col + 1, n) {
                return true;
            }
            board[i][col] = 0;
        }
    }

    false
}

fn main() {
    let n = 8;
    let mut board = vec![vec![0; n]; n];
    solve(&mut board, 0, n);
    std::process::exit(0);
}
