def main():
    n = 100
    a = [[i + j for j in range(n)] for i in range(n)]
    b = [[i - j for j in range(n)] for i in range(n)]
    c = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            sum_val = 0
            for k in range(n):
                sum_val += a[i][k] * b[k][j]
            c[i][j] = sum_val

    return 0

if __name__ == "__main__":
    exit(main())
