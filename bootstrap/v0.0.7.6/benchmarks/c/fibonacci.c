#include <stdio.h>

int fibonacci(int n) {
    if (n < 2) {
        return n;
    } else {
        int a = fibonacci(n - 1);
        int b = fibonacci(n - 2);
        return a + b;
    }
}

int main() {
    int result = fibonacci(35);
    return result;
}