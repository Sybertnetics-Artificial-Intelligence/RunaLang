def count_primes(limit):
    count = 0
    n = 2
    while n < limit:
        is_prime = 1
        i = 2
        while i * i <= n:
            remainder = n % i
            if remainder == 0:
                is_prime = 0
            i = i + 1
        if is_prime == 1:
            count = count + 1
        n = n + 1
    return count

if __name__ == "__main__":
    result = count_primes(10000)
    exit(result)