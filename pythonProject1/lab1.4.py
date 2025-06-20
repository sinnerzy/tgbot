from collections import Counter
def count_it(sequence):
    if not sequence.isdigit():
        return {}
    counts = Counter(map(int, sequence))
    return dict(counts.most_common(3))

# Пример использования
print(count_it("111222333444455556666"))  # {6: 4, 5: 4, 4: 4}