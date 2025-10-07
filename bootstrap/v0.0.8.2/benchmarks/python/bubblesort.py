def main():
    n = 1000
    arr = [n - i for i in range(n)]

    sorted_flag = False
    while not sorted_flag:
        sorted_flag = True
        for i in range(n - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False

    return 0

if __name__ == "__main__":
    exit(main())
