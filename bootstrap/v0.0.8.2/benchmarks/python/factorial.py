def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == "__main__":
    sum_val = 0
    i = 1
    while i <= 20:
        result = factorial(i)
        sum_val = sum_val + result
        i = i + 1
    exit(0)