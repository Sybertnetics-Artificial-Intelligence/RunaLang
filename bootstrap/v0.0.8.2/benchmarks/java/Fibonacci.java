public class Fibonacci {
    public static int fibonacci(int n) {
        if (n < 2) {
            return n;
        } else {
            int a = fibonacci(n - 1);
            int b = fibonacci(n - 2);
            return a + b;
        }
    }

    public static void main(String[] args) {
        int result = fibonacci(35);
        System.exit(result);
    }
}