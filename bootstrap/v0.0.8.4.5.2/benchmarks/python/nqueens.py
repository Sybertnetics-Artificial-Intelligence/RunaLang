def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i]:
            return False

    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j]:
            return False
        i -= 1
        j -= 1

    i, j = row + 1, col - 1
    while i < n and j >= 0:
        if board[i][j]:
            return False
        i += 1
        j -= 1

    return True

def solve(board, col, n):
    if col >= n:
        return True

    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve(board, col + 1, n):
                return True
            board[i][col] = 0

    return False

def main():
    n = 8
    board = [[0 for _ in range(n)] for _ in range(n)]
    solve(board, 0, n)
    return 0

if __name__ == "__main__":
    exit(main())
