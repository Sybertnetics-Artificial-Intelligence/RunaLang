def string_length(s):
    return len(s)

def copy_string(src):
    return src[:]

def main():
    iterations = 10000
    base_str = "Hello"
    total_len = 0

    for i in range(iterations):
        result_str = copy_string(base_str)
        length = string_length(result_str)
        total_len += length

    return 0

if __name__ == "__main__":
    exit(main())
