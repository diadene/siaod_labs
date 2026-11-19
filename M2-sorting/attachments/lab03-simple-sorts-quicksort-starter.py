#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time
import matplotlib.pyplot as plt
import math
import os

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list) -> tuple[list, int, int]:
    """Сортировка пузырьком. Ожидаемая сложность: TODO (обосновать в отчёте).

    Подсказка: досрочный выход, если за проход не было ни одного обмена, —
    именно он даёт лучший случай на упорядоченном входе.
    """
    # TODO: реализовать; считать сравнения и обмены
    copy_a = a.copy()
    n = len(copy_a)
    swapps = 0
    count = 0
    if n > 0:
        for i in range(n - 1):
            swapped = False

            for j in range (n - 1 - i):
                count += 1
                if copy_a[j] > copy_a[j + 1]:
                    copy_a[j], copy_a[j + 1] = copy_a[j + 1], copy_a[j]
                    swapped = True
                    swapps += 1
            if swapped == False:
                break
    return (copy_a, count, swapps)

def insertion_sort(a: list) -> tuple[list, int, int]:
    """Сортировка вставками. Ожидаемая сложность: TODO (лучший/худший случаи)."""
    # TODO: реализовать; считать сравнения и перемещения (сдвиги)

    copy_a = a.copy()
    n = len(copy_a)
    count, swapps = 0, 0
    if n > 0:
        for i in range(1, n):
            for j in range(i, 0, -1):
                count += 1
                if copy_a[j] < copy_a[j - 1]:
                    copy_a[j], copy_a[j - 1] = copy_a[j - 1], copy_a[j]
                    swapps += 1
                else:
                    break
    return copy_a, count, swapps

def selection_sort(a: list) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: TODO (почему не зависит от входа?)."""
    # TODO: реализовать; считать сравнения и обмены

    n = len(a)
    copy_a = a.copy()
    count, swapps = 0, 0
    if n > 0:
        for i in range(0, n - 1):
            m = copy_a[i]
            index = i
            for j in range (i + 1, n):
                count += 1
                if m > copy_a[j]:
                    m = copy_a[j]
                    index = j

            if index != i:
                swapps += 1
                temp = copy_a[i]
                copy_a[i] = copy_a[index]
                copy_a[index] = temp
    return copy_a, count, swapps

# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность: в среднем O(n log n) TODO, в худшем случае O(n^2) TODO (обосновать
    в отчёте, объяснить роль рандомизации). rng передаётся снаружи, чтобы
    запуск был воспроизводим по seed варианта.
    """
    if len(a) <= 1 : return a

    copy_a = a.copy()

    if rng is None:
        rng = random.Random()

    pivot = copy_a[rng.randrange(0, len(copy_a))]

    left = []
    right = []
    eq = []

    for i in copy_a:
        if i < pivot:
            left.append(i)
        if i > pivot:
            right.append(i)
        if i == pivot:
            eq.append(i)

    copy_a = quick_sort(left, rng) + eq + quick_sort(right, rng)
    return copy_a

    # TODO: реализовать (рекурсивно или циклом со стеком);
    # TODO: опорный элемент — a[rng.randrange(lo, hi)], не первый и не последний.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.

    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """
    # Исходный массив пар (ключ, метка)
    data = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]

    print("\nДемонстрация стабильности сортировок:")
    print("Исходный массив:", data)

    # Сортируем пары только по первому элементу — ключу
    def key_compare(a, b):
        return a[0] < b[0]

    # Создаём копии функций, чтобы использовать сравнение только по ключу
    def bubble(a):
        arr = a.copy()
        for i in range(len(arr)):
            for j in range(len(arr) - 1 - i):
                if key_compare(arr[j + 1], arr[j]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def insertion(a):
        arr = a.copy()
        for i in range(1, len(arr)):
            j = i
            while j > 0 and key_compare(arr[j], arr[j - 1]):
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
                j -= 1
        return arr

    def selection(a):
        arr = a.copy()
        for i in range(len(arr)):
            min_index = i
            for j in range(i + 1, len(arr)):
                if key_compare(arr[j], arr[min_index]):
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
        return arr

    def quick(a):
        if len(a) <= 1:
            return a

        pivot = a[0][0]

        left = [x for x in a if x[0] < pivot]
        equal = [x for x in a if x[0] == pivot]
        right = [x for x in a if x[0] > pivot]

        return quick(left) + equal + quick(right)

    algorithms = {
        "Bubble Sort": bubble,
        "Insertion Sort": insertion,
        "Selection Sort": selection,
        "Quick Sort": quick,
    }

    for name, sort_fn in algorithms.items():
        result = sort_fn(data)

        # Проверяем сохранение исходного порядка меток
        stable = True

        for key in (1, 2):
            original = [x[1] for x in data if x[0] == key]
            sorted_labels = [x[1] for x in result if x[0] == key]

            if original != sorted_labels:
                stable = False
                break

        print(f"\n{name}:")
        print("Результат:", result)
        print("Порядок меток:", [x[1] for x in result])
        print("Стабильная" if stable else "Нестабильная")


# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов; результат — таблица в stdout."""
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]

    results = {}
    for name, fn, sizes in plans:
        print(f"\n{name}:")
        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                print(f"  n={n:>7}  вход={cls:<13} t={bench(fn, data):.6f} c")
    # Сбор результатов для графиков
    results = {}

    for name, fn, sizes in plans:
        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                elapsed = bench(fn, data)

                if (name, cls) not in results:
                    results[(name, cls)] = {
                        "sizes": [],
                        "times": []
                    }

                results[(name, cls)]["sizes"].append(n)
                results[(name, cls)]["times"].append(elapsed)

    # Создание папки для графиков
    os.makedirs("plots", exist_ok=True)

    for file in os.listdir("plots"):
        if file.endswith(".png"):
            os.remove(os.path.join("plots", file))
    # Построение log-log графиков
    classes = ["упорядоченный", "случайный", "обратный"]

    for cls in classes:
        plt.figure(figsize=(10, 6))

        for name, fn, sizes in plans:
            x = results[(name, cls)]["sizes"]
            y = results[(name, cls)]["times"]

            plt.loglog(x, y, marker="o", label=name)

        plt.xlabel("Размер массива (n)")
        plt.ylabel("Время выполнения (секунды)")
        plt.title(f"Сравнение сортировок: {cls} вход")
        plt.grid(True, which="both")
        plt.legend()

        plt.savefig(f"plots/{cls}.png", dpi=150)
        plt.close()

    print("\nГрафики сохранены в папке plots/")

    # Таблицы счётчиков сравнений и обменов
    counter_algorithms = {
        "bubble_sort": bubble_sort,
        "insertion_sort": insertion_sort,
        "selection_sort": selection_sort
    }

    print("\nТАБЛИЦЫ СЧЁТЧИКОВ")
    print("=" * 85)

    for name, sort_fn in counter_algorithms.items():
        print(f"\n{name}:")
        print(
            f"{'Размер':>8} | {'Тип входа':<15} | "
            f"{'Сравнения':>15} | {'Обмены':>15}"
        )
        print("-" * 70)

        for n in SIZES_QUADRATIC:
            for cls, data in make_inputs(n, seed).items():
                _, comparisons, swaps = sort_fn(data)

                print(
                    f"{n:>8} | {cls:<15} | "
                    f"{comparisons:>15} | {swaps:>15}"
                )

    # Сопоставление наклонов графиков с теоретической сложностью
    print("\nЭМПИРИЧЕСКАЯ ОЦЕНКА СЛОЖНОСТИ")
    print("=" * 85)

    for name, fn, sizes in plans:
        print(f"\n{name}:")

        for cls in classes:
            x = results[(name, cls)]["sizes"]
            y = results[(name, cls)]["times"]

            # Переход к логарифмическим координатам
            log_x = [math.log(n) for n in x]
            log_y = [math.log(t) for t in y]

            # Вычисление наклона прямой методом наименьших квадратов
            mean_x = statistics.mean(log_x)
            mean_y = statistics.mean(log_y)

            numerator = sum(
                (a - mean_x) * (b - mean_y)
                for a, b in zip(log_x, log_y)
            )

            denominator = sum(
                (a - mean_x) ** 2 for a in log_x
            )

            slope = numerator / denominator

            print(f"  {cls:<15} наклон: {slope:.3f}")

    # Теоретические пояснения
    print("\nТЕОРЕТИЧЕСКАЯ СЛОЖНОСТЬ")
    print("-" * 85)
    print("Bubble Sort:")
    print("  Лучший случай: O(n) — упорядоченный массив.")
    print("  Средний и худший случаи: O(n^2).")

    print("\nInsertion Sort:")
    print("  Лучший случай: O(n) — упорядоченный массив.")
    print("  Средний и худший случаи: O(n^2).")

    print("\nSelection Sort:")
    print("  Лучший, средний и худший случаи: O(n^2).")

    print("\nQuick Sort:")
    print("  Средний случай: O(n log n).")
    print("  Худший случай: O(n^2).")
    print("  Рандомизация pivot снижает вероятность худшего случая.")

    print("\nНаклоны могут отличаться от теоретических оценок")
    print("из-за особенностей оборудования, интерпретатора Python,")
    print("размеров тестовых массивов и погрешностей измерений.")

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
