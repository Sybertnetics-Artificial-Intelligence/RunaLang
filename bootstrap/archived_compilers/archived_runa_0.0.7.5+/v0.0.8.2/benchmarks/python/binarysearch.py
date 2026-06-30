def main():
    n = 10000
    searches = 1000
    arr = list(range(n))

    total = 0
    for i in range(searches):
        target = i % n
        left = 0
        right = n - 1

        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                total += mid
                break
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

    return 0

if __name__ == "__main__":
    exit(main())
