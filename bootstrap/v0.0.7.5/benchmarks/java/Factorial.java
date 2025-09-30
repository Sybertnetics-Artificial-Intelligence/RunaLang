public class Factorial {
    public static long factorial(int n) {
        if (n <= 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }

    public static void main(String[] args) {
        long sum = 0;
        int i = 1;
        while (i <= 20) {
            long result = factorial(i);
            sum = sum + result;
            i = i + 1;
        }
        System.exit(0);
    }
}