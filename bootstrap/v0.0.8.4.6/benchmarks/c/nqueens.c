#include <stdlib.h>

int is_safe(int** board, int row, int col, int n) {
    for (int i = 0; i < col; i++) {
        if (board[row][i]) return 0;
    }

    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
        if (board[i][j]) return 0;
    }

    for (int i = row + 1, j = col - 1; i < n && j >= 0; i++, j--) {
        if (board[i][j]) return 0;
    }

    return 1;
}

int solve(int** board, int col, int n) {
    if (col >= n) return 1;

    for (int i = 0; i < n; i++) {
        if (is_safe(board, i, col, n)) {
            board[i][col] = 1;
            if (solve(board, col + 1, n)) return 1;
            board[i][col] = 0;
        }
    }

    return 0;
}

int main() {
    int n = 8;
    int** board = malloc(n * sizeof(int*));
    for (int i = 0; i < n; i++) {
        board[i] = calloc(n, sizeof(int));
    }

    solve(board, 0, n);

    for (int i = 0; i < n; i++) {
        free(board[i]);
    }
    free(board);

    return 0;
}
