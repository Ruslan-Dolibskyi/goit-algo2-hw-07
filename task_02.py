import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

# Реалізація дерева Splay
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _zig(self, node):
        parent = node.left
        node.left = parent.right
        parent.right = node
        return parent

    def _zag(self, node):
        parent = node.right
        node.right = parent.left
        parent.left = node
        return parent

    def _splay(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            if not node.left:
                return node
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._zig(node)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right:
                    node.left = self._zag(node.left)
            return self._zig(node) if node.left else node
        else:
            if not node.right:
                return node
            if key > node.right.key:
                node.right.right = self._splay(node.right.right, key)
                node = self._zag(node)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left:
                    node.right = self._zig(node.right)
            return self._zag(node) if node.right else node

    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return
        new_node = Node(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

# Числа Фібоначчі з кешуванням LRU
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Числа Фібоначчі з використанням Splay Tree
def fibonacci_splay(n, tree):
    cached_result = tree.search(n)
    if cached_result is not None:
        return cached_result
    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

# Вимірювання продуктивності
n_values = range(0, 951, 50)
lru_times = []
splay_times = []

tree = SplayTree()

for n in n_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    tree = SplayTree()  # Скидання дерева для кожного n
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10) / 10
    splay_times.append(splay_time)

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label="LRU Cache", marker="o")
plt.plot(n_values, splay_times, label="Splay Tree", marker="x")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid()
plt.show()

# Виведення таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
print("-" * 50)
for n, lru, splay in zip(n_values, lru_times, splay_times):
    print(f"{n:<10}{lru:<20.8f}{splay:<20.8f}")
