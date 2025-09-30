public class Primes {
    public static int countPrimes(int limit) {
        int count = 0;
        int n = 2;
        while (n < limit) {
            int isPrime = 1;
            int i = 2;
            while (i * i <= n) {
                int remainder = n % i;
                if (remainder == 0) {
                    isPrime = 0;
                }
                i = i + 1;
            }
            if (isPrime == 1) {
                count = count + 1;
            }
            n = n + 1;
        }
        return count;
    }

    public static void main(String[] args) {
        int result = countPrimes(10000);
        System.exit(result);
    }
}