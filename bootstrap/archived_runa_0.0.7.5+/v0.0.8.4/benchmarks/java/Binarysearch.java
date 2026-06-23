public class Binarysearch {
    public static void main(String[] args) {
        int n = 10000;
        int searches = 1000;
        int[] arr = new int[n];

        for (int i = 0; i < n; i++) {
            arr[i] = i;
        }

        int total = 0;
        for (int i = 0; i < searches; i++) {
            int target = i % n;
            int left = 0;
            int right = n - 1;

            while (left <= right) {
                int mid = (left + right) / 2;
                if (arr[mid] == target) {
                    total += mid;
                    break;
                } else if (arr[mid] < target) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }

        System.exit(0);
    }
}
