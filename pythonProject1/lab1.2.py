def change(lst):
    if len(lst) < 2:
        return lst
    lst[0], lst[-1] = lst[-1], lst[0]
    return lst

# Пример использования
print(change([1, 2, 3, 4]))  # [4, 2, 3, 1]