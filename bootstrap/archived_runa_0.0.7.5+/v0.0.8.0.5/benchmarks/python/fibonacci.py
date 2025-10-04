def fibonacci(n):
    if n < 2:
        return n
    else:
        a = fibonacci(n - 1)
        b = fibonacci(n - 2)
        return a + b

if __name__ == "__main__":
    result = fibonacci(35)
    exit(result)