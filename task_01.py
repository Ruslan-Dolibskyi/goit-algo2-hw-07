import random
from collections import OrderedDict
import timeit

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, index):
        to_remove = []
        for key in self.cache.keys():
            if key[0] <= index <= key[1]:
                to_remove.append(key)
        for key in to_remove:
            del self.cache[key]

def range_sum_no_cache(array, L, R):
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value

cache = LRUCache(1000)

def range_sum_with_cache(array, L, R):
    result = cache.get((L, R))
    if result is None:
        result = range_sum_no_cache(array, L, R)
        cache.put((L, R), result)
    return result

def update_with_cache(array, index, value):
    update_no_cache(array, index, value)
    cache.invalidate(index)

# Генерація масиву та запитів
N = 100000
array = [random.randint(1, 100) for _ in range(N)]
Q = 50000
queries = []
for _ in range(Q):
    if random.random() < 0.5:
        L = random.randint(0, N-1)
        R = random.randint(L, N-1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N-1)
        value = random.randint(1, 100)
        queries.append(('Update', index, value))

def execute_queries_no_cache(queries, array):
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, query[1], query[2])
        elif query[0] == 'Update':
            update_no_cache(array, query[1], query[2])

def execute_queries_with_cache(queries, array):
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(array, query[1], query[2])
        elif query[0] == 'Update':
            update_with_cache(array, query[1], query[2])

# Вимірювання часу виконання
time_no_cache = timeit.timeit(lambda: execute_queries_no_cache(queries, array), number=1)
time_with_cache = timeit.timeit(lambda: execute_queries_with_cache(queries, array), number=1)

print(f"Час виконання без кешу: {time_no_cache} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache} секунд")
