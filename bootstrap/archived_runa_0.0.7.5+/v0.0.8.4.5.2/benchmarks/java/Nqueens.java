public class Nqueens {
    static boolean isSafe(int[][] board, int row, int col, int n) {
        for (int i = 0; i < col; i++) {
            if (board[row][i] == 1) return false;
        }

        for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
            if (board[i][j] == 1) return false;
        }

        for (int i = row + 1, j = col - 1; i < n && j >= 0; i++, j--) {
            if (board[i][j] == 1) return false;
        }

        return true;
    }

    static boolean solve(int[][] board, int col, int n) {
        if (col >= n) return true;

        for (int i = 0; i < n; i++) {
            if (isSafe(board, i, col, n)) {
                board[i][col] = 1;
                if (solve(board, col + 1, n)) return true;
                board[i][col] = 0;
            }
        }

        return false;
    }

    public static void main(String[] args) {
        int n = 8;
        int[][] board = new int[n][n];
        solve(board, 0, n);
        System.exit(0);
    }
}
