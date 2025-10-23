def main():
    table = {}

    # Insert 10000 key-value pairs
    for i in range(10000):
        table[i] = i * 2

    # Lookup 10000 values
    total = 0
    for i in range(10000):
        if i in table:
            value = table[i]
            total += value

    return 0

if __name__ == "__main__":
    exit(main())
