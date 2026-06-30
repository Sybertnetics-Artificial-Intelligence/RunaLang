#include <stdlib.h>

int main() {
    int n = 1000;
    int *arr = malloc(n * sizeof(int));

    for (int i = 0; i < n; i++) {
        arr[i] = n - i;
    }

    int sorted = 0;
    while (!sorted) {
        sorted = 1;
        for (int i = 0; i < n - 1; i++) {
            if (arr[i] > arr[i + 1]) {
                int temp = arr[i];
                arr[i] = arr[i + 1];
                arr[i + 1] = temp;
                sorted = 0;
            }
        }
    }

    free(arr);
    return 0;
}
