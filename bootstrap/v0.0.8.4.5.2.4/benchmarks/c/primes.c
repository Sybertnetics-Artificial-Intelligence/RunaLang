#include <stdio.h>

int count_primes(int limit) {
    int count = 0;
    int n = 2;
    while (n < limit) {
        int is_prime = 1;
        int i = 2;
        while (i * i <= n) {
            int remainder = n % i;
            if (remainder == 0) {
                is_prime = 0;
            }
            i = i + 1;
        }
        if (is_prime == 1) {
            count = count + 1;
        }
        n = n + 1;
    }
    return count;
}

int main() {
    int result = count_primes(10000);
    return result;
}