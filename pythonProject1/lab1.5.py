def sieve(lst):
    unique_elements = list(dict.fromkeys(lst))
    return tuple(reversed(unique_elements))

# Пример использования
print(sieve([1, 2, 2, 3, 4, 4, 5]))  # (5, 4, 3, 2, 1)